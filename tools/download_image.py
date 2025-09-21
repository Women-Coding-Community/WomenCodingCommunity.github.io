import os
import sys
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

IMAGE_FILE_PATH='../assets/images/mentors'

def download_image(url, mentor_name):
    """
    Download the image from the given URL and save it to the specified directory.
    The image will be named based on the mentor's name.
    """
    try:
        image_path = os.path.join(IMAGE_FILE_PATH, f"{mentor_name.lower().replace(' ', '_')}.jpeg")

        os.makedirs(IMAGE_FILE_PATH, exist_ok=True)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(image_path, 'wb') as out_file:
            out_file.write(response.content)

        logging.info(f"Image for {mentor_name} downloaded successfully to {image_path}")
        return image_path

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download image from {url}: {e}")
        return None

def run_automation():
    if len(sys.argv) == 3:
        mentor_name = sys.argv[1]
        url = sys.argv[2]
        image_path = download_image(url, mentor_name)
        if image_path:
            print(f"Image saved to {image_path}")
        else:
            print("Failed to download the image.")

    else:
        logging.info(f"Add parameters for download")


if __name__ == "__main__":
    run_automation()