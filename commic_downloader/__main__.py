#!/usr/bin/env python3
 
import sys

from .manga_cross import download as mc_dl
from .jamp_plus import download as j_dl
from .kurage_bunch import download as kb_dl

def download(url:str, root_dir:str):
    if 'mangacross.jp' in url:
        mc_dl(url, root_dir)
    elif 'shonenjumpplus.com' in url:
        j_dl(url, root_dir)
    elif 'kuragebunch.com' in url:
        kb_dl(url, root_dir)
    else:
        print('サポート外のサイトです。')

if __name__ == '__main__':
    args = sys.argv

    root_dir = ''
    if len(args) >= 2:
        root_dir = args[1]
    else:
        root_dir = input('保存先のルートフォルダを指定してください。 : ')

    urls = []
    for arg in args[2:]:
        urls.append(arg)

    if len(urls) == 0:
        print('URLを追加してください。（空でDL開始）')
        while True:
            url = input("URL : ")
            if not url:
                break
            urls.append(url)

    for url in urls:
        download(url, 'D:')
