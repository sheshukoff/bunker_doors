import json

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time
import os
import shutil
from bs4 import BeautifulSoup


def get_page_soup_from_url() -> list:
    """
    Функция возращает html разметку города.
    param city_url: str
    return: BeautifulSoup
    """

    chrome_options = Options()  # после получение разметки можно не использовать
    chrome_options.add_argument('--no-sandbox')  # после получение разметки можно не использовать
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(ChromeDriverManager().install())  # после получение разметки можно не использовать

    number_page = 2

    list_soup = []

    for number in range(1, number_page + 1):
        base_doors = f'https://bunkerdoors.ru/prod/bunker-termo?page={number}'
        try:
            driver.get(base_doors)
        except selenium.common.exceptions.WebDriverException as error:
            print(f"адрес сайта не доступен или есть ошибка {base_doors}")
            exit(1)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        list_soup.append(soup)

    return list_soup


def write_file_from_soup(list_soup: BeautifulSoup, name_path: str, name_file: str):
    """
    Функция записывает в файл html разметку города в файл формата HTML
    param soup: BeautifulSoup
    name_city: str
    """
    number_file = 1

    ways_to_files = []

    for soup in list_soup:
        with open(f"{name_path}/{name_file}_{number_file}.html", "w", encoding='utf-8') as file:  # делаем файл в html, чтобы дергать сайт лишний раз
            file.write(str(soup))
            ways_to_files.append(f"{name_path}/{name_file}_{number_file}.html")

        number_file += 1

    return ways_to_files


def check_path(path: str):
    """
    Функция проверяет существует ли папка
    :param path: str
    :return:
    """
    if os.path.exists(path):
        shutil.rmtree(path)


def get_page_soup_from_file(file_name: str) -> BeautifulSoup:
    """
    Функция возращает html разметку из файла
    param file_name: str
    return: BeautifulSoup
    """
    with open(file_name, "r", encoding='utf-8') as file:  # правильное открытие файла в формате html
        file_html = file.read()

    soup = BeautifulSoup(file_html, 'html.parser')

    return soup


def get_all_link(product_card: BeautifulSoup) -> dict:
    """
    Функция возращает все ссылку на карточку
    param product_card: BeautifulSoup
    return: dict
    """

    link = product_card.find('a').get('href').strip()

    return link


def get_data_from_link(file_name: str):
    products_cards = file_name.find_all('div', {'class': 'products-list-01-item__inner'})

    doors = 'Termo_series'
    roster_doors = {}
    list_links = []

    for product_card in products_cards:
        link_to_product = get_all_link(product_card)
        list_links.append(f'https://bunkerdoors.ru{link_to_product}')

    roster_doors[doors] = list_links

    return roster_doors


def parsing_links_termo_doors():
    get_soup = get_page_soup_from_url()

    name_path = 'Termo_doors'
    check_path(name_path)
    os.mkdir(name_path)

    name_file = 'Termo_series'
    files = write_file_from_soup(get_soup, name_path, name_file)

    name_path_for_json = 'links_to_bunker_doors'
    os.makedirs(os.path.join(name_path_for_json, name_path))

    number_page = 1

    for file in files:
        opened_file = get_page_soup_from_file(file)

        receive_links = get_data_from_link(opened_file)
        print(receive_links)

        with open(f'{name_path_for_json}/{name_path}/{name_file}_{number_page}.json', 'a', encoding='utf-8') as file_json:
            json.dump(receive_links, file_json, indent=4, ensure_ascii=False)

        number_page += 1