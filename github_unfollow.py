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
