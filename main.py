import requests
from dotenv import load_dotenv
import os
from urllib.parse import  urlparse

load_dotenv()
SERVICE_VK_KEY = os.getenv('SERVICE_KEY')


def shorten_link(token, link):
    if is_shorten_link(link):
        return link

    params = {
        'url': link,
        'access_token': token,
        'v': '5.191',
    }
    url_short_link = 'https://api.vk.ru/method/utils.getShortLink'

    try:
        response = requests.get(url_short_link, params=params)
        response.raise_for_status()

        data = response.json()
        if 'error' in data:
            error_msg = data['error'].get('error_msg', 'неизвестная ошибка')
            return f'Ошибка: {error_msg}'
        short_link = data['response']['short_url']
        return short_link
    except requests.exceptions.RequestException as e:
        return f'Произошла ошибка {e}'


def count_clicks(token, link):
    if not is_shorten_link(link):
        link = shorten_link(token, link)


    # short_link = shorten_link(token, link)
    parsed_url = urlparse(link)
    key = parsed_url.path.strip('/')
    print(parsed_url)
    print(key, token, sep='\n')
    params = {
        'access_token': token,
        'key': key,
        'v': '5.191',
        'intervals_count': 100,
        'extended': 0,
    }
    url_status = 'https://api.vk.com/method/utils.getLinkStats'


    try:
        response = requests.get(url_status, params=params)
        response.raise_for_status()
        data = response.json()

        if 'error' in data:
            error_msg = data['error'].get('error_msg', 'неизвестная ошибка')
            return f'Ошибка: {error_msg}'
        clicks = sum(interval['views'] for interval in data['response']['stats'])
        return f'Количество кликов по ссылке: {clicks}'
    except requests.exceptions.RequestException as e:
        return f'Произошла ошибка: {e}'


def is_shorten_link(url):
    parced_url = urlparse(url)
    return parced_url.netloc == 'vk.cc'


def main():
    long_link = input('Введите свою ссылку: ')
    # if is_shorten_link(long_link):
    #     print(count_clicks(SERVICE_VK_KEY, long_link))
    # else:
    #     print(shorten_link(SERVICE_VK_KEY, long_link))
    print(count_clicks(SERVICE_VK_KEY, long_link))

if __name__ == '__main__':
    main()