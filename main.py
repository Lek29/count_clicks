import requests
from dotenv import load_dotenv
import os
from urllib.parse import urlparse


def shorten_link(token, link):
    # if is_shorten_link(link):
    #     return link

    params = {
        'url': link,
        'access_token': token,
        'v': '5.191',
    }
    url_short_link = 'https://api.vk.com/method/utils.getShortLink'

    response = requests.get(url_short_link, params=params)
    response.raise_for_status()

    json_params = response.json()
    if 'error' in json_params:
        error_msg = ['error'].get('error_msg', 'неизвестная ошибка')
        return f'Ошибка: {error_msg}'
    short_link = json_params['response']['short_url']
    return short_link


def count_clicks(token, link):
    # if not is_shorten_link(link):
    #     link = shorten_link(token, link)

    parsed_url = urlparse(link)
    key = parsed_url.path.strip('/')

    params = {
        'access_token': token,
        'key': key,
        'v': '5.191',
        'intervals_count': 100,
        'extended': 0,
    }
    url_status = 'https://api.vk.com/method/utils.getLinkStats'


    response = requests.get(url_status, params=params)
    response.raise_for_status()
    json_params = response.json()

    if 'error' in json_params:
        error_msg = (
            json_params['error']
            .get('error_msg', 'неизвестная ошибка')
        )
        return f'Ошибка: {error_msg}'
    clicks = sum(
        interval['views']
        for interval in json_params['response']['stats']
    )
    return f'Количество кликов по ссылке: {clicks}'


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
            print(count_clicks(SERVICE_VK_KEY, long_link))
        else:
            print(shorten_link(SERVICE_VK_KEY, long_link))
    except requests.exceptions.RequestException as e:
        print(f'Произошла ошибка при выполнении запроса: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    load_dotenv()
    main()
