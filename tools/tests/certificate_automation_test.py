import json
import os
import sys
import platform
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open
import pytest

# Add the certificate_automation/src to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'certificate_automation', 'src'))

import generate_certificates
from generate_certificates import (
    load_config,
    check_duplicates,
    load_names,
    generate_pptx,
    generate_pdf,
    check_metrics,
    generate_certificates_for_type,
    IS_WINDOWS,
    POWERPOINT_AVAILABLE
)


class TestLoadConfig:
    def test_load_config_returns_dict(self, tmp_path):
        """Test that load_config returns a dictionary with expected structure."""
        config_data = {
            "certificate_types": [
                {
                    "type": "test",
                    "template": "template.pptx",
                    "names_file": "names.txt",
                    "pdf_dir": "pdfs/",
                    "ppt_dir": "ppts/",
                    "placeholder_text": "Sample"
                }
            ]
        }

        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config_data))

        result = load_config(str(config_file))

        assert isinstance(result, dict)
        assert "certificate_types" in result
        assert len(result["certificate_types"]) == 1
        assert result["certificate_types"][0]["type"] == "test"
        assert result["certificate_types"][0]["placeholder_text"] == "Sample"
        assert result["certificate_types"][0]["template"] == "template.pptx"
        assert result["certificate_types"][0]["names_file"] == "names.txt"
        assert result["certificate_types"][0]["pdf_dir"] == "pdfs/"
        assert result["certificate_types"][0]["ppt_dir"] == "ppts/"

class TestCheckDuplicates:
    def test_check_duplicates_with_no_duplicates(self, capsys):
        """Test check_duplicates with unique names."""
        names = ["Alice", "Bob", "Charlie"]

        check_duplicates(names, "mentee")

        captured = capsys.readouterr()
        assert "WARNING" not in captured.out

    def test_check_duplicates_with_duplicates(self, capsys):
        """Test check_duplicates identifies duplicate names."""
        names = ["Alice", "Bob", "Alice", "Charlie", "Bob"]

        check_duplicates(names, "mentee")

        captured = capsys.readouterr()
        assert "WARNING" in captured.out
        assert "2 duplicate name(s)" in captured.out
        assert "Alice" in captured.out
        assert "Bob" in captured.out


class TestLoadNames:
    def test_load_names_returns_set(self, tmp_path):
        """Test that load_names returns a set of unique names."""
        names_file = tmp_path / "names.txt"
        names_file.write_text("Alice\nBob\nCharlie\n")

        result = load_names(str(names_file), "mentee")

        assert isinstance(result, set)
        assert len(result) == 3

    def test_load_names_strips_whitespace(self, tmp_path):
        """Test that load_names strips whitespace from names."""
        names_file = tmp_path / "names.txt"
        names_file.write_text("  Alice  \n\n  Bob\n  Charlie  \n")

        result = load_names(str(names_file), "mentee")

        assert "Alice" in result
        assert "  Alice  " not in result
        assert len(result) == 3

    def test_load_names_deduplicates(self, tmp_path):
        """Test that load_names returns unique names only."""
        names_file = tmp_path / "names.txt"
        names_file.write_text("Alice\nBob\nAlice\nCharlie\n")

        result = load_names(str(names_file), "mentee")

        assert len(result) == 3  # Alice should appear only once


class TestGeneratePptx:
    @patch('generate_certificates.Presentation')
    def test_generate_pptx_creates_file(self, mock_presentation_class, tmp_path):
        """Test that generate_pptx creates a PPTX file."""
        # Setup mock
        mock_prs = MagicMock()
        mock_presentation_class.return_value = mock_prs

        mock_slide = MagicMock()
        mock_shape = MagicMock()
        mock_shape.has_text_frame = True
        mock_shape.text.strip.return_value = "Sample Sample"
        mock_text_frame = MagicMock()
        mock_shape.text_frame = mock_text_frame
        mock_slide.shapes = [mock_shape]
        mock_prs.slides = [mock_slide]

        output_dir = str(tmp_path)
        template = "template.pptx"

        result = generate_pptx("John Doe", output_dir, "Sample Sample", template)

        assert result == os.path.join(output_dir, "John Doe.pptx")
        mock_prs.save.assert_called_once_with(os.path.join(output_dir, "John Doe.pptx"))

    @patch('generate_certificates.Presentation')
    def test_generate_pptx_replaces_placeholder(self, mock_presentation_class):
        """Test that generate_pptx replaces placeholder text with name."""
        mock_prs = MagicMock()
        mock_presentation_class.return_value = mock_prs

        mock_slide = MagicMock()
        mock_shape = MagicMock()
        mock_shape.has_text_frame = True
        mock_shape.text.strip.return_value = "Sample Sample"

        mock_text_frame = MagicMock()
        mock_paragraph = MagicMock()
        mock_original_run = MagicMock()
        mock_original_run.font.name = "Arial"
        mock_original_run.font.size = 50
        mock_original_run.font.bold = False
        mock_original_run.font.italic = False
        mock_original_run.font.underline = False
        mock_original_run.font.color.type = None
        mock_text_frame.paragraphs = [MagicMock(runs=[mock_original_run])]

        mock_new_run = MagicMock()
        mock_paragraph.add_run.return_value = mock_new_run
        mock_text_frame.paragraphs[0].add_run.return_value = mock_new_run

        mock_shape.text_frame = mock_text_frame

        mock_slide.shapes = [mock_shape]
        mock_prs.slides = [mock_slide]

        generate_pptx("Jane Smith", "/tmp", "Sample Sample", "template.pptx")

        mock_text_frame.clear.assert_called_once()
        assert mock_new_run.text == "Jane Smith"

    @patch('generate_certificates.Presentation')
    def test_generate_pptx_handles_exceptions(self, mock_presentation_class):
        """Test that generate_pptx propagates exceptions."""
        mock_presentation_class.side_effect = Exception("Template not found")

        with pytest.raises(Exception) as exc_info:
            generate_pptx("John Doe", "/tmp", "Sample", "bad_template.pptx")

        assert "Template not found" in str(exc_info.value)


@pytest.mark.skipif(not POWERPOINT_AVAILABLE, reason="PDF generation only works on Windows with PowerPoint")
class TestGeneratePdf:
    def test_generate_pdf_creates_file(self, tmp_path):
        """Test that generate_pdf creates a PDF file."""
        import generate_certificates

        # Create a fake PPTX file
        input_dir = tmp_path / "ppts"
        input_dir.mkdir()
        pptx_file = input_dir / "John Doe.pptx"
        pptx_file.write_text("fake pptx")

        output_dir = tmp_path / "pdfs"
        output_dir.mkdir()

        # Mock the powerpoint global variable
        mock_presentation = MagicMock()
        mock_powerpoint = MagicMock()
        mock_powerpoint.Presentations.Open.return_value = mock_presentation

        # Inject the mock into the module's namespace
        generate_certificates.powerpoint = mock_powerpoint

        result = generate_pdf("John Doe", str(input_dir), str(output_dir))

        assert result == output_dir / "John Doe.pdf"
        mock_powerpoint.Presentations.Open.assert_called_once()
        mock_presentation.SaveAs.assert_called_once()
        mock_presentation.Close.assert_called_once()

    def test_generate_pdf_raises_error_if_pptx_missing(self, tmp_path):
        """Test that generate_pdf raises FileNotFoundError if PPTX doesn't exist."""
        import generate_certificates

        input_dir = tmp_path / "ppts"
        input_dir.mkdir()
        output_dir = tmp_path / "pdfs"
        output_dir.mkdir()

        # Mock the powerpoint global (even though we won't use it)
        generate_certificates.powerpoint = MagicMock()

        with pytest.raises(FileNotFoundError) as exc_info:
            generate_pdf("Nonexistent Person", str(input_dir), str(output_dir))

        assert "PPTX not found" in str(exc_info.value)


class TestCheckMetrics:
    def test_check_metrics_all_files_present(self, tmp_path, capsys):
        """Test check_metrics when all certificates are present."""
        output_dir = tmp_path / "ppts"
        output_dir.mkdir()

        names = {"Alice", "Bob", "Charlie"}
        for name in names:
            (output_dir / f"{name}.pptx").write_text("fake")

        cert_config = {
            "type": "mentee",
            "ppt_dir": str(output_dir)
        }

        check_metrics(names, cert_config, "pptx")

        captured = capsys.readouterr()
        assert "Expected certificates: 3" in captured.out
        assert "Found certificates: 3" in captured.out
        assert "All mentee certificates are present!" in captured.out

    def test_check_metrics_missing_files(self, tmp_path, capsys):
        """Test check_metrics when some certificates are missing."""
        output_dir = tmp_path / "ppts"
        output_dir.mkdir()

        # Create only 2 out of 3 files
        (output_dir / "Alice.pptx").write_text("fake")
        (output_dir / "Bob.pptx").write_text("fake")

        names = {"Alice", "Bob", "Charlie"}
        cert_config = {
            "type": "mentee",
            "ppt_dir": str(output_dir)
        }

        check_metrics(names, cert_config, "pptx")

        captured = capsys.readouterr()
        assert "Expected certificates: 3" in captured.out
        assert "Found certificates: 2" in captured.out
        assert "Missing 1 certificate(s):" in captured.out
        assert "Charlie" in captured.out

    def test_check_metrics_directory_not_exists(self, capsys):
        """Test check_metrics when output directory doesn't exist."""
        names = {"Alice"}
        cert_config = {
            "type": "mentee",
            "ppt_dir": "/nonexistent/path"
        }

        result = check_metrics(names, cert_config, "pptx")

        captured = capsys.readouterr()
        assert "ERROR: Directory does not exist" in captured.out
        assert result == (0, 1)


class TestGenerateCertificatesForType:
    @patch('generate_certificates.generate_pptx')
    def test_generate_certificates_for_type_pptx(self, mock_generate_pptx, tmp_path, capsys):
        """Test generate_certificates_for_type for PPTX generation."""
        output_dir = tmp_path / "ppts"
        output_dir.mkdir()

        mock_generate_pptx.return_value = str(output_dir / "Alice.pptx")

        names = {"Alice", "Bob"}
        cert_config = {
            "type": "mentee",
            "template": "template.pptx",
            "ppt_dir": str(output_dir),
            "placeholder_text": "Sample",
            "font_name": "Arial",
            "font_size": 50
        }

        result = generate_certificates_for_type(names, cert_config, "pptx")

        assert result == 2
        assert mock_generate_pptx.call_count == 2

        captured = capsys.readouterr()
        assert "Successfully generated 2/2 mentee certificates" in captured.out

    @patch('generate_certificates.generate_pptx')
    def test_generate_certificates_handles_errors(self, mock_generate_pptx, tmp_path, capsys):
        """Test that generate_certificates_for_type handles errors gracefully."""
        output_dir = tmp_path / "ppts"
        output_dir.mkdir()

        # First call succeeds, second fails
        mock_generate_pptx.side_effect = [
            str(output_dir / "Alice.pptx"),
            Exception("Template error")
        ]

        names = {"Alice", "Bob"}
        cert_config = {
            "type": "mentee",
            "template": "template.pptx",
            "ppt_dir": str(output_dir),
            "placeholder_text": "Sample",
            "font_name": "Arial",
            "font_size": 50
        }

        result = generate_certificates_for_type(names, cert_config, "pptx")

        assert result == 1  # Only 1 successful

        captured = capsys.readouterr()
        assert "ERROR generating pptx certificate" in captured.out
        assert "Successfully generated 1/2 mentee certificates" in captured.out
