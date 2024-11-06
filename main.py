import argparse
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
    return api_response['response']['short_url']


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

    return sum(interval['views'] for interval in api_response['response']['stats'])


def is_shorten_link(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc == 'vk.cc'


def main():
    load_dotenv()
    vk_service_key = os.environ['VK_SERVICE_KEY']

    parser = argparse.ArgumentParser(description='Создание коротких ссылок и подсчет кликов через VK API')
    parser.add_argument('-l', '--link', required=True, help='Введите свою ссылку')
    args = parser.parse_args()
    link = args.link

    try:
        if is_shorten_link(link):
            reduction_result = count_clicks(vk_service_key, link)
            result_message = 'Количество кликов: {}'
        else:
            reduction_result = shorten_link(vk_service_key, link)
            result_message = 'Короткая ссылка: {}'

        print(result_message.format(reduction_result))
    except requests.exceptions.RequestException as error:
        print(f"Ошибка сети: {error}")
    except KeyError as error:
        print(f"Ошибка в ответе API: {error}")
    except Exception as error:
        print(f'Неизвестная ошибка: {error}')


if __name__ == '__main__':
    main()