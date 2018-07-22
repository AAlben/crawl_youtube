import os
import pandas as pd
import re

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


def download(frame):
    for index in range(28, 5000):
        item = frame.iloc[index]
        url = item[2]
        print(url)
        _id = re.findall(r'watch[?]v=(.+)', url)[0]
        youtube.download(
            url,
            output_dir='/data/videos',
            merge=False
        )

if __name__ == '__main__':
    frame = pd.read_csv('data/crawled_d.csv')
    download(frame)
