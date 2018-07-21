import re
import json
import requests
import pandas as pd


def crawl():
    frame = pd.read_csv('data/channel.csv')
    for item in frame.values:
        channel = item[0]
        url = item[1] + '/videos?pbj=1'

        channel_id = re.findall(r'channel/(.+)', url)[0]
        headers = {'referer': item[1]}
        r = requests.get(url, headers=headers)
        print(r.headers)
        with open('html/channel_{0}.html'.format(channel_id), 'w') as fp:
            fp.write(r.text)


if __name__ == '__main__':
    crawl()
