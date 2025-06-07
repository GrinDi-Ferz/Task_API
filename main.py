
import pprint
import requests
import json
from tqdm import tqdm
from time import sleep

breed = input('Введите породу собаки:')
token = input('Введите token Полигона Яндекс.Диска:')

progress_bar =[]
files = []
url_all_breed = 'https://dog.ceo/api/breeds/list/all'

# Функция с задержкой исполнения
def fun(x):
    sleep(0.5)
    return x

# Создание папки на яндекс диске
url = 'https://cloud-api.yandex.net/v1/disk/resources'
params = {'path':[breed]}
headers = {'Authorization':token}
response = requests.put(url, params=params, headers=headers)

# Подсчитываем кол-во подпород
response = requests.get(url_all_breed)
number_sub_breed = (len(response.json()['message'][breed]))

# Скачиваем по 1-му фото рандомному если есть подпорода и все фото если только порода
if number_sub_breed > 0:
    response = requests.get(f'https://dog.ceo/api/breed/{breed}/list')
    dog = (response.json()['message'])
    for i in dog:
        response = requests.get(f'https://dog.ceo/api/breed/{breed}/{i}/images/random')
        image_url = response.json()['message']
        name = (f'{breed}_{i}_{image_url.split('/')[-1]}')
        to_json = {'file_name': name}
        files.append(to_json)
        progress_bar.append(name)
        response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                 params={'url': f'{image_url}', 'path': f'{breed}/{name}'},
                                 headers=headers)

# Скачиваем все фото если нет подпород
else:
    response = requests.get(f'https://dog.ceo/api/breed/{breed}/images')
    image_url = response.json()['message']
    for i in image_url:
        name = (f'{breed}_{i.split('/')[-1]}')
        to_json = {'file_name': name}
        files.append(to_json)
        progress_bar.append(name)
        response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                params={'url': f'{i}', 'path': f'{breed}/{name}'},
                                headers=headers)

# Запись в json
dict_bread = {breed: files}
with open('breed.json', 'w') as f:
    json.dump(dict_bread, f)

# Цикл с прогресс-бара
for i in tqdm(range(len(progress_bar))):
    fun(i)

