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

## 1. 项目价值

[快速开始](#2-快速开始)

## 2. 快速开始

| 能力 | 状态 |
|---|---|
| 本地运行 | 已验证 |

```text
# 代码块中的井号不是 README 标题
```
"""

GOOD_EN = """<div align=\"center\"><h1>Example Project</h1></div>

![Example interface](docs/hero.svg)

## 1. Project value

[Quick start](#2-quick-start)

## 2. Quick start

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

    def test_decimal_heading_format_and_depth(self) -> None:
        # Require a trailing dot and the same number depth as the Markdown heading level.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            invalid_zh = GOOD_ZH.replace("## 2. 快速开始", "## 2 快速开始\n\n### 2.1.1. 层级错误")
            invalid_en = GOOD_EN.replace("## 2. Quick start", "## 2 Quick start\n\n### 2.1.1. Wrong depth")
            (root / "README.md").write_text(invalid_zh, encoding="utf-8")
            (root / "README.en.md").write_text(invalid_en, encoding="utf-8")

            result = audit_repository(root)

        self.assertEqual("FAIL", result["status"])
        self.assertIn("SECTION_NUMBER_FORMAT", {item["code"] for item in result["errors"]})

    def test_decimal_heading_three_levels_pass(self) -> None:
        # Accept dotted decimal numbering when every number depth matches its Markdown heading level.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            zh = GOOD_ZH + "\n### 2.1. 验证范围\n\n#### 2.1.1. 输入边界\n"
            en = GOOD_EN + "\n### 2.1. Validation scope\n\n#### 2.1.1. Input boundary\n"
            (root / "README.md").write_text(zh, encoding="utf-8")
            (root / "README.en.md").write_text(en, encoding="utf-8")

            result = audit_repository(root)

        self.assertEqual("PASS", result["status"])
        self.assertNotIn("SECTION_NUMBER_FORMAT", {item["code"] for item in result["errors"]})

    def test_default_caption_below_and_ieee_table_exception(self) -> None:
        # Keep ordinary captions below every object while allowing IEEE table captions above.
        table = "| 能力 | 状态 |\n|---|---|\n| 本地运行 | 已验证 |"
        table_en = "| Capability | Status |\n|---|---|\n| Local runtime | Verified |"
        below_zh = GOOD_ZH.replace(table, table + "\n\n表 2.1 验证结果")
        below_en = GOOD_EN.replace(table_en, table_en + "\n\nTable 2.1. Validation result")
        above_zh = GOOD_ZH.replace(table, "表 2.1 验证结果\n\n" + table)
        above_en = GOOD_EN.replace(table_en, "Table 2.1. Validation result\n\n" + table_en)

        def run(zh: str, en: str, standard: str = "default") -> dict[str, object]:
            with tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                (root / "docs").mkdir()
                (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
                (root / "README.md").write_text(zh, encoding="utf-8")
                (root / "README.en.md").write_text(en, encoding="utf-8")
                return audit_repository(root, publication_standard=standard)

        self.assertNotIn("CAPTION_POSITION", {item["code"] for item in run(below_zh, below_en)["errors"]})
        self.assertIn("CAPTION_POSITION", {item["code"] for item in run(above_zh, above_en)["errors"]})
        self.assertNotIn("CAPTION_POSITION", {item["code"] for item in run(above_zh, above_en, "ieee")["errors"]})
        self.assertIn("IEEE_TABLE_CAPTION_POSITION", {item["code"] for item in run(below_zh, below_en, "ieee")["errors"]})

    def test_figure_and_mermaid_captions_stay_below_in_default_and_ieee_modes(self) -> None:
        # Keep image and Mermaid captions below their objects even when the IEEE table exception is active.
        image_zh = "![示例界面](docs/hero.svg)"
        image_en = "![Example interface](docs/hero.svg)"
        diagram = "```mermaid\nflowchart TD\nA[读取] --> B[检查]\nB --> C[输出]\n```"
        below_zh = GOOD_ZH.replace(image_zh, image_zh + "\n\n图 1.1 示例界面") + "\n\n" + diagram + "\n\n图 2.1 验证流程\n"
        below_en = GOOD_EN.replace(image_en, image_en + "\n\nFigure 1.1. Example interface") + "\n\n" + diagram + "\n\nFigure 2.1. Validation flow\n"
        above_zh = GOOD_ZH.replace(image_zh, "图 1.1 示例界面\n\n" + image_zh) + "\n\n图 2.1 验证流程\n\n" + diagram + "\n"
        above_en = GOOD_EN.replace(image_en, "Figure 1.1. Example interface\n\n" + image_en) + "\n\nFigure 2.1. Validation flow\n\n" + diagram + "\n"

        def run(zh: str, en: str, standard: str) -> dict[str, object]:
            with tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                (root / "docs").mkdir()
                (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
                (root / "README.md").write_text(zh, encoding="utf-8")
                (root / "README.en.md").write_text(en, encoding="utf-8")
                return audit_repository(root, publication_standard=standard)

        for standard in ("default", "ieee"):
            self.assertNotIn("CAPTION_POSITION", {item["code"] for item in run(below_zh, below_en, standard)["errors"]})
            self.assertIn("CAPTION_POSITION", {item["code"] for item in run(above_zh, above_en, standard)["errors"]})

    def test_figure_caption_before_table_is_not_a_table_caption(self) -> None:
        # A figure caption can sit between a Mermaid block and the next table without becoming that table's caption.
        diagram_and_table = "\n\n```mermaid\nflowchart TD\nA[读取] --> B[检查]\nB --> C[输出]\n```\n\n图 2.1 验证流程\n\n| 项目 | 结果 |\n|---|---|\n| 状态 | 通过 |\n"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH + diagram_and_table, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN + diagram_and_table.replace("图 2.1 验证流程", "Figure 2.1. Validation flow"), encoding="utf-8")

            result = audit_repository(root)

        self.assertNotIn("CAPTION_POSITION", {item["code"] for item in result["errors"]})

    def test_parallel_items_and_nested_classification(self) -> None:
        # Reject inline parallel items and child categories that stay at the parent indentation.
        invalid = "\n\n包括：第一项、第二项、第三项\n\n- 分类：\n- 子项一\n- 子项二\n"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH + invalid, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")

            result = audit_repository(root)

        codes = {item["code"] for item in result["errors"]}
        self.assertIn("PARALLEL_ITEMS_INLINE", codes)
        self.assertIn("LIST_NESTING_REQUIRED", codes)

    def test_nested_classification_allows_following_sibling(self) -> None:
        # A sibling after correctly indented children must not be treated as another child.
        valid = "\n\n- 分类：\n  - 子项一\n  - 子项二\n- 下一个分类：说明\n"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH + valid, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")

            result = audit_repository(root)

        self.assertNotIn("LIST_NESTING_REQUIRED", {item["code"] for item in result["errors"]})

    def test_three_step_flow_requires_mermaid(self) -> None:
        # Require a diagram for three observable process nodes and accept a vertical diagram.
        steps = "\n\n第一步，读取\n\n第二步，检查\n\n第三步，输出\n"
        diagram = "\n```mermaid\nflowchart TD\nA[读取] --> B[检查]\nB --> C[输出]\n```\n"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH + steps, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")
            missing = audit_repository(root)
            (root / "README.md").write_text(GOOD_ZH + steps + diagram, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN + diagram, encoding="utf-8")
            present = audit_repository(root)

        self.assertIn("MERMAID_REQUIRED", {item["code"] for item in missing["errors"]})
        self.assertNotIn("MERMAID_REQUIRED", {item["code"] for item in present["errors"]})

    def test_technical_term_spelling_explanation_and_webp_boundary(self) -> None:
        # Preserve official spelling, require an operational explanation, and reject a fabricated WebP expansion.
        bare = "\n\nnpm\n"
        explained = "\n\nnpm 是 JavaScript 包管理工具，用于安装依赖；终端会显示安装进度，成功后可以运行项目\n\nWebP 是一种图片格式，用于缩小网页资源；浏览器会显示图片，加载失败时保留替代文本\n"
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            (root / "README.md").write_text(GOOD_ZH + bare, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")
            bare_result = audit_repository(root)
            (root / "README.md").write_text(GOOD_ZH + explained, encoding="utf-8")
            explained_result = audit_repository(root)
            (root / "README.md").write_text(GOOD_ZH + "\n\nNPM 与 Web Picture\n", encoding="utf-8")
            invalid_result = audit_repository(root)

        self.assertIn("TERM_EXPLANATION_REVIEW", {item["code"] for item in bare_result["warnings"]})
        self.assertNotIn("TERM_EXPLANATION_REVIEW", {item["code"] for item in explained_result["warnings"]})
        invalid_codes = {item["code"] for item in invalid_result["errors"]}
        self.assertIn("OFFICIAL_TERM_CASE", invalid_codes)
        self.assertIn("FABRICATED_TERM_EXPANSION", invalid_codes)

    def test_chinese_full_stop_excludes_literal_regions(self) -> None:
        # Block ordinary Chinese full stops while preserving quoted and code evidence.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            literal = "\n\n> 引文保留句号。\n\n```text\n日志保留句号。\n```\n"
            (root / "README.md").write_text(GOOD_ZH + literal, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")
            literal_result = audit_repository(root)
            (root / "README.md").write_text(GOOD_ZH + "\n\n正文包含句号。\n", encoding="utf-8")
            body_result = audit_repository(root)

        self.assertNotIn("CHINESE_FULL_STOP", {item["code"] for item in literal_result["errors"]})
        self.assertIn("CHINESE_FULL_STOP", {item["code"] for item in body_result["errors"]})

    def test_chinese_line_end_semicolon_excludes_literal_regions(self) -> None:
        # Reject a Chinese semicolon at the end of body or list lines while preserving literal evidence.
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs").mkdir()
            (root / "docs" / "hero.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\"></svg>", encoding="utf-8")
            literal = "\n\n> 引文保留分号；\n\n```text\n日志保留分号；\n```\n"
            (root / "README.md").write_text(GOOD_ZH + literal, encoding="utf-8")
            (root / "README.en.md").write_text(GOOD_EN, encoding="utf-8")
            literal_result = audit_repository(root)
            (root / "README.md").write_text(GOOD_ZH + "\n\n正文行尾包含分号；\n\n- 列表行尾包含分号；\n", encoding="utf-8")
            body_result = audit_repository(root)

        self.assertNotIn("CHINESE_LINE_END_SEMICOLON", {item["code"] for item in literal_result["errors"]})
        self.assertEqual(2, sum(item["code"] == "CHINESE_LINE_END_SEMICOLON" for item in body_result["errors"]))

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
                "## 2. 快速开始", '<a id="quick-start"></a>\n\n## 2. 快速开始'
            )
            en = GOOD_EN.replace("[Quick start](#2-quick-start)", "[Quick start](#quick-start)").replace(
                "## 2. Quick start", '<a name="quick-start"></a>\n\n## 2. Quick start'
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
