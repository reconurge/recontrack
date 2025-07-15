import argparse
import sys
import os
# Add parent directory to path when run as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from recontrack import TrackingCodeExtractor

def cli():
    parser = argparse.ArgumentParser(description="Extract tracking codes from a website.")
    parser.add_argument("url", help="URL of the website to analyze")
    args = parser.parse_args()

    extractor = TrackingCodeExtractor(args.url)
    try:
        print(f"Fetching content from: {args.url}")
        extractor.fetch()
        print(f"Final URL after redirects: {extractor.final_url}")
        extractor.extract_codes()

        results = extractor.get_results()
        if results:
            print("\nFound Tracking Codes:")
            for tracking in results:
                print(f" - {tracking.source}: {tracking.code}")
        else:
            print("\nNo tracking codes found.")
    except RuntimeError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    cli()
