import unittest
import sys
import os
from io import BytesIO
from PIL import Image

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from generate_certificates import generate_qr_code


class TestQRCode(unittest.TestCase):
    """Test cases for QR code generation."""

    def test_generate_qr_code_returns_bytesio(self):
        """Test that QR code generation returns BytesIO object."""
        url = "https://www.womencodingcommunity.com/verify?cert=ABC123DEF456"
        qr_img = generate_qr_code(url)
        self.assertIsInstance(qr_img, BytesIO)

    def test_generate_qr_code_creates_valid_image(self):
        """Test that QR code is a valid image."""
        url = "https://www.womencodingcommunity.com/verify?cert=ABC123DEF456"
        qr_img = generate_qr_code(url)

        # Try to open as image
        try:
            img = Image.open(qr_img)
            self.assertIsNotNone(img)
        except Exception as e:
            self.fail(f"Generated QR code is not a valid image: {e}")

    def test_generate_qr_code_image_format(self):
        """Test that QR code is in PNG format."""
        url = "https://www.womencodingcommunity.com/verify?cert=ABC123DEF456"
        qr_img = generate_qr_code(url)

        img = Image.open(qr_img)
        self.assertEqual(img.format, 'PNG')

    def test_generate_qr_code_image_mode(self):
        """Test that QR code image has correct color mode."""
        url = "https://www.womencodingcommunity.com/verify?cert=ABC123DEF456"
        qr_img = generate_qr_code(url)

        img = Image.open(qr_img)
        # QR codes should be in RGB or similar mode
        self.assertIn(img.mode, ['RGB', 'L', '1'])

    def test_generate_qr_code_with_different_urls(self):
        """Test that different URLs generate different QR codes."""
        url1 = "https://www.womencodingcommunity.com/verify?cert=ABC123"
        url2 = "https://www.womencodingcommunity.com/verify?cert=DEF456"

        qr_img1 = generate_qr_code(url1)
        qr_img2 = generate_qr_code(url2)

        # Read image data
        img1_data = qr_img1.getvalue()
        img2_data = qr_img2.getvalue()

        # Different URLs should generate different QR codes
        self.assertNotEqual(img1_data, img2_data)

    def test_generate_qr_code_deterministic(self):
        """Test that same URL generates same QR code."""
        url = "https://www.womencodingcommunity.com/verify?cert=ABC123DEF456"

        qr_img1 = generate_qr_code(url)
        qr_img2 = generate_qr_code(url)

        # Read image data
        img1_data = qr_img1.getvalue()
        img2_data = qr_img2.getvalue()

        # Same URL should generate same QR code
        self.assertEqual(img1_data, img2_data)

    def test_generate_qr_code_with_long_url(self):
        """Test QR code generation with very long URL."""
        url = "https://www.womencodingcommunity.com/verify?cert=ABC123DEF456&extra=verylongparametervalue"
        qr_img = generate_qr_code(url)

        # Should still generate valid image
        img = Image.open(qr_img)
        self.assertIsNotNone(img)

    def test_generate_qr_code_image_not_empty(self):
        """Test that generated QR code image is not empty."""
        url = "https://www.womencodingcommunity.com/verify?cert=ABC123DEF456"
        qr_img = generate_qr_code(url)

        img = Image.open(qr_img)
        width, height = img.size

        # Image should have reasonable size
        self.assertGreater(width, 0)
        self.assertGreater(height, 0)


if __name__ == '__main__':
    unittest.main()
