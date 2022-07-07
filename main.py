import requests
from pprint import pprint
import logging
from logging import StreamHandler




URL = 'https://api.vk.com/method/photos.get'
TOKEN = 'vk'
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
#     fh = logging.FileHandler(filename='logs')
#     fh.setFormatter(logging.Formatter(FORMAT))
#     fh.setLevel(logging.INFO)
#     logger.addHandler(fh)
#
# logging.basicConfig(filename='logs', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
# init_logger('test')
# logger = logging.getLogger('test.main')
# logger.info('info')
# logging.debug('This is a debug message')

if __name__ == '__main__':
    token = 'yd'
    uploader = YaUploader(token)
    for el in item:
        photo = {}
        file_name = el['likes']['count']
        for picture in el.get('sizes'):
            if picture.get('type') == 'z':
                photo_url = picture.get('url')
                photo[file_name] = photo_url
                # print(photo_url)
        for key, value in photo.items():
            file_path = f"photo/{key}"
            result = uploader.upload_file_to_disk(file_path, value)

