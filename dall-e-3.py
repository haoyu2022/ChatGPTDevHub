import requests
import os
from datetime import datetime, timedelta, timezone
from PIL import Image


def download_image(url, folder_path):
    response = requests.get(url)
    file_path = os.path.join(folder_path, os.path.basename(url))
    with open(file_path, "wb") as file:
        file.write(response.content)
    return file_path


if __name__ == "__main__":
    model_name = "dall-e-3"
    image_size = "1024x1024"
    download_folder = r"存放图片的绝对路径"
    os.makedirs(download_folder, exist_ok=True)

    while True:
        prompt = input("请输入prompt（输入exit退出）：")
        if prompt == "exit":
            break

        try:
            num_images = int(input("请输入图片数量（默认为1）：") or "1")
            print("正在生成图片，请耐心等待……")
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers={
                    "Authorization": "Bearer $OPENAI_API_KEY"},
                json={"model": model_name, "size": image_size, "prompt": prompt, "n": num_images},
            )
            response.raise_for_status()
            data = response.json()["data"]

            current_time = datetime.now(timezone.utc) + timedelta(hours=8)
            current_time_str = current_time.strftime("%Y%m%d-%H%M")

            for i, image in enumerate(data):
                image_url = image["url"]
                file_name = current_time_str + f"-{str(i + 1).zfill(3)}.png"
                file_path = download_image(image_url, download_folder)
                new_file_path = os.path.join(download_folder, file_name)
                os.rename(file_path, new_file_path)
                print("图片已下载至：", new_file_path)

        except requests.exceptions.HTTPError as err:
            print("请求错误：", err.response.text)

        except Exception as e:
            print("发生错误：", str(e))