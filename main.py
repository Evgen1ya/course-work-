import requests
import json
from pprint import pprint
import os
import logging
from datetime import date
import yadisk


URL = 'https://api.vk.com/method/photos.get'
TOKEN = 'd'
count = 5
params = {
    'user_ids': '8175842',
    'access_token': TOKEN,
    'v': '5.131',
    'album_id': 'profile',
    'rev': '1',
    'extended': '1',
    'count': count,
    'photo_sizes': '1'
}
res = requests.get(URL, params=params).json()
# pprint(res)

item = res['response']['items']
# pprint(item)

for el in item:
    photo = {}
    file_name = el['likes']['count']
    for picture in el.get('sizes'):
        if picture.get('type') == 'z':
            photo_url = picture.get('url')
            photo[file_name] = photo_url
    # pprint(photo)

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

if __name__ == '__main__':
    token = ''
    uploader = YaUploader(token)
    for key, value in photo.items():
        file_path = f"photo/{key}"
        result = uploader.upload_file_to_disk(file_path, value)

# В чем здесь ошибка может быть? Код беру из предыдущего домашнего задания. Он точно работал, потому что файл с ноутбука загружался на ЯД,
# но если менять на URL фото из VK, то код не работает.

y = yadisk.YaDisk(token='')
y.upload(file_name, photo_url)

# Хотела попробовать через библиотеку, но также не получается по URL