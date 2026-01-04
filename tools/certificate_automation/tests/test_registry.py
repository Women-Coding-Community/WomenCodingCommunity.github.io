import unittest
import sys
import os
import json
import tempfile
import shutil

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from generate_certificates import (
    load_certificate_registry,
    save_certificate_registry,
    add_to_registry
)


class TestCertificateRegistry(unittest.TestCase):
    """Test cases for certificate registry management."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.registry_path = os.path.join(self.test_dir, 'test_registry.json')

    def tearDown(self):
        """Tear down test fixtures."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir)

    def test_load_certificate_registry_new_file(self):
        """Test loading registry when file doesn't exist."""
        registry = load_certificate_registry(self.registry_path)

        self.assertIsInstance(registry, dict)
        self.assertIn('certificates', registry)
        self.assertIsInstance(registry['certificates'], list)
        self.assertEqual(len(registry['certificates']), 0)

    def test_load_certificate_registry_existing_file(self):
        """Test loading registry from existing file."""
        # Create a test registry file
        test_data = {
            "certificates": [
                {
                    "id": "ABC123",
                    "name": "Test User",
                    "type": "mentee",
                    "issue_date": "2026-01-04",
                    "verification_url": "https://www.womencodingcommunity.com/verify?cert=ABC123"
                }
            ]
        }

        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)

        # Load the registry
        registry = load_certificate_registry(self.registry_path)

        self.assertEqual(len(registry['certificates']), 1)
        self.assertEqual(registry['certificates'][0]['id'], 'ABC123')
        self.assertEqual(registry['certificates'][0]['name'], 'Test User')

    def test_save_certificate_registry(self):
        """Test saving registry to file."""
        registry = {
            "certificates": [
                {
                    "id": "TEST123",
                    "name": "Jane Doe",
                    "type": "mentor",
                    "issue_date": "2026-01-04",
                    "verification_url": "https://www.womencodingcommunity.com/verify?cert=TEST123"
                }
            ]
        }

        save_certificate_registry(registry, self.registry_path)

        # Verify file was created
        self.assertTrue(os.path.exists(self.registry_path))

        # Verify content
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)

        self.assertEqual(len(saved_data['certificates']), 1)
        self.assertEqual(saved_data['certificates'][0]['id'], 'TEST123')

    def test_add_to_registry_new_certificate(self):
        """Test adding a new certificate to registry."""
        registry = {"certificates": []}

        cert = add_to_registry(
            registry,
            cert_id="NEW123",
            name="Alice Johnson",
            cert_type="volunteer",
            issue_date="2026-01-04"
        )

        self.assertEqual(len(registry['certificates']), 1)
        self.assertEqual(cert['id'], 'NEW123')
        self.assertEqual(cert['name'], 'Alice Johnson')
        self.assertEqual(cert['type'], 'volunteer')
        self.assertEqual(cert['issue_date'], '2026-01-04')
        self.assertIn('verification_url', cert)

    def test_add_to_registry_duplicate_certificate(self):
        """Test that duplicate certificates are not added."""
        registry = {"certificates": []}

        # Add first certificate
        add_to_registry(
            registry,
            cert_id="DUP123",
            name="Bob Smith",
            cert_type="mentee",
            issue_date="2026-01-04"
        )

        # Try to add duplicate
        add_to_registry(
            registry,
            cert_id="DUP123",
            name="Bob Smith",
            cert_type="mentee",
            issue_date="2026-01-04"
        )

        # Should still only have one certificate
        self.assertEqual(len(registry['certificates']), 1)

    def test_add_to_registry_verification_url_format(self):
        """Test that verification URL has correct format."""
        registry = {"certificates": []}

        cert = add_to_registry(
            registry,
            cert_id="URL123",
            name="Test User",
            cert_type="mentee",
            issue_date="2026-01-04"
        )

        expected_url = "https://www.womencodingcommunity.com/verify?cert=URL123"
        self.assertEqual(cert['verification_url'], expected_url)

    def test_add_to_registry_multiple_certificates(self):
        """Test adding multiple different certificates."""
        registry = {"certificates": []}

        add_to_registry(registry, "CERT1", "User 1", "mentee", "2026-01-04")
        add_to_registry(registry, "CERT2", "User 2", "mentor", "2026-01-04")
        add_to_registry(registry, "CERT3", "User 3", "volunteer", "2026-01-04")

        self.assertEqual(len(registry['certificates']), 3)

        # Verify all certificates are present
        cert_ids = [cert['id'] for cert in registry['certificates']]
        self.assertIn("CERT1", cert_ids)
        self.assertIn("CERT2", cert_ids)
        self.assertIn("CERT3", cert_ids)

    def test_save_registry_preserves_unicode(self):
        """Test that registry saves unicode characters correctly."""
        registry = {
            "certificates": [
                {
                    "id": "UNI123",
                    "name": "María José González",
                    "type": "mentee",
                    "issue_date": "2026-01-04",
                    "verification_url": "https://www.womencodingcommunity.com/verify?cert=UNI123"
                }
            ]
        }

        save_certificate_registry(registry, self.registry_path)

        # Load and verify
        with open(self.registry_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)

        self.assertEqual(saved_data['certificates'][0]['name'], "María José González")

    def test_registry_round_trip(self):
        """Test saving and loading registry maintains data integrity."""
        original_registry = {"certificates": []}

        add_to_registry(original_registry, "RT1", "Round Trip User 1", "mentee", "2026-01-04")
        add_to_registry(original_registry, "RT2", "Round Trip User 2", "mentor", "2026-01-05")

        # Save
        save_certificate_registry(original_registry, self.registry_path)

        # Load
        loaded_registry = load_certificate_registry(self.registry_path)

        # Verify
        self.assertEqual(len(loaded_registry['certificates']), 2)
        self.assertEqual(loaded_registry['certificates'][0]['id'], 'RT1')
        self.assertEqual(loaded_registry['certificates'][1]['id'], 'RT2')


if __name__ == '__main__':
    unittest.main()
