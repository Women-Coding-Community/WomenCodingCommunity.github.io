import os
import sys
import io
import tempfile
import pytest
import builtins
import requests
from unittest import mock

import download_image


class TestDownloadImage:
    def test_successful_download_creates_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(download_image, "IMAGE_FILE_PATH", str(tmp_path))

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake image data"
        mock_response.raise_for_status = mock.Mock()
        monkeypatch.setattr(requests, "get", mock.Mock(return_value=mock_response))

        url = "https://example.com/test.jpeg"
        mentor_name = "Alice Smith"
        image_path = download_image.download_image(url, mentor_name)

        assert image_path.endswith("alice_smith.jpeg")
        assert os.path.exists(image_path)
        with open(image_path, "rb") as f:
            assert f.read() == b"fake image data"

    def test_download_failure_returns_none(self, tmp_path, monkeypatch):
        monkeypatch.setattr(download_image, "IMAGE_FILE_PATH", str(tmp_path))

        monkeypatch.setattr(requests, "get", mock.Mock(side_effect=requests.exceptions.RequestException("network error")))

        result = download_image.download_image("https://badurl.com/image.jpeg", "Bob")
        assert result is None

    def test_directory_created_if_not_exists(self, tmp_path, monkeypatch):
        image_dir = tmp_path / "new_images"
        monkeypatch.setattr(download_image, "IMAGE_FILE_PATH", str(image_dir))

        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = b"123"
        mock_response.raise_for_status = mock.Mock()
        monkeypatch.setattr(requests, "get", mock.Mock(return_value=mock_response))

        result = download_image.download_image("https://example.com/img.jpg", "John Doe")
        assert os.path.exists(image_dir)
        assert result.endswith("john_doe.jpeg")

    def test_filename_sanitization(self, tmp_path, monkeypatch):
        monkeypatch.setattr(download_image, "IMAGE_FILE_PATH", str(tmp_path))

        mock_response = mock.Mock()
        mock_response.content = b"data"
        mock_response.raise_for_status = mock.Mock()
        monkeypatch.setattr(requests, "get", mock.Mock(return_value=mock_response))

        result = download_image.download_image("https://example.com/img.jpg", "Alice Smith-Jones")
        assert "alice_smith-jones.jpeg" in result


class TestRunAutomation:
    def test_run_automation_success(self, tmp_path, monkeypatch, caplog):
        caplog.set_level("INFO")
        monkeypatch.setattr(sys, "argv", ["download_image.py", "samples/mentors.xlsx"])

        fake_path = str(tmp_path / "success-download.jpeg")
        monkeypatch.setattr(download_image, "download_image", mock.Mock(return_value=fake_path))

        download_image.run_automation()

        assert "Successfully downloaded 2 images." in caplog.text
        assert "Image download process completed." in caplog.text

    def test_run_automation_failure(self, monkeypatch, caplog):
        caplog.set_level("INFO")
        monkeypatch.setattr(sys, "argv", ["download_image.py", "samples/mentors.xlsx"])
        monkeypatch.setattr(download_image, "download_image", mock.Mock(return_value=None))

        download_image.run_automation()
        assert "Successfully downloaded 0 images." in caplog.text

    def test_run_automation_no_args(self, monkeypatch, caplog):
        monkeypatch.setattr(sys, "argv", ["download_image.py"])
        caplog.set_level("INFO")

        download_image.run_automation()

        assert "Script needs 1 parameter (xlsx_file_path) to run" in caplog.text
