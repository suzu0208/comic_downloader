#!/usr/bin/env python3
 
import json
import os
import requests

from PIL import Image
from io import BytesIO

agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100'

def download(url:str, root_dir:str):
    """
    コミプレのコミックをダウンロードします。

    * <root_dir>\作品名\話数 のディレクトリに保存する。
    * ファイル名は 01.jpg からの連番。

    引数:
        url (str) : URL
        root_dir (str) : 保存先のルートディレクトリ
    """

    req = requests.get(f'{url}.json', headers={'User-Agent': agent})
    if req.status_code != 200:
        print(f"{req} にアクセスできません。\r")
        return

    j = json.loads(req.text)

    title = j['readableProduct']['series']['title']
    number = j['readableProduct']['number']
    dir = os.path.join(root_dir, title, str(number).zfill(3))
    os.makedirs(dir, exist_ok=True)

    pages = j["readableProduct"]["pageStructure"]["pages"]
    page_number = 1
    for count, page in enumerate(pages):
        if page['type'] != 'main':
            continue

        image = convert(page)
        file_name = f'{dir}\\{str(page_number).zfill(2)}.jpg'
        image.save(file_name)

        print(f'\r{title} {number} : {str(count)}/{str(len(pages))}', end="")
        page_number += 1
    print("\r")

def convert(page):
    """
    分割配置された画像を元の1枚にします。

    引数:
        page : ページの情報

    戻り値
        Image : 復元した画像
    """
    data = requests.get(page['src'], headers={'User-Agent': agent}).content
    in_image = Image.open(BytesIO(data))
    out_image = Image.open(BytesIO(data))

    # 画像は4分割されている
    width = in_image.width
    height = in_image.height

    crop_width = round(width/4)
    crop_height = round(height/4)

    # 分割画像を抜き出して再配置
    for x in range(4):
        for y in range(4):
            crop = in_image.crop(box=(crop_width*x, crop_height*y, crop_width*(x+1), crop_height*(y+1)))
            out_image.paste(crop, (crop_width*y, crop_height*x))

    return out_image

if __name__ == "__main__":
    print("コミプレのページのURLを追加してください。（空でDL開始）\n")
    urls = []
    while True:
        url = input("URL : ")
        if not url:
            break
        urls.append(url)
    for url in urls:
        download(url, 'D:')
    