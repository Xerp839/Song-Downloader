# Song-Downloader
Download your spotify playlist songs in mp3, using spotipy and pytube 

![2](https://github.com/user-attachments/assets/b41be614-9f2d-4333-ac62-103f8c9e1704)


![3](https://github.com/user-attachments/assets/0e9a1c4a-2daa-4df2-83ef-e7ba0af66068)


![4](https://github.com/user-attachments/assets/626a12bf-1e80-4c44-b6be-ae1784ea7d60)


![6](https://github.com/user-attachments/assets/404ce158-9aee-4db3-b8fe-9e61ac17448b)

## 🛠️ How Does It Work?

1. **Enter Spotify Playlist Link**: 
   - Provide a valid Spotify playlist link to the application.

2. **Fetch Tracks**: 
   - The app interacts with the Spotify API to retrieve all the tracks from the provided playlist.

3. **Search YouTube**: 
   - For each track in the playlist, the app performs a search on YouTube and retrieves the top result matching the song title and artist.

4. **Download MP3**: 
   - The app then downloads the audio from the top YouTube result and converts it to MP3 format, saving it locally.

## there is an issue with pytube 15.0.0
so i added cipher.py file, 
replace this with your cipher.py which would be in pytube folder where your python libs are installed 
