import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from generate_certificates import generate_certificate_id


class TestCertificateID(unittest.TestCase):
    """Test cases for certificate ID generation."""

    def test_generate_certificate_id_returns_string(self):
        """Test that certificate ID is returned as a string."""
        cert_id = generate_certificate_id("John Smith", "mentee", "2026-01-04")
        self.assertIsInstance(cert_id, str)

    def test_generate_certificate_id_length(self):
        """Test that certificate ID has correct length (12 characters)."""
        cert_id = generate_certificate_id("John Smith", "mentee", "2026-01-04")
        self.assertEqual(len(cert_id), 12)

    def test_generate_certificate_id_uppercase(self):
        """Test that certificate ID is uppercase."""
        cert_id = generate_certificate_id("John Smith", "mentee", "2026-01-04")
        self.assertEqual(cert_id, cert_id.upper())

    def test_generate_certificate_id_deterministic(self):
        """Test that same inputs generate same ID."""
        cert_id1 = generate_certificate_id("John Smith", "mentee", "2026-01-04")
        cert_id2 = generate_certificate_id("John Smith", "mentee", "2026-01-04")
        self.assertEqual(cert_id1, cert_id2)

    def test_generate_certificate_id_unique_for_different_names(self):
        """Test that different names generate different IDs."""
        cert_id1 = generate_certificate_id("John Smith", "mentee", "2026-01-04")
        cert_id2 = generate_certificate_id("Jane Doe", "mentee", "2026-01-04")
        self.assertNotEqual(cert_id1, cert_id2)

    def test_generate_certificate_id_unique_for_different_types(self):
        """Test that different certificate types generate different IDs."""
        cert_id1 = generate_certificate_id("John Smith", "mentee", "2026-01-04")
        cert_id2 = generate_certificate_id("John Smith", "mentor", "2026-01-04")
        self.assertNotEqual(cert_id1, cert_id2)

    def test_generate_certificate_id_unique_for_different_dates(self):
        """Test that different dates generate different IDs."""
        cert_id1 = generate_certificate_id("John Smith", "mentee", "2026-01-04")
        cert_id2 = generate_certificate_id("John Smith", "mentee", "2026-01-05")
        self.assertNotEqual(cert_id1, cert_id2)

    def test_generate_certificate_id_with_special_characters(self):
        """Test certificate ID generation with special characters in name."""
        cert_id = generate_certificate_id("María José", "mentee", "2026-01-04")
        self.assertIsInstance(cert_id, str)
        self.assertEqual(len(cert_id), 12)

    def test_generate_certificate_id_with_long_name(self):
        """Test certificate ID generation with very long name."""
        long_name = "Christopher Alexander Montgomery-Wellington III"
        cert_id = generate_certificate_id(long_name, "mentee", "2026-01-04")
        self.assertIsInstance(cert_id, str)
        self.assertEqual(len(cert_id), 12)

    def test_generate_certificate_id_hexadecimal(self):
        """Test that certificate ID contains only hexadecimal characters."""
        cert_id = generate_certificate_id("John Smith", "mentee", "2026-01-04")
        valid_chars = set("0123456789ABCDEF")
        self.assertTrue(all(c in valid_chars for c in cert_id))


if __name__ == '__main__':
    unittest.main()
