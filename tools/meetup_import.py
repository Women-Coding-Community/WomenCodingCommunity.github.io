import logging
import sys
from datetime import datetime
from enum import Enum
from urllib.request import urlretrieve

import requests
import yaml
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel


class WriteMode(Enum):
    # Create new a file
    WRITE = "w"
    # Append in existent yml file
    APPEND = "a"


class Image(BaseModel):
    path: str = "/assets/images/events/default.jpg"
    alt: str = "Square poster of event"


class WebLink(BaseModel):
    path: str | None
    title: str = "View meetup event"
    target: str = "_target"


class MeetupEvents(BaseModel):
    title: str
    description: str
    category: str | None = "Online Event"
    category_name: str | None = "Online Event"
    date: str
    expiration: str | None = ""
    host: str | None = ""
    speaker: str | None = ""
    time: str | None = ""
    image: Image | None
    link: WebLink | None
    


def download_image(image_url: str) -> str:
    """
    Downloads an image from the given URL and saves it to the '/assets' folder.

    :param image_url: The URL of the image to download.
    :return: The path of the downloaded image.
    """
    image_path = f"/assets/images/events/{image_url.split('/')[-1]}"
    urlretrieve(image_url, f"..{image_path}")
    return image_path


def get_upcoming_meetups(url: str) -> list[MeetupEvents]:
    """
    This function scrapes the given Meetup.com webpage URL to extract upcoming meetup info.

    :param url: The URL of the Meetup.com group page.
    :return: A list of dictionaries with details about the upcoming meetups (name, date, time, etc.).
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    upcoming_meetups: list[MeetupEvents] = []
    host: str = ""
    speaker: str = ""
    date: str = ""
    time: str = ""
    expiration: str = ""

    # Find all upcoming meetup listings
    upcoming_listings = soup.find_all("div", class_="rounded-md bg-white p-4 shadow-sm sm:p-5")
    for listing in upcoming_listings:
        # Find the title and description elements once and reuse them
        title = listing.find("span",
                             class_="ds-font-title-3 block break-words leading-7 utils_cardTitle__sAAHG").text.strip()
        listing.find_all_next("div", class_="flex items-start space-x-1.5")
        # Find all description elements
        description_elements = listing.findAll("p", class_="mb-4")
        # Get the first description element
        description = description_elements[0].text.strip()
        # if len(description_elements) > 1:
        #    description_element = description_elements[1].text.strip()
        for description_div in description_elements:
            if description_div.text.startswith("Host:"):
                host = extract_name(description_div)
            if description_div.text.startswith("Co-Host:"):
                host = f'{host} and {extract_name(description_div)}'
            if description_div.text.startswith("Speaker:"):
                speaker = extract_name(description_div)

        time_element = listing.find("time", class_="text-[#00829B] text-sm font-medium uppercase").text
        if time_element:
            date = ",".join(time_element.split(",")[:3])
            time = time_element.split(",")[-1].strip()
        if date:
            expiration = convert_date(date)

        image_path = listing.find("img").attrs.get("src")
        image_alt = listing.find("img").attrs.get("alt")

        # Download the image from image_path and save it to the '/assets' folder and update the image_path
        image_path = download_image(image_path)

        url = listing.find("a").attrs.get("href")
        upcoming_meetups.append(
            MeetupEvents(title=title, description=description.replace("\n", " "),
                         date=date, host=host, speaker=speaker,
                         time=time, expiration=expiration, image=Image(path=image_path, alt=image_alt),
                         link=WebLink(path=url, title=title)))
    return upcoming_meetups


def export_to_yaml(upcoming_meetups, yaml_file: str, mode: WriteMode):
    """
    Appends data to a YAML file.

    :param mode: Write mode to use.
    :param upcoming_meetups: Upcoming meetups to append to the YAML file.
    :param yaml_file: Path to the YAML file.
    :return: None
    """
    # Convert Pydantic objects to dictionaries
    meetup_dicts = [meetup.dict() for meetup in upcoming_meetups]
    if mode == WriteMode.APPEND:
        logging.info("Appending to existing YML file")
        try:
            with open(yaml_file, "r") as file:
                existing_data = yaml.safe_load(file) or []  # Handle empty file

            if not isinstance(existing_data, list):
                raise ValueError("Existing data is not a list")

            existing_data.extend(meetup_dicts)

            with open(yaml_file, "w") as file:
                yaml.dump(existing_data, file, default_flow_style=False, sort_keys=False), 

        except FileNotFoundError:
            print(f"File '{yaml_file}' not found. Creating a new file.")
            with open(yaml_file, "w") as file:
                yaml.dump(meetup_dicts, file)
    if mode == WriteMode.WRITE:
        logging.info("Overriding YML file")
        with open(yaml_file, "w") as file:
            yaml.dump(meetup_dicts, file)
    logging.info("Data exported to %s", yaml_file)


def extract_name(user_info: Tag) -> str:
    """
    Extracts the name from the user info element.

    :param user_info: The user info element.
    :return: The name of the user.
    """
    u_list = user_info.find_all("strong")
    if len(u_list) > 1:
        user_info = u_list[1].text.strip()
    else:
        user_info = u_list[0].text.strip()
        user_info = user_info.split(":")[1]
    return user_info.strip()


def convert_date(date_str: str) -> str:
    # Parse the date string to a datetime object
    date_obj = datetime.strptime(date_str, "%a, %b %d, %Y")
    # Format the datetime object to the desired string format
    return date_obj.strftime("%Y%m%d")


def fetch_events():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if len(sys.argv) == 4:
        meetup_group_url = sys.argv[1]
        yml_file_path = sys.argv[2]
        mode = WriteMode(sys.argv[3])
    else:
        meetup_group_url = "https://www.meetup.com/women-coding-community/events/?type=upcoming"
        yml_file_path = "../_data/events.yml"
        mode = WriteMode.APPEND

    logging.info("Params: Url: %s yml: %s mode: %s", meetup_group_url, yml_file_path, mode)

    upcoming_meetups = get_upcoming_meetups(meetup_group_url)
    # expired_meetups = get_expired_meetups("https://www.meetup.com/women-coding-community/events/?type=past")

    # Print the extracted information
    logging.info("Upcoming Meetups:")
    for meetup in upcoming_meetups:
        logging.info(f"{meetup.title}")
    export_to_yaml(upcoming_meetups, yml_file_path, mode)


if __name__ == "__main__":
    fetch_events()
