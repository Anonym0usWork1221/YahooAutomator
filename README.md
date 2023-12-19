YahooAutomator: Automated Yahoo Login Tool
====
YahooAutomator, an automated tool designed for simplifying the Yahoo login process. 
This tool is specifically created for educational purposes to help individuals understand 
web automation and the challenges involved in automating login processes.

Important Notice
----
* **Educational Purpose Only**: YahooAutomator is intended for educational purposes, helping users learn about 
    web automation and login processes.
* **Responsible Usage**: Do not use this tool for malicious activities or unauthorized access. 
    Respect the privacy and rights of others.
* **Security**: If you discover any security vulnerabilities or issues related to this tool, please responsibly 
    disclose them to the author.

Author Information
----
* **Author**: Abdul Moez
* **Version**: 0.1
* **Study**: Undergraduate at GCU Lahore, Pakistan

Remember, unauthorized access to accounts or systems is illegal and unethical. 
Use YahooAutomator responsibly, following cybersecurity and privacy principles.


Introduction
-----
YahooAutomator provides functionality to automate the login to a 
Yahoo account using provided credentials, handle various challenges 
such as CAPTCHA, and interact with the Yahoo login page seamlessly. 
This tool aims to facilitate learning about web automation while emphasizing 
responsible and ethical usage.

Features
-----
* **Automated Yahoo Login**: Effortlessly log in to your Yahoo account using the provided email and password.
* **Challenges Handling**: Navigate through common challenges like CAPTCHA to ensure a smooth login process.
* **Educational Purpose**: Designed for educational purposes, YahooAutomator serves as a valuable tool to 
    understand web automation concepts.

Getting Started
-----
To use YahooAutomator, follow these simple steps:
1. **Install FFmpeg**:
    * Windows
      ```shell
       winget install --id=Gyan.FFmpeg -e
      ```
    * Linux
      ```shell
       sudo apt install ffmpeg
      ```
    * MacOS
      ```shell
       brew install ffmpeg
      ```
2. Install Python Packages:
    ```shell
    pip3 install -r requirements.txt
    ```
3. Sample Usage:
    ```python
    from yahoo_automator import YahooAutomator
    
    yahoo_automator = YahooAutomator(
        profile_dir="./temp_profile",
        predefined_cookies="./defaults/startup_cookies.pkl"
    )
    
    status = yahoo_automator.login_to_yahoo(
        yahoo_mail="yahoo@yahoo.com",
        passwords_combo=["wrong_pass121", "wrong_pass212", "correctpassword"]
    )
    
    if status[0]:
        print(f"Successfully logged in with password: {yahoo_automator.correct_password}")
    else:
        print(f"Login failed. Reason: {status[1]}")
    ```

YahooAutomator Parameters
----
- `profile_dir (str)`: Path to the profile directory.
- `predefined_cookies (str)`: Path to the file containing predefined cookies.
- `estimated_wait (int)`: Estimated wait time for various actions.
- `short_wait (int)`: Short wait time for specific actions.
- `verbose (bool)`: Enable verbose mode for printing status messages.
- `headless_mode (bool)`: Run the browser in headless mode.

YahooAutomator Public Methods
----
* `correct_password() -> str`: Returns the correct password used for a successful login.
* `get_browser() -> WebDriver`: Get the WebDriver object for the current browser session.
* `login_to_yahoo(yahoo_mail: str, passwords_combo: list[str], first_run: bool = True, pace: float = 0.5) -> tuple[bool, str]`: Logs in to a Yahoo account using provided credentials.


Important tips
-----
* If you are using this tool to automate the emailing process, you cannot use any browser other than the one 
  provided by this tool. You can create or utilize browsers created by the `login_to_yahoo` function 
  automatically through the `get_browser()` function. It creates a detection-free 
  browser for seamless integration with Yahoo.
* Occasionally, you may face a **one-hour** ban from Yahoo, especially when attempting to log in for the 
  first time without predefined cookies. In such cases, please wait for one hour before resuming your work.

# Contributor

<a href = "https://github.com/Anonym0usWork1221/YahooAutomator/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=Anonym0usWork1221/YahooAutomator"/>
</a>

-----------
Support and Contact Information
----------
> If you require any assistance or have questions, please feel free to reach out to me through the following channels:  
* **Email**: `abdulmoez123456789@gmail.com`

> I have also established a dedicated Discord group for more interactive communication:  
* **Discord Server**: `https://discord.gg/RMNcqzmt9f`


-----------

Buy Me a coffee
--------------
__If you'd like to show your support and appreciation for my work, you can buy me a coffee using the 
following payment option:__

**Payoneer**: `abdulmoez123456789@gmail.com`

> Your support is greatly appreciated and helps me continue providing valuable assistance and resources. 
Thank you for your consideration.

