from pathvalidate import sanitize_filename
import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from tools import download_image_or_lyrics
import argparse
from environs import Env


def get_song(song_id, headers):
    url = f'https://api.genius.com/songs/{song_id}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    song = response.json()['response']['song']

    lyrics_folder_path = f'songs/{song['artist_names']}/texts'
    os.makedirs(lyrics_folder_path, exist_ok=True)
    lyrics_file_path = os.path.join(
        lyrics_folder_path,
        sanitize_filename(song['title'])
        )

    images_folder_path = f'songs/{song['artist_names']}/images'
    os.makedirs(images_folder_path, exist_ok=True)

    image_url = song['header_image_thumbnail_url']

    response = requests.get(
        image_url,
        headers=headers
    )
    response.raise_for_status()

    image_extension = Path(image_url).suffix

    filename = f"{song['title'].replace('/', '_')}{image_extension}"
    file_path = os.path.join(images_folder_path, sanitize_filename(filename))

    download_image_or_lyrics(file_path, response.content, True)

    print(f"""
Название: {song['title']}
Музыкант: {song['artist_names']}
Ссылка на текст: {song['url']}
Ссылка на изображение: {song['song_art_image_url']}
Дата выхода: {song['release_date_for_display']}""")

    url = f'https://genius.com/{song['path']}'
    song = requests.get(url)

    soup = BeautifulSoup(song.text, "html.parser")

    lyrics = soup.select_one('.Lyrics__Container-sc-68a46031-1')
    lyrics.select_one('.LyricsHeader__Container-sc-6f4ef545-1').decompose()
    lyrics = lyrics.get_text(separator="\n")

    download_image_or_lyrics(lyrics_file_path, lyrics, False)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        description='Запуская данный скрипт вы получаете данные по одной песне, а также в папку songs сохраняется её обложка и текст'
        )
    parser.add_argument('-id', '--song_id', help='ID песни', required=True, type=int)
    args = parser.parse_args()

    headers = {'Authorization': f'Bearer {env('API_KEY')}'}
    get_song(args.song_id, headers)
