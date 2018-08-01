import pandas as pd
import copy


def parse():
    frame = pd.read_csv('data/crawled.csv')
    frame = frame.drop_duplicates('url')
    frame.to_csv('data/crawled_d.csv', index=None, encoding='utf-8')


def duplicate():
    old_frame = pd.read_csv('data/crawled_d.csv')
    new_frame = pd.read_csv('data/crawled_d_1.csv')
    copy_frame = copy.deepcopy(new_frame)
    new_urls = new_frame.loc[:, ['url']]

    for index in old_frame.index:
        url = old_frame.loc[index]['url']
        if url in new_urls.values:
            copy_frame.drop(index, inplace=True)
            # print(url)
    copy_frame.to_csv('data/crawled_d_2.csv', index=None, encoding='utf-8')


if __name__ == '__main__':
    duplicate()
