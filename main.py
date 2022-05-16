import requests
from bs4 import BeautifulSoup
import json


def get_html(url):
    r = requests.get(url=url)
    return r.text


def get_data():
    pass


def main():
    url = "https://news.sportbox.ru/"
    print(get_html(url))


if __name__ == '__main__':
    main()
