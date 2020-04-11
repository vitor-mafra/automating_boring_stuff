from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import os


def data_to_dict(group, album_dict):
    for item in group:
        if item != None:
            try:
                # defining dict keys -> the albums' names themselves
                key = str(item.find("span").get_text())
                # values -> this may seem complicated, but is only string manipulation
                album_dict[key] = str(item)[
                    str(item).find('href="')
                    + len('href="') : str(item).find("style")
                    - 2
                ]
            except:
                pass


def manage_dir(path, album_dict):
    # defining path
    if album_dict == fandom_albums:
        path = path + "/fandom"
        os.mkdir(path)

    elif album_dict == official_albums:
        path = path + "/official"
        os.mkdir(path)

    for album in album_dict:
        os.mkdir(path + "/" + album)


def get_album_cover(path, url_base, album_group):
    for album in album_group:
        response = urlopen(url_base + album_group[album])
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")

        cover = soup.find("img")
        cover_url = str(cover)[str(cover).find('src="') + len('src="') : -3]

        if album_group == fandom_albums:
            os.chdir(path + "/fandom" + "/" + album)
        elif album_group == official_albums:
            os.chdir(path + "/official" + "/" + album)

        urlretrieve((url_base + cover_url), album + ".jpg")

        get_songs_cover(soup)


def get_songs_cover(album_html):

    try:
        songs = album_html.find("ol").find_all("a")
    except:
        songs = None

    if songs != None:
        for song in songs:
            song_url = str(song)[
                str(song).find('href="')
                + len('href="') : str(song).find("html")
                + len("html")
            ]

            response = urlopen(url_base + song_url)
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")

            cover = soup.find("img")
            cover_url = str(cover)[str(cover).find('src="') + len('src="') : -3]

            song_name = soup.find("div", id="content").find("h1").get_text()

            # file names cannot contain "\"
            if song_name.find("/"):
                song_name = song_name.replace("/", "-")

            if cover != None:
                urlretrieve((url_base + cover_url), song_name + ".jpg")
                print(song_name + " ✅")

            else:
                print(song_name + " 🚫")

# CHANGE THIS TO THE PATH YOU WANT TO SAVE
path = "/home/vitor/Desktop/homestuck_albums_scraper/homestuck_albums"

url_base = "https://hsmusic.github.io/"

response = urlopen(url_base)
html = response.read()

soup = BeautifulSoup(html, "html.parser")

# 'album name' : 'album/album-name/index.html'
fandom_albums = {}
official_albums = {}

# getting the album's name and url
fandom = soup.find_all("div", {"class": "grid-listing"})[0]
official = soup.find_all("div", {"class": "grid-listing"})[1]

data_to_dict(fandom, fandom_albums)
data_to_dict(official, official_albums)


manage_dir(path, fandom_albums)
manage_dir(path, official_albums)

get_album_cover(path, url_base, fandom_albums)
get_album_cover(path, url_base, official_albums)
