#!/usr/bin/python

from collections import deque
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue, Pool, Manager

import queue

WEBSITE = "https://books.toscrape.com"

def f(to_visit, visited, results):
    while True:
        try:
            url = to_visit.get(timeout=5)
        except queue.Empty:
            break

        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a"):
            link = a.get("href")

            if not link:
                continue

            link = urljoin(url, link)

            if link in visited:
                continue

            visited[link] = True
            to_visit.put(link)
            results.put(link)

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

    def start(self):
        for proc in self.processes:
            proc.start()

    def get_results(self):
        while True:
            try:
                res = self.results.get(timeout=5)
                yield res
            except queue.Empty:
                break

    def stop(self):
        for proc in self.processes:
            proc.join()


def main():
    s = Scraper(WEBSITE, processes=16)
    s.start()

    for i in s.get_results():
        print(i)

    s.stop()

if __name__ == "__main__":
    main()
