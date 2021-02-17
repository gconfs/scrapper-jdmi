#!/usr/bin/python

from collections import deque
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue, Pool, Manager

import queue

import sys
sys.setrecursionlimit(1000000)

WEBSITE = "https://books.toscrape.com"

class Scraper:
    def __init__(self, root_url: str, processes: int =1):
        self.root = root_url


        self.manager = Manager()

        self.to_visit = Queue()
        self.to_visit.put(root_url)

        self.results = Queue()

        self.visited = self.manager.dict()

        self.processes = []

        for _ in range(processes):
            proc = Process(target=f, args=(self.to_visit, self.visited, self.results))
            self.processes.append(proc)

    def worker(to_visit, visited, results):
        while True:
            try:
                url = to_visit.get(timeout=5)
            except queue.Empty:
                return

            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")

            results.put((url, soup))

            for a in soup.find_all("a"):
                link = a.get("href")

                if not link:
                    continue

                link = urljoin(url, link)

                if link in visited:
                    continue

                visited[link] = True
                to_visit.put(link)


    def start(self):
        for proc in self.processes:
            proc.start()

    def get_results(self):
        while True:
            try:
                res = self.results.get(timeout=5)
                yield res
            except queue.Empty:
                return

    def stop(self):
        for i, proc in enumerate(self.processes):
            proc.join()


def is_book(soup):
    product_description = soup.find("div", {"id": "product_description"})
    return product_description != None

def get_price(soup):
    price_string = soup.find("p", {"class": "price_color"})
    if not price_string:
        return None

    price_string = price_string.string
    price = float(price_string[2:])

    return price

def get_book_title(soup):
    product_main = soup.find("div", {"class": "product_main"})
    if not product_main:
        return None

    return product_main.h1.string

def main():
    s = Scraper(WEBSITE, processes=16)
    s.start()

    total = 0

    for link, soup in s.get_results():
        isbook = is_book(soup)
        if not isbook:
            continue

        price = get_price(soup)
        total += price

    print(total)

    s.stop()

if __name__ == "__main__":
    main()
