# 🐍 GitHub Unfollow Script

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![GitHub](https://img.shields.io/badge/GitHub-API-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

## 📜 Description

The **GitHub Unfollow Script** is a powerful Python tool designed to help you manage your GitHub following list effectively. This script automatically unfollows users who are not following you back, ensuring your network remains relevant and streamlined.

Perfect for maintaining a streamlined and relevant network on GitHub! This script is for developers and GitHub users who want to keep their following list clean and relevant, automating the tedious task of unfollowing inactive or non-reciprocal followers.

### How It Works

- **GitHub API Integration:** The script interacts with GitHub using the official GitHub API.
- **Authentication via Personal Access Token:** Securely authenticate using a personal access token, which you provide in a `.env` file.
- **Automated Unfollowing:** The script fetches your list of followers and the users you are following, identifies those who do not follow you back, and automatically unfollows them.
- **Comprehensive Reporting:** Generates a detailed report of the operation, including the current followers, current following, and a list of users who were unfollowed. The report is saved in the `logs` directory with a timestamp, and the result is also printed in the console.



<br>


## 🚀 Features

- **Automatic Unfollowing:** Unfollows users who don't follow you back.
- **Detailed Reporting:** Generates a comprehensive report with current followers, following, and the list of unfollowed users.
- **Easy Setup:** Simple configuration with a `.env` file.
- **Cross-Platform:** Works on Unix-like systems and Windows.

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/github-unfollow.git
   cd github-unfollow
   ```

2. Set up a virtual environment:
   - On Unix-like systems:
     ```bash
     source setup_venv.sh 
     ```
   - On Windows:
     ```bash
     .\setup_venv.ps1
     ```

3. Create a `.env` file in the root directory of the project with your GitHub credentials. You can use the provided `.env.example` template and rename it to `.env`:
   ```
   cp .env.example .env
   ```

   Then edit the `.env` file:
   ```
   GITHUB_USERNAME=your_username
   GITHUB_PASSWORD=your_password
   ```

## ▶️ How to run

Run the script:
```bash
python github_unfollow.py
```

After running the script, a report will be saved in the `logs` directory with the current date and time in the filename.

## Example Report

Example content of a report file:

> 2024-06-30 14:45  
> Current followers: 51  
> Current following: 54  
>   
> Unfollowed 3 users:  
> nickname1  
> nickname2  
> nickname3

This script helps you keep your following list up to date by unfollowing users who are not following you back.

## 📄 License

This project is licensed under the MIT License.

---

**SEO Keywords:** GitHub automation, manage GitHub followers, unfollow script, Python GitHub API, automate GitHub, GitHub following management, GitHub unfollow tool, GitHub user management, streamline GitHub network, GitHub follower report

**Contact:** For any questions or suggestions, feel free to open an issue or contact me at [e-nicko@ya.ru](mailto:e-nicko@ya.ru).

