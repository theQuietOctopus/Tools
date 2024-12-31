# Tools

## Comments Web Crawler
**`comments_crawl.py`**: A web crawler to extract HTML comments and recursively explore links.

### Usage
```bash
python3 comments_crawl.py [-h] [--depth DEPTH] url
```
## SMTP User Verification

**`smtp_vrfy.py`**: A script to brute-force SMTP VRFY commands to identify valid user names on a mail server.

### Usage
```bash
python3 smtp_vrfy.py <IP> <PORT> <WORDLIST> <VALID_CODE>
```
## API Brute-Force

**`api_bruteforce.py`**: A script to brute-force POST REQUESTS in API. Additional arguments for headers, attempts and interval are also supplied to prevent IP blacklist.

### Usage
```bash
python3 api_bruteforce.py [-h] [-l USERNAME] [-L USERNAME_LIST] [-p PASSWORD] [-P PASSWORD_LIST] --url URL [--headers [HEADERS ...]] --body BODY --failed-response FAILED_RESPONSE [--attempts ATTEMPTS] [--interval INTERVAL]
```

## CVE-2024-23334

**`CVE-2024-23334.sh`**: A script to exploit the path traversal vulnerability in the python AioHTTP library =< 3.9.1. Props to [z3rObyte](https://github.com/z3rObyte/CVE-2024-23334-PoC)

### Usage
```bash
chmod +x CVE-2024-23334.sh
./CVE-2024-23334.sh <URL> <PATH> <FILE>
```
