import re
import json
import requests
import time
import pandas as pd
import csv
import os


def crawl():
    frame = pd.read_csv('data/search.csv')
    for item in frame.values:
        channel = item[0]
        url = item[1]
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        print(url)

        r = requests.get(url, headers=headers)
        print(r.headers)
        time.sleep(1)
        with open('html/search_{0}.html'.format(channel), 'w') as fp:
            fp.write(r.text)
        if 'responseContext' in r.text:
            print('responseContext in response!!!')
            parse(r.text, channel)


def parse(page_html, channel):
    fields = ['title', 'data_source', 'url',
              'response_url', 'desc', 'tag', 'channel']
    with open('data/crawled.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        result = re.findall(r'({"responseContext"[^;]+)', page_html)[0]
        videos = json.loads(result)
        contents = videos['contents']
        if contents.get('twoColumnBrowseResultsRenderer'):
            tabs = contents['twoColumnBrowseResultsRenderer']['tabs']
            parse_common(tabs, channel, writer)
        elif contents.get('twoColumnSearchResultsRenderer'):
            tabs = contents.get('twoColumnSearchResultsRenderer')[
                'primaryContents']
            parse_search(tabs, channel, writer)


def parse_common(content, channel, writer):
    for item in content:
        if not item:
            continue
        if not item.get('tabRenderer'):
            continue

        data = item['tabRenderer']
        if not data.get('content'):
            continue
        contents = data['content']['sectionListRenderer']['contents']
        for a in contents:
            items = None
            key = None
            if not a:
                continue
            if a.get('itemSectionRenderer'):
                for b in a['itemSectionRenderer']['contents']:
                    if b.get('shelfRenderer'):
                        c = b['shelfRenderer']['content']
                        if c.get('horizontalMovieListRenderer'):
                            items = c['horizontalMovieListRenderer']['items']
                            key = 'gridMovieRenderer'
                    elif b.get('gridRenderer'):
                        items = b['gridRenderer']['items']
                        key = 'gridVideoRenderer'
            else:
                print('else continue')
            if items:
                for one in items:
                    d = {
                        'title': one[key]['title']['simpleText'],
                        'data_source': 'youtube',
                        'url': 'https://www.youtube.com/watch?v=' + one[key]['videoId'],
                        'response_url': 'https://www.youtube.com/watch?v=' + one[key]['videoId'],
                        'desc': None,
                        'tag': None,
                        'channel': channel
                    }
                    # print(d)
                    writer.writerow(d)


def parse_search(data, channel, writer):
    contents = data['sectionListRenderer']['contents']
    for a in contents:
        items = []
        key = None
        if not a:
            continue
        if a.get('itemSectionRenderer'):
            for b in a['itemSectionRenderer']['contents']:
                if b.get('shelfRenderer'):
                    c = b['shelfRenderer']['content']
                    if c.get('horizontalMovieListRenderer'):
                        items = c['horizontalMovieListRenderer']['items']
                        key = 'gridMovieRenderer'
                elif b.get('gridRenderer'):
                    items = b['gridRenderer']['items']
                    key = 'gridVideoRenderer'
                elif b.get('videoRenderer'):
                    items.append(b)
                    key = 'videoRenderer'

        else:
            print('else continue')
        if items:
            for one in items:
                d = {
                    'title': one[key]['title']['simpleText'],
                    'data_source': 'youtube',
                    'url': 'https://www.youtube.com/watch?v=' + one[key]['videoId'],
                    'response_url': 'https://www.youtube.com/watch?v=' + one[key]['videoId'],
                    'desc': None,
                    'tag': None,
                    'channel': channel
                }
                # print(d)
                writer.writerow(d)


if __name__ == '__main__':
    crawl()