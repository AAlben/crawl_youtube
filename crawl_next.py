import re
import json
import requests
import time
import pandas as pd
import csv
import os
from urllib.parse import quote
from optparse import OptionParser


def crawl(index, session):
    frame = pd.read_csv('data/next_d.csv')
    item = frame.iloc[index]
    channel = item[0]
    url = item[1]
    while True:
        d = crawl_next(channel, url, session)
        if not d:
            break
        channel = d['channel']
        url = d['url']
        time.sleep(1)


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


def crawl_next(channel, url, session):
    _next_d = None
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'referer': 'https://www.youtube.com/results?search_query=' + quote(channel),
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'VISITOR_INFO1_LIVE=CbnOz6SOk-g; PREF=f1=50000000; YSC=96Qx3UVUups; GPS=1',
        'origin': 'https://www.youtube.com',
        'x-spf-referer': '',
        'x-youtube-utc-offset': '480',
        'x-spf-previous': 'https://www.youtube.com/results?search_query=' + quote(channel),
        'x-client-data': 'CIS2yQEIpLbJAQjEtskBCKmdygEIuZ3KAQjXncoBCKifygEIqKPKARi2mMoB',
        'x-youtube-client-version': '2.20180731',
        'x-youtube-variants-checksum': 'de689acd275e940694e023da1daa3ff5',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'x-youtube-client-name': '1',
        'authority': 'www.youtube.com'
    }
    print(url)
    data = {'session_token': 'QUFFLUhqa2JyVEpEOTdJZmN6a2dBSUtjVUJycnhXbnRhUXxBQ3Jtc0tsWnhqZGlidUFFbUpsZFNZTVR6LTVNMEtIQjBHQVpoeUNCcnZvaTNLWnpLVWhSUzNBdVJNMmd0OHdXVnZxTG1kNGk3ZGFLTmNSVHM1a1VjTVdXQ0l2V0FiU0VuWWtFY0xFTVNrUzkzV1Mxc0E2d0ZTOE9fR3UtRlZ1bmRVcklwRnNkNEZRSjZZZXVRM3BVdEQwUDlETm92Q0V2Tnc'}
    r = session.post(url, headers=headers, data=data)
    print(r.headers)
    with open('html/next_{0}.html'.format(channel), 'w') as fp:
        fp.write(r.text)
    if 'responseContext' in r.text:
        print('responseContext in response!!!')
        _next_d = parse(r.text, channel)
    return _next_d


def duplicate():
    frame = pd.read_csv('data/next.csv')
    g_frame = frame.groupby(['channel']).tail(1)
    g_frame.to_csv('data/next_d.csv', index=None, encoding='utf-8')

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--index", dest="index",
                      help="skip index")
    (options, args) = parser.parse_args()
    index = int(options.index)
    s = requests.session()
    duplicate()
    while True:
        for index in range(0, 57):
            print(index)
            crawl(index, s)
            time.sleep(60)
        duplicate()
