import os
import sys
import requests
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

IMAGE_FILE_PATH='../assets/images/mentors'
SHEET_NAME = "Mentors Images"

def download_image(url, mentor_name):
    """
    Download the image from the given URL and save it to the specified directory.
    The image will be named based on the mentor's name.
    """
    try:
        image_path = os.path.join(IMAGE_FILE_PATH, f"{mentor_name.lower().replace(' ', '_')}.jpeg")

        os.makedirs(IMAGE_FILE_PATH, exist_ok=True)

        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        with open(image_path, 'wb') as out_file:
            out_file.write(response.content)

        return image_path

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download image for {mentor_name}: {e}")
        return None

def run_automation():
    if len(sys.argv) == 2:
        xlsx_file_path = sys.argv[1]
        success_count = 0

        try:
            df_mentors = pd.read_excel(xlsx_file_path, sheet_name=SHEET_NAME)
            df_mentors.columns = [col.strip() for col in df_mentors.columns]
        except Exception as e:
            logging.error(f"Failed to read Excel file {xlsx_file_path}: {e}")
            return

        for _, row in df_mentors.iterrows():
            mentor_name = str(row["Mentor Name"]).strip()
            url = str(row["Image Download URL"]).strip()

            if pd.isna(mentor_name) or pd.isna(url) or url == "":
                logging.warning(f"Skipping download for row with missing data: {row} \n This needs to be fixed manually")
                continue

            image_path = download_image(url, mentor_name)
            if image_path:
                success_count += 1
        
        logging.info(f"Successfully downloaded {success_count} images.")
        logging.info("Image download process completed.")

    else:
        logging.info(f"Script needs 1 parameter (xlsx_file_path) to run")


if __name__ == "__main__":
    run_automation()