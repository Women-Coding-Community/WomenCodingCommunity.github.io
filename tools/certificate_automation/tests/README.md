# WCC Certificate Automation - Test Suite

Comprehensive test suite for the Women Coding Community certificate automation system, including QR code verification
functionality.

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