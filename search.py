import requests
from songs import get_song
from environs import Env
import argparse


def search(request, headers):
    url = 'https://api.genius.com/search/'
    response = requests.get(url, headers=headers, params={'q': request})
    response.raise_for_status()

    for song in response.json()['response']['hits']:
        get_song(song['result']['id'], headers)


def main():
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        description='Запуская данный скрипт вы получаете результаты поиска по вашему запросу, а также данные по песням, их текста и обложки(в папке songs)'
        )
    parser.add_argument('-r', '--request', help='Ваш запрос', required=True)
    args = parser.parse_args()

    headers = {'Authorization': f'Bearer {env('API_KEY')}'}
    search(args.request, headers)


if __name__ == '__main__':
    main()
