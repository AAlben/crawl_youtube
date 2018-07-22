import re
import json
import requests
import time
import pandas as pd
import csv


def crawl():
    frame = pd.read_csv('data/channel.csv')
    for item in frame.values:
        channel = item[0]
        url = item[1] + '/videos'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        channel_id = re.findall(r'channel/([^/]+)', url)[0]
        print(url)
        r = requests.get(url, headers=headers)
        print(r.headers)
        time.sleep(1)
        with open('html/channel_{0}.html'.format(channel_id), 'w') as fp:
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
        tabs = videos['contents']['twoColumnBrowseResultsRenderer']['tabs']
        parse_common(tabs, channel, writer)


def parse_common(content, channel, writer):
    for item in content:
        if not item:
            print('not item')
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
            print('index')
            if not a:
                continue
            print(a.keys())
            if a.get('itemSectionRenderer'):
                for b in a['itemSectionRenderer']['contents']:
                    if b.get('shelfRenderer'):
                        items = b['shelfRenderer']['content'][
                            'horizontalMovieListRenderer']['items']
                        key = 'gridMovieRenderer'
                    elif b.get('gridRenderer'):
                        items = b['gridRenderer']['items']
                        key = 'gridVideoRenderer'
            elif a.get(''):
                print('gridRenderer')
            elif a.get('sectionListRenderer'):
                print('sectionListRenderer')
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
                    print(d)
                    writer.writerow(d)


if __name__ == '__main__':
    crawl()
