# Recontrack

**Recontrack** is a CLI tool that extracts tracking codes from websites. It follows redirects, fetches full HTML content, and scans embedded scripts to identify tracking IDs from popular platforms like Google Analytics, Facebook Pixel, Hotjar, Google Tag Manager, LinkedIn Insight, and more.

---

## Features

- Follows HTTP redirects to get the final URL
- Parses HTML and script tags for common tracking codes
- Supports major tracking services with regex-based detection
- Easy-to-use command-line interface

---

## Installation

It’s recommended to use a **virtualenv** to isolate dependencies:

```bash
# 1. Install virtualenv if you don’t have it yet
pip install virtualenv
```

```bash
# 2. Create a new virtual environment named "recontrack-env"
virtualenv recontrack-env
```

```bash
# 4. Install required dependencies
pip install -r requirements.txt
```

## Usage
Run the tool from the command line, providing the URL you want to analyze:

```bash
python main.py https://example.com
#> 🔗 Fetching content from: https://example.com
#> ↪️ Final URL after redirects: https://www.example.com
#> 🔍 Found Tracking Codes:
#>  - Google Analytics (UA): UA-12345678-1
#>  - Facebook Pixel: 123456789012345
```