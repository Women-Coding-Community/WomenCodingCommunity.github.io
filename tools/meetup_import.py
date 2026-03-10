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

class MeetupEvent(BaseModel):
    title: str
    description: str
    category_style: Optional[str] = "tech-talk"
    uid: str
    category_name: Optional[str] = "Tech Talk"
    date: str
    expiration: str = ""
    host: Optional[str] = ""
    speaker: Optional[str] = ""
    time: Optional[str] = ""
    image: Optional[Image] = None
    link: Optional[WebLink] = None


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
def get_upcoming_meetups_from_ical_file(ical_path: str) -> list[MeetupEvent]:
    with open(ical_path, "r", encoding="utf-8") as f:
        calendar = Calendar(f.read())

    # sort events to ensure order by event date
    sorted_events = sorted(calendar.events, key=lambda e: e.begin)

    upcoming_meetups: list[MeetupEvent] = []

    for event in sorted_events:
        title = event.name
        date_obj = event.begin.datetime
        expiration = date_obj.strftime("%Y%m%d")
        date = date_obj.strftime("%a, %b %d, %Y").upper()
        time = event.begin.datetime.strftime("%I:%M %p %Z")
        url = event.url or ""
        uid = event.uid

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
            MeetupEvent(
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
                uid=uid,
            )
        )
    return upcoming_meetups

# --- Processing and output ---
def build_event_uid_from_title_and_date(title: str, date: str) -> str:
    # This is only necessary for some past events that were missing UIDs
    # Going forward we should have UIDs for all events from the iCal feed so this is just a fallback
    # (uid is a required field in MeetupEvent)
    normalized_title = "_".join((title or "").split()).replace(",", "").replace("&", "").lower()
    normalized_date = "_".join((date or "").split()).replace(",", "").lower()
    return f"{normalized_title}_{normalized_date}"


def add_missing_uid_fields_for_past_events(events: list[dict]) -> list[dict]:
    for event in events:
        if not event.get("uid"):
            event["uid"] = build_event_uid_from_title_and_date(event.get("title", ""), event.get("expiration", event.get("date", "")))
    return events

def process_meetup_data(meetup: MeetupEvent) -> dict:
    meetup["title"] = to_literal_str(meetup["title"])
    meetup["description"] = to_literal_str(meetup["description"])
    meetup["expiration"] = QuotedString(meetup["expiration"])
    meetup["uid"] = to_quoted_str(meetup["uid"])
    meetup["host"] = QuotedString(meetup.get("host", ""))
    meetup["speaker"] = QuotedString(meetup.get("speaker", ""))
        
    if meetup.get("image"):
        meetup["image"]["path"] = to_quoted_str(meetup["image"]["path"])
        meetup["image"]["alt"] = to_quoted_str(meetup["image"]["alt"])
    if meetup.get("link") and meetup["link"].get("title"):
        meetup["link"]["title"] = to_quoted_str(meetup["link"]["title"])
    return meetup

# --- Get existing events in yml file ----
def load_existing_events_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            events = yaml.safe_load(file) or []
            return add_missing_uid_fields_for_past_events(events)
    except FileNotFoundError:
        return []
    except (IOError, yaml.YAMLError) as e:
        logging.error(f"Error reading file '{file_path}': {e}")
        return []

# ---- Appends specified data to yml file -----
def append_events_to_yaml_file(file_path, data):
    try:
        with open(file_path, "a") as file:
            for yaml_obj in data:
                file.write("\n")
                file.write(yaml.dump([yaml_obj], sort_keys=False, width=2000))
    except (IOError, yaml.YAMLError) as e:
        logging.error(f"Error appending new events to file '{file_path}': {e}")
        raise

def get_event_key(event: Union[MeetupEvent, dict]) -> str:
    if isinstance(event, dict):
        return event.get("uid") or build_event_uid_from_title_and_date(event.get("title", ""), event.get("date", ""))
    return event.uid

def add_upcoming_events_to_existing_events(upcoming_events: list[MeetupEvent], existing_events: list[dict]) -> list[dict]:
    from datetime import datetime

    # Merge all events by UID (upcoming overwrites existing)
    all_events_dict = {get_event_key(event): event for event in existing_events}
    for future_event in upcoming_events:
        event_key = get_event_key(future_event)
        all_events_dict[event_key] = future_event.model_dump()

    all_events = list(all_events_dict.values())

    # Split into past and future events based on expiration
    today = datetime.now().strftime("%Y%m%d")
    def is_future(event):
        exp = event.get("expiration", "") if isinstance(event, dict) else getattr(event, "expiration", "")
        return exp >= today

    past_events = [e for e in all_events if not is_future(e)]
    future_events = [e for e in all_events if is_future(e)]

    # Sort only the future events by expiration - past events will already be sorted by date
    future_events_sorted = sorted(future_events, key=lambda e: e.get("expiration", "") if isinstance(e, dict) else getattr(e, "expiration", ""))

    # Concatenate past (already sorted) + sorted future
    return past_events + future_events_sorted

def write_all_events_to_yaml_file(file_path, all_events: list[dict]):
    try:
        with open(file_path, "w") as file:
            for event in all_events:
                file.write("\n")
                file.write(yaml.dump([process_meetup_data(event)], sort_keys=False, width=2000))
    except (IOError, yaml.YAMLError) as e:
        logging.error(f"Error writing events to file '{file_path}': {e}")
        raise

# --- Script Start ---
def fetch_events():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    ical_file_path = "files/meetup.ics"
    yml_file_path = "../_data/events.yml"

    logging.info("Params: iCal URL: %s yml: %s", ical_file_path, yml_file_path)
    upcoming_events = get_upcoming_meetups_from_ical_file(ical_file_path)
    existing_events = load_existing_events_from_file(yml_file_path)
    all_events = add_upcoming_events_to_existing_events(upcoming_events, existing_events)

    write_all_events_to_yaml_file(yml_file_path, all_events)

if __name__ == "__main__":
    fetch_events()
