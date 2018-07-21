import json
import pandas as pd


def parse():
    with open('html/videos.html', 'rb') as fp:
        page_html = fp.read().decode('utf-8')
    videos = json.loads(page_html)
    return videos


def parse_json(videos, l):
    a = videos[1]
    b = a['response']['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]
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
        l.append(d)
    return l


if __name__ == '__main__':
    l = []
    videos = parse()
    l = parse_json(videos, l)
    frame = pd.DataFrame(l)
    frame.to_csv('data/video.csv', index=None, encoding='utf-8')
