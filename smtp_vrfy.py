import smtplib
import sys
import time
from termcolor import colored  # For colored output


def brute_force_smtp_vrfy(ip, port, wordlist, valid_code):
    valid_names = []  # To store all valid results

    try:
        with open(wordlist, 'r') as file:
            names = file.read().splitlines()

        for name in names:
            try:
                # Establish connection
                smtp = smtplib.SMTP(ip, port)
                smtp.ehlo_or_helo_if_needed()

                # Send VRFY command
                code, response = smtp.verify(name)
                response = response.decode() if isinstance(response, bytes) else response

                if code == valid_code:
                    print(colored(f"[VALID] {name}: {code} - {response}", "green"))
                    valid_names.append(name)
                else:
                    print(colored(f"[INVALID] {name}: {code} - {response}", "red"))

                smtp.quit()
                time.sleep(0.5)  # Add a delay to avoid rate-limiting

            except smtplib.SMTPException as e:
                print(colored(f"Error verifying {name}: {e}", "yellow"))
                continue
            except ConnectionError as e:
                print(colored(f"Connection error with {name}: {e}", "yellow"))
                time.sleep(2)  # Wait before retrying
    except FileNotFoundError:
        print(colored(f"Wordlist file '{wordlist}' not found.", "red"))
    except Exception as e:
        print(colored(f"Unexpected error: {e}", "red"))

    # Summary of valid results
    print("\n" + "="*30)
    print(colored("Summary of Valid Results:", "green"))
    for valid in valid_names:
        print(colored(valid, "green"))
    print("="*30)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 smtp_vrfy.py <IP> <PORT> <WORDLIST> <VALID_CODE>")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    wordlist = sys.argv[3]
    valid_code = int(sys.argv[4])

    brute_force_smtp_vrfy(ip, port, wordlist, valid_code)

