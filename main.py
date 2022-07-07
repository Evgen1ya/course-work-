import requests
import json
from pprint import pprint
import os
import logging
from datetime import date
import yadisk


URL = 'https://api.vk.com/method/photos.get'
TOKEN = 'da2b2fd9779dae3e30be1602af544051c4a2a8f18fc6f2bcdc647fbff64df5e246d50630bfe0aaf49a966'
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
        params = {"path": disk_file_path, "overwrite": "true", "url": photo_url}
        response = requests.get(upload_url, headers=headers, params=params)
        pprint(response.json())
        return response.json()

    def upload_file_to_disk(self, disk_file_path, url):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, url)
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

# def init_logger(name):
#     logger = logging.getLogger(name)
#     FORMAT = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s -  %(message)s'
#     logger.setLevel(logging.INFO)
#     fh = logging.FileHandler(filename='course-work/logs')
#     fh.setFormatter(logging.Formatter(FORMAT))
#     fh.setLevel(logging.INFO)
#     logger.addHandler(fh)
#
# init_logger('test')
# logger = logging.getLogger('test.main')

if __name__ == '__main__':
    token = 'AQAAAAA1v4gCAADLW7iaegIcy0RSgeQjHhDImZg'
    uploader = YaUploader(token)
    for el in item:
        photo = {}
        file_name = el['likes']['count']
        for picture in el.get('sizes'):
            if picture.get('type') == 'z':
                photo_url = picture.get('url')
                photo[file_name] = photo_url
        for key, value in photo.items():
            file_path = f"photo/{key}"
            result = uploader.upload_file_to_disk(file_path, value)


