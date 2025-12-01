import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup


def download_image_or_lyrics(file_path, data, is_image=False):
    if is_image:
        with open(file_path, 'wb') as image:
            image.write(data)
    else:
        with open(file_path, 'w', encoding='utf-8') as text:
            text.write(data)


def download_songs_texts(songs):
    for song in songs['response']['songs']:
        folder_path = f'songs/{song['artist_names']}/texts'
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, song['title'])

        url = f'https://genius.com/{song['path']}'
        song = requests.get(url)

        soup = BeautifulSoup(song.text, "html.parser")

        lyrics = soup.select_one('.Lyrics__Container-sc-68a46031-1')
        lyrics.select_one('.LyricsHeader__Container-sc-6f4ef545-1').decompose()
        lyrics = lyrics.get_text(separator="\n")

        download_image_or_lyrics(file_path, lyrics, False)


def download_songs_covers(songs, headers):
    for song in songs['response']['songs']:
        folder_path = f'songs/{song["artist_names"]}/images'
        os.makedirs(folder_path, exist_ok=True)

        image_url = song['header_image_thumbnail_url']

        response = requests.get(
            image_url,
            headers=headers
        )
        response.raise_for_status()

        image_extension = Path(image_url).suffix

        filename = f"{song['title'].replace('/', '_')}{image_extension}"
        file_path = os.path.join(folder_path, filename)

        download_image_or_lyrics(file_path, response.content, True)
