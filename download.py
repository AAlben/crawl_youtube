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


def download(frame, index=0):
    with open('download_index.txt', 'a') as fp:
        start_flag = False
        for i, item in enumerate(frame.values):
            fp.write(str(i) + '\n')
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


def get_index():
    with open('download_index.txt', 'r') as fp:
        data = fp.readlines()
    index = int(data[-2])
    return index

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--index", dest="index",
                      help="skip index")
    (options, args) = parser.parse_args()
    index = int(options.index)
    if index == -1:
        index = get_index()

    frame = pd.read_csv('data/crawled_d_2.csv')
    download(frame, index)
