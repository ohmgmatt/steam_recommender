import requests
import json
import sqlite3
import time
import config

## STATIC
API_KEY = confi.API_KEY
BASE_URL = 'http://api.steampowered.com/'


def steamFriends(steamid):
    time.sleep(2)
    ## Establish the URL
    friend_url = ''.join([BASE_URL,
        'ISteamUser/GetFriendList/v0001/?key=',API_KEY,
        '&steamid=',str(steamid),
        '&relationship=friend'])
    ## Setting connection to DB
    conn = sqlite3.connect('steam.db')
    c = conn.cursor()
    ## Pull from using API
    r = requests.get(friend_url)
    if r.status_code != 200:
        return r.status_code
    content = json.loads(r.content)
    if 'friendslist' not in content:
        return 200
    for i in content['friendslist']['friends']:
        sid = int(i['steamid'])
        c.execute('SELECT * FROM parse_id WHERE id = ? UNION SELECT * FROM finished_id WHERE id = ?', (sid,sid))
        rows = c.fetchall()
        if len(rows) == 0:
            insert = "INSERT INTO parse_id VALUES (" + str(sid) + ")"
            c.execute(insert)
        else:
            continue
    conn.commit()
    conn.close()
    return 200

def steamGames(steamid):
    time.sleep(2)
    ## Establish the URL
    game_url = ''.join([BASE_URL,
                      'IPlayerService/GetOwnedGames/v0001/?key=',API_KEY,
                      '&steamid=',str(steamid),
                      '&format=json'])
    ## Setting connection to DB
    conn = sqlite3.connect('steam.db')
    c = conn.cursor()
    ## Pulling from API
    r = requests.get(game_url)
    if r.status_code != 200:
        return r.status_code
    content = json.loads(r.content)
    if content['response'] == {}:
        return 200
    games = content['response']['games']
    for g in games:
        appid = g['appid']
        playtime = g['playtime_forever']
        if playtime == 0:
            continue
        row = [steamid, appid, playtime]
        c.execute("INSERT INTO gameplay (steamID, appID, playtime) VALUES (?,?,?);", row)
    conn.commit()
    conn.close()
    return 200

status = 200

while status == 200:
    time.sleep(2)
    conn = sqlite3.connect('steam.db')
    c = conn.cursor()
    ## Pull ID
    c.execute("SELECT id FROM parse_id LIMIT 1")
    steamID = c.fetchone()[0]
    ## Insert ID
    check = "SELECT * FROM finished_id WHERE id = "+str(steamID)
    c.execute(check)
    rows = c.fetchall()
    if len(rows) == 0:
        insert = 'INSERT INTO finished_id VALUES ('+str(steamID)+')'
        c.execute(insert)
    ## Delete ID
    delete = 'DELETE FROM parse_id WHERE id = '+str(steamID)
    c.execute(delete)
    conn.commit()
    conn.close()
    status = steamFriends(steamID)
    status = steamGames(steamID)
    if status != 200:
        print(status)
