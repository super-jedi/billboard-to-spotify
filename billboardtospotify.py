from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = "INSERT CLIENT ID"
SPOTIFY_CLIENT_SECRET = "INSERT CLIENT SECRET"
SPOTIFY_REDIRECT = "https://example.com"
date = input("Enter the billboard date (YYYY-MM-DD): ")
billboard_url = f"https://www.billboard.com/charts/hot-100/{date}/"

page_data = requests.get(url=billboard_url)
page_data = page_data.text

soup = BeautifulSoup(page_data, "html.parser")

all_articles = soup.select("li ul li h3")

song_titles = [song.getText().strip() for song in all_articles]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT,
                                               scope="playlist-modify-private",
                                               cache_path="token.txt"))


user = sp.current_user()
user_id = user["id"]

song_uris = []
year = date.split("-")[0]

for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify.")

# print(song_uris[0:5])

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard Hot 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

