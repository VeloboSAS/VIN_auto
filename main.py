from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_vin():
    number = input("Enter the car number: ")
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
    return vin


def get_history(vin):
    driver = webdriver.Chrome(executable_path="Path")

    driver.get('https://xn--90adear.xn--p1ai/check/auto')
    time.sleep(30)

    elem = driver.find_element_by_id('checkAutoVIN')
    elem.send_keys(vin)
    share = driver.find_element_by_class_name('checker')
    share.click()

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'close_modal_window'))).click()
        time.sleep(15)
    except:
        print("Error")

    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    model = soup.find("span", class_="field vehicle-model").text
    year = soup.find("span", class_="field vehicle-year").text
    color = soup.find("span", class_="field vehicle-color").text
    volume = soup.find("span", class_="field vehicle-engineVolume").text
    power = soup.find("span", class_="field vehicle-powerKwtHp").text
    owner_cards = soup.find("ul", class_="ownershipPeriods").find_all("li")

    owner_list = []
    for oc in owner_cards:
        period_from = oc.find('span', class_="ownershipPeriods-from").text
        period_to = oc.find("span", class_="ownershipPeriods-to").text
        owner = oc.find('span', class_="simplePersonType").text
        owner_list.append(f"С: {period_from}, По: {period_to}, Владелец: {owner})")

    data = {
        'Модель': model,
        'Год выпуска': year,
        'Цвет': color,
        'Рабочий объем(см³)': volume,
        'Мощность (кВт/л.с.)': power,
        'Периоды владения тс': owner_list,
    }

    with open('data.json', "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    vin = get_vin()
    get_history(vin)


if __name__ == '__main__':
    main()
