# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 13:59:19 2017

@author: 凌丰
"""
import sys
import os

from urllib.parse import unquote, quote
import urllib.request


import json
# import requests


def caesar(location):
    num = int(location[0])
    avg_len = len(location[1:]) // num
    remainder = len(location[1:]) % num

    result = []
    for i in range(remainder):
        line = location[i * (avg_len + 1) + 1: (i + 1) * (avg_len + 1) + 1]
        result.append(line)

    for i in range(num - remainder):
        line = location[(avg_len + 1) * remainder:][i *
                                                    avg_len + 1: (i + 1) * avg_len + 1]
        result.append(line)

    s = []
    for i in range(avg_len):
        for j in range(num):
            s.append(result[j][i])

    for i in range(remainder):
        s.append(result[i][-1])

    return unquote(''.join(s)).replace('^', '0')


def get_url(id):

    target_url = 'http://www.xiami.com/song/playlist/id/' + \
        str(id) + '/object_name/default/object_id/0/cat/json'
    # print(target_url)
    request = urllib.request.Request(target_url)
    request.add_header('content-type', 'application/json')
    request.add_header(
        'User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0')

    response = urllib.request.urlopen(request).read().decode('utf8')
    json_content = json.loads(response)
    # print(json_content)
    # print(json_content.json()['data']['trackList'][0]['location'])
    name = json_content['data']['trackList'][0]['songName'] + '-' + \
        json_content['data']['trackList'][0]['singers'] + '.mp3'

    encoded_url = json_content['data']['trackList'][0]['location']

    return name, encoded_url


def reporthook(blocknum, blocksize, totalsize, filename):
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\rDownloading " + filename + "%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize:  # near the end
            sys.stderr.write("\n")
    else:  # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))


def download(url, name):
    # TODO: name the file by checking the url's extension
    # Such as : 'http://om5.alicdn.com/158/7158/1136455538/1774490672_1478671781016.mp3?auth_key=3ec3aafaee5fa46d100887c99b2f3e31-1505790000-0-null', should be added '.mp3' extension

    # with open('mp3/' + name, 'wb') as f:
    #     f.write(urllib.request.urlopen(url).read())

    extension = url.split('?')[0].split('.')[-1]
    urllib.request.urlretrieve(
        url, 'mp3/' + name + '.' + extension, lambda x, y, z: reporthook(x, y, z, name))
    print(name + " successful")


def search(name, num=10):
    """ Search song by name

    Args:
        name (str): Name of song 
        num (int): Default to 10, how many songs shown

    Retrun：
        A list of songs in the format:
        Song name, Artist name, Album name, Download address,

    """
    url = 'http://api.xiami.com/web?v=2.0&app_key=1&key={}&page=1&limit={}&r=search/songs'.format(
        quote(name), num)
    request = urllib.request.Request(url)
    request.add_header('content-type', 'application/json, text/plain, */*')
    request.add_header(
        'User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0')
    request.add_header('Referer', 'http://m.xiami.com/')
    response = urllib.request.urlopen(request).read().decode('utf8')
    json_content = json.loads(response)
    # print(json_content)
    # print(response.read())

    res = []
    for i in range(num):
        try:
            song = []
            song.append(json_content['data']['songs'][i].get('song_name'))
            song.append(json_content['data']['songs'][i].get('artist_name'))
            song.append(json_content['data']['songs'][i].get('album_name'))
            song.append(json_content['data']['songs'][i].get('listen_file'))
            res.append(song)
        except Exception as e:
            print(e)
            break

    return res


def download_by_id(song_id):
    # TODO: fix encode error below
    name, encoded_url = get_url(song_id)
    download(caesar(encoded_url), name)
    print(name.encode('utf-8').decode('utf-8') + " successful")


def download_by_name(name_list):
    for i in name_list:
        download(*search(i))


def colored(string):
    # return '\x1b[1;32;40m{}\x1b[0m'.format(string)
    import os
    if os.name == 'nt':
        return string
    return '\033[92m{}\033[0m'.format(string)


if __name__ == '__main__':

    if not os.path.exists('mp3'):
        os.makedirs('mp3')

    song = input("Please input the song name:\n")
    while 1:
        if not song:
            song = input("Please input the song name:\n")
            continue
        song_list = search(song)

        term_list = ['Song name', 'Artist name', 'Album name']
        row_format = "{:<7}" + "\t{:<18}" * (len(term_list))
        print(row_format.format('Index', *term_list))
        for index, song in enumerate(song_list):
            print(row_format.format(
                colored('[' + str(index + 1) + ']'), *song[:-1]), sep='\t')

        number = input(
            "Please input the index of the song, e.g. 1, q for quit:\n")
        if number.lower() == 'q':
            song = ""
            continue
        while 1:
            try:
                number = int(number) - 1
                download(song_list[number][3], song_list[number]
                         [0] + '-' + song_list[number][1])
            except Exception as e:
                print(e)
                number = input("Please input the index of the song:\n")
                if number.lower() == 'q':
                    break
            else:
                break

        command = input("Enter q to quit, else continue to download:")
        if command.lower() == 'q':
            exit(0)
        else:
            song = command
