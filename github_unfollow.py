"""
GitHub Unfollow Script

Safely identify and optionally unfollow GitHub users you follow who do not
follow you back. Supports dry-run mode by default, logging, exclusions, and
limits to minimize risk. Requires a personal access token.

Environment variables (loaded from .env if present):
  - GITHUB_USERNAME: Your GitHub username (optional)
  - GITHUB_TOKEN:    A PAT with 'read:user' and 'user:follow' scopes (required)

Examples:
  Dry run (default):
    python github_unfollow.py

  Actually unfollow up to 25 users, excluding some handles:
    python github_unfollow.py --apply --limit 25 --exclude alice bob team-org

  Use a different token env var:
    python github_unfollow.py --token-var ALT_GH_TOKEN
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List, Set

from dotenv import load_dotenv
from github import Github, GithubException


@dataclass
class ExecutionConfig:
    token_env_var: str
    apply_changes: bool
    limit: int | None
    excludes: Set[str]
    log_dir: str


def parse_args(argv: List[str]) -> ExecutionConfig:
    parser = argparse.ArgumentParser(
        description="Identify and optionally unfollow non-follow-back users",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes (unfollow). Default is dry-run (no changes).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max number of accounts to unfollow (or show in dry run).",
    )
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=[],
        help="Usernames to exclude from unfollow (space-separated)",
    )
    parser.add_argument(
        "--token-var",
        default="GITHUB_TOKEN",
        help="Environment variable name that holds the token (default: GITHUB_TOKEN)",
    )
    parser.add_argument(
        "--log-dir",
        default="logs",
        help="Directory to write reports/logs (default: logs)",
    )

    args = parser.parse_args(argv)
    return ExecutionConfig(
        token_env_var=args.token_var,
        apply_changes=args.apply,
        limit=args.limit,
        excludes={u.lower() for u in args.exclude},
        log_dir=args.log_dir,
    )


def load_token_from_env(token_env_var: str) -> str:
    load_dotenv()  # best-effort, okay if .env is absent
    token = os.getenv(token_env_var, "").strip()
    if not token:
        raise RuntimeError(
            f"GitHub token not found in env var '{token_env_var}'. "
            "Set it in your environment or .env file."
        )
    return token


def get_authenticated_user(client: Github):
    try:
        return client.get_user()
    except GithubException as exc:
        raise RuntimeError(f"Failed to authenticate with GitHub: {exc}") from exc


def fetch_login_set(iterable: Iterable) -> Set[str]:
    # Github paginated lists are iterable; collect logins lowercased
    return {item.login.lower() for item in iterable}


def ensure_directory(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def build_report(
    timestamp: str,
    followers: Set[str],
    following: Set[str],
    non_followers: List[str],
    applied: bool,
    limit: int | None,
    excludes: Set[str],
) -> List[str]:
    report_lines: List[str] = [
        f"{timestamp}",
        f"Current followers: {len(followers)}",
        f"Current following: {len(following)}",
        f"Mode: {'apply' if applied else 'dry-run'}",
    ]
    if excludes:
        report_lines.append(f"Excluded: {', '.join(sorted(excludes))}")
    if limit is not None:
        report_lines.append(f"Limit: {limit}")
    report_lines.append("")

    if non_followers:
        header_action = "Unfollowed" if applied else "Would unfollow"
        report_lines.append(f"{header_action} {len(non_followers)} users:")
        report_lines.extend(non_followers)
    else:
        report_lines.append("No users to unfollow.")
    return report_lines


def write_report(log_dir: str, timestamp_fs: str, report_lines: List[str]) -> str:
    ensure_directory(log_dir)
    file_path = os.path.join(log_dir, f"unfollow_report_{timestamp_fs}.txt")
    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(report_lines))
    return file_path


def unfollow_non_followers(config: ExecutionConfig) -> int:
    token = load_token_from_env(config.token_env_var)

    client = Github(token)
    user = get_authenticated_user(client)

    followers = fetch_login_set(user.get_followers())
    following = fetch_login_set(user.get_following())

    non_followers_all = sorted((following - followers) - config.excludes)

    if config.limit is not None and config.limit >= 0:
        non_followers = non_followers_all[: config.limit]
    else:
        non_followers = non_followers_all

    applied_usernames: List[str] = []
    if config.apply_changes:
        for login in non_followers:
            try:
                target = client.get_user(login)
                user.remove_from_following(target)
                applied_usernames.append(login)
                print(f"Unfollowed {login}")
            except GithubException as exc:
                print(f"Failed to unfollow {login}: {exc}", file=sys.stderr)
    else:
        for login in non_followers:
            print(f"DRY-RUN: would unfollow {login}")
        applied_usernames = non_followers

    timestamp_display = datetime.now().strftime("%Y-%m-%d %H:%M")
    timestamp_fs = datetime.now().strftime("%Y-%m-%d__%H-%M")
    report_lines = build_report(
        timestamp_display,
        followers,
        following,
        applied_usernames,
        applied=config.apply_changes,
        limit=config.limit,
        excludes=config.excludes,
    )
    report_path = write_report(config.log_dir, timestamp_fs, report_lines)
    print(f"Report saved to {report_path}")
    return 0


def main(argv: List[str]) -> int:
    try:
        config = parse_args(argv)
        return unfollow_non_followers(config)
    except Exception as exc:  # final safety net for CLI
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
