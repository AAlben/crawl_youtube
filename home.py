import re
import json
import pandas as pd


def parse():
    with open('html/channel.html', 'rb') as fp:
        page_html = fp.read().decode('utf-8')
    result = re.findall(r'({"responseContext"[^;]+)', page_html)[0]
    channel = json.loads(result)
    return channel


def parse_json(channel, l):
    for content in channel['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents']:
        item = content['itemSectionRenderer']['contents'][0]
        for a in item['shelfRenderer']['content']['horizontalListRenderer']['items']:
            d = {
                'channel': a['gridChannelRenderer']['title']['simpleText'],
                'url': 'https://www.youtube.com/channel/' + a[
                    'gridChannelRenderer']['channelId']
            }
            l.append(d)
    return l


if __name__ == '__main__':
    l = []
    channel = parse()
    l = parse_json(channel, l)
    frame = pd.DataFrame(l)
    frame.to_csv('data/channel.csv', index=None, encoding='utf-8')
