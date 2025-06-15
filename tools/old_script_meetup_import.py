# OLD MEETUP IMPORT SCRIPT: DO NOT USE

import logging
import sys
from datetime import datetime
from enum import Enum
from typing import Optional, Union
from urllib.request import urlretrieve

import requests
import yaml
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel

CODING_CLUB_BANNER = "/assets/images/events/event-coding-club-3.jpg"
WRITING_CLUB_BANNER = "/assets/images/events/event-writing-club.jpeg"


class LiteralString(str):
    pass

class QuotedString(str):
    pass

class NoQuoteString(str):
    pass

def literal_string_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

def double_quote_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')

def no_quote(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='')


yaml.add_representer(LiteralString, literal_string_representer)
yaml.add_representer(QuotedString, double_quote_representer)
yaml.add_representer(NoQuoteString, no_quote)


def to_literal_str(data: str) -> Union[LiteralString, str]:
    special_characters = "!@#$%^&*()-+?_=,<>/:"

    # Pass the string in regex_search
    if data and ("\n" in data or any(c in special_characters for c in data)):
        data = data.rstrip()
        data = f"{data}\n"
        return LiteralString(data)
    return data


def to_quoted_str(data: str) -> Union[QuotedString, NoQuoteString]:
    special_characters = "!@#$%^&*()-+?_=,<>/:"
    if data and ("\n" in data or any(c in special_characters for c in data)):
        return QuotedString(data)
    return NoQuoteString(data)


class WriteMode(Enum):
    # Create new a file
    WRITE = "w"
    # Append in existent yml file
    APPEND = "a"


class Image(BaseModel):
    path: str = "/assets/images/events/default.jpg"
    alt: str = "Square poster of event"


class WebLink(BaseModel):
    path: Optional[str]
    title: str = "View meetup event"
    target: str = "_target"


class MeetupEvents(BaseModel):
    title: str
    description: str
    category_style: Optional[str] = "tech-talk"
    category_name: Optional[str] = "Tech Talk"
    date: str
    expiration: Optional[str] = ""
    host: Optional[str] = ""
    speaker: Optional[str] = ""
    time: Optional[str] = ""
    image: Optional[Image]
    link: Optional[WebLink]


def download_image(image_url: str, description: str, category_style: str, expiration: str) -> str:
    """
    Downloads an image from the given URL and saves it to the '/assets' folder.

    :param image_url: The URL of the image to download.
    :return: The path of the downloaded image.
    """
    image_path = f"/assets/images/events/{category_style}-{expiration}.webp"
    if description:
        if "coding club" in description.lower():
            image_path = CODING_CLUB_BANNER
        elif "writing club" in description.lower():
            image_path = WRITING_CLUB_BANNER
        else:
            try:
                urlretrieve(image_url, f"..{image_path}")
            except Exception as e:
                logging.error(f"Error downloading image from '{image_url}': {e}")
                image_path = "/assets/images/events/default.jpg"
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

    # Find all upcoming meetup listings
    upcoming_listings = soup.find_all("div", class_="rounded-md bg-white p-4 shadow-sm sm:p-5")

    for listing in upcoming_listings:
        # Reset host, speaker, date, etc., for each new listing
        host: str = ""
        speaker: str = ""
        date: str = ""
        time: str = ""
        expiration: str = ""
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
            if description_div.text.lower().startswith("co-host:"):
                host = f'{host} and {extract_name(description_div)}'
            if description_div.text.startswith("Speaker:"):
                speaker = extract_name(description_div)

        time_element = listing.find("time", class_="text-[#00829B] text-sm font-medium uppercase").text
        if time_element:
            date = ",".join(time_element.split(",")[:3]).upper()
            time = time_element.split(",")[-1].strip()
        if date:
            expiration = convert_date(date)

        image_path = listing.find("img").attrs.get("src")
        image_alt = listing.find("img").attrs.get("alt")

        url = listing.find("a").attrs.get("href")

        category_style = "tech-talk"
        category_name = "Tech Talk"
        if description:
            if "coding club" in description.lower():
                category_style = "coding-club"
                category_name = "Coding Club"
            elif "writing club" in description.lower():
                category_style = "writing-club"
                category_name = "Writing Club"
            elif "book club" in title.lower():
                category_style = "book-club"
                category_name = "Book Club"
            elif "career club" in title.lower():
                category_style = "career-club"
                category_name = "Career Club"
            elif "career talk" in description.lower():
                category_style = "career-talk"
                category_name = "Career Talk"

        # No longer needed: image path can refer directly to meetup img url
        # image_path = download_image(image_path, description, category_style, expiration)

        upcoming_meetups.append(
            MeetupEvents(title=title, description=description.replace("\n", " "),
                         category_style=category_style, category_name=category_name,
                         date=date, host=host, speaker=speaker,
                         time=time, expiration=expiration, image=Image(path=image_path, alt=image_alt),
                         link=WebLink(path=url)))
    return upcoming_meetups


def process_meetup_data(meetup: dict) -> dict:
    """
    Process the meetup data to ensure that it is in the correct format for writing to a YAML file.
    :param meetup: The meetup data to process.
    :return: The processed meetup data.
    """
    meetup["title"] = to_literal_str(meetup["title"])
    meetup["description"] = to_literal_str(meetup["description"])
    meetup["expiration"] = QuotedString(meetup["expiration"])
    if "speaker" in meetup:
        meetup["speaker"] = QuotedString(meetup["speaker"])
    if "host" in meetup:
        meetup["host"] = QuotedString(meetup["host"])
    if "image" in meetup:
        if "path" in meetup["image"]:
            meetup["image"]["path"] = to_quoted_str(meetup["image"]["path"])
        if "alt" in meetup["image"]:
            meetup["image"]["alt"] = to_quoted_str(meetup["image"]["alt"])
    if "link" in meetup and "title" in meetup["link"]:
        meetup["link"]["title"] = to_quoted_str(meetup["link"]["title"])
    return meetup


def write_yaml_file(file_path, data) -> None:
    """
    Writes the given data to a YAML file.
    
    :param file_path: The path of the YAML file to write to.
    :param data: The data to write to the file.
    :return: None    
    """
    try:
        with open(file_path, "w") as file:
            for yaml_obj in data:
                file.write(yaml.dump([yaml_obj], sort_keys=False, width=2000))
                file.write("\n")
    except (IOError, yaml.YAMLError) as e:
        logging.error(f"Error writing to file '{file_path}': {e}")
        raise


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
    existing_data = []
    try:
        if mode == WriteMode.APPEND:
            logging.info("Appending to existing YML file")
            with open(yaml_file, "r") as file:
                existing_data = yaml.safe_load(file) or []  # Handle empty file
            existing_data.extend(meetup_dicts)
            meetup_dicts = existing_data
        if not isinstance(existing_data, list):
            raise ValueError("Existing data is not a list")

        meetup_dicts = [process_meetup_data(meetup) for meetup in meetup_dicts]
        write_yaml_file(yaml_file, meetup_dicts)

    except FileNotFoundError:
        print(f"File '{yaml_file}' not found. Creating a new file.")
        with open(yaml_file, "w") as file:
            yaml.dump(meetup_dicts, file, default_flow_style=False, sort_keys=False)

    except (IOError, yaml.YAMLError) as e:
        logging.error(f"Error processing file '{yaml_file}': {e}")
        raise

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
    """
    Convert the date string to the desired format.
    :param date_str: The date string to convert.
    :return: The date string in the desired format.
    """
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
