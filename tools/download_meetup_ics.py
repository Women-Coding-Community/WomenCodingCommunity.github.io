#!/usr/bin/env python3
"""Download the Meetup iCal feed and save as `tools/files/meetup.ics`.

This script prefers `requests` if available but falls back to the
standard-library `urllib` so it has no hard dependency.
"""
from pathlib import Path
import sys

URL = "https://www.meetup.com/women-coding-community/events/ical/"
OUT_PATH = Path(__file__).parent / "files" / "meetup.ics"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)


def download_with_requests():
    import requests

    headers = {"User-Agent": "wcc-ical-downloader/1.0 (+https://github.com/silkenodwell)"}
    resp = requests.get(URL, headers=headers, stream=True, timeout=30)
    resp.raise_for_status()
    with open(OUT_PATH, "wb") as f:
        for chunk in resp.iter_content(8192):
            if chunk:
                f.write(chunk)
    return resp.headers.get("Content-Type", "")


def download_with_urllib():
    import urllib.request

    req = urllib.request.Request(URL, headers={"User-Agent": "wcc-ical-downloader/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r, open(OUT_PATH, "wb") as f:
        f.write(r.read())
    return r.getheader("Content-Type") or ""


def main():
    try:
        try:
            content_type = download_with_requests()
        except Exception as e:  # fallback to stdlib
            print(f"requests download failed ({e}), falling back to urllib", file=sys.stderr)
            content_type = download_with_urllib()
    except Exception as e:
        print(f"Failed to download iCal: {e}", file=sys.stderr)
        sys.exit(2)

    print(f"Saved iCal to {OUT_PATH} (Content-Type: {content_type})")


if __name__ == "__main__":
    main()
