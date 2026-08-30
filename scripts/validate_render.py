#!/usr/bin/env python3
"""Validate local README previews in desktop and mobile Chrome viewports."""

from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


VIEWPORTS = {"desktop": (1280, 900), "mobile": (390, 844)}


def find_chrome() -> str:
    configured = os.environ.get("README_CHROME_BINARY")
    if configured and Path(configured).is_file():
        return configured
    for name in ("chrome", "google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    for root_name in ("PROGRAMFILES", "PROGRAMFILES(X86)"):
        root = os.environ.get(root_name)
        if not root:
            continue
        candidate = Path(root) / "Google" / "Chrome" / "Application" / "chrome.exe"
        if candidate.is_file():
            return str(candidate)
    raise RuntimeError("Chrome was not found; set README_CHROME_BINARY to the browser executable")


def inspect(driver: webdriver.Chrome, page: Path, width: int, height: int) -> dict[str, object]:
    driver.execute_cdp_cmd(
        "Emulation.setDeviceMetricsOverride",
        {"width": width, "height": height, "deviceScaleFactor": 1, "mobile": width <= 480},
    )
    driver.get(page.resolve().as_uri())
    data = driver.execute_script(
        """
        const root = document.documentElement;
        const images = [...document.images];
        const h1 = document.querySelector('h1');
        return {
          innerWidth: window.innerWidth,
          scrollWidth: root.scrollWidth,
          imageCount: images.length,
          unloadedImages: images.filter(image => !image.complete || image.naturalWidth === 0).length,
          h1Found: Boolean(h1),
          h1TextAlign: h1 ? getComputedStyle(h1).textAlign : null
        };
        """
    )
    data["page"] = page.name
    data["viewport"] = width
    data["overflow"] = data["scrollWidth"] > data["innerWidth"]
    data["passed"] = (
        not data["overflow"]
        and data["unloadedImages"] == 0
        and data["h1Found"]
        and data["h1TextAlign"] in {"center", "-webkit-center"}
    )
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pages", nargs="+", type=Path)
    args = parser.parse_args()

    options = Options()
    options.binary_location = find_chrome()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--allow-file-access-from-files")

    pages = [Path(match) for pattern in args.pages for match in glob.glob(str(pattern))]
    if not pages:
        parser.error("no preview pages matched the supplied paths")

    records: list[dict[str, object]] = []
    with webdriver.Chrome(options=options) as driver:
        for page in pages:
            for width, height in VIEWPORTS.values():
                records.append(inspect(driver, page, width, height))

    passed = all(record["passed"] for record in records)
    print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": records}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
