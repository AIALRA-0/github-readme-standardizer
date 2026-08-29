#!/usr/bin/env python3
"""Exercise the README auditor with passing and failing repositories."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from audit_readme import audit_repository


GOOD_ZH = """<div align=\"center\"><h1>示例项目</h1></div>

![示例界面](docs/hero.svg)

## 1 项目价值

[快速开始](#2-快速开始)

## 2 快速开始

| 能力 | 状态 |
|---|---|
| 本地运行 | 已验证 |

```text
# 代码块中的井号不是 README 标题
```
"""

GOOD_EN = """<div align=\"center\"><h1>Example Project</h1></div>

![Example interface](docs/hero.svg)

## 1 Project value

[Quick start](#2-quick-start)

## 2 Quick start

| Capability | Status |
|---|---|
| Local runtime | Verified |

```text
# A hash inside a code fence is not a README heading
```
"""


def synthetic_private_ipv4(*octets: int) -> str:
    """Build a private-address fixture without publishing a reusable address literal."""
    return ".".join(str(octet) for octet in octets)


def synthetic_aws_key() -> str:
    """Build a credential-shaped fixture without storing the complete value in source."""
    return "".join(("AK", "IA", "1234567890", "ABCDEF"))


def synthetic_credential_url(host_label: str, top_level_domain: str) -> str:
    """Build a user-info URL fixture without storing a complete credential URL in source."""
    host = ".".join((host_label, top_level_domain))
    user_info = ":".join(("synthetic-user", "synthetic-pass"))
    return "".join(("https://", user_info, "@", host, "/path"))


def synthetic_windows_user_path() -> str:
    """Build a user-directory path without storing a host-specific path literal."""

    return "".join(("C", ":", "\\", "Users", "\\", "synthetic-user", "\\", "project"))


class AuditReadmeTests(unittest.TestCase):
    """Verify observable pass and fail behavior."""

    def test_valid_bilingual_repository_passes(self) -> None:
        # Build a minimal bilingual repository with one local visual asset.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")

            result = audit_repository(root)

        self.assertEqual("PASS", result["status"])
        self.assertEqual(0, result["summary"]["error_count"])
        self.assertNotIn(1, result["readmes"][0]["heading_levels"])
        self.assertEqual(1, result["readmes"][0]["tables"])

    def test_every_h1_must_be_centered(self) -> None:
        # Reject Markdown H1 and uncentered HTML H1 while accepting direct or container alignment.
        cases = (
            ("# 示例项目", "# Example Project", False),
            ("<h1>示例项目</h1>", "<h1>Example Project</h1>", False),
            ('<h1 align="center">示例项目</h1>', '<h1 align="center">Example Project</h1>', True),
            ('<div align="center"><h1>示例项目</h1></div>', '<div align="center"><h1>Example Project</h1></div>', True),
        )
        for zh_title, en_title, should_pass in cases:
            with self.subTest(zh_title=zh_title, should_pass=should_pass), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                (root / "docs").mkdir()
                (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
                (root / "README.md").write_text(GOOD_ZH.replace('<div align="center"><h1>示例项目</h1></div>', zh_title), encoding="utf-8")
                (root / "README.en.md").write_text(GOOD_EN.replace('<div align="center"><h1>Example Project</h1></div>', en_title), encoding="utf-8")

                result = audit_repository(root)

            codes = {item["code"] for item in result["errors"]}
            self.assertEqual(should_pass, "H1_NOT_CENTERED" not in codes)

    def test_mermaid_direction_and_decorative_numbering_are_hard_errors(self) -> None:
        # Reject horizontal or implicit flowcharts and decorative numbering without blocking ordinary digits.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            invalid = "\n\n① 启动\n\n```mermaid\nflowchart LR\nA --> B\n```\n"
            (root / "README.md").write_text(GOOD_ZH + invalid, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN + invalid, encoding="utf-8")

            result = audit_repository(root)

        codes = {item["code"] for item in result["errors"]}
        self.assertEqual("FAIL", result["status"])
        self.assertIn("MERMAID_DIRECTION", codes)
        self.assertIn("DECORATIVE_NUMBERING", codes)

    def test_vertical_mermaid_and_decimal_numbers_pass(self) -> None:
        # Preserve ordinary versions and decimal headings while accepting both vertical direction aliases.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            diagram = "\n\nVersion 2.1\n\n```mermaid\ngraph TB\nA --> B\n```\n"
            (root / "README.md").write_text(GOOD_ZH + diagram, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN + diagram, encoding="utf-8")

            result = audit_repository(root)

        self.assertEqual("PASS", result["status"])

    def test_sensitive_and_missing_content_fail(self) -> None:
        # Include multiple independent failures and confirm the scanner returns codes without secret text.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixture_value = synthetic_aws_key()
            private_address = synthetic_private_ipv4(10, 1, 2, 3)
            (root / "README.md").write_text(
                f"# 示例\n\n![缺失图片](missing.png)\n\n## 1 启动\n\n{fixture_value}\n\n{private_address}\n",
                encoding="utf-8",
            )

            result = audit_repository(root)
            serialized = str(result)

        codes = {item["code"] for item in result["errors"]}
        self.assertEqual("FAIL", result["status"])
        self.assertIn("MISSING_README", codes)
        self.assertIn("MISSING_IMAGE", codes)
        self.assertIn("AWS_ACCESS_KEY", codes)
        self.assertIn("PRIVATE_IPV4", codes)
        self.assertNotIn(fixture_value, serialized)

    def test_explicit_html_anchors_pass(self) -> None:
        # Allow stable page links to target a sanitized HTML anchor placed before a numbered heading.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            zh = GOOD_ZH.replace("[快速开始](#2-快速开始)", "[快速开始](#quick-start)").replace(
                "## 2 快速开始", '<a id="quick-start"></a>\n\n## 2 快速开始'
            )
            en = GOOD_EN.replace("[Quick start](#2-quick-start)", "[Quick start](#quick-start)").replace(
                "## 2 Quick start", '<a name="quick-start"></a>\n\n## 2 Quick start'
            )
            (root / "README.md").write_text(zh, encoding="utf-8")
            (root / "README.en.md").write_text(en, encoding="utf-8")

            result = audit_repository(root)

        self.assertEqual("PASS", result["status"])
        self.assertNotIn("BROKEN_ANCHOR", {item["code"] for item in result["errors"]})

    def test_default_scope_ignores_unreferenced_test_fixture(self) -> None:
        # Keep source-code fixtures outside the README publication scan unless full-repository mode is requested.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "server").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")
            synthetic_secret = "sk-" + ("A" * 48)
            (root / "server" / "fixture.txt").write_text(synthetic_secret, encoding="utf-8")

            default_result = audit_repository(root)
            full_result = audit_repository(root, scan_repository=True)

        self.assertEqual("PASS", default_result["status"])
        self.assertEqual("FAIL", full_result["status"])
        self.assertIn("OPENAI_API_KEY", {item["code"] for item in full_result["errors"]})

    def test_full_scope_preserves_long_skill_identifiers(self) -> None:
        # Domain identifiers can start with sk- but remain readable lowercase slugs rather than high-entropy credentials.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "server").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")
            (root / "server" / "skills.txt").write_text(
                "sk-physical-design-setup-analysis\nsk-design-verification-scoreboard",
                encoding="utf-8",
            )

            result = audit_repository(root, scan_repository=True)

        self.assertEqual("PASS", result["status"])
        self.assertNotIn("OPENAI_API_KEY", {item["code"] for item in result["errors"]})

    def test_full_scope_skips_generated_framework_directories(self) -> None:
        # Generated dependency trees can contain unreadable cross-platform links and must stay outside publication scans.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / ".next" / "standalone").mkdir(parents=True)
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")
            synthetic_secret = "sk-" + ("B" * 48)
            (root / ".next" / "standalone" / "generated.txt").write_text(synthetic_secret, encoding="utf-8")

            result = audit_repository(root, scan_repository=True)

        self.assertEqual("PASS", result["status"])
        self.assertNotIn("OPENAI_API_KEY", {item["code"] for item in result["errors"]})

    def test_full_scope_scans_hardware_design_files(self) -> None:
        # HDL, constraints, and memory fixtures can leak the same values as application source files.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "src").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")
            private_address = synthetic_private_ipv4(10, 20, 30, 40)
            (root / "src" / "design.v").write_text(
                f"// synthetic fixture {private_address}\nmodule design; endmodule\n",
                encoding="utf-8",
            )

            result = audit_repository(root, scan_repository=True)

        self.assertEqual("FAIL", result["status"])
        self.assertIn("PRIVATE_IPV4", {item["code"] for item in result["errors"]})

    def test_reserved_credential_url_fixture_does_not_hide_real_hosts(self) -> None:
        # Negative security tests may use reserved hosts, while user-info URLs on other hosts must still fail.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "tests").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")
            (root / "tests" / "reserved.txt").write_text(
                synthetic_credential_url("workflow", "example"),
                encoding="utf-8",
            )

            reserved_result = audit_repository(root, scan_repository=True)
            (root / "tests" / "real-host.txt").write_text(
                synthetic_credential_url("workflow", "internal"),
                encoding="utf-8",
            )
            real_host_result = audit_repository(root, scan_repository=True)

        self.assertEqual("PASS", reserved_result["status"])
        self.assertEqual("FAIL", real_host_result["status"])
        self.assertIn("CREDENTIAL_URL", {item["code"] for item in real_host_result["errors"]})

    def test_referenced_image_format_mismatch_warns(self) -> None:
        # Use a JPEG signature behind a PNG name and confirm the publication audit reports the mismatch.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.png").write_bytes(b"\xff\xd8\xff\xe0synthetic-jpeg")
            zh = GOOD_ZH.replace("hero.svg", "hero.png")
            en = GOOD_EN.replace("hero.svg", "hero.png")
            (root / "README.md").write_text(zh, encoding="utf-8")
            (root / "README.en.md").write_text(en, encoding="utf-8")

            result = audit_repository(root)

        self.assertEqual("PASS", result["status"])
        self.assertIn("IMAGE_FORMAT_MISMATCH", {item["code"] for item in result["warnings"]})

    def test_exact_private_ipv4_allowlist_passes_and_reports_usage(self) -> None:
        # Preserve a required upstream example only when path, digest and occurrence count all match.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "assets").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")
            matched_value = synthetic_private_ipv4(192, 168, 1, 0)
            (root / "assets" / "upstream.json").write_text(
                json.dumps({"source": matched_value, "fallback": matched_value}),
                encoding="utf-8",
            )

            without_allowlist = audit_repository(root, scan_repository=True)
            (root / ".readme-audit-allowlist.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "entries": [
                            {
                                "code": "PRIVATE_IPV4",
                                "path": "assets/upstream.json",
                                "match_sha256": hashlib.sha256(matched_value.encode("utf-8")).hexdigest(),
                                "occurrences": 2,
                                "reason": "Required upstream documentation fixture preserved for exact runtime matching",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            with_allowlist = audit_repository(root, scan_repository=True)

        self.assertEqual("FAIL", without_allowlist["status"])
        self.assertEqual("PASS", with_allowlist["status"])
        self.assertEqual(1, with_allowlist["summary"]["allowlist_entries"])
        self.assertEqual(2, with_allowlist["summary"]["allowlisted_matches"])
        self.assertIn("SENSITIVE_ALLOWLIST_APPLIED", {item["code"] for item in with_allowlist["warnings"]})

    def test_allowlist_occurrence_drift_fails(self) -> None:
        # Treat a stale expected count as a hard failure so new or removed matches require review.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "assets").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")
            matched_value = synthetic_private_ipv4(10, 20, 30, 40)
            (root / "assets" / "upstream.json").write_text(json.dumps({"source": matched_value}), encoding="utf-8")
            (root / ".readme-audit-allowlist.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "entries": [
                            {
                                "code": "PRIVATE_IPV4",
                                "path": "assets/upstream.json",
                                "match_sha256": hashlib.sha256(matched_value.encode("utf-8")).hexdigest(),
                                "occurrences": 2,
                                "reason": "Required upstream documentation fixture preserved for exact runtime matching",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = audit_repository(root, scan_repository=True)

        self.assertEqual("FAIL", result["status"])
        self.assertIn("ALLOWLIST_COUNT_MISMATCH", {item["code"] for item in result["errors"]})

    def test_safe_svg_has_stable_size_and_accessible_name(self) -> None:
        # Accept a static local SVG with a scalable canvas, accessible title, and local paint reference.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 50">'
                '<title>Validated workflow</title><defs><linearGradient id="g"/></defs>'
                '<rect width="100" height="50" fill="url(#g)"/></svg>',
                encoding="utf-8",
            )
            (root / "README.md").write_text(GOOD_ZH, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")

            result = audit_repository(root)

        self.assertEqual("PASS", result["status"])
        self.assertEqual(1, result["summary"]["vector_images_scanned"])
        self.assertNotIn("SVG_UNSTABLE_SIZE", {item["code"] for item in result["warnings"]})

    def test_svg_active_content_and_external_reference_fail(self) -> None:
        # Block scripts, event handlers, and remote image loads inside a referenced vector asset.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            external = "".join(("https", "://", "assets", ".example", "/pixel.png"))
            (root / "docs" / "hero.svg").write_text(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50" onload="run()">'
                f'<title>Unsafe fixture</title><script>run()</script><image href="{external}"/></svg>',
                encoding="utf-8",
            )
            (root / "README.md").write_text(GOOD_ZH, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")

            result = audit_repository(root)

        codes = {item["code"] for item in result["errors"]}
        self.assertEqual("FAIL", result["status"])
        self.assertIn("SVG_ACTIVE_CONTENT", codes)
        self.assertIn("SVG_EVENT_HANDLER", codes)
        self.assertIn("SVG_EXTERNAL_REFERENCE", codes)

    def test_malformed_svg_fails(self) -> None:
        # Treat a truncated vector as a hard error because browsers may render it inconsistently.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"><title>Broken', encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")

            result = audit_repository(root)

        self.assertEqual("FAIL", result["status"])
        self.assertIn("MALFORMED_SVG", {item["code"] for item in result["errors"]})

    def test_png_text_metadata_warns(self) -> None:
        # Detect PNG textual chunks that may retain author, software, prompt, or source-path details.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            signature = b"\x89PNG\r\n\x1a\n"
            text_chunk = (0).to_bytes(4, "big") + b"tEXt" + b"\x00\x00\x00\x00"
            end_chunk = (0).to_bytes(4, "big") + b"IEND" + b"\x00\x00\x00\x00"
            (root / "docs" / "hero.png").write_bytes(signature + text_chunk + end_chunk)
            (root / "README.md").write_text(GOOD_ZH.replace("hero.svg", "hero.png"), encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN.replace("hero.svg", "hero.png"), encoding="utf-8")

            result = audit_repository(root)

        self.assertEqual("FAIL", result["status"])
        self.assertIn("IMAGE_METADATA", {item["code"] for item in result["errors"]})

    def test_local_user_directory_path_fails_without_echoing_value(self) -> None:
        # Detect host-specific user directories and keep the matched value out of the result.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            local_path = synthetic_windows_user_path()
            (root / "README.md").write_text(GOOD_ZH + "\n" + local_path, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")

            result = audit_repository(root)
            serialized = str(result)

        self.assertEqual("FAIL", result["status"])
        self.assertIn("WINDOWS_USER_PATH", {item["code"] for item in result["errors"]})
        self.assertNotIn(local_path, serialized)


if __name__ == "__main__":
    unittest.main()
