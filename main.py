#!/usr/bin/python

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

WEBSITE = "https://books.toscrape.com"

def visit(url, visited, max_depth=-1, done=print):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    done(url)
    print(visited)

    for a in soup.find_all("a"):
        link = a.get("href")

        if not link:
            continue

        link = urljoin(url, link)

        if link in visited:
            continue

        visited[link] = True
        visit(link, visited)


def main():
    visited = {}
    visit(WEBSITE, visited)

if __name__ == "__main__":
    main()
