import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver


def get_vin():
    number = input("Введите гос.номер авто: ")
    time.sleep(3)

    driver = webdriver.Chrome(
        executable_path="Path")

    driver.get(url='https://vin01.ru/')
    time.sleep(2)
    numb = driver.find_element_by_class_name("form-control")

    numb.send_keys(number)
    time.sleep(2)
    driver.find_element_by_id("searchByGosNumberButton").click()
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    vin = soup.find("select", class_="form-control").text

    print(vin)


def get_data():
    pass


def main():
    get_vin()


if __name__ == '__main__':
    main()
