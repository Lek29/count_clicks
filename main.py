from dbm import error

import requests
from dotenv import load_dotenv
import os
from urllib.parse import urlparse


def shorten_link(token, link):
    params = {
        'url': link,
        'access_token': token,
        'v': '5.191',
    }
    short_link_api_url = 'https://api.vk.com/method/utils.getShortLink'

    response = requests.get(short_link_api_url, params=params)
    response.raise_for_status()

    response_json = response.json()
    if 'error' in response_json:
        error_msg = ['error'].get('error_msg', 'неизвестная ошибка')
        return None, error_msg
    short_link = response_json['response']['short_url']
    return short_link, None


def count_clicks(token, link):
    parsed_url = urlparse(link)
    key = parsed_url.path.strip('/')

    params = {
        'access_token': token,
        'key': key,
        'v': '5.191',
        'intervals_count': 100,
        'extended': 0,
    }
    link_status_api_url = 'https://api.vk.com/method/utils.getLinkStats'

    response = requests.get(link_status_api_url, params=params)
    response.raise_for_status()
    response_json = response.json()

    if 'error' in response_json:
        error_msg = (
            response_json['error']
            .get('error_msg', 'неизвестная ошибка')
        )
        return None, error_msg
    clicks = sum(
        interval['views']
        for interval in response_json['response']['stats']
    )
    return clicks, None


def is_shorten_link(url):
    parced_url = urlparse(url)
    return parced_url.netloc == 'vk.cc'


def handle_link(token, link):
    try:
        if is_shorten_link(link):
            return count_clicks(token, link)
        else:
            return shorten_link(token, link)
    except requests.exceptions.RequestException as error:
        return None, error
    except Exception as error:
        return None, error


def main():
    try:
        service_vk_key = os.environ['SERVICE_VK_KEY']
    except KeyError:
        print('Ошибка: переменная окружения SERVICE_VK_KEY не установлена')
        return

    long_link = input('Введите свою ссылку: ')

    result_of_reduction, error_msg = handle_link(service_vk_key, long_link)

    if error_msg:
        print(f'Ошибка: {error_msg}')
    else:
        if is_shorten_link(long_link):
            print(f'Количество кликов: {result_of_reduction}')
        else:
            print(f'Сокращенная ссылка: {result_of_reduction}')


if __name__ == '__main__':
    load_dotenv()
    main()
