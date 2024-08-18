from flask import Flask, request, render_template, send_file
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from pytube import YouTube
import os
import tempfile
import logging
import shutil

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Spotify API credentials
SPOTIFY_CLIENT_ID = 'your spotify client id'
SPOTIFY_CLIENT_SECRET = 'your secret key'

# YouTube API credentials
YOUTUBE_API_KEY = 'your youtube data api key'

# Function to get tracks from Spotify playlist
def get_spotify_tracks(playlist_link):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))
    playlist_id = playlist_link.split('/')[-1].split('?')[0]
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    songs = [f"{track['track']['name']} {track['track']['artists'][0]['name']}" for track in tracks]
    return songs

# Function to search song on YouTube
def search_youtube(query):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(q=query, part='snippet', type='video', maxResults=1)
    response = request.execute()
    return response['items'][0]['id']['videoId']

# Function to download MP3 from YouTube
def download_mp3(url, download_folder):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        out_file = stream.download(output_path=download_folder)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        return new_file
    except Exception as e:
        print(f"An error occurred while downloading {url}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    playlist_link = request.form['playlist_link']
    if not playlist_link:
        return render_template('index.html', message='Please enter a Spotify playlist link.')

    # Hardcoded download folder
    download_folder = r"D:\lockedin\projects\spotify_song_downloader\songs"

    try:
        logging.debug("Getting Spotify tracks...")
        songs = get_spotify_tracks(playlist_link)
        logging.debug(f"Tracks retrieved from Spotify: {songs}")
        
        youtube_urls = []
        for song in songs:
            video_id = search_youtube(song)
            youtube_urls.append(f"https://www.youtube.com/watch?v={video_id}")
        logging.debug(f"YouTube URLs: {youtube_urls}")

        downloaded_files = []
        for url in youtube_urls:
            mp3_file = download_mp3(url, download_folder)
            if mp3_file:
                downloaded_files.append(mp3_file)
                logging.debug(f"Downloaded: {url}")

        # Redirect to index with a success message
        return render_template('index.html', message=f"Successfully downloaded {len(downloaded_files)} songs to {download_folder}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return render_template('index.html', message=f"An error occurred: {e}")

if __name__ == '__main__':
    app.run(debug=True)
