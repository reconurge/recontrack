from dataclasses import dataclass
from typing import Dict, Optional
import re
import requests
from bs4 import BeautifulSoup
import argparse


@dataclass
class TrackingCode:
    code: str
    source: str


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
            response = requests.get(self.original_url, timeout=10)
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

        combined_script_text = "\n".join(script.get_text() + str(script.get("src")) for script in scripts)

        for source, pattern in self.TRACKING_PATTERNS.items():
            matches = pattern.findall(combined_script_text)
            if matches:
                for match in matches:
                    code = match if isinstance(match, str) else match[0]
                    if code not in self.codes:
                        self.codes[code] = TrackingCode(code=code, source=source)

    def get_results(self):
        return list(self.codes.values())


def cli():
    parser = argparse.ArgumentParser(description="Extract tracking codes from a website.")
    parser.add_argument("url", help="URL of the website to analyze")
    args = parser.parse_args()

    extractor = TrackingCodeExtractor(args.url)
    try:
        print(f"🔗 Fetching content from: {args.url}")
        extractor.fetch()
        print(f"↪️ Final URL after redirects: {extractor.final_url}")
        extractor.extract_codes()

        results = extractor.get_results()
        if results:
            print("\n🔍 Found Tracking Codes:")
            for tracking in results:
                print(f" - {tracking.source}: {tracking.code}")
        else:
            print("\n✅ No tracking codes found.")
    except RuntimeError as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    cli()
