import re
import json
import requests
import time
import pandas as pd
import csv
import os
from urllib.parse import quote


def crawl(index):
    frame = pd.read_csv('data/next.csv')
    item = frame.iloc[index]
    channel = item[0]
    url = item[1]
    while True:
        d = crawl_next(channel, url)
        if not d:
            break
        channel = d['channel']
        url = d['url']


def parse(page_html, channel):
    fields = ['title', 'data_source', 'url',
              'response_url', 'desc', 'tag', 'channel']
    with open('data/crawled.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)

        next_fields = ['channel', 'url']
        with open('data/next.csv', 'a') as next_csvfile:
            next_writer = csv.DictWriter(next_csvfile, fieldnames=next_fields)

            result = json.loads(page_html)
            result = result[1]
            data = result['response']['continuationContents']
            _next_d = parse_next(data, channel, writer, next_writer)

    return _next_d


def parse_next(data, channel, writer, next_writer):
    contents = data['itemSectionContinuation']['contents']
    _next_d = None
    if data['itemSectionContinuation'].get('continuations'):
        _next = data['itemSectionContinuation'][
            'continuations'][0]['nextContinuationData']
        _next_d = extract(channel, _next, next_writer)

    for b in contents:
        items = []
        key = None
        if not b:
            continue
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
                print(d)
                writer.writerow(d)

    return _next_d


def extract(channel, _next, next_writer):
    continuation = _next['continuation']
    clickTrackingParams = _next['clickTrackingParams']
    url = 'https://www.youtube.com/results?search_query={0}&pbj=1&ctoken={1}&continuation={1}&itct={2}'.format(
        quote(channel), quote(continuation), quote(clickTrackingParams))
    d = {'channel': channel, 'url': url}
    next_writer.writerow(d)
    return d


def crawl_next(channel, url):
    _next_d = None
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'referer': 'https://www.youtube.com/results?search_query=' + quote(channel),
        'cookie': 'VISITOR_INFO1_LIVE=7JuVLxpHvVs; PREF=f1=10000000; YSC=Y78BceQVSUI; GPS=1',
        'origin': 'https://www.youtube.com',
        'x-youtube-page-label': 'youtube.ytfe.desktop_20180718_9_RC0',
        'x-youtube-page-cl': '205170210',
        'x-spf-referer': '',
        'x-youtube-utc-offset': '480',
        'x-spf-previous': 'https://www.youtube.com/results?search_query=^%^E7^%^A4^%^BE^%^E4^%^BC^%^9A^%^E6^%^91^%^87',
        'x-client-data': 'CIS2yQEIpLbJAQjEtskBCKmdygEIuZ3KAQjXncoBCKifygEIqKPKARi2mMoB',
        'x-youtube-client-version': '2.20180719',
        'x-youtube-variants-checksum': '24f9a19047d45980ec580660ddb604bb',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'x-youtube-client-name': '1',
        'authority': 'www.youtube.com'

    }
    print(url)
    data = {'session_token': 'QUFFLUhqbVppR1RKeWtmSjl2bk93QzRZcDQwSHpIcmp2d3xBQ3Jtc0tudjFOamtpYWJzNFV3cllxOEdzODRNcmZNQ3d4eVlGVkxSTEtkcGxBTTJzUmlwRlVHakdqWWJlQUp5MmRmOTNsSEk2aXdQRm1SRzRJVzFNMkRRNGVOSDJaZnk1Z2xUbENyd01tZWduR0s2TzVOZ21INm1IVm1VZ2k3NnhWc1E4cWxDMjl4YXR3bkRNdWxqLVBfSjhKaDhxNlVxVkE='}
    r = requests.post(url, headers=headers, data=data)
    print(r.headers)
    time.sleep(1)
    with open('html/next_{0}.html'.format(channel), 'w') as fp:
        fp.write(r.text)
    if 'responseContext' in r.text:
        print('responseContext in response!!!')
        _next_d = parse(r.text, channel)
    return _next_d

if __name__ == '__main__':
    crawl(0)
