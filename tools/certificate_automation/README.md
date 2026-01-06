# WCC Certificate Automation

Automated certificate generation from PowerPoint templates and converting them to PDF format using JSON configuration

> **⚠️ Warning: PDF conversion currently only works on Windows**
> The PDF export functionality uses Microsoft PowerPoint COM automation via `comtypes`, which is only available on
> Windows. On macOS and Linux, the script will generate PPTX files, but PDF conversion will not work.

## Prerequisites

- Python 3.7 or higher
- Microsoft PowerPoint (required for PDF conversion on Windows)

## Installation

Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

#### Dependencies

- `python-pptx>=0.6.21`: PowerPoint file manipulation
- `comtypes>=1.1.14`: COM automation for PowerPoint
- `qrcode>=7.4.2`: QR code generation for certificate verification
- `pillow>=10.0.0`: Image processing for QR codes

## Project Structure

```
wcc_certificate_automation/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── src/
│   ├── config.json                   # Main configuration file
│   └── generate_certificates.py      # Main automation script
└── data/
    ├── input/
    │   ├── templates/                # PPTX template files
    │   │   ├── mentee.pptx
    │   │   └── mentor.pptx
    │   └── names/                    # Names text files
    │       ├── mentees.txt
    │       └── mentors.txt
    └── output/                        # Generated certificates
        ├── ppts/                      # Generated PPTX files
        │   ├── mentee/
        │   └── mentor/
        └── pdfs/                      # Generated PDF files
            ├── mentee/
            └── mentor/
```

## Configuration

Edit `src/config.json` to customize certificate generation settings.

### Config File

```json
{
  "certificate_types": [
    {
      "type": "mentee",
      "template": "../data/input/templates/mentee.pptx",
      "names_file": "../data/input/names/mentees.txt",
      "pdf_dir": "../data/output/pdfs/mentee/",
      "ppt_dir": "../data/output/ppts/mentee/",
      "placeholder_text": "Sample Sample",
      "qr_left_cm": 47.8,
      "qr_top_cm": 28.91,
      "qr_width_cm": 3.0,
      "qr_height_cm": 3.0
    }
  ]
}
```

#### Required Parameters

- **type**: Certificate type identifier (e.g., "mentee", "mentor", "volunteer", "leader")
- **template**: Path to the PPTX template file
- **names_file**: Path to text file containing names (one per line)
- **pdf_dir**: Output directory for PDF certificates
- **ppt_dir**: Output directory for PPTX certificates
- **placeholder_text**: Text in template to be replaced with names

#### Optional Parameters (QR Code Position)

- **qr_left_cm**: Distance from left edge in centimeters (e.g., 47.8)
- **qr_top_cm**: Distance from top edge in centimeters (e.g., 28.91)
- **qr_width_cm**: QR code width in centimeters (default: 3.0)
- **qr_height_cm**: QR code height in centimeters (default: 3.0)

**Note**: If QR position parameters are not specified, the QR code will be placed in the top-right corner by default.

#### Text Formatting

All text formatting (font name, font size, color, bold, italic, underline) is **automatically preserved** from the
placeholder text in your PowerPoint template. Simply style the placeholder text ("Sample Sample") in your template
exactly how you want the names to appear, and the script will apply the same formatting to each person's name.

### Names Files

Create text files in `data/input/names/` with one name per line:

**Example** (`data/input/names/mentees.txt`):

```
John Smith
Jane Doe
Alice Johnson
```

### Template Files

Create PPTX template files in `data/input/templates/` with text placeholder:

**Example** (`data/input/templates/mentee.pptx`):

## Usage

Navigate to the `src` directory and run the main script:

```bash
cd src
python generate_certificates.py
```

The script will automatically:

1. Check for duplicate names in the input files
2. Generate PPTX certificates for each person
3. Verify all PPTX certificates were created
4. Convert all PPTX certificates to PDF format
5. Verify all PDF certificates were created
6. Display summary statistics

## Output Format

Generated certificate files are named using the person's name directly:

- PPTX: `data/output/ppts/mentee/John Smith.pptx`
- PDF: `data/output/pdfs/mentee/John Smith.pdf`

## QR Code Verification

Each generated certificate includes a QR code for verification purposes. The system automatically:

1. **Generates Unique Certificate IDs**: Each certificate gets a unique ID based on the recipient's name, certificate
   type, and issue date
2. **Embeds QR Codes**: QR codes are automatically added to the bottom-right corner of each certificate
3. **Maintains Certificate Registry**: All issued certificates are recorded in `data/output/certificate_registry.json`
4. **Provides Verification Page**: Recipients can verify certificates at `https://www.womencodingcommunity.com/verify`

### How Verification Works

1. **For Recipients**: Scan the QR code on your certificate or visit the verification page and enter your certificate ID
2. **For Verifiers**: The verification page checks the certificate against the official registry and displays:
    - Certificate ID
    - Recipient name
    - Certificate type
    - Issue date
    - Validation status

### Certificate Registry

The certificate registry (`data/output/certificate_registry.json`) contains all issued certificates:

```json
{
  "certificates": [
    {
      "id": "ABC123DEF456",
      "name": "John Smith",
      "type": "mentee",
      "issue_date": "2026-01-04",
      "verification_url": "https://www.womencodingcommunity.com/verify?cert=ABC123DEF456"
    }
  ]
}
```

**Important**: The certificate registry file must be committed to the repository and deployed to GitHub Pages for the
verification system to work.

### Publishing Certificates for Web Verification

After generating certificates, you need to publish the certificate registry to make it available on the website:

1. **Generated Registry Location**: `tools/certificate_automation/data/output/certificate_registry.json`
2. **Published Registry Location**: `assets/js/certificates_registry.json`

#### Option 1: Manual Copy (First Time)

If this is your first batch of certificates:

```bash
cp tools/certificate_automation/data/output/certificate_registry.json assets/js/certificates_registry.json
git add assets/js/certificates_registry.json
git commit -m "Add certificate registry for verification"
git push
```

#### Option 2: Append New Certificates (Recommended)

If you already have certificates published and want to add new ones:

```bash
python3 tools/certificate_automation/scripts/publish_registry.py
```

The script will:
- Read the existing `assets/js/certificates_registry.json`
- Read the newly generated `tools/certificate_automation/data/output/certificate_registry.json`
- Merge certificates, avoiding duplicates (by certificate ID)
- Save the merged result to `assets/js/certificates_registry.json`

Then commit and push:

```bash
git add assets/js/certificates_registry.json
git commit -m "Add new certificates to registry"
git push
```

**Note**: The `tools/` directory is for generation only and can be deleted/recreated. The `assets/js/certificates_registry.json` file is served by the website.

## Sample Logs

```
Generating MENTEE mentee certificates at ../data/output/ppts/mentee/
[1/68] Generated: ../data/output/ppts/mentee/John Smith.pptx
[2/68] Generated: ../data/output/ppts/mentee/Jane Doe.pptx
...

Successfully generated 68/68 mentee certificates

Checking metrics MENTEE certificates

Expected certificates: 68
Found certificates: 68

All mentee certificates are present!

Generating MENTEE mentee certificates at ../data/output/pdfs/mentee/
[1/68] Generated: ../data/output/pdfs/mentee/John Smith.pdf
...

Type: mentee Total: 68 PPTX Generated: 68 PDF Generated: 68

Certificate registry saved with 68 total certificates
```
