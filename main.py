from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import config


# Getting a car's VIN by number
def get_vin():
    number = input("Enter the car number: ")
    time.sleep(3)

    driver = webdriver.Chrome(
        executable_path="path")   # enter the path to the file chromedriver.exe

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


# getting information about the registration history, traffic accidents and being wanted
def get_info_gibdd(vin):
    driver = webdriver.Chrome(executable_path="path")   # enter the path to the file chromedriver.exe

    driver.get('https://xn--90adear.xn--p1ai/check/auto')  # https://гибдд.рф/check/auto
    time.sleep(30)

    elem = driver.find_element_by_id('checkAutoVIN')
    elem.send_keys(vin)

    data = []
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

        data.append({
            'Модель': model,
            'Год выпуска': year,
            'Цвет': color,
            'Рабочий объем(см³)': volume,
            'Мощность (кВт/л.с.)': power,
            'Периоды владения тс': owner_list,
        })

        print(f'[+] Processed: {task} is done')
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
            title = i.find("p", class_="ul-title").text.strip()
            data_time = i.find_all("li")[0].find("span", class_="field").text.strip()
            type_dtp = i.find_all("li")[1].find("span", class_="field").text.strip()
            region = i.find_all("li")[2].find("span", class_="field").text.strip()
            place = i.find_all("li")[3].find("span", class_="field").text.strip()
            model = i.find_all("li")[4].find("span", class_="field").text.strip()
            year = i.find_all("li")[5].find("span", class_="field").text.strip()
            owner = i.find_all("li")[6].find("span", class_="field").text.strip()
            number = i.find_all("li")[7].find("span", class_="field").text.strip()

            data.append({
                "Информация о происшествии": title,
                "Дата и время происшествия:": data_time,
                "Тип происшествия:": type_dtp,
                "Регион происшествия:": region,
                "Место происшествия:": place,
                "Марка (модель) ТС:": model,
                "Год выпуска ТС:": year,
                "ОПФ собственника:": owner,
                "Номер ТС/из всего ТС в ДТП:": number,
            })

        print(f'[+] Processed: {task} is done')
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

        data.append({
            'Проверка нахождения в розыске': result
        })

        with open('data.json', "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f'[+] Processed: {task} is done')
    except:
        print("The check failed with an error on the server side")


# getting information about Technical data, Number of owners, Being wanted, Availability of restrictions, Being pledged
def get_info_gos_uslugi(vin):
    driver = webdriver.Chrome(
        executable_path="path")  # enter the path to the file chromedriver.exe

    driver.get('https://www.gosuslugi.ru/600308/1/form')   # https://www.gosuslugi.ru/
    time.sleep(10)

    username = driver.find_element_by_id("login")
    password = driver.find_element_by_id("password")

    username.send_keys(config.login)
    time.sleep(3)
    password.send_keys(config.password)
    time.sleep(6)

    driver.find_element_by_xpath("//button[@class='plain-button wide']").click()
    time.sleep(4)
    driver.find_element_by_xpath("//button[@class='button font-']").click()
    time.sleep(5)

    driver.find_element_by_xpath("//input[@name='q1'][@type='text']").send_keys(vin)
    time.sleep(7)
    driver.find_element_by_xpath("//button[@class='button font-']").click()
    time.sleep(3)
    html = driver.page_source

    data = []
    soup = BeautifulSoup(html, "lxml")
    number = soup.find_all("div", class_="car-info-group")[0].find_all('div', class_="info-list-value")[0].text.strip()
    status = soup.find_all("div", class_="car-info-group")[0].find_all('div', class_="info-list-value")[1].text.strip()
    division = soup.find_all("div", class_="car-info-group")[0].find_all('div', class_="info-list-value")[2].text.strip()
    last = soup.find_all("div", class_="car-info-group")[0].find_all('div', class_="info-list-value")[3].text.strip()
    lizing = soup.find_all("div", class_="car-info-group")[0].find_all('div', class_="info-list-value")[4].text.strip()
    model = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[0].text.strip()
    year = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[1].text.strip()
    maker = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[2].text.strip()
    VIN = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[3].text.strip()
    VIN2 = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[4].text.strip()
    frame = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[5].text.strip()
    body = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[6].text.strip()
    color = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[7].text.strip()
    volume = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[8].text.strip()
    engine = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[9].text.strip()
    fuel = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[10].text.strip()
    power = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[11].text.strip()
    type = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[12].text.strip()
    category = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[13].text.strip()
    category_union = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[14].text.strip()
    ecology_class = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[15].text.strip()
    wheel = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[16].text.strip()
    transmission = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[17].text.strip()
    privod = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[18].text.strip()
    seria = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[19].text.strip()
    utilisation = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[20].text.strip()
    declar = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[21].text.strip()
    limit = soup.find_all("div", class_="car-info-group")[1].find_all('div', class_="info-list-value")[21].text.strip()
    owner_cards = soup.find_all("div", class_="car-info-group")[2].find_all('div', class_="info-list-group-item")
    owner_list = []
    for oc in owner_cards:
        owner = oc.find("div", class_="info-list-subtitle").text.strip()
        period = oc.find("div", class_="info-list-value").text.strip()
        owner_list.append(f"Период: {period}, Владелец: {owner}")
    search = soup.find_all("div", class_="car-info-group")[3].find_all('div', class_="info-list-value")[0].text.strip()
    limit_reg = soup.find_all("div", class_="car-info-group")[3].find_all('div', class_="info-list-value")[1].text.strip()
    search_pts = soup.find_all("div", class_="car-info-group")[3].find("div", class_="info-list-group-item").find("div", class_="info-list-value").text.strip()
    zalog = soup.find_all("div", class_="car-info-group")[4].find('div', class_="info-list-value").text.strip()

    data.append({
        'Номер реестровой записи': number,
        'Статус в ГИБДД': status,
        'Наименование подразделения': division,
        'Последняя операция': last,
        'В лизинге': lizing,
        'Марка и модель': model,
        'Год выпуска': year,
        'Изготовитель': maker,
        'Идентификационный номер (VIN)': VIN,
        'Идентификационный номер (VIN2)': VIN2,
        'Номер шасси (рамы)': frame,
        'Номер кузова (кабины)': body,
        'Цвет кузова (кабины)': color,
        'Рабочий объём (куб.см)': volume,
        'Модель двигателя': engine,
        'Тип топлива': fuel,
        'Мощность (кВТ/л.с.)': power,
        'Тип транспортного средства': type,
        'Категория': category,
        'Категория (Там. Союз)': category_union,
        'Экологический класс': ecology_class,
        'Положение руля': wheel,
        'Тип коробки передач': transmission,
        'Тип привода': privod,
        'Серия и номер одобрения типа': seria,
        'Статус утилизационного сбора': utilisation,
        'Номер таможенной декларации (ТД, ТПО)': declar,
        'Таможенные ограничения': limit,
        'История регистрационных действий': owner_list,
        'В розыске': search,
        'Ограничения на регистрацию': limit_reg,
        'В розыске ПТС': search_pts,
        'Находится в залоге': zalog
    })

    with open('data.json', "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    vin = get_vin()
    get_info_gos_uslugi(vin)
    get_info_gibdd(vin)


if __name__ == '__main__':
    main()
