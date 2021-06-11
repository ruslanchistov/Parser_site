"""Парсинг сайтов"""

import requests  # для работы с запросами.
from bs4 import BeautifulSoup  # разбирает HTML страницу, делает из неё объект.
import csv  # для создания файла, который можно потом открыть в EXEL или OpenOffice.

FILE_NAME = 'toys.csv'
HOST = 'https://www.toy.ru'  # сайт, который мы будем пастить.
URL = 'https://www.toy.ru/catalog/pazly/'  # url страницы,которую будем пастить.
# Прописываем заголовки, чтобы сайт не подумал, что мы бот.
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
              '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.141 Safari/537.36'
}


# обращение к странице, чтобы получить HTML.
def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)  # запрашиваем данные со страницы.
    return r


# получаем контент со страницы (c одной).
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')  # сохраняем объект страницы.
    items = soup.find_all('div', class_='col-12 col-sm-6 col-md-6 col-lg-4 col-xl-4 my-2')
    toys = []
    for item in items:
        toys.append(
            {
                'title': item.find('img', class_='img-fluid').get('alt'),
                'linc': HOST + item.find('div', class_='h-100 row').find('a').get('href'),
                'photo': item.find('img', class_='img-fluid').find('img').get('src')
            }
        )
    return toys


# Промежуточный тест:
# html = get_html(URL)
# print(get_content(html.text))

""" Функция записи данных """


def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';', dialect='excel')
        writer.writerow(['Название_игрушки', 'Ссылка_на_игрушку', 'Изображение_игрушки'])  # Первая строка.
        for item in items:
            writer.writerow([item['title'], item['linc'], item['photo']])


""" Основная функция парсинга """


def pars():
    page_count = int(input('Укажите количество страниц для парсинга: '))
    html = get_html(URL)
    if html.status_code == 200:  # Проверям приходят ли к нам данные со страницы.
        toys = []
        for page in range(1, page_count + 1):
            print(f'Парсим {page} страницу')
            params = '?count=9&PAGEN_3=' + str(page)
            html = get_html(URL + params)
            toys.extend(get_content(html.text))
        print('Парсинг закончен.')
        save_doc(toys, FILE_NAME)
    else:
        print('ERROR !')


pars()

""" Функция чтения csv файла в консоль """
with open("toys.csv") as r_file:
    # Создаем объект словарь, указываем символ-разделитель ","
    file_reader = csv.DictReader(r_file, delimiter=";")
    # Счетчик для подсчета количества строк и вывода заголовков столбцов
    count = 0
    # Считывание данных из CSV файла
    for row in file_reader:
        if count == 0:
            # Вывод строки, содержащей заголовки для столбцов.
            print('             ', "                               \
                             ".join(row))
        # Вывод содержимого строки по ключу.
        print(f' {row["Название_игрушки"]} -- {row["Ссылка_на_игрушку"]}\
         -- {row["Изображение_игрушки"]}')
        count += 1
