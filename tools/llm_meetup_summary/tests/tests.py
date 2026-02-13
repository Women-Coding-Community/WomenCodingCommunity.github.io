import pytest

from tools.llm_meetup_summary.llm_event_summary import summarize_meetup_events_with_llms

import pytest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
import sys
import os

# Add parent directory to path for absolute imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.llm_meetup_summary.llm_event_summary import (
    _get_llm_summary,
    _format_for_slack,
    _validate_event,
    _load_events,
    get_date_of_event_iso,
)

class TestGetLlmSummary:
    """Tests for _get_llm_summary function"""

    @patch("tools.llm_meetup_summary.summarise_events_with_llms.openai.chat.completions.create")
    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.read_text")
    def test_get_llm_summary_success(self, mock_read_text, mock_file, mock_openai):
        """Test successful LLM summary generation"""
        mock_read_text.return_value = "Example content"
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Here's a summary of upcoming events"
        mock_openai.return_value = mock_response
        
        result = _get_llm_summary("## Event 1\nTitle: Test Event")
        
        assert result == "Here's a summary of upcoming events"
        assert mock_openai.called

    @patch("tools.llm_meetup_summary.summarise_events_with_llms.openai.chat.completions.create")
    @patch("pathlib.Path.read_text")
    def test_get_llm_summary_error_response(self, mock_read_text, mock_openai):
        """Test when LLM returns error message"""
        mock_read_text.return_value = "Example content"
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "#ERROR: Invalid event format"
        mock_openai.return_value = mock_response
        
        with pytest.raises(ValueError, match="LLM Error"):
            _get_llm_summary("## Event 1")

    @patch("tools.llm_meetup_summary.summarise_events_with_llms.openai.chat.completions.create")
    @patch("pathlib.Path.read_text")
    def test_get_llm_summary_creates_prompt_file(self, mock_read_text, mock_openai):
        """Test that prompt is saved to current_prompt.md"""
        mock_read_text.return_value = "Example content"
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Summary content"
        mock_openai.return_value = mock_response
        
        with patch("builtins.open", mock_open()) as mock_file:
            _get_llm_summary("## Event 1")
            mock_file.assert_called()


class TestFormatForSlack:
    """Tests for _format_for_slack function"""

    def test_format_for_slack_converts_bold(self):
        """Test markdown bold conversion to Slack format"""
        result = _format_for_slack("This is **bold** text")
        assert result == "This is *bold* text"

    def test_format_for_slack_converts_links(self):
        """Test markdown link conversion to Slack format"""
        result = _format_for_slack("[Click here](https://example.com)")
        assert result == "<https://example.com|Click here>"

    def test_format_for_slack_multiple_conversions(self):
        """Test multiple markdown conversions"""
        result = _format_for_slack("**Bold** and [link](https://example.com)")
        assert "*Bold*" in result
        assert "<https://example.com|link>" in result

    def test_format_for_slack_none_input(self):
        """Test that None input raises ValueError"""
        with pytest.raises(ValueError, match="No text provided"):
            _format_for_slack(None)


class TestValidateEvent:
    """Tests for _validate_event function"""

    def test_validate_event_valid(self):
        """Test validation passes for complete event"""
        event = {
            'title': 'Test',
            'description': 'Desc',
            'date': '2024-01-01',
            'time': '18:00',
            'link': {'path': 'https://example.com'}
        }
        _validate_event(event)  # Should not raise

    def test_validate_event_missing_field(self):
        """Test validation fails for missing field"""
        event = {
            'title': 'Test',
            'description': 'Desc',
            'date': '2024-01-01'
        }
        with pytest.raises(ValueError, match="missing fields"):
            _validate_event(event)


class TestLoadEvents:
    """Tests for _load_events function"""

    @patch("builtins.open", new_callable=mock_open, read_data="- title: Event1\n  description: Desc")
    @patch("yaml.safe_load")
    def test_load_events_success(self, mock_yaml, mock_file):
        """Test successful event loading"""
        mock_yaml.return_value = [{'title': 'Event1'}]
        result = _load_events("test.yml")
        assert result == [{'title': 'Event1'}]

    def test_load_events_file_not_found(self):
        """Test FileNotFoundError for missing file"""
        with pytest.raises(FileNotFoundError):
            _load_events("/nonexistent/path.yml")


class TestGetDateOfEventIso:
    """Tests for get_date_of_event_iso function"""

    def test_get_date_of_event_iso_valid(self):
        """Test date formatting from YYYYMMDD"""
        event = {'expiration': '20240115'}
        result = get_date_of_event_iso(event)
        assert result == '20240115'

    def test_get_date_of_event_iso_invalid_length(self):
        """Test assertion error for invalid date length"""
        event = {'expiration': '2024011'}
        with pytest.raises(AssertionError):
            get_date_of_event_iso(event)