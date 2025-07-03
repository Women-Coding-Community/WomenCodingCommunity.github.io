import logging
from enum import Enum
from typing import Optional, Union

import re
import requests
import yaml
import unicodedata
from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel
from ics import Calendar

# Banner paths
CODING_CLUB_BANNER = "/assets/images/events/event-coding-club-3.jpg"
WRITING_CLUB_BANNER = "/assets/images/events/event-writing-club.jpeg"

# ----- YAML formatting classes -----
class LiteralString(str): pass
class QuotedString(str): pass
class NoQuoteString(str): pass

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
    special_characters = "!@#$%^&*()-+?_=,<>/:;\\"

    if data and ("\n" in data or any(c in special_characters for c in data)):
        return LiteralString(data.rstrip() + "\n")
    return data

def to_quoted_str(data: str) -> Union[QuotedString, NoQuoteString]:
    special_characters = "!@#$%^&*()-+?_=,<>/:;\\"

    if data and ("\n" in data or any(c in special_characters for c in data)):
        return QuotedString(data)
    return NoQuoteString(data)


# ----- Models ------
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


# ----- Helper function to clean bold/italics markdown from a name -----
def clean_name(s):
    s = re.sub(r'[*_~`]+', '', s)
    s = s.strip()
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    if '|' in s:
        s = s.split('|')[0].strip()
    return s

# ----- Gets all hosts/co-hosts/speakers and formats accordingly -------
def get_hosts_and_speakers(event_desc: str) -> tuple[str, str]:
    hosts = []
    cohosts = []
    speakers = []

    text = event_desc.replace('\\', '')
    lines = text.splitlines()

    for line in lines:
        line = line.strip()

        host_match = re.match(r'\**Host:\**\s*(.+)', line, re.IGNORECASE)
        if host_match:
            host_name = clean_name(host_match.group(1))
            if host_name:
                hosts.append(host_name)
            continue

        cohost_match = re.match(r'\**Co-host:\**\s*(.+)', line, re.IGNORECASE)
        if cohost_match:
            cohost_name = clean_name(cohost_match.group(1))
            if cohost_name:
                cohosts.append(cohost_name)
            continue

        speaker_match = re.match(r'\**(Guest Presenter|Speaker):\**\s*(.+)', line, re.IGNORECASE)
        if speaker_match:
            speaker_name = clean_name(speaker_match.group(2))
            if speaker_name:
                speakers.append(speaker_name)
            continue

    speaker = ', '.join(speakers)
    host = ""

    if hosts and cohosts:
        host = f"{', '.join(hosts)} and {', '.join(cohosts)}"
    elif cohosts and not hosts:
        host = ', '.join(cohosts)
    else:
        host = ', '.join(hosts)

    return host, speaker

# ----- Removes all formatting, unicodes, emojis, etc from event description -----
def clean_description(text: str) -> str:
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'[*_~`]+', '', text)
    text = unicodedata.normalize('NFKD', text)
    allowed_chars = set(
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        " \t\n\r"
        ".,;:!?'\"-()’"
    )
    text = ''.join(ch for ch in text if ch in allowed_chars)
    return text

# ----- Truncates event description to 1st sentence only and removes WCC prefix in sentence -----
def get_formatted_event_description(event_desc: str) -> str:
    full_description = (clean_description(event_desc) or "").strip()
    first_sentence = full_description.split(".")[0].strip()
    if first_sentence:
        description = f"{first_sentence}."
    else:
        description = full_description # use full description if cannot truncate to 1st sentence only

    prefix = "Women Coding Community"
    if description.strip().startswith(prefix):
        return description.strip()[len(prefix):].lstrip()
    
    return description.strip()

# ------ Scrape a single Meetup event page to extract the main image URL ------
def get_event_image_url(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Look for the Open Graph image tag first (most reliable)
    og_image = soup.find("meta", property="og:image")
    if og_image:
        return og_image.get("content")

    # Fallback
    img_tag = soup.find("img")
    if img_tag:
        image_url = img_tag.get("src")
    
    return image_url


# --- Main logic using downloaded iCal file ---
def get_upcoming_meetups_from_ical_file(ical_path: str) -> list[MeetupEvents]:
    with open(ical_path, "r", encoding="utf-8") as f:
        calendar = Calendar(f.read())

    upcoming_meetups: list[MeetupEvents] = []

    for event in calendar.events:
        title = event.name
        date_obj = event.begin.datetime
        expiration = date_obj.strftime("%Y%m%d")
        date = date_obj.strftime("%a, %b %d, %Y").upper()
        time = event.begin.datetime.strftime("%I:%M %p %Z")
        url = event.url or ""

        full_description = (event.description or "").strip()

        host, speaker = get_hosts_and_speakers(full_description)
        description = get_formatted_event_description(full_description)
        image_url = get_event_image_url(url)

        # Categorize event type
        category_style = "tech-talk"
        category_name = "Tech Talk"
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

        upcoming_meetups.append(
            MeetupEvents(
                title=title,
                description=description.replace("\n", " "),
                category_style=category_style,
                category_name=category_name,
                date=date,
                time=time,
                expiration=expiration,
                host=host,
                speaker=speaker,
                image=Image(path=image_url, alt="WCC Meetup event image"),
                link=WebLink(path=url),
            )
        )
    return upcoming_meetups

# --- Processing and output ---
def process_meetup_data(meetup: dict) -> dict:
    meetup["title"] = to_literal_str(meetup["title"])
    meetup["description"] = to_literal_str(meetup["description"])
    meetup["expiration"] = QuotedString(meetup["expiration"])
    meetup["host"] = QuotedString(meetup.get("host", ""))
    meetup["speaker"] = QuotedString(meetup.get("speaker", ""))
    if "image" in meetup:
        meetup["image"]["path"] = to_quoted_str(meetup["image"]["path"])
        meetup["image"]["alt"] = to_quoted_str(meetup["image"]["alt"])
    if "link" in meetup and "title" in meetup["link"]:
        meetup["link"]["title"] = to_quoted_str(meetup["link"]["title"])
    return meetup

# ---- Write specified data to file -----
def write_yaml_file(file_path, data) -> None:
    try:
        with open(file_path, "w") as file:
            for yaml_obj in data:
                file.write(yaml.dump([yaml_obj], sort_keys=False, width=2000))
                file.write("\n")
    except (IOError, yaml.YAMLError) as e:
        logging.error(f"Error writing to file '{file_path}': {e}")
        raise

# ---- Process events data into yaml file -----
def export_to_yaml(upcoming_meetups, yaml_file: str):
    meetup_dicts = [meetup.dict() for meetup in upcoming_meetups]
    try:
        meetup_dicts = [process_meetup_data(meetup) for meetup in meetup_dicts]
        write_yaml_file(yaml_file, meetup_dicts)

    except FileNotFoundError:
        logging.warning(f"File '{yaml_file}' not found. Creating a new file.")
        with open(yaml_file, "w") as file:
            yaml.dump(meetup_dicts, file, default_flow_style=False, sort_keys=False)
    except (IOError, yaml.YAMLError) as e:
        logging.error(f"Error processing file '{yaml_file}': {e}")
        raise


# --- Script Start ---
def fetch_events():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    ical_file_path = "files/meetup.ics"
    yml_file_path = "../_data/imported_events.yml"

    logging.info("Params: iCal URL: %s yml: %s mode: %s", ical_file_path, yml_file_path)
    upcoming_meetups = get_upcoming_meetups_from_ical_file(ical_file_path)
    
    logging.info("Upcoming Meetups:")
    for meetup in upcoming_meetups:
        logging.info(f"{meetup.title}")
    export_to_yaml(upcoming_meetups, yml_file_path)


if __name__ == "__main__":
    fetch_events()
