# WCC Certificate Automation

Automated certificate generation from PowerPoint templates and converting them to PDF format using JSON configuration

> **⚠️ Warning: PDF conversion currently only works on Windows**
> The PDF export functionality uses Microsoft PowerPoint COM automation via `comtypes`, which is only available on Windows. On macOS and Linux, the script will generate PPTX files, but PDF conversion will not work.

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
      "font_name": "Georgia",
      "font_size": 59.5
    }
  ]
}
```

- **type**: Certificate type identifier (e.g., "mentee", "mentor")
- **template**: Path to the PPTX template file
- **names_file**: Path to text file containing names (one per line)
- **pdf_dir**: Output directory for PDF certificates
- **ppt_dir**: Output directory for PPTX certificates
- **placeholder_text**: Text in template to be replaced with names
- **font_name**: Font to use for names
- **font_size**: Font size in points

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

1. **Generates Unique Certificate IDs**: Each certificate gets a unique ID based on the recipient's name, certificate type, and issue date
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

**Important**: The certificate registry file must be committed to the repository and deployed to GitHub Pages for the verification system to work.

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
