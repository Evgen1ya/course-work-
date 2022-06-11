import requests
from pprint import pprint

URL = 'https://api.vk.com/method/photos.get'
TOKEN = 'token vk'
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


# name = res['response']['items'][0]['likes']['count']
item = res['response']['items']

for el in item:
    # pprint(type(el))
    for picture in el.get('likes'):
        # print(type(picture)) Почему выводится строка, если у ключа likes должен быть словарь?
        # name = picture.get('count')
        pprint(picture)

for el in item:
    for picture in el.get('sizes'):
        if picture.get('type') == 'z':
            photo_url = picture.get('url')
            pprint(photo_url)

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

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.post(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

if __name__ == '__main__':
    path_to_file = f"photo/{name}"
    token = 'token YD'
    uploader = YaUploader(token)
    result = uploader.upload_file_to_disk(path_to_file, photo_url)
