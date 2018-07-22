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
        # writer.writeheader()
        result = re.findall(r'({"responseContext"[^;]+)', page_html)[0]
        videos = json.loads(result)
        b = videos['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]
        c = b['tabRenderer']['content']['sectionListRenderer'][
            'contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items']
        for item in c:
            d = {
                'title': item['gridVideoRenderer']['title']['simpleText'],
                'data_source': 'youtube',
                'url': 'https://www.youtube.com/watch?v=' + item['gridVideoRenderer']['videoId'],
                'response_url': 'https://www.youtube.com/watch?v=' + item['gridVideoRenderer']['videoId'],
                'desc': None,
                'tag': None,
                'channel': None
            }
            writer.writerow(d)

if __name__ == '__main__':
    crawl()
