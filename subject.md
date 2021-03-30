# Brrrrrr Scraper subject

In this activity you are going to [scrape a website](https://en.wikipedia.org/wiki/Web_scraping). We are here to help you, don't hesitate to ask any questions, there is no stupid question.

## Part 1: Build your own web scraper

We are going to use the [`requests`](https://requests.readthedocs.io/en/latest/user/quickstart/) library to send HTTP requests and the [`BeautifulSoup` ](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library to parse HTML.

Before doing anything, please run ``pip install bs4`` in a terminal

Here is how to make an HTTP request with [`requests`](https://requests.readthedocs.io/en/latest/user/quickstart/):
```python3
>>> import requests
>>> r = requests.get("https://google.com")
>>> r.text
<!doctype html><html itemscope="" itemtype="http://schema.org/WebPage" lang="fr"><head><meta content="text/html;...
```

And here is how we can parse some HTML :)
```python3
>>> html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/jacky" class="brother" id="link3">Jacky</a>;
and they lived at the bottom of a well.</p>"""

>>> from bs4 import BeautifulSoup
>>> soup = BeautifulSoup(html_doc, "html.parser")
>>> # Let's find all *a* tags
>>> soup.find_all("a")
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
  <a class="brother" href="http://example.com/jacky" id="link3">Jacky</a>]
```

If we only want to get the brother we can do this:
```python3
>>> soup.find("a", {"class": "brother"})
<a class="brother" href="http://example.com/jacky" id="link3">Jacky</a>
```

### General Algorithm
- Make request
- Parse HTML
- Look into the parsed HTML for data to gather
- back to step 1

*Don't forget about Python __dictionaries__*.

**Question 1**: How many links are there on ``http://books.toscrape.com``?
**Question 2**: How many **different** book is there on the website?


## Part 2: Extract usefull data
Your scraper is not realy fast (ask for the Part 3 if you have done every other questions, we will walk you through our implementation and you could try to do the "same"). Because we are trying to find data in the whole website, you would have to wait a realy long time each time you will try to test a new version of your code.

To avoid this issue, we have provied you a shiny fast scraper to use for this part. [scraper.py](https://gist.githubusercontent.com/n1tram1/a87cba1ea6972cc0b0dbffe207933b05/raw/696258e8e7b4882770c325db4c14747aa4496423/scraper.py)

Here is how you should use the given scraper:
``` python
s = Scraper("your website here") # Create a new scraper
s.start() # Start downloading the website content

for link, soup in s.get_results():
    # Do stuff here.
    # ``link`` is the URL of the webpage.
    # ``soup`` is the BeatifullSoup object corresponding to this page.
    
s.stop() # Stop the scraper
```

**Question 3**: Compute the total cost of buying every book of the [Mystery](https://books.toscrape.com/catalogue/category/books/mystery_3/index.html) category?

**Question 4**: List every book of the [Fiction](https://books.toscrape.com/catalogue/category/books/fiction_10/ing 1 to 20. dex.html) section under 35£?
