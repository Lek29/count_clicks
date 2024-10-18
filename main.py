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

def print_clicks(clicks, error_msg):
    if error_msg:
        print(f'Ошибка {error_msg}')
    else:
        print(f'Количество кликов {clicks}')


def print_short_links(short_links, error_msg):
    if error_msg:
        print(f'Ошибка {error_msg}')
    else:
        print(f'Сокращенная ссылка {short_links}')


def is_shorten_link(url):
    parced_url = urlparse(url)
    return parced_url.netloc == 'vk.cc'


def main():
    global SERVICE_VK_KEY

    try:
        SERVICE_VK_KEY = os.environ['SERVICE_KEY_VK']
    except KeyError:
        print('Ошибка: переменная окружения SERVICE_KEY_VK не установлена')
        return

    try:
        long_link = input('Введите свою ссылку: ')
        if is_shorten_link(long_link):
            clicks, error_msg = count_clicks(SERVICE_VK_KEY, long_link)
            print_clicks(clicks, error_msg)
        else:
            short_link, error_msg = shorten_link(SERVICE_VK_KEY, long_link)
            print_short_links(short_link, error_msg)
    except requests.exceptions.RequestException as e:
        print(f'Произошла ошибка при выполнении запроса: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    load_dotenv()
    main()
