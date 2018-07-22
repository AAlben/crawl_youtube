import os
import pandas as pd
import re
from optparse import OptionParser

from you_get.extractors import youtube


def test_youtube():
    youtube.download(
        'http://www.youtube.com/watch?v=CboJMlgfyMA',
        output_dir='/data/videos',
        merge=True
    )


def parse():
    frame = pd.read_csv('data/crawled.csv')
    frame = frame.drop_duplicates('url')
    frame.to_csv('data/crawled_d.csv', index=None, encoding='utf-8')


def download(frame, index=0):
    start_flag = False
    for i, item in enumerate(frame.values):
        url = item[2]
        print(i)
        print(url)
        if index == i:
            start_flag = True
            continue
        if not start_flag:
            continue
        result = youtube.download(
            url,
            output_dir='/data/videos',
            merge=False
        )


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--index", dest="index",
                      help="skip index")
    (options, args) = parser.parse_args()
    index = int(options.index)
    frame = pd.read_csv('data/crawled_d.csv')
    download(frame, index)