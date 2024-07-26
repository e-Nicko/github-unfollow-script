"""
GitHub Unfollow Script

This Python script helps you manage your GitHub following list by automatically unfollowing users who do not follow you back.
It utilizes the GitHub API for interactions and requires a personal access token for authentication.

Features:
- Fetches the list of users you follow and those who follow you.
- Identifies users who are not following you back.
- Automatically unfollows those users.
- Generates a comprehensive report with the following details:
  - Current number of followers
  - Current number of users you are following
  - List of users who were unfollowed
- Saves the report in the 'logs' directory with a timestamp.
- Outputs the result of the operation to the console.

Requirements:
- Python 3.8+
- GitHub personal access token with 'read:user' and 'user:follow' scopes.
- The following Python packages:
  - PyGithub
  - python-dotenv

Setup:
1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the dependencies from requirements.txt.
4. Create a .env file with your GitHub username and personal access token.

.env file example:
    GITHUB_USERNAME=your_username
    GITHUB_TOKEN=your_personal_access_token

Usage:
Run the script:
    python github_unfollow.py

Author:
- Your Name (your_email@example.com)

License:
- This project is licensed under the MIT License. See the LICENSE file for details.
"""

import os
from github import Github
from dotenv import load_dotenv
from datetime import datetime

def unfollow_non_followers():
    # Load environment variables from .env file
    load_dotenv()
    username = os.getenv("GITHUB_USERNAME")
    token = os.getenv("GITHUB_TOKEN")

    if not username or not token:
        print("Username or token not found in .env file")
        return

    # Authenticate to GitHub
    g = Github(token)
    user = g.get_user()

    # Get list of followers
    followers = {follower.login for follower in user.get_followers()}

    # Get list of following
    following = {followee.login for followee in user.get_following()}

    # Determine users who are not following back
    non_followers = following - followers

    # Prepare the report
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = [f"{current_time}",
              f"Current followers: {len(followers)}",
              f"Current following: {len(following)}",
              ""]

    if non_followers:
        report.append(f"Unfollowed {len(non_followers)} users:")
        for non_follower in non_followers:
            user_to_unfollow = g.get_user(non_follower)
            user.remove_from_following(user_to_unfollow)
            report.append(non_follower)
            print(f"Unfollowed {non_follower}")
    else:
        report.append("No users to unfollow.")

    # Create logs directory if it does not exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Format the current date and time for the filename
    file_time = datetime.now().strftime("%Y-%m-%d__%H-%M")

    # Write the report to a file
    with open(f'logs/unfollow_report_{file_time}.txt', 'w') as file:
        file.write("\n".join(report))

    print(f"Report saved to logs/unfollow_report_{file_time}.txt")

if __name__ == "__main__":
    unfollow_non_followers()
