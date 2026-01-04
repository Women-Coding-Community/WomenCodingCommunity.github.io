# WCC Certificate Automation - Test Suite

Comprehensive test suite for the Women Coding Community certificate automation system, including QR code verification functionality.

## Test Structure

```
tests/
├── __init__.py                          # Test package initialization
├── test_certificate_id.py               # Unit tests for certificate ID generation
├── test_qr_code.py                      # Unit tests for QR code generation
├── test_registry.py                     # Unit tests for certificate registry
├── test_certificate_generation.py       # Unit tests for PPTX generation
├── test_integration.py                  # Integration tests
└── README.md                            # This file
```

## Test Coverage

### 1. Certificate ID Generation Tests (`test_certificate_id.py`)
- ID format validation (12 characters, uppercase, hexadecimal)
- Deterministic generation (same inputs → same ID)
- Uniqueness (different inputs → different IDs)
- Special character handling
- Long name handling

### 2. QR Code Generation Tests (`test_qr_code.py`)
- QR code image creation
- PNG format validation
- Deterministic generation
- Different URLs generate different codes
- Image validity checks

### 3. Certificate Registry Tests (`test_registry.py`)
- Registry creation and loading
- Certificate addition
- Duplicate prevention
- Registry persistence (save/load)
- Unicode character support
- Multiple certificate management

### 4. Certificate Generation Tests (`test_certificate_generation.py`)
- PPTX file creation
- Placeholder text replacement
- QR code embedding
- Registry integration
- Name loading from files
- Duplicate name detection
- Whitespace handling

### 5. Integration Tests (`test_integration.py`)
- Complete workflow (ID → QR → Registry → PPTX)
- Multiple certificate batch generation
- Different certificate types
- Same name, different types
- QR code verification
- Registry persistence across sessions

## Running Tests

### Option 1: Using the Test Runner Script

Run all tests:
```bash
python run_tests.py
```

Run with verbose output:
```bash
python run_tests.py -v
```

Run with coverage report:
```bash
python run_tests.py --coverage
```

### Option 2: Using unittest

Run all tests:
```bash
cd tools/certificate_automation
python -m unittest discover tests
```

Run specific test file:
```bash
python -m unittest tests.test_certificate_id
```

Run specific test class:
```bash
python -m unittest tests.test_certificate_id.TestCertificateID
```

Run specific test method:
```bash
python -m unittest tests.test_certificate_id.TestCertificateID.test_generate_certificate_id_length
```

### Option 3: Using pytest (Recommended)

Install pytest:
```bash
pip install -r requirements-dev.txt
```

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_certificate_id.py
```

Run with verbose output:
```bash
pytest -v
```

## Test Requirements

Install test dependencies:
```bash
pip install -r requirements-dev.txt
```

Or install individually:
```bash
pip install pytest pytest-cov coverage
```

## Writing New Tests

### Test File Naming
- Test files must start with `test_`
- Example: `test_new_feature.py`

### Test Class Naming
- Test classes must start with `Test`
- Example: `class TestNewFeature(unittest.TestCase):`

### Test Method Naming
- Test methods must start with `test_`
- Use descriptive names
- Example: `def test_feature_handles_empty_input(self):`

### Example Test Structure

```python
import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from generate_certificates import your_function


class TestYourFeature(unittest.TestCase):
    """Test cases for your feature."""

    def setUp(self):
        """Set up test fixtures before each test."""
        pass

    def tearDown(self):
        """Clean up after each test."""
        pass

    def test_your_feature_basic_case(self):
        """Test basic functionality."""
        result = your_function("input")
        self.assertEqual(result, "expected_output")

    def test_your_feature_edge_case(self):
        """Test edge case."""
        result = your_function("")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
```

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

### GitHub Actions Example
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd tools/certificate_automation
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          cd tools/certificate_automation
          pytest --cov=src --cov-report=xml
```

## Test Best Practices

1. **Isolation**: Each test should be independent
2. **Clarity**: Use descriptive test names and docstrings
3. **Coverage**: Aim for high code coverage (>80%)
4. **Speed**: Keep tests fast (use mocks for slow operations)
5. **Assertions**: Use specific assertions (assertEqual vs assertTrue)
6. **Setup/Teardown**: Clean up resources after tests
7. **Edge Cases**: Test boundary conditions and error cases

## Coverage Goals

- **Overall Coverage**: > 80%
- **Critical Functions**: > 95%
  - `generate_certificate_id()`
  - `add_to_registry()`
  - `generate_qr_code()`
  - `generate_pptx()`

## Common Issues

### Import Errors
If you get import errors, ensure you're running tests from the correct directory:
```bash
cd tools/certificate_automation
python -m unittest discover tests
```

### Missing Dependencies
Install all test dependencies:
```bash
pip install -r requirements-dev.txt
```

### PowerPoint Tests on Non-Windows
Some PowerPoint-related tests may be skipped on non-Windows systems. This is expected as PowerPoint COM automation requires Windows.

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Add tests for edge cases
4. Update this README if adding new test files
5. Maintain or improve coverage percentage
