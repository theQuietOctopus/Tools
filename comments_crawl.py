import requests
from bs4 import BeautifulSoup, Comment
import argparse
import urllib.parse

def fetch_page(url):
    """
    Fetch the content of the page at the given URL.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[!] Error fetching {url}: {e}")
        return None

def extract_comments(html):
    """
    Extract all HTML comments from the given HTML content.
    """
    soup = BeautifulSoup(html, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    return comments

def find_links(html, base_url):
    """
    Find all unique links in the HTML content, and normalize them with the base URL.
    """
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urllib.parse.urljoin(base_url, href)
        links.add(full_url)
    return links

def crawl(url, depth, visited):
    """
    Crawl the webpage and find comments and links recursively up to the specified depth.
    """
    if depth == 0 or url in visited:
        return

    visited.add(url)
    print(f"[+] Crawling: {url}")
    html = fetch_page(url)
    if not html:
        return

    comments = extract_comments(html)
    if comments:
        print(f"[!] Found comments in {url}:")
        for comment in comments:
            print(f"    {comment.strip()}")

    links = find_links(html, url)
    for link in links:
        crawl(link, depth - 1, visited)

def main():
    parser = argparse.ArgumentParser(description="Crawl a web page to find HTML comments.")
    parser.add_argument("url", help="Full URL of the target web page (e.g., http://example.com:8080/).")
    parser.add_argument("--depth", type=int, default=1, help="Depth of directory searching (default: 1).")
    args = parser.parse_args()

    print(f"[+] Starting crawl at {args.url} with depth {args.depth}")
    crawl(args.url, args.depth, set())

if __name__ == "__main__":
    main()

