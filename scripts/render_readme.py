#!/usr/bin/env python3
"""Render a local README preview for desktop and mobile browser checks."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

import markdown


CSS = """
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--canvas); color: var(--fg); font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
.markdown-body { width: min(1012px, 100%); margin: 0 auto; padding: 32px; overflow-wrap: anywhere; }
h1, h2 { border-bottom: 1px solid var(--border); padding-bottom: .3em; }
img, svg, video { max-width: 100%; height: auto; }
table { display: block; width: max-content; max-width: 100%; overflow-x: auto; border-collapse: collapse; }
th, td { border: 1px solid var(--border); padding: 6px 13px; }
pre { max-width: 100%; overflow-x: auto; padding: 16px; background: var(--muted); border-radius: 6px; }
code { background: var(--muted); border-radius: 4px; padding: .15em .35em; }
pre code { padding: 0; }
body.light { --canvas: #ffffff; --fg: #1f2328; --muted: #f6f8fa; --border: #d0d7de; }
body.dark { --canvas: #0d1117; --fg: #e6edf3; --muted: #161b22; --border: #30363d; }
@media (max-width: 480px) { .markdown-body { padding: 16px; } }
"""


def render(readme: Path, output: Path, theme: str) -> dict[str, object]:
    source = readme.read_text(encoding="utf-8")
    body = markdown.markdown(
        source,
        extensions=["extra", "fenced_code", "tables", "sane_lists"],
        output_format="html5",
    )
    title = html.escape(readme.name)
    document = (
        "<!doctype html><html><head><meta charset=\"utf-8\">"
        f"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><base href=\"{readme.parent.resolve().as_uri()}/\"><title>{title}</title>"
        f"<style>{CSS}</style></head><body class=\"{theme}\"><main class=\"markdown-body\">{body}</main></body></html>"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8", newline="\n")
    return {
        "readme": readme.name,
        "theme": theme,
        "output": output.name,
        "tables": source.count("\n|---"),
        "images": source.count("<img ") + source.count("!["),
        "mermaid_blocks": source.count("```mermaid"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("readme", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    records = []
    for theme in ("light", "dark"):
        target = args.output_dir / f"{args.readme.stem}.{theme}.html"
        records.append(render(args.readme.resolve(), target.resolve(), theme))
    print(json.dumps({"status": "PASS", "renders": records}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
