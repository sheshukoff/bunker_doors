from parsing_links_base_doors import parsing_links_base_doors
from parsing_links_hit_doors import parsing_links_hit_doors
from parsing_links_prime_doors import parsing_links_prime_doors
from parsing_links_termo_doors import parsing_links_termo_doors

from getting_all_attributes import recieve_four_json_file
from write_date_to_excel import write_all_doors_to_excel

import os
import shutil


def check_path(path: str):
    """
    Функция проверяет существует ли папка
    :param path: str
    :return:
    """
    if os.path.exists(path):
        shutil.rmtree(path)


def recieve_links_bunker_doors():
    """
    Функция записывает все ссылки дверей с сайта bunkerdoors.ru в json файл
    :return:
    """
    name_path = 'links_to_bunker_doors'
    check_path(name_path)
    os.mkdir(name_path)

    parsing_links_base_doors()
    parsing_links_hit_doors()
    parsing_links_prime_doors()
    parsing_links_termo_doors()


def main():
    print('Hello World')
    recieve_links_bunker_doors()
    recieve_four_json_file()
    write_all_doors_to_excel()


if __name__ == '__main__':
    main()
