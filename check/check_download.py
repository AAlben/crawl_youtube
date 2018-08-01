import os
import time


def check(old_index):
    with open('./download_index.txt', 'r') as fp:
        data = fp.readlines()
    index = int(data[-2])

    if old_index != index:
        old_index = index
    else:
        command = 'ps -ef|grep format|grep -v grep|cut -c 9-15|xargs kill -9'
        os.popen(command)
        command = 'cd /home/code/crawl_youtube ; python3 format.py -i -1 &'
        os.popen(command)
    return old_index


if __name_ == '__main__':
    old_index = 0
    while True:
        old_index = check()
        time.sleep(60)
