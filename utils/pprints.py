"""
PPrints Module
This module defines the PPrints class, which provides utilities for printing formatted information and handling logs.
Classes:
    PPrints: A utility class for pretty printing information and handling logs.
"""

# Import necessary modules

from platform import system as system_platform
from threading import active_count
from os.path import isfile
from psutil import Process
from os import system


class PPrints:
    """
    PPrints Class
    This class encapsulates methods for printing formatted information and optionally logging it.
        Attributes:
            _HEADER (str): ANSI escape sequence for header color.
            _BLUE (str): ANSI escape sequence for blue color.
            _CYAN (str): ANSI escape sequence for cyan color.
            _GREEN (str): ANSI escape sequence for green color.
            _WARNING (str): ANSI escape sequence for warning color.
            _RED (str): ANSI escape sequence for red color.
            _RESET (str): ANSI escape sequence to reset text color.
        Methods:
            __init__(self, logs_file="logs.txt"): Initialize the PPrints object.
            clean_terminal(): Clean the terminal screen based on the platform.
            pretty_print(current_site, status, mode, limit, total_results="Calculating",
                        current_index="Calculating", logs=False): Print formatted information with optional logging.
    """

    # Private elements
    _HEADER = '\033[95m'
    _BLUE = '\033[94m'
    _CYAN = '\033[96m'
    _GREEN = '\033[92m'
    _WARNING = '\033[93m'
    _RED = '\033[91m'
    _RESET = '\033[0m'

    def __init__(self, logs_file: str = "logs.txt") -> None:
        """
        Initialize the PPrints object.
            Args:
                logs_file (str): The name of the log file to write logs to.
        """

        self._process = Process()
        self._log_file = logs_file

    @staticmethod
    def clean_terminal() -> str:
        """
        Clean the terminal screen based on the platform.
            Returns:
                str: The name of the platform.
        """

        if system_platform().lower() == "windows":
            system("cls")
        else:
            system("clear")
        return system_platform()

    def pretty_print(self,
                     status: str,
                     mode: str,
                     logs: bool = False,
                     ) -> None:
        """
        Print formatted information along with optional logging.
            Args:
                status (str): The status of the process.
                mode (str): The mode of operation.
                logs (bool, optional): Whether to log the information. Defaults to False.
        """

        memory_info = self._process.memory_info()
        current_memory_usage = memory_info.rss / 1024 / 1024  # Convert bytes to megabytes

        print(f"{self._GREEN}Platform: {self.clean_terminal()}\n"
              f"{self._WARNING}Status: {status}\n"
              f"{self._BLUE}Mode: {mode}\n"
              f"{self._BLUE}LaunchedDrivers: {active_count()}\n"
              f"{self._RED}MemoryUsageByScript: {current_memory_usage: .2f}MB\n{self._RESET}")
        if logs:
            log_msg = f"Status: {status}\n" \
                      f"Mode: {mode}\n\n"
            if isfile(self._log_file):
                with open(self._log_file, 'a') as file_obj:
                    file_obj.write(log_msg)
            else:
                with open(self._log_file, 'w') as file_obj:
                    file_obj.write(log_msg)
