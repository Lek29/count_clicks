from dbm import error
from itertools import count

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

    api_response = response.json()
    if 'error' in api_response:
        error_msg = ['error'].get('error_msg', 'неизвестная ошибка')
        return None, error_msg
    short_link = api_response['response']['short_url']
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
    api_response = response.json()

    if 'error' in api_response:
        error_msg = (
            api_response['error']
            .get('error_msg', 'неизвестная ошибка')
        )
        return None, error_msg
    clicks = sum(
        interval['views']
        for interval in api_response['response']['stats']
    )
    return clicks, None


def is_shorten_link(url):
    parced_url = urlparse(url)
    return parced_url.netloc == 'vk.cc'


def main():
    load_dotenv()
    vk_service_key = os.environ['VK_SERVICE_KEY']

    long_link = input('Введите свою ссылку: ')

    try:
        if is_shorten_link(long_link):
            reduction_result, error_msg = count_clicks(vk_service_key, long_link)
            result_message = 'Количество кликов {}'
        else:
            reduction_result, error_msg = shorten_link(vk_service_key, long_link)
            result_message = 'Короткая ссылка: {}'

        if error_msg:
            print(f'Ошибка: {error_msg}')
        else:
            print(result_message.format(reduction_result))
    except requests.exceptions.RequestException as error:
        print(f"Ошибка сети: {error}")
    except Exception as error:
        print(f'Неизвестная ошибка: {error}')


if __name__ == '__main__':
    main()
