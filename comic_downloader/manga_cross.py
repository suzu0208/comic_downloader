#!/usr/bin/env python3
 
import json
import os
import requests

def download(url: str, root_dir:str):
    """
    マンガクロスのコミックをダウンロードします。

    * <root_dir>\作品名\話数 のディレクトリに保存する。
    * ファイル名は 01.jpg からの連番。

    引数:
        url (str) : URL
        root_dir (str) : 保存先のルートディレクトリ
    """

    req = requests.get(f'{url}/viewer.json')
    if req.status_code != 200:
        print(f"{req} にアクセスできません。\r")
        return

    j = json.loads(req.text)

    title = j['comic']['title']
    number = j['volume']
    dir = os.path.join(root_dir, title, number)
    os.makedirs(dir, exist_ok=True)

    pages = j['episode_pages']
    for count, page in enumerate(pages):
        page = page['image']['pc_url']
        data = requests.get(page).content

        file_name = f'{dir}\\{str(count).zfill(2)}.jpg'
        with open(file_name, "wb") as local_file:
            local_file.write(data)
        print(f'\r{title} {number} : {str(count)}/{str(len(pages))}', end="")
    print("\r")

if __name__ == "__main__":
    print("マンガクロスのページのURLを追加してください。（空でDL開始）\n")
    urls = []
    while True:
        url = input("URL : ")
        if not url:
            break
        urls.append(url)
    for url in urls:
        download(url, 'D:')
