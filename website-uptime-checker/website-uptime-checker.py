"""
Website Uptime Checker (Interactive & Colored)
---------------------------------------------
Checks whether a website is UP or DOWN, shows response time,
and logs results to a file.

Author: Hadi Jawdi
Usage:
    python website_uptime_checker.py          # Interactive URL prompt
    python website_uptime_checker.py --interval 10
"""

import sys
import time
import requests
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def check_website(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        response_time = round(time.time() - start_time, 2)

        return {
            "status": "UP",
            "code": response.status_code,
            "time": response_time
        }

    except requests.exceptions.RequestException:
        return {
            "status": "DOWN",
            "code": None,
            "time": None
        }


def log_result(url, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if result["status"] == "UP":
        status_color = Fore.GREEN + "UP"
        details = (
            f"{Fore.YELLOW}Code:{Style.RESET_ALL} {result['code']} | "
            f"{Fore.CYAN}Response Time:{Style.RESET_ALL} {result['time']}s"
        )
    else:
        status_color = Fore.RED + "DOWN"
        details = Fore.RED + "Website is not reachable"

    # Print colored output
    print(f"[{timestamp}] {url} - {status_color} | {details}")

    # Log without colors to file
    clean_log = f"[{timestamp}] {url} - {result['status']}"
    if result["status"] == "UP":
        clean_log += f" | Code: {result['code']} | Response Time: {result['time']}s"

    with open("uptime_log.txt", "a") as file:
        file.write(clean_log + "\n")


def main():
    # Check for interval argument
    interval = None
    if "--interval" in sys.argv:
        index = sys.argv.index("--interval")
        try:
            interval = int(sys.argv[index + 1])
        except (IndexError, ValueError):
            print("Invalid interval. Must be an integer (seconds).")
            sys.exit(1)

    # Always prompt user for URL
    url = input("Enter website URL (e.g., https://example.com): ").strip()

    # Ensure URL has http/https scheme
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Start monitoring
    if interval:
        print(Fore.MAGENTA + f"\nMonitoring {url} every {interval} seconds...\n")
        while True:
            result = check_website(url)
            log_result(url, result)
            time.sleep(interval)
    else:
        result = check_website(url)
        log_result(url, result)


if __name__ == "__main__":
    main()
