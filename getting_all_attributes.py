import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import time
import json
import os
import shutil


def get_page_soup_from_url(link: str) -> BeautifulSoup:
    """
    Функция возращает html разметку города.
    :param link: str
    return: BeautifulSoup
    """

    chrome_options = Options()  # после получение разметки можно не использовать
    chrome_options.add_argument('--no-sandbox')  # после получение разметки можно не использовать
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(ChromeDriverManager().install(),
                              chrome_options=chrome_options)  # после получение разметки можно не использовать

    try:
        driver.get(link)
    except selenium.common.exceptions.WebDriverException as error:
        print(f"адрес сайта не доступен или есть ошибка {link}")
        exit(1)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    return soup


def write_file_from_soup(list_soup: list, root_folder: str, name_path: str, name_file: str) -> list:
    """
    Функция записывает в файл html разметку города в файл формата HTML
    param soup: BeautifulSoup
    name_city: str
    """
    number_file = 1

    ways_to_files = []

    for soup in list_soup:
        with open(f"{root_folder}/{name_path}/{name_file}_{number_file}.html", "w",
                  encoding='utf-8') as file:  # делаем файл в html, чтобы дергать сайт лишний раз
            file.write(str(soup))
            ways_to_files.append(f"{root_folder}/{name_path}/{name_file}_{number_file}.html")
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


def get_attributes_door(product_card: BeautifulSoup) -> dict:
    """
    Функция возращает все атрибуты двери
    :param product_card: BeautifulSoup
    :return: dict
    """

    domen_name = 'https://bunkerdoors.ru'

    media_img = product_card.find('a', {'class': 'product-gallery-04__stage-item-img-container'})
    picture = media_img.img['src'].strip()

    link_to_picture = domen_name + picture
    name_door = product_card.find('h1', {'class': 'product-01__title'}).text.strip()
    price = product_card.find('div', {'class': 'product-01__current-price'}).text.strip()

    full_description_product_card = {
        'name': name_door,
        'price': price
    }

    parameters = product_card.findAll('dl', {'class': 'product-01__parameters-item'})

    for parameter in parameters:
        attribute = parameter.find('dt', {'class': 'product-01__parameters-item-term'}).text.strip()
        description = parameter.find('dd', {'class': 'product-01__parameters-item-dscr'}).text.strip()
        full_description_product_card[attribute] = description

    full_description_product_card['link'] = link_to_picture

    return full_description_product_card


def receive_soup_base_doors() -> list:
    """
    Функция возвращает soup base doors с сайта bunkerdoors.ru
    :return: list
    """
    name_path_for_json = 'links_to_bunker_doors'
    base_doors = 'Base_doors'
    number_page = 1
    quantity = 0
    print(base_doors)

    file_base_series = open(f'{name_path_for_json}/{base_doors}/Base_series_{number_page}.json')
    receive_data = json.load(file_base_series)
    print(receive_data)

    list_soup_base_doors = []

    for link in receive_data['Base_series']:
        soup_door = get_page_soup_from_url(link)
        list_soup_base_doors.append(soup_door)
        quantity += 1
        print(f'Количество обработанных ссылок {base_doors} - {quantity}')

    file_base_series.close()

    return list_soup_base_doors


def receive_soup_hit_doors() -> list:
    """
    Функция возвращает soup hit doors с сайта bunkerdoors.ru
    :return: list
    """

    name_path_for_json = 'links_to_bunker_doors'
    hit_doors = 'Hit_doors'
    number_page = 7
    quantity = 0
    print(hit_doors)

    list_soup_hit_doors = []

    for number in range(1, number_page + 1):
        print(f'{number} - номер файла')
        file_hit_series = open(f'{name_path_for_json}/{hit_doors}/Hit_series_{number}.json')
        receive_data = json.load(file_hit_series)
        print(receive_data)
        for link in receive_data['Hit_series']:
            soup_door = get_page_soup_from_url(link)
            list_soup_hit_doors.append(soup_door)
            quantity += 1
            print(f'Количество обработанных ссылок {hit_doors} - {quantity}')

        file_hit_series.close()

    return list_soup_hit_doors


def receive_soup_prime_doors() -> list:
    """
    Функция возвращает soup prime doors с сайта bunkerdoors.ru
    :return: list
    """

    name_path_for_json = 'links_to_bunker_doors'
    prime_doors = 'Prime_doors'
    number_page = 2
    quantity = 0

    print(prime_doors)

    list_soup_prime_doors = []

    for number in range(1, number_page + 1):
        print(f'{number} - номер файла')
        file_prime_series = open(f'{name_path_for_json}/{prime_doors}/Prime_series_{number}.json')
        receive_data = json.load(file_prime_series)
        print(receive_data)
        for link in receive_data['Prime_series']:
            soup_door = get_page_soup_from_url(link)
            list_soup_prime_doors.append(soup_door)
            quantity += 1
            print(f'Количество обработанных ссылок {prime_doors} - {quantity}')

        file_prime_series.close()

    return list_soup_prime_doors


def receive_soup_termo_doors() -> list:
    """
    Функция возвращает soup termo doors с сайта bunkerdoors.ru
    :return: list
    """

    name_path_for_json = 'links_to_bunker_doors'
    termo_doors = 'Termo_doors'
    number_page = 2
    quantity = 0
    print(termo_doors)

    list_soup_termo_doors = []

    for number in range(1, number_page + 1):
        print(f'{number} - номер файла')
        file_termo_series = open(f'{name_path_for_json}/{termo_doors}/Termo_series_{number}.json')
        receive_data = json.load(file_termo_series)
        print(receive_data)
        for link in receive_data['Termo_series']:
            soup_door = get_page_soup_from_url(link)
            list_soup_termo_doors.append(soup_door)
            quantity += 1
            print(f'Количество обработанных ссылок {termo_doors} - {quantity}')

        file_termo_series.close()

    return list_soup_termo_doors


def parsing_attributes_bunker_doors(list_soup_series_doors: list, root_folder: str, name_path: str,
                                    name_file: str) -> dict:
    """
    Функция парсит атрибуты дверей пример ("Толщина стали, полотна": "Лист металла 1,2 мм, Толщина полотна 90 мм")
    :param list_soup_series_doors: list
    :param root_folder: str
    :param name_path: str
    :param name_file: str
    :return: dict
    """

    files = write_file_from_soup(list_soup_series_doors, root_folder, name_path, name_file)

    file_for_json = {}
    attributes_doors = []

    for file in files:
        product_card = get_page_soup_from_file(file)
        full_description_product_card = get_attributes_door(product_card)
        attributes_doors.append(full_description_product_card)

    file_for_json[name_path] = attributes_doors

    return file_for_json


def parsing_base_attributes_doors() -> dict:
    """
    Функция записывае данные с категории base doors и записывает их в словарь
    :return: dict
    """
    root_folder = 'all attributes doors'
    path_base_series = 'Base_series'
    file_base_door = 'Base_door'

    #----------------получение атрибутов base_series_doors
    os.makedirs(os.path.join(root_folder, path_base_series))  # папка для атрибутов base_series кладется soup

    list_soup_base_doors = receive_soup_base_doors()  # парсинг атрибутов base дверей
    file_for_json_base_series = parsing_attributes_bunker_doors(
        list_soup_base_doors, root_folder, path_base_series, file_base_door
    )

    return file_for_json_base_series


def parsing_hit_attributes_doors() -> dict:
    """
    Функция записывае данные с категории hit doors и записывает их в словарь
    :return: dict
    """
    root_folder = 'all attributes doors'
    path_hit_series = 'Hit_series'
    file_hit_door = 'Hit_door'

    #------------------получение атрибутов hit_series_doors
    os.makedirs(os.path.join(root_folder, path_hit_series))

    list_soup_hit_doors = receive_soup_hit_doors()  # парсинг атрибутов hit дверей
    file_for_json_hit_series = parsing_attributes_bunker_doors(
        list_soup_hit_doors, root_folder, path_hit_series, file_hit_door
    )

    return file_for_json_hit_series


def parsing_prime_attributes_doors() -> dict:
    """
    Функция записывае данные с категории prime doors и записывает их в словарь
    :return: dict
    """
    root_folder = 'all attributes doors'
    path_prime_series = 'Prime_series'
    file_prime_door = 'Prime_door'

    #-----------------получение атрибутов prime_series_doors
    os.makedirs(os.path.join(root_folder, path_prime_series))

    list_soup_prime_doors = receive_soup_prime_doors()  # парсинг атрибутов prime дверей
    file_for_json_prime_series = parsing_attributes_bunker_doors(
        list_soup_prime_doors, root_folder, path_prime_series, file_prime_door
    )

    return file_for_json_prime_series


def parsing_termo_attributes_doors() -> dict:
    """
    Функция записывае данные с категории termo doors и записывает их в словарь
    :return: dict
    """
    root_folder = 'all attributes doors'
    path_termo_series = 'Termo_series'
    file_termo_door = 'Termo_door'

    #----------------получение атрибутов termo_series_doors
    os.makedirs(os.path.join(root_folder, path_termo_series))
    list_soup_termo_doors = receive_soup_termo_doors()  # парсинг атрибутов termo дверей
    file_for_json_termo_series = parsing_attributes_bunker_doors(
        list_soup_termo_doors, root_folder, path_termo_series, file_termo_door
    )

    return file_for_json_termo_series


def parsing_all_attributes_doors() -> list:
    """
    Функция возвращает данные в виде листа (в листе данные по всем категориям base, hit, prime, termo)
    :return: list
    """
    root_folder = 'all attributes doors'
    check_path(root_folder)
    os.mkdir(root_folder)

    file_for_json_base_series = parsing_base_attributes_doors()
    file_for_json_hit_series = parsing_hit_attributes_doors()
    file_for_json_prime_series = parsing_prime_attributes_doors()
    file_for_json_termo_series = parsing_termo_attributes_doors()

    return [file_for_json_base_series, file_for_json_hit_series, file_for_json_prime_series, file_for_json_termo_series]


def recieve_four_json_file():
    """
    Функция записывает в json файл атрибуты всех категорий (base, hit, prime, termo)
    :return:
    """

    name_path_for_json = 'attributes bunker doors for json'
    series_doors = ['Base_door', 'Hit_door', 'Prime_door', 'Termo_door']

    check_path(name_path_for_json)
    os.mkdir(name_path_for_json)

    all_attributes_doors = parsing_all_attributes_doors()

    number_series = 0

    for file_series_door in all_attributes_doors:
        with open(f'{name_path_for_json}/{series_doors[number_series]}.json', 'a', encoding='utf-8') as file_json:
            json.dump(file_series_door, file_json, indent=4, ensure_ascii=False)
            number_series += 1
