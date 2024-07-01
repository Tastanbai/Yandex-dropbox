import os
import requests
from PIL import Image
from io import BytesIO
import dropbox

# Функция для получения списка изображений из публичной папки на Yandex Disk
def get_image_urls_from_public_yandex_disk(public_url):
    image_urls = []
    headers = {"Authorization": f"OAuth {yandex_token}"}
    
    def fetch_items(url):
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        try:
            items = response.json()['_embedded']['items']
        except (KeyError, requests.exceptions.JSONDecodeError) as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response content: {response.content}")
            return
        
        for item in items:
            if item['type'] == 'file' and item['media_type'] == 'image':
                image_urls.append(item['file'])
            elif item['type'] == 'dir':
                fetch_items(f"https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_url}&path={item['path']}")

    fetch_items(f"https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_url}")
    return image_urls

# Функция для загрузки изображений из списка URL
def download_images(image_urls, token):
    headers = {"Authorization": f"OAuth {token}"}
    images = []
    for image_url in image_urls:
        response = requests.get(image_url, headers=headers)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            images.append(img)
    return images

# Функция для сохранения изображений в Dropbox
def save_images_to_dropbox(images, output_file, dbx):
    with BytesIO() as output:
        images[0].save(output, save_all=True, append_images=images[1:], format='TIFF', compression="tiff_deflate")
        output.seek(0)
        dbx.files_upload(output.read(), f'/{output_file}', mode=dropbox.files.WriteMode('overwrite'))
    print(f"TIFF file saved to Dropbox as: /{output_file}")

# Пример использования
public_yandex_disk_url = 'https://disk.yandex.ru/d/V47MEP5hZ3U1kg'
yandex_token = os.getenv('YANDEX_TOKEN')  # Получение токена из переменной окружения

image_urls = get_image_urls_from_public_yandex_disk(public_yandex_disk_url)
print(f"Found {len(image_urls)} image URLs")
images = download_images(image_urls, yandex_token)

# Авторизация в Dropbox
dropbox_token = os.getenv('DROPBOX_TOKEN')  # Получение токена из переменной окружения
dbx = dropbox.Dropbox(dropbox_token)

output_file = 'Result3.tif'
save_images_to_dropbox(images, output_file, dbx)
