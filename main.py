#Spotify Liked Artist Playlist Generator

import spotipy as sp
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


#spotify credentials

#Spotify API credentials
#These are the credentials that allow us to access the Spotify API
#You can get your own credentials by creating a Spotify Developer account
#https://developer.spotify.com/dashboard/login
#be sure to make the redirect uri the same as below


client_id = "YOURIDHERE"
client_secret = "YOURSECRETHERE"
scope = "playlist-modify-public user-library-read"
token = util.prompt_for_user_token(
    None, scope, client_id, client_secret, redirect_uri="https://localhost:8080"
)
spotify = sp.Spotify(auth=token)
user = spotify.me()["id"]

# user input
artist = input("Enter the name of the artist you like a playlist of: ")
playlistName ="Liked Songs by " + artist
description = "Liked songs by " + artist + " from your library"
print("Creating playlist...")

# get the artist uri
result = spotify.search(q=artist, type="artist")
#error handling
if len(result["artists"]["items"]) == 0:
    print("No artist found!")
    exit()

# create a playlist
playlist = spotify.user_playlist_create(
    user, playlistName, public=True, collaborative=False, description=description
)


artist_uri = result["artists"]["items"][0]["uri"]

# get user's liked songs
songs = []
results = spotify.current_user_saved_tracks()
while results:
    songs.extend(results["items"])
    results = spotify.next(results)

# add the songs from the artist to the playlist
likedSongs = [song["track"]["uri"] for song in songs if artist_uri in song["track"]["artists"][0]["uri"]]
spotify.user_playlist_add_tracks(user, playlist["id"], likedSongs)
print("Playlist created!")

# add top 10 songs from that artist to the playlist
addSongs = input("Would you like to add more songs from that artist? (y/n): ")
if addSongs == "y":
    print("Adding songs...")
    topSongs = [song["uri"] for song in spotify.artist_top_tracks(artist_uri)["tracks"] if song["uri"] not in likedSongs]
    spotify.user_playlist_add_tracks(user, playlist["id"], topSongs)
    print("Songs added!")
else: 
    print("goodbye!")
