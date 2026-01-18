import re
import logging
from datetime import date
import openai
import requests
import yaml
import dotenv
import os
import argparse

dotenv.load_dotenv()

# Constants
EVENTS_FILE = '../../_data/events.yml'
MODEL = "gpt-3.5-turbo"
REQUIRED_EVENT_FIELDS = ['title', 'description', 'date', 'time', 'link']

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def summarise_events_with_llm(events_file):
    try:
        events = _load_events(events_file)
        future_events = _filter_future_events(events)
        
        if not future_events:
            logger.warning("No future events found")
            return "No upcoming events scheduled."
        
        formatted_events = _format_events(future_events)
        llm_summary = _get_llm_summary(formatted_events)
        formatted_summary = _format_for_slack(llm_summary)
        
        return formatted_summary
    except Exception as e:
        logger.error(f"Error summarizing events: {e}", exc_info=True)
        raise

def _load_events(events_file):
    try:
        with open(events_file) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Events file not found: {events_file}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in events file: {e}")

def _filter_future_events(events):
    today = date.today().isoformat()
    return [event for event in events if event.get('date', '') > today]

def _validate_event(event):
    missing_fields = [field for field in REQUIRED_EVENT_FIELDS if field not in event]
    if missing_fields:
        raise ValueError(f"Event missing fields: {missing_fields}")

def _format_events(events):
    formatted = ''
    for index, event in enumerate(events):
        _validate_event(event)
        formatted += (
            f"## Event {index}\n\n"
            f"Title: {event['title']}\n\n"
            f"Description: {event['description']}\n\n"
            f"Date: {event['date']}\n\n"
            f"Time: {event['time']}\n\n"
            f"Meetup Link: {event['link'].get('path', 'N/A')}\n\n"
        )
    return formatted

def _get_llm_summary(formatted_events):
    prompt = f"""
    Summarise the upcoming Meetup events for our community, Women Coding Community, in the form of a Slack 
    message in markdown format.
    Output an error message if you have any problems, in the format '#ERROR: message'.

    ## Upcoming Meetup events
    {formatted_events}
    """
    
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    
    summary = response.choices[0].message.content
    
    if '#ERROR:' in summary:
        raise ValueError(f'LLM Error: {summary}')
    
    return summary

def _format_for_slack(text):
    # Convert Markdown bold to Slack format
    text = text.replace('**', '*')
    # Reformat Markdown links to Slack format
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<\2|\1>', text)
    return text

def _post_to_slack(message):
    webhook_url = os.getenv('SLACK_SUMMARY_BOT_WEBHOOK')
    if not webhook_url:
        raise ValueError("SLACK_SUMMARY_BOT_WEBHOOK not set in environment variables")

    response = requests.post(webhook_url, json={'text': message})
    response.raise_for_status()
    logger.info("Message posted to Slack successfully")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarise upcoming Meetup events and post to Slack.")
    parser.add_argument("--events_file", help="Path to the events YAML file.", default=EVENTS_FILE)
    args = parser.parse_args()
    try:
        summary = summarise_events_with_llm(args.events_file)
        _post_to_slack(summary)
    except Exception as e:
        logger.error(f"Failed to summarize and post events: {e}", exc_info=True)
        raise