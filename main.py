from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Getting a car's VIN by number
def get_vin():
    number = input("Enter the car number: ")
    time.sleep(3)

    driver = webdriver.Chrome(
        executable_path="C:\\Users\\vovik\\PycharmProjects\\test\\Sel\\ChromeDriver\\chromedriver.exe")

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


# Checking the registration history in the traffic police
def get_history(vin):
    driver = webdriver.Chrome(executable_path="Path")

    driver.get('https://xn--90adear.xn--p1ai/check/auto')
    time.sleep(30)

    elem = driver.find_element_by_id('checkAutoVIN')
    elem.send_keys(vin)
    driver.find_element_by_class_name('checker').click()

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'close_modal_window'))).click()
        time.sleep(15)
    except TimeoutException:
        print("TimeoutException")

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

    with open('data_history.json', "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Checking for participation in road accidents
def get_dtp(vin):
    driver = webdriver.Chrome(executable_path=
                              "C:\\Users\\vovik\\PycharmProjects\\test\\Sel\\ChromeDriver\\chromedriver.exe")

    driver.get('https://xn--90adear.xn--p1ai/check/auto')
    time.sleep(30)

    elem = driver.find_element_by_id('checkAutoVIN')
    elem.send_keys(vin)
    driver.find_element_by_xpath("//a[@class='checker'][@data-type='aiusdtp']").click()

    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'close_modal_window'))).click()
    except TimeoutException:
        print("TimeoutException")

    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    cards = soup.find("ul", class_="aiusdtp-list").find_all("li")[::17]

    for i in cards:
        try:
            title = i.find("p", class_="ul-title").text.strip()
        except:
            title = ''
        try:
            data_time = i.find_all("li")[0].find("span", class_="field").text.strip()
        except:
            data_time = ""
        try:
            type_dtp = i.find_all("li")[1].find("span", class_="field").text.strip()
        except:
            type_dtp = ''
        try:
            region = i.find_all("li")[2].find("span", class_="field").text.strip()
        except:
            region = ''
        try:
            place = i.find_all("li")[3].find("span", class_="field").text.strip()
        except:
            place = ''
        try:
            model = i.find_all("li")[4].find("span", class_="field").text.strip()
        except:
            model = ''
        try:
            year = i.find_all("li")[5].find("span", class_="field").text.strip()
        except:
            year = ''
        try:
            owner = i.find_all("li")[6].find("span", class_="field").text.strip()
        except:
            owner = ''
        try:
            number = i.find_all("li")[7].find("span", class_="field").text.strip()
        except:
            number = ''

        data = {
                "Информация о происшествии": title,
                "Дата и время происшествия:": data_time,
                "Тип происшествия:": type_dtp,
                "Регион происшествия:": region,
                "Место происшествия:": place,
                "Марка (модель) ТС:": model,
                "Год выпуска ТС:": year,
                "ОПФ собственника:": owner,
                "Номер ТС/из всего ТС в ДТП:": number,
            }
        with open('data_dtp.json', "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


# Verification of being wanted
def get_search(vin):
    driver = webdriver.Chrome(executable_path=
                              "C:\\Users\\vovik\\PycharmProjects\\test\\Sel\\ChromeDriver\\chromedriver.exe")

    driver.get('https://xn--90adear.xn--p1ai/check/auto')
    time.sleep(30)

    elem = driver.find_element_by_id('checkAutoVIN')
    elem.send_keys(vin)
    driver.find_element_by_xpath("//a[@class='checker'][@data-type='wanted']").click()

    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'close_modal_window'))).click()
    except TimeoutException:
        print("TimeoutException")

    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    result = soup.find("div", id="checkAutoWanted").find_all("p")[1].text

    data = {
        'Проверка нахождения в розыске': result
    }

    with open('data_search.json', "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_info(vin):
    driver = webdriver.Chrome(executable_path=
                              "C:\\Users\\vovik\\PycharmProjects\\test\\Sel\\ChromeDriver\\chromedriver.exe")

    driver.get('https://xn--90adear.xn--p1ai/check/auto')
    time.sleep(30)

    elem = driver.find_element_by_id('checkAutoVIN')
    elem.send_keys(vin)
    try:
        task = "the registration history"
        driver.find_element_by_class_name('checker').click()

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'close_modal_window'))).click()
            time.sleep(15)
        except TimeoutException:
            print("TimeoutException")

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

        with open('data.json', "a", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.write(',\n')

        print(f'[+] Processed:{task} is done')
    except:
        print("The check failed with an error on the server side")

    try:
        task = "participation in road accidents"
        driver.find_element_by_xpath("//a[@class='checker'][@data-type='aiusdtp']").click()

        try:
            WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CLASS_NAME, 'close_modal_window'))).click()
        except TimeoutException:
            print("TimeoutException")

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        cards = soup.find("ul", class_="aiusdtp-list").find_all("li")[::17]

        for i in cards:
            try:
                title = i.find("p", class_="ul-title").text.strip()
            except:
                title = ''
            try:
                data_time = i.find_all("li")[0].find("span", class_="field").text.strip()
            except:
                data_time = ""
            try:
                type_dtp = i.find_all("li")[1].find("span", class_="field").text.strip()
            except:
                type_dtp = ''
            try:
                region = i.find_all("li")[2].find("span", class_="field").text.strip()
            except:
                region = ''
            try:
                place = i.find_all("li")[3].find("span", class_="field").text.strip()
            except:
                place = ''
            try:
                model = i.find_all("li")[4].find("span", class_="field").text.strip()
            except:
                model = ''
            try:
                year = i.find_all("li")[5].find("span", class_="field").text.strip()
            except:
                year = ''
            try:
                owner = i.find_all("li")[6].find("span", class_="field").text.strip()
            except:
                owner = ''
            try:
                number = i.find_all("li")[7].find("span", class_="field").text.strip()
            except:
                number = ''

            data = {
                "Информация о происшествии": title,
                "Дата и время происшествия:": data_time,
                "Тип происшествия:": type_dtp,
                "Регион происшествия:": region,
                "Место происшествия:": place,
                "Марка (модель) ТС:": model,
                "Год выпуска ТС:": year,
                "ОПФ собственника:": owner,
                "Номер ТС/из всего ТС в ДТП:": number,
            }
            with open('data.json', "a", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
                file.write(',\n')

        print(f'[+] Processed:{task} is done')
    except:
        print("The check failed with an error on the server side")

    try:
        task = "Verification of being wanted"
        driver.find_element_by_xpath("//a[@class='checker'][@data-type='wanted']").click()

        try:
            WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CLASS_NAME, 'close_modal_window'))).click()
        except TimeoutException:
            print("TimeoutException")

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        result = soup.find("div", id="checkAutoWanted").find_all("p")[1].text

        data = {
            'Проверка нахождения в розыске': result
        }

        with open('data.json', "a", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f'[+] Processed:{task} is done')
    except:
        print("The check failed with an error on the server side")


def main():
    # vin = "X9FMXXEEBMCG01011"
    vin = "XUFTA69EJEN029234"
    # vin = get_vin()
    # get_history(vin)
    # get_dtp(vin)
    # get_search(vin)
    get_info(vin)


if __name__ == '__main__':
    main()
