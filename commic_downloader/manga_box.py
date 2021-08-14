#!/usr/bin/env python3
 
import os
import re
import requests
from bs4 import BeautifulSoup

def download(url: str, root_dir:str):
    """
    マンガボックスのコミックをダウンロードします。

    * <root_dir>\作品名\話数 のディレクトリに保存する。
    * ファイル名は 01.jpg からの連番。

    引数:
        url (str) : URL
        root_dir (str) : 保存先のルートディレクトリ
    """

    req = requests.get(f'{url}')
    if req.status_code != 200:
        print(f"{req} にアクセスできません。\r")
        return

    html = BeautifulSoup(req.text, "html.parser")

    page_title = html.find('title').text
    title = re.sub(r'\|.*', '', re.sub(r'.*/', '', page_title)).strip()
    number = re.search(r'第.*話.*', page_title).group()
    dir = os.path.join(root_dir, title, number)
    os.makedirs(dir, exist_ok=True)

    images = [tag.get('src') for tag in html.find_all('img')]
    for count, image in enumerate(images):
        data = requests.get(image).content
        file_name = f'{dir}\\{str(count).zfill(2)}.jpg'
        with open(file_name, "wb") as local_file:
            local_file.write(data)
        print(f'\r{title} {number} : {str(count)}/{str(len(images))}', end="")
    print("\r")

if __name__ == "__main__":
    print("マンガボックスのページのURLを追加してください。（空でDL開始）\n")
    urls = []
    while True:
        url = input("URL : ")
        if not url:
            break
        urls.append(url)
    for url in urls:
        download(url, 'D:')
