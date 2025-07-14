from dataclasses import dataclass
from typing import Dict, Optional
import re
import requests
from bs4 import BeautifulSoup

@dataclass
class TrackingCode:
    code: str
    source: str

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

class TrackingCodeExtractor:
    TRACKING_PATTERNS: Dict[str, re.Pattern] = {
        "Google Analytics (UA)": re.compile(r"UA-\d{4,10}-\d+"),
        "Google Analytics (GA4)": re.compile(r"G-[A-Z0-9]{6,}"),
        "Google Tag Manager": re.compile(r"GTM-[A-Z0-9]+"),
        "Facebook Pixel": re.compile(r"fbq\('init',\s*'(\d{15,})'\)"),
        "Hotjar": re.compile(r"_hjSettings\s*=\s*\{hjid:(\d+)", re.MULTILINE),
        "LinkedIn Insight": re.compile(r"partnerId=(\d{6,})"),
    }

    def __init__(self, url: str):
        self.original_url = url
        self.final_url: Optional[str] = None
        self.html: Optional[str] = None
        self.codes: Dict[str, TrackingCode] = {}

    def fetch(self):
        try:
            response = requests.get(self.original_url, timeout=10, headers=headers)
            response.raise_for_status()
            self.final_url = response.url
            self.html = response.text
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch URL '{self.original_url}': {e}")

    def extract_codes(self):
        if not self.html:
            raise RuntimeError("HTML content is empty. Did you run fetch()?")

        soup = BeautifulSoup(self.html, "html.parser")
        scripts = soup.find_all("script")

        combined_script_text = "\n".join(script.get_text() + (script.get("src") or "") for script in scripts)

        for source, pattern in self.TRACKING_PATTERNS.items():
            matches = pattern.findall(combined_script_text)
            if matches:
                for match in matches:
                    code = match if isinstance(match, str) else match[0]
                    if code not in self.codes:
                        self.codes[code] = TrackingCode(code=code, source=source)

    def get_results(self):
        return list(self.codes.values())
