# Recontrack

Recontrack is a command-line tool and Python library designed to extract tracking codes from websites.  
It follows redirects, downloads the full HTML content, and scans embedded scripts to identify tracking IDs from popular platforms such as Google Analytics, Facebook Pixel, Google Tag Manager, Hotjar, LinkedIn Insight, and others.

---

## Features

- Follow HTTP redirects to get the final page URL  
- Extract tracking codes from HTML and JavaScript  
- Detect multiple popular tracking services using regex patterns  
- Provide a simple CLI for quick usage  
- Python module for integration in your own projects  

---

## Installation

### Using `virtualenv` (recommended)

1. Install `virtualenv` if necessary:

```bash
pip install virtualenv
````

2. Create and activate a new virtual environment:

```bash
virtualenv recontrack-env
source recontrack-env/bin/activate
```

3. Install Recontrack locally (run this command in the project root where `setup.py` is located):

```bash
pip install -r requirements.txt
```

This installs the package in editable mode.

---

## Usage

### Command-line Interface (CLI)

After installation, use the `recontrack` command:

```bash
python3 recontrack/cli.py <url>
```

Example:

```bash
python3 recontrack/cli.py https://example.com
```

Sample output:

```
Fetching content from: https://example.com
Final URL after redirects: https://www.example.com
Found Tracking Codes:
 - Google Analytics (UA): UA-12345678-1
 - Facebook Pixel: 123456789012345
```

For help:

```bash
python3 recontrack/cli.py -h
```

---

### Python Module

You can also use Recontrack programmatically:

Add to your `requirements.txt`:

```bash
# requirements.txt
git+https://github.com/reconurge/recontrack.git
```

Or install using python:

```bash
pip install git+https://github.com/reconurge/recontrack.git
```

Import as a module.

```python
from recontrack import TrackingCodeExtractor

extractor = TrackingCodeExtractor("https://example.com")
extractor.fetch()
extractor.extract_codes()
results = extractor.get_results()

for tracking in results:
    print(f"{tracking.source}: {tracking.code}")
```

---

## Dependencies

* Python 3.6+
* requests
* beautifulsoup4

These dependencies are automatically installed via `pip` when you install the package.

---

## Development

* Core code is in the `recontrack/` package
* CLI script is in `recontrack/cli.py`
* Tests can be added in a `tests/` folder

---

## License

[MIT License](https://github.com/reconurge/recontrack/blob/main/LICENSE).