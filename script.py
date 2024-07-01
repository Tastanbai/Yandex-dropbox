import dropbox
import os

# Функция для загрузки файла из Dropbox
def download_file_from_dropbox(dbx, file_path, local_path):
    try:
        metadata, res = dbx.files_download(file_path)
        with open(local_path, 'wb') as f:
            f.write(res.content)
        print(f"File {file_path} downloaded successfully to {local_path}.")
    except dropbox.exceptions.ApiError as err:
        print(f"Failed to download file: {err}")

# Авторизация в Dropbox
dropbox_token = os.getenv('DROPBOX_TOKEN')  # Получение токена из переменной окружения
dbx = dropbox.Dropbox(dropbox_token)

dropbox_file_path = '/Result.tif'
local_file_path = 'Result_downloaded.tif'

# Загрузка файла
download_file_from_dropbox(dbx, dropbox_file_path, local_file_path)
