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

# Get current folder
current_folder = os.path.dirname(os.path.abspath(__file__))

# Constants
EVENTS_FILE = os.path.join(current_folder, '../../_data/events.yml')
MODEL = "gpt-4.1-nano"
REQUIRED_EVENT_FIELDS = ['title', 'description', 'date', 'time', 'link']

try:
    SLACK_TEST_WEBHOOK= os.getenv('SLACK_BOT_TEST_WEBHOOK')
    SLACK_WEBHOOK= os.getenv('SLACK_BOT_WEBHOOK')
except KeyError as e:
    raise KeyError(f"Environment variable not set: {e}")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def summarise_events_with_llm(events_file=EVENTS_FILE):
    try:
        events = _load_events(events_file)
        future_events = _filter_future_events(events)

        print("Future Events:\n", future_events)
        
        if not future_events:
            logger.warning("No future events found")
            return "No upcoming events scheduled."
        
        formatted_events = _format_events_as_markdown(future_events)

        print("Formatted Events for LLM:\n", formatted_events[:2000])

        llm_summary = _get_llm_summary(formatted_events)
    except Exception as e:
        logger.error(f"Error summarizing events: {e}", exc_info=True)
        raise

    formatted_summary = _format_for_slack(llm_summary)
    return formatted_summary

def _load_events(events_file):
    try:
        with open(events_file) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Events file not found: {events_file}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in events file: {e}")

def get_date_of_event_iso(event):
    event_date = event.get('expiration') # should be in the format 'YYYYMMDD'
    assert len(event_date)==8
    event_date_formatted = event_date[:4] + event_date[4:6] + event_date[6:8]
    return event_date_formatted

def _filter_future_events(events):
    today = date.today().isoformat()
    return [event for event in events if get_date_of_event_iso(event) > today]

def _validate_event(event):
    missing_fields = [field for field in REQUIRED_EVENT_FIELDS if field not in event]
    if missing_fields:
        raise ValueError(f"Event missing fields: {missing_fields}")

def _format_events_as_markdown(events):
    formatted = ''
    for index, event in enumerate(events):
        _validate_event(event)

        event_description = event['description']
        wcc_description_idx = event['description'].find('About Women Coding Community')

        if wcc_description_idx != -1:
            event_description = event_description[:wcc_description_idx]

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
    from pathlib import Path

    examples_dir = Path(__file__).parent / "examples"

    Example1 = (examples_dir / "01_example_events.md").read_text()
    Example2 = (examples_dir / "02_example_events.md").read_text()
    Example3 = (examples_dir / "03_example_events.md").read_text()

    Summary1 = (examples_dir / "01_summary.md").read_text()
    Summary2 = (examples_dir / "02_summary.md").read_text()
    Summary3 = (examples_dir / "03_summary.md").read_text()

    prompt = f"""
Summarise the upcoming events for our community, Women Coding Community, in the form of a Slack 
message in markdown format. Start directly with the summary without any introduction.

Output an error message if you have any problems, in the format '#ERROR: message'.

# About Women Coding Community 
Empowering women in their tech careers through education, mentorship, community building, and career 
services is our mission. We provide workshops and events, connect members with industry mentors, foster 
a supportive community through meetups and conferences, and raise awareness for more inclusive industry 
practices.

# Example Events 1
{Example1}

# Summary 1
{Summary1}

# Example Events 2
{Example2}

# Summary 2
{Summary2}

# Example Events 3
{Example3}

# Summary 3
{Summary3}
---

Now summarise the following upcoming events:

# Upcoming Meetup Events
{formatted_events}
    """

    with open(os.path.join(examples_dir, "current_prompt.md"), 'w') as txt:
        txt.write(prompt) # save for reference
    
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    
    summary = response.choices[0].message.content
    
    if '#ERROR:' in summary:
        raise ValueError(f'LLM Error: {summary}')
    
    return summary

def _format_for_slack(text):
    if text is None:
        raise ValueError("No text provided for Slack formatting")
    # Convert Markdown bold to Slack format
    text = text.replace('**', '*')
    # Reformat Markdown links to Slack format
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<\2|\1>', text)
    return text

def _post_to_slack(message, slack_webhook_url=SLACK_TEST_WEBHOOK):
    if not slack_webhook_url:
        raise ValueError("SLACK_SUMMARY_WEBHOOK not set in environment variables")

    response = requests.post(slack_webhook_url, json={'text': message})
    response.raise_for_status()
    logger.info("Message posted to Slack successfully")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarise upcoming Meetup events and post to Slack.")
    parser.add_argument(
        "--test", 
        action="store_true", 
        help="Post the summary to the test Slack channel #test-meetup-summaries. Otherwise, post to #events."
    )
    parser.add_argument("--events_file", help="Path to the events YAML file.", default=EVENTS_FILE)
    args = parser.parse_args()
    
    test_mode_activated = args.test

    if test_mode_activated:
        slack_webhook_url = SLACK_TEST_WEBHOOK
    else:
        slack_webhook_url = SLACK_WEBHOOK

    try:
        summary = summarise_events_with_llm(args.events_file)
        _post_to_slack(summary, slack_webhook_url)
    except Exception as e:
        logger.error(f"Failed to summarize and post events: {e}", exc_info=True)
        raise