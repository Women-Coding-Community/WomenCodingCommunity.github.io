import tempfile
import os
import pytest
import yaml
from unittest import mock
import requests
from meetup_import import (
    clean_name,
    get_hosts_and_speakers,
    clean_description,
    get_formatted_event_description,
    get_event_image_url,
    to_literal_str,
    to_quoted_str,
    LiteralString,
    QuotedString,
    NoQuoteString,
    get_event_key,
    get_existing_event_keys,
    load_existing_events_from_file,
    process_meetup_data
)

def test_clean_name_variants():
    assert clean_name('**Alice**') == 'Alice'
    assert clean_name('_Alice_') == 'Alice'
    assert clean_name('[Alice](https://x.com)') == 'Alice'
    assert clean_name('Alice | Other') == 'Alice'
    assert clean_name('  Alice  ') == 'Alice'

def test_get_hosts_and_speakers_variants():
    text = """Host: Alice
    Co-host: Bob
    Speaker: Dr. Jane Doe"""
    host, speaker = get_hosts_and_speakers(text)
    assert 'Alice' in host and 'Bob' in host
    assert 'Dr. Jane Doe' in speaker

def test_get_hosts_and_speakers_empty():
    host, speaker = get_hosts_and_speakers('')
    assert host == '' and speaker == ''

def test_clean_description_removes_formatting():
    text = '**Bold** [link](https://x.com) café 😀'
    result = clean_description(text)
    assert '**' not in result
    assert 'https' not in result
    assert 'cafe' in result
    assert '😀' not in result

def test_get_formatted_event_description_variants():
    desc1 = 'This is first. This is second.'
    desc2 = 'Women Coding Community presents event.'
    desc3 = 'Single sentence'
    assert get_formatted_event_description(desc1) == 'This is first.'
    assert 'Women Coding Community' not in get_formatted_event_description(desc2)
    assert get_formatted_event_description(desc3).endswith('.')

def test_get_event_image_url_with_og_image(monkeypatch):
    mock_html = '''<html>
        <head>
            <meta property="og:image" content="https://example.com/event-image.jpg">
        </head>
    </html>'''
    mock_response = mock.Mock()
    mock_response.content = mock_html.encode()
    monkeypatch.setattr(requests, "get", mock.Mock(return_value=mock_response))
    
    url = get_event_image_url("https://meetup.com/event/123")
    assert url == "https://example.com/event-image.jpg"

def test_get_event_image_url_fallback_to_img_tag(monkeypatch):
    mock_html = '''<html>
        <body>
            <img src="https://example.com/fallback.jpg" alt="Event">
        </body>
    </html>'''
    mock_response = mock.Mock()
    mock_response.content = mock_html.encode()
    monkeypatch.setattr(requests, "get", mock.Mock(return_value=mock_response))
    
    url = get_event_image_url("https://meetup.com/event/456")
    assert url == "https://example.com/fallback.jpg"

def test_to_literal_and_quoted_str():
    assert isinstance(to_literal_str('Line 1\nLine 2'), LiteralString)
    assert isinstance(to_literal_str('Simple text'), str)
    assert isinstance(to_quoted_str('Hello!'), QuotedString)
    assert isinstance(to_quoted_str('Simple'), NoQuoteString)

def test_get_event_key():
    event = {'title': '  Talk ', 'date': 'JAN 1, 2025'}
    assert get_event_key(event) == 'Talk - JAN 1, 2025'

def test_get_existing_event_keys():
    events = [{'title': 'A', 'date': '1'}, {'title': 'B', 'date': '2'}]
    keys = get_existing_event_keys(events)
    assert len(keys) == 2 and all(isinstance(k, str) for k in keys)

def test_load_existing_events_from_file(tmp_path):
    events = [{'title': 'E1', 'date': 'D1'}]
    path = tmp_path / 'data.yml'
    with open(path, 'w') as f:
        yaml.dump(events, f)
    loaded = load_existing_events_from_file(path)
    assert loaded[0]['title'] == 'E1'

def test_load_existing_events_handles_missing_file():
    result = load_existing_events_from_file('/no/such/file.yml')
    assert result == []

def test_process_meetup_data_fields():
    meetup = {
        'title': 'Event\nTitle',
        'description': 'Desc\nline',
        'expiration': '20250101',
        'host': 'Host',
        'speaker': 'Speaker',
        'image': {'path': 'https://img', 'alt': 'Alt'},
        'link': {'path': 'https://x', 'title': 'View'}
    }
    result = process_meetup_data(meetup)
    assert isinstance(result['title'], (LiteralString, str))
    assert isinstance(result['expiration'], QuotedString)
    assert isinstance(result['image']['path'], (QuotedString, NoQuoteString))
    assert isinstance(result['link']['title'], (QuotedString, NoQuoteString))