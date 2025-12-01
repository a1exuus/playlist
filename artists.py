import requests
from environs import Env
import argparse
from tools import download_songs_covers, download_songs_texts


def get_songs_list(artist_id, headers):

    url = f'https://api.genius.com/artists/{artist_id}/songs'
    params = {'per_page': 10, 'sort': 'popularity'}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    response = response.json()

    for song in response['response']['songs']:
        print(f"""
Название: {song['title']}
Музыкант: {song['artist_names']}
Ссылка на текст: {song['url']}
Ссылка на изображение: {song['song_art_image_url']}
Дата выхода: {song['release_date_for_display']}""")

    download_songs_texts(response)
    download_songs_covers(response, headers)

    return response


if __name__ == '__main__':
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        description='Запуская данный скрипт вы получаете список песен автора'
        )
    parser.add_argument('-id', '--author_id', help='ID автора', required=True, type=int)
    args = parser.parse_args()

    headers = {'Authorization': f'Bearer {env('API_KEY')}'}
    get_songs_list(args.author_id, headers)
