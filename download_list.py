import requests
import json
import os
import time
import pandas
import sys

import datetime
import dateutil.parser as parser

from bs4 import BeautifulSoup

def downloadfile(name,url):
    name=name+".mp4"
    r=requests.get(url)

    script_dir_x = os.path.dirname(__file__)
    file_path_x = os.path.join(script_dir_x, name)

    f=open(file_path_x,'wb')
    for chunk in r.iter_content(chunk_size=255):
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()


script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'blacklist_id.txt')
blacklisted = open(file_path, 'r')
BLACKLISTED_IDS = blacklisted.read().split(";")
BLACKLISTED_IDS = BLACKLISTED_IDS[:-1]

authURL = 'https://id.twitch.tv/oauth2/token' #u have to login here to get client id and secret
Client_ID = '***'
Secret  = '***'

AutParams = {'client_id': Client_ID,
'Accept': 'application/vnd.twitchtv.v5+json',
'client_secret': Secret,
'grant_type': 'client_credentials'
}

#getting authorization token
AutCall = requests.post(url=authURL, params=AutParams)
access_token = AutCall.json()['access_token']

head = {
'Client-ID' : Client_ID,
'Authorization' :  "Bearer " + access_token,
'Accept': 'application/vnd.twitchtv.v5+json'
}

STREAMERS = ['ArQueL', 'Nervarien', 'rybsonlol_', 'kubon_', 'overpow', 'randombrucetv', 'vysotzky', 'mamm0n', 'Cinkrofwest']
array_of_clips = []

for streamer in STREAMERS:
    URL = "https://api.twitch.tv/kraken/clips/top?channel=" + streamer + "&limit=10&period=week"
    r = requests.get(URL, headers = head).json()

    try:
        for i in range(len(r["clips"])):
            try:
                if r["clips"][i] is not None:
                    clipURL = ""
                    if r["clips"][i]['vod'] is None:
                        clipURL = "VOD został usunięty :("
                    else:
                        clipURL = r["clips"][i]['vod']['url']

                    if r["clips"][i]['tracking_id'] not in BLACKLISTED_IDS:
                        new_clip = {
                        'ID': r["clips"][i]['tracking_id'],
                        'URL': r["clips"][i]['url'],
                        'TITLE': r["clips"][i]['title'],
                        'GAME': r["clips"][i]['game'],
                        'VIEWS': r["clips"][i]['views'],
                        'BROADCASTER_NAME': r["clips"][i]['broadcaster']['display_name'],
                        'BROADCASTER_URL': r["clips"][i]['broadcaster']['channel_url'],
                        'CLIP_CREATOR': r["clips"][i]['curator']['display_name'],
                        'VOD_URL': clipURL,
                        'DOWNLOAD_URL': r["clips"][i]['thumbnails']['medium'].split("-preview-480x272.jpg")[0] + ".mp4",
                        }
                        array_of_clips.append(new_clip)
            except IndexError:
                print("Index error.")
    except IndexError:
        print("No Clips!")



################################## SELECT TOP 6 CLIPS
array_of_clips.sort(key = lambda json: json['VIEWS'])
array_of_clips = array_of_clips[::-1]
array_of_clips = array_of_clips[:6]

################################## DOWNLOAD SELECTED CLIPS PART
script_dir2 = os.path.dirname(__file__)
file_path2 = os.path.join(script_dir2, 'downloaded.csv')
downloaded_file = open(file_path2, 'a', encoding='utf-8')

script_dir3 = os.path.dirname(__file__)
file_path3 = os.path.join(script_dir3, 'blacklist_id.txt')
blacklisted = open(file_path3, 'a', encoding='utf-8')
for item in array_of_clips:
    print("Downloading ID:" + item["ID"] + "...")
    downloadfile("clips\\" + item["BROADCASTER_NAME"] + "_" + item["ID"], item["DOWNLOAD_URL"])
    downloaded_file.write(item["ID"] + ";" + item["URL"] + ";" + item["TITLE"] + ";" + item["GAME"] + ";" + str(item["VIEWS"]) + ";" + item["BROADCASTER_NAME"] + ";" + item["BROADCASTER_URL"] + ";" + item["CLIP_CREATOR"] + ";" + item["VOD_URL"] + ";" + item["DOWNLOAD_URL"] + "\n")
    blacklisted.write(item["ID"] + ";")
    time.sleep(3)
    print("Done!")



DATE_TIME = datetime.datetime.now() + datetime.timedelta(days=1)
DATE_TIME = DATE_TIME.replace(hour=8, minute=0, second=0)

##od 8 do 24 jest 960 min
inc_ratio = 960/len(array_of_clips)
ADD_MINUTES_DATE = datetime.timedelta(minutes=inc_ratio)

for item in array_of_clips:
    publishAt = DATE_TIME.isoformat()
    item["VIDEO"] = {
        'TITLE': item['TITLE'] + " | " + item['BROADCASTER_NAME'],
        'DESCRIPTION': "Streamer: " + item["BROADCASTER_URL"] + " NEWLINE " + "Twórca shota: " + item['CLIP_CREATOR'] + " NEWLINE " + "VOD: " + item["VOD_URL"] + " NEWLINE " + "Jeżeli masz do mnie jakąś sprawę pisz na email: intergalaktyczne.shoty@gmail.com" + " NEWLINE " + "#twitch #clip #lol #" + item['BROADCASTER_NAME'],
        'TAGS': "twitch, clip, lol, " + item['BROADCASTER_NAME'],
        'PUBLISH_TIME': publishAt,
        'DESTINATION': "clips\\" + item["BROADCASTER_NAME"] + "_" + item["ID"] + ".mp4"
    }
    DATE_TIME = DATE_TIME + ADD_MINUTES_DATE

script_dir4 = os.path.dirname(__file__)
file_path4 = os.path.join(script_dir4, 'temp_download_list.json')
with open(file_path4, 'w', encoding='utf-8') as f:
    json.dump(array_of_clips, f, ensure_ascii=False, indent=4)



#INTERGALACTIC SHOTS PART
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'blacklist_id_world.txt')
blacklisted_world = open(file_path, 'r')
BLACKLISTED_WORLD_IDS = blacklisted_world.read().split(";")
BLACKLISTED_WORLD_IDS = BLACKLISTED_WORLD_IDS[:-1]

array_of_clips = []
URL = "https://api.twitch.tv/kraken/clips/top?limit=100"
r = requests.get(URL, headers = head).json()

try:
    for i in range(len(r["clips"])):
        try:
            if r["clips"][i] is not None:
                clipURL = ""
                if r["clips"][i]['vod'] is None:
                    clipURL = "VOD został usunięty :("
                else:
                    clipURL = r["clips"][i]['vod']['url']

                if r["clips"][i]['tracking_id'] not in BLACKLISTED_WORLD_IDS:
                    new_clip = {
                    'ID': r["clips"][i]['tracking_id'],
                    'URL': r["clips"][i]['url'],
                    'TITLE': r["clips"][i]['title'],
                    'GAME': r["clips"][i]['game'],
                    'VIEWS': r["clips"][i]['views'],
                    'BROADCASTER_NAME': r["clips"][i]['broadcaster']['display_name'],
                    'BROADCASTER_URL': r["clips"][i]['broadcaster']['channel_url'],
                    'CLIP_CREATOR': r["clips"][i]['curator']['display_name'],
                    'VOD_URL': clipURL,
                    'DOWNLOAD_URL': r["clips"][i]['thumbnails']['medium'].split("-preview-480x272.jpg")[0] + ".mp4",
                    }
                    array_of_clips.append(new_clip)
        except IndexError:
            print("Index error.")
except IndexError:
    print("No Clips!")



################################## SELECT TOP 6 CLIPS
array_of_clips.sort(key = lambda json: json['VIEWS'], reverse=True)
array_of_clips = array_of_clips[:6]

################################## DOWNLOAD SELECTED CLIPS PART
script_dir2 = os.path.dirname(__file__)
file_path2 = os.path.join(script_dir2, 'downloaded_world.csv')
downloaded_file = open(file_path2, 'a', encoding='utf-8')

script_dir3 = os.path.dirname(__file__)
file_path3 = os.path.join(script_dir3, 'blacklist_id_world.txt')
blacklisted = open(file_path3, 'a', encoding='utf-8')
for item in array_of_clips:
    print("Downloading ID:" + item["ID"] + "...")
    downloadfile("clips_top_world\\" +item["BROADCASTER_NAME"] + "_" + item["ID"], item["DOWNLOAD_URL"])
    downloaded_file.write(item["ID"] + ";" + item["URL"] + ";" + item["TITLE"] + ";" + item["GAME"] + ";" + str(item["VIEWS"]) + ";" + item["BROADCASTER_NAME"] + ";" + item["BROADCASTER_URL"] + ";" + item["CLIP_CREATOR"] + ";" + item["VOD_URL"] + ";" + item["DOWNLOAD_URL"] + "\n")
    blacklisted.write(item["ID"] + ";")
    time.sleep(1)
    print("Done!")



DATE_TIME = datetime.datetime.now() + datetime.timedelta(days=1)
DATE_TIME = DATE_TIME.replace(hour=8, minute=0, second=0)

inc_ratio = 960/len(array_of_clips)
ADD_MINUTES_DATE = datetime.timedelta(minutes=inc_ratio)

for item in array_of_clips:
    publishAt = DATE_TIME.isoformat()
    item["VIDEO"] = {
        'TITLE': item['TITLE'] + " | " + item['BROADCASTER_NAME'],
        'DESCRIPTION': "Streamer: " + item["BROADCASTER_URL"] + " NEWLINE " + "Clip creator: " + item['CLIP_CREATOR'] + " NEWLINE " + "VOD: " + item["VOD_URL"] + " NEWLINE " + "If you have any business with me, write to me by e-mail: intergalactic.clips@gmail.com" + " NEWLINE " + "#twitch #clip #" + item['BROADCASTER_NAME'],
        'TAGS': "twitch, clip, " + item['BROADCASTER_NAME'],
        'PUBLISH_TIME': publishAt,
        'DESTINATION': "clips_top_world\\" + item["BROADCASTER_NAME"] + "_" + item["ID"] + ".mp4"
    }
    DATE_TIME = DATE_TIME + ADD_MINUTES_DATE

script_dir4 = os.path.dirname(__file__)
file_path4 = os.path.join(script_dir4, 'temp_download_list_world.json')
with open(file_path4, 'w', encoding='utf-8') as f:
    json.dump(array_of_clips, f, ensure_ascii=False, indent=4)
