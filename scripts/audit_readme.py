#!/usr/bin/env python3
"""Audit bilingual GitHub README files without modifying the target repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlsplit


# Keep the scanner dependency-free so it can run in ordinary repository environments.
SKIPPED_DIRECTORIES = {
    ".git",
    ".idea",
    ".next",
    ".venv",
    ".vscode",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
}

TEXT_SUFFIXES = {
    ".bat",
    ".cmd",
    ".css",
    ".env",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mem",
    ".mk",
    ".mjs",
    ".py",
    ".sdc",
    ".sh",
    ".sv",
    ".svh",
    ".svg",
    ".tcl",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".v",
    ".vhd",
    ".vhdl",
    ".vh",
    ".xdc",
    ".yaml",
    ".yml",
}

SENSITIVE_PATTERNS = {
    "AWS_ACCESS_KEY": re.compile(r"(?<![A-Z0-9])AKIA[0-9A-Z]{16}(?![A-Z0-9])"),
    "GITHUB_TOKEN": re.compile(r"(?<![A-Za-z0-9_])gh[pousr]_[A-Za-z0-9_]{30,}"),
    "OPENAI_API_KEY": re.compile(
        r"(?<![A-Za-z0-9_-])sk-(?:(?:proj|svcacct|admin)-[A-Za-z0-9_-]{32,}|[A-Za-z0-9_]{32,})"
    ),
    "PRIVATE_KEY": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "CREDENTIAL_URL": re.compile(r"https?://[^\s/:]+:[^\s/@]+@(?:\[[0-9A-Fa-f:.]+\]|[A-Za-z0-9.-]+)"),
    "PRIVATE_IPV4": re.compile(
        r"(?<![0-9])(?:10\.(?:\d{1,3}\.){2}\d{1,3}|"
        r"192\.168\.(?:\d{1,3}\.)\d{1,3}|"
        r"172\.(?:1[6-9]|2\d|3[01])\.(?:\d{1,3}\.)\d{1,3})(?![0-9])"
    ),
    "WINDOWS_USER_PATH": re.compile(
        r"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/][^\\/\s\"'<>]+)"
    ),
    "UNIX_USER_PATH": re.compile(r"(?<![A-Za-z0-9])/(?:home|Users)/[^/\s\"'<>]+"),
}

ALLOWLIST_FILENAME = ".readme-audit-allowlist.json"
ALLOWLISTABLE_CODES = {"PRIVATE_IPV4"}


def is_reserved_credential_url_fixture(match: re.Match[str]) -> bool:
    """Allow synthetic user-info URLs only on reserved test or loopback hosts."""

    try:
        host = (urlsplit(match.group(0)).hostname or "").lower().rstrip(".")
    except ValueError:
        return False
    return host in {"localhost", "127.0.0.1", "::1"} or host.endswith(".example")


@dataclass(frozen=True)
class Finding:
    """Represent one non-sensitive audit result."""

    level: str
    code: str
    file: str
    line: int | None
    message: str


@dataclass
class SensitiveAllowlistEntry:
    """Represent one exact, counted sensitive-pattern exception."""

    code: str
    path: str
    match_sha256: str
    occurrences: int
    reason: str
    used: int = 0


def add_finding(
    findings: list[Finding],
    level: str,
    code: str,
    file: Path,
    message: str,
    line: int | None = None,
) -> None:
    """Add a finding without copying the matched secret into output."""

    findings.append(
        Finding(
            level=level,
            code=code,
            file=file.as_posix(),
            line=line,
            message=message,
        )
    )


def line_number(text: str, index: int) -> int:
    """Convert a character offset to a one-based line number."""

    return text.count("\n", 0, index) + 1


def read_text(path: Path) -> str:
    """Read repository text with a stable UTF-8 fallback."""

    return path.read_text(encoding="utf-8-sig", errors="replace")


def load_sensitive_allowlist(
    root: Path,
    findings: list[Finding],
    files: Iterable[Path],
) -> list[SensitiveAllowlistEntry]:
    """Load narrow repository exceptions without storing matched values."""

    config_path = root / ALLOWLIST_FILENAME
    if not config_path.is_file():
        return []

    def report(message: str) -> None:
        # Keep configuration failures separate from secret findings so maintainers can repair intent.
        add_finding(findings, "error", "INVALID_ALLOWLIST", Path(ALLOWLIST_FILENAME), message)

    try:
        document = json.loads(read_text(config_path))
    except json.JSONDecodeError:
        report("敏感扫描例外文件不是有效 JSON")
        return []

    if not isinstance(document, dict):
        report("敏感扫描例外文件必须使用对象结构")
        return []
    if set(document) != {"version", "entries"}:
        report("敏感扫描例外文件只允许 version 和 entries 两个顶层字段")
        return []
    if isinstance(document.get("version"), bool) or document.get("version") != 1:
        report("敏感扫描例外文件版本必须为 1")
        return []
    raw_entries = document.get("entries")
    if not isinstance(raw_entries, list):
        report("敏感扫描例外 entries 必须是数组")
        return []

    scoped_files = {path.resolve() for path in files}
    entries: list[SensitiveAllowlistEntry] = []
    seen: set[tuple[str, str, str]] = set()
    expected_fields = {"code", "path", "match_sha256", "occurrences", "reason"}

    for index, raw_entry in enumerate(raw_entries, start=1):
        prefix = f"第 {index} 条敏感扫描例外"
        if not isinstance(raw_entry, dict) or set(raw_entry) != expected_fields:
            report(f"{prefix}必须且只能包含 code、path、match_sha256、occurrences 和 reason")
            continue

        code = raw_entry.get("code")
        relative_path = raw_entry.get("path")
        match_sha256 = raw_entry.get("match_sha256")
        occurrences = raw_entry.get("occurrences")
        reason = raw_entry.get("reason")

        valid = True
        if code not in ALLOWLISTABLE_CODES:
            report(f"{prefix}使用了不允许豁免的检查代码")
            valid = False
        if (
            not isinstance(relative_path, str)
            or not relative_path
            or "\\" in relative_path
            or Path(relative_path).is_absolute()
            or ".." in Path(relative_path).parts
        ):
            report(f"{prefix}必须使用仓库内的精确相对路径")
            valid = False
        if not isinstance(match_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", match_sha256):
            report(f"{prefix}的 match_sha256 必须是小写 SHA-256 摘要")
            valid = False
        if isinstance(occurrences, bool) or not isinstance(occurrences, int) or occurrences < 1:
            report(f"{prefix}的 occurrences 必须是正整数")
            valid = False
        if not isinstance(reason, str) or len(reason.strip()) < 20:
            report(f"{prefix}必须提供不少于 20 个字符的审核理由")
            valid = False
        if not valid:
            continue

        target = (root / relative_path).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            report(f"{prefix}指向的仓库文件不存在")
            continue

        identity = (code, relative_path, match_sha256)
        if identity in seen:
            report(f"{prefix}与已有例外重复")
            continue
        seen.add(identity)

        # Publication-surface scans activate only exceptions for files in that scan.
        if target not in scoped_files:
            continue
        entries.append(
            SensitiveAllowlistEntry(
                code=code,
                path=relative_path,
                match_sha256=match_sha256,
                occurrences=occurrences,
                reason=reason.strip(),
            )
        )

    return entries


def mask_fenced_code(text: str) -> str:
    """Hide fenced code while preserving character and line offsets."""

    pattern = re.compile(r"(?ms)^(?P<fence>`{3,}|~{3,})[^\n]*\n.*?^(?P=fence)\s*$")
    return pattern.sub(lambda match: re.sub(r"[^\n]", " ", match.group(0)), text)


def iter_repository_files(root: Path) -> Iterable[Path]:
    """Yield files while excluding generated dependency directories."""

    for path in root.rglob("*"):
        # Check path components before stat calls because generated trees can
        # contain platform-specific symlinks that are unreadable on the host.
        try:
            relative_parts = path.relative_to(root).parts
        except ValueError:
            continue
        if any(part in SKIPPED_DIRECTORIES for part in relative_parts):
            continue
        try:
            is_file = path.is_file()
        except OSError:
            # A repository audit must not fail on an inaccessible generated or
            # special filesystem entry. Readable publication files are still
            # scanned, while the repository-specific secret scan remains the
            # authoritative gate for protected runtime paths.
            continue
        if not is_file:
            continue
        yield path


def github_slug(value: str) -> str:
    """Approximate GitHub heading anchors for local link validation."""

    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"[`*_~]", "", value).strip().lower()
    value = re.sub(r"[^\w\-\s\u3400-\u9fff]", "", value, flags=re.UNICODE)
    return re.sub(r"\s+", "-", value)


def heading_outline(text: str) -> tuple[list[int], list[str], list[str]]:
    """Return heading levels, unique GitHub-style slugs, and H2 section numbers."""

    levels: list[int] = []
    slugs: list[str] = []
    section_numbers: list[str] = []
    slug_counts: dict[str, int] = {}

    visible_text = mask_fenced_code(text)
    for match in re.finditer(r"(?m)^(#{1,6})\s+(.+?)\s*$", visible_text):
        level = len(match.group(1))
        title = match.group(2)
        base_slug = github_slug(title)
        duplicate_index = slug_counts.get(base_slug, 0)
        slug_counts[base_slug] = duplicate_index + 1
        slug = base_slug if duplicate_index == 0 else f"{base_slug}-{duplicate_index}"
        levels.append(level)
        slugs.append(slug)

        # Compare chapter numbers instead of translated heading text.
        if level == 2:
            number_match = re.match(r"(\d+(?:\.\d+)*)\b", title)
            section_numbers.append(number_match.group(1) if number_match else "")

    return levels, slugs, section_numbers


def explicit_html_anchors(text: str) -> set[str]:
    """Return stable anchors declared with HTML id or name attributes."""

    visible_text = mask_fenced_code(text)
    anchors: set[str] = set()
    for match in re.finditer(
        r"<(?:a|div|span)\b[^>]*\b(?:id|name)=[\"']([^\"']+)[\"'][^>]*>",
        visible_text,
        flags=re.IGNORECASE,
    ):
        anchors.add(unquote(match.group(1)).lower())
    return anchors


def extract_targets(text: str) -> tuple[list[tuple[str, str, int]], list[tuple[str, str, int]]]:
    """Extract links and images from Markdown and embedded HTML."""

    visible_text = mask_fenced_code(text)
    links: list[tuple[str, str, int]] = []
    images: list[tuple[str, str, int]] = []

    # Parse Markdown images before ordinary links so image targets are not double-counted.
    image_spans: list[tuple[int, int]] = []
    for match in re.finditer(r"!\[([^\]]*)\]\((?:<([^>]+)>|([^\s)]+))(?:\s+[\"'][^\"']*[\"'])?\)", visible_text):
        target = match.group(2) or match.group(3)
        images.append((target, match.group(1).strip(), line_number(text, match.start())))
        image_spans.append(match.span())

    for match in re.finditer(r"(?<!!)\[([^\]]+)\]\((?:<([^>]+)>|([^\s)]+))(?:\s+[\"'][^\"']*[\"'])?\)", visible_text):
        if any(start <= match.start() < end for start, end in image_spans):
            continue
        target = match.group(2) or match.group(3)
        links.append((target, match.group(1).strip(), line_number(text, match.start())))

    # Parse embedded HTML elements that GitHub preserves in README files.
    for match in re.finditer(r"<a\b[^>]*\bhref=[\"']([^\"']+)[\"'][^>]*>", visible_text, flags=re.IGNORECASE):
        links.append((match.group(1), "", line_number(text, match.start())))

    for match in re.finditer(r"<img\b([^>]*)>", visible_text, flags=re.IGNORECASE):
        attributes = match.group(1)
        source_match = re.search(r"\bsrc=[\"']([^\"']+)[\"']", attributes, flags=re.IGNORECASE)
        alt_match = re.search(r"\balt=[\"']([^\"']*)[\"']", attributes, flags=re.IGNORECASE)
        if source_match:
            images.append(
                (
                    source_match.group(1),
                    alt_match.group(1).strip() if alt_match else "",
                    line_number(text, match.start()),
                )
            )

    for match in re.finditer(r"<source\b[^>]*\bsrcset=[\"']([^\"']+)[\"'][^>]*>", visible_text, flags=re.IGNORECASE):
        images.append((match.group(1), "theme source", line_number(text, match.start())))

    return links, images


def is_external(target: str) -> bool:
    """Identify network, email, data, and protocol-relative targets."""

    return bool(re.match(r"^(?:https?:|mailto:|data:|//)", target, flags=re.IGNORECASE))


def resolve_local_target(readme: Path, target: str) -> Path:
    """Resolve a relative README target without following a fragment or query."""

    normalized = unquote(target.split("#", 1)[0].split("?", 1)[0])
    return (readme.parent / normalized).resolve()


def audit_readme_file(root: Path, readme: Path, findings: list[Finding]) -> dict[str, object]:
    """Audit one README and return measurements used for bilingual comparison."""

    text = read_text(readme)
    levels, slugs, section_numbers = heading_outline(text)
    valid_anchors = set(slugs) | explicit_html_anchors(text)
    links, images = extract_targets(text)

    # Require a searchable project title in either Markdown or semantic HTML.
    has_h1 = 1 in levels or bool(re.search(r"<h1(?:\s|>)", text, flags=re.IGNORECASE))
    if not has_h1:
        add_finding(findings, "error", "MISSING_H1", readme, "README 缺少可搜索的一级标题")

    # Chinese remains the default primary language while allowing project-specific review.
    if readme.name.lower() == "readme.md" and not re.search(r"[\u3400-\u9fff]", text[:4000]):
        add_finding(findings, "warning", "PRIMARY_LANGUAGE_REVIEW", readme, "主 README 前部未检测到中文，需要确认语言优先级")

    # Validate page anchors against the generated heading outline.
    for target, _, line in links:
        if target.startswith("#"):
            anchor = unquote(target[1:]).lower()
            if anchor not in valid_anchors:
                add_finding(findings, "error", "BROKEN_ANCHOR", readme, "页内入口没有匹配标题", line)

    # Validate local files and record external image dependencies for review.
    for target, alt, line in images:
        if not alt:
            add_finding(findings, "error", "MISSING_IMAGE_ALT", readme, "图片缺少替代文本", line)
        if is_external(target):
            add_finding(findings, "warning", "REMOTE_IMAGE", readme, "README 使用远程图片，需要确认隐私、稳定性和维护责任", line)
            continue
        if "{{" in target:
            continue
        resolved = resolve_local_target(readme, target)
        if not resolved.is_relative_to(root):
            add_finding(findings, "error", "ASSET_OUTSIDE_REPOSITORY", readme, "图片路径离开仓库边界", line)
        elif not resolved.is_file():
            add_finding(findings, "error", "MISSING_IMAGE", readme, "图片文件不存在", line)

    for target, _, line in links:
        if target.startswith("#") or is_external(target) or target.startswith("{{"):
            continue
        resolved = resolve_local_target(readme, target)
        if not resolved.is_relative_to(root):
            add_finding(findings, "error", "LINK_OUTSIDE_REPOSITORY", readme, "链接路径离开仓库边界", line)
        elif not resolved.exists():
            add_finding(findings, "error", "MISSING_LOCAL_LINK", readme, "本地链接目标不存在", line)

    # Visual evidence can be an image, table, or Mermaid relationship diagram.
    visible_text = mask_fenced_code(text)
    table_count = len(re.findall(r"(?m)^\|(?:\s*:?-+:?\s*\|)+\s*$", visible_text)) + len(
        re.findall(r"<table(?:\s|>)", visible_text, flags=re.IGNORECASE)
    )
    mermaid_count = len(re.findall(r"```mermaid\s", text, flags=re.IGNORECASE))
    if not images and table_count == 0 and mermaid_count == 0:
        add_finding(findings, "warning", "NO_VISUAL_EVIDENCE", readme, "README 缺少图片、表格或 Mermaid 关系图")

    return {
        "file": readme.relative_to(root).as_posix(),
        "heading_levels": levels,
        "section_numbers": section_numbers,
        "images": len(images),
        "tables": table_count,
        "mermaid_blocks": mermaid_count,
        "links": len(links),
    }


def collect_readme_scope(root: Path, readmes: Iterable[Path]) -> set[Path]:
    """Collect README files and the local documents or assets they reference."""

    scope: set[Path] = set()
    pending = [path.resolve() for path in readmes if path.is_file()]

    # Follow local Markdown documents so linked deployment and security guidance is scanned too.
    while pending:
        path = pending.pop()
        if path in scope:
            continue
        scope.add(path)
        if path.suffix.lower() != ".md":
            continue

        links, images = extract_targets(read_text(path))
        for target, _, _ in [*links, *images]:
            if target.startswith("#") or is_external(target) or "{{" in target:
                continue
            resolved = resolve_local_target(path, target)
            if resolved.is_relative_to(root) and resolved.is_file() and resolved not in scope:
                pending.append(resolved)

    return scope


def scan_sensitive_text(
    root: Path,
    findings: list[Finding],
    files: Iterable[Path],
    allowlist: list[SensitiveAllowlistEntry],
) -> tuple[int, int]:
    """Scan selected text files and report locations without exposing matched values."""

    scanned = 0
    allowlisted_matches = 0
    allowlist_index = {(item.code, item.path, item.match_sha256): item for item in allowlist}
    for path in sorted(set(files)):
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name.lower() not in {"license", "dockerfile", "makefile"}:
            continue
        scanned += 1
        text = read_text(path)
        relative_path = path.relative_to(root).as_posix()
        for pattern_name, pattern in SENSITIVE_PATTERNS.items():
            for match in pattern.finditer(text):
                if pattern_name == "CREDENTIAL_URL" and is_reserved_credential_url_fixture(match):
                    continue
                match_sha256 = hashlib.sha256(match.group(0).encode("utf-8")).hexdigest()
                exception = allowlist_index.get((pattern_name, relative_path, match_sha256))
                if exception is not None and exception.used < exception.occurrences:
                    exception.used += 1
                    allowlisted_matches += 1
                    continue
                add_finding(
                    findings,
                    "error",
                    pattern_name,
                    path.relative_to(root),
                    "检测到可能的敏感值，输出已隐藏匹配内容",
                    line_number(text, match.start()),
                )

        # SVG metadata can disclose authoring tools or embedded document details.
        if path.suffix.lower() == ".svg" and re.search(r"<metadata(?:\s|>)", text, flags=re.IGNORECASE):
            add_finding(
                findings,
                "warning",
                "SVG_METADATA",
                path.relative_to(root),
                "SVG 包含 metadata 元素，需要确认没有作者、路径或设备信息",
            )

    for exception in allowlist:
        if exception.used != exception.occurrences:
            add_finding(
                findings,
                "error",
                "ALLOWLIST_COUNT_MISMATCH",
                Path(exception.path),
                f"敏感扫描例外预期 {exception.occurrences} 处，实际匹配 {exception.used} 处",
            )
            continue
        add_finding(
            findings,
            "warning",
            "SENSITIVE_ALLOWLIST_APPLIED",
            Path(exception.path),
            f"已按审核理由接受 {exception.used} 处精确匹配，仍需人工确认例外有效性",
        )
    return scanned, allowlisted_matches


def xml_local_name(name: str) -> str:
    """Return an XML name without its namespace."""

    return name.rsplit("}", 1)[-1].lower()


def scan_svg_safety(root: Path, findings: list[Finding], files: Iterable[Path]) -> int:
    """Validate SVG structure, active content, external references, and stable sizing."""

    scanned = 0
    blocked_elements = {"script", "foreignobject", "iframe", "object", "embed"}
    for path in sorted(set(files)):
        if path.suffix.lower() != ".svg":
            continue
        scanned += 1
        text = read_text(path)
        relative = path.relative_to(root)

        if re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", text, flags=re.IGNORECASE):
            add_finding(
                findings,
                "error",
                "SVG_DOCUMENT_DECLARATION",
                relative,
                "SVG 包含文档类型或实体声明，无法作为可审查的静态资源发布",
            )

        try:
            document = ET.fromstring(text)
        except ET.ParseError:
            add_finding(findings, "error", "MALFORMED_SVG", relative, "SVG 不是可解析的 XML 文档")
            continue

        if xml_local_name(document.tag) != "svg":
            add_finding(findings, "error", "INVALID_SVG_ROOT", relative, "SVG 文件缺少 svg 根元素")
            continue

        title_present = False
        active_content_found = False
        external_reference_found = False
        event_handler_found = False
        for element in document.iter():
            element_name = xml_local_name(element.tag)
            if element_name == "title":
                title_present = True
            if element_name in blocked_elements:
                active_content_found = True

            for raw_name, raw_value in element.attrib.items():
                attribute_name = xml_local_name(raw_name)
                value = raw_value.strip()
                if attribute_name.startswith("on"):
                    event_handler_found = True
                if attribute_name in {"href", "src"} and value and not value.startswith("#"):
                    external_reference_found = True
                if attribute_name in {"style", "fill", "filter", "mask", "clip-path"}:
                    for match in re.finditer(r"url\(\s*['\"]?([^)'\"\s]+)", value, flags=re.IGNORECASE):
                        reference = match.group(1)
                        if not reference.startswith("#"):
                            external_reference_found = True

        if active_content_found:
            add_finding(findings, "error", "SVG_ACTIVE_CONTENT", relative, "SVG 包含脚本或可嵌入活动内容")
        if event_handler_found:
            add_finding(findings, "error", "SVG_EVENT_HANDLER", relative, "SVG 包含事件处理器属性")
        if external_reference_found:
            add_finding(findings, "error", "SVG_EXTERNAL_REFERENCE", relative, "SVG 引用了仓库外部或数据地址资源")

        has_accessible_name = title_present or any(
            key in document.attrib for key in ("aria-label", "aria-labelledby")
        )
        if not has_accessible_name:
            add_finding(findings, "warning", "SVG_ACCESSIBLE_NAME", relative, "SVG 缺少 title 或无障碍名称")

        has_viewbox = "viewBox" in document.attrib or "viewbox" in document.attrib
        has_dimensions = "width" in document.attrib and "height" in document.attrib
        if not has_viewbox and not has_dimensions:
            add_finding(findings, "warning", "SVG_UNSTABLE_SIZE", relative, "SVG 缺少 viewBox 或明确宽高，主题和窄屏缩放需要复核")

    return scanned


def png_chunk_types(data: bytes) -> set[bytes]:
    """Return PNG chunk names without decoding embedded values."""

    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return set()
    chunk_types: set[bytes] = set()
    offset = 8
    while offset + 12 <= len(data):
        length = int.from_bytes(data[offset : offset + 4], "big")
        chunk_type = data[offset + 4 : offset + 8]
        if length > len(data) - offset - 12:
            break
        chunk_types.add(chunk_type)
        offset += 12 + length
        if chunk_type == b"IEND":
            break
    return chunk_types


def scan_binary_image_metadata(root: Path, findings: list[Finding], files: Iterable[Path]) -> int:
    """Flag common embedded metadata containers in selected images."""

    scanned = 0
    for path in sorted(set(files)):
        if path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        scanned += 1
        data = path.read_bytes()

        # Match common extensions to byte signatures before browsers apply content sniffing.
        suffix = path.suffix.lower()
        format_matches = {
            ".jpg": data.startswith(b"\xff\xd8\xff"),
            ".jpeg": data.startswith(b"\xff\xd8\xff"),
            ".png": data.startswith(b"\x89PNG\r\n\x1a\n"),
            ".webp": data.startswith(b"RIFF") and data[8:12] == b"WEBP",
        }
        if not format_matches[suffix]:
            add_finding(
                findings,
                "warning",
                "IMAGE_FORMAT_MISMATCH",
                path.relative_to(root),
                "图片扩展名与字节格式不一致，需要改名或重新编码",
            )

        markers = (b"Exif\x00\x00", b"Photoshop 3.0", b"XML:com.adobe.xmp", b"<x:xmpmeta")
        metadata_found = any(marker in data for marker in markers)
        if suffix == ".png" and png_chunk_types(data) & {b"eXIf", b"iTXt", b"tEXt", b"zTXt"}:
            metadata_found = True
        if suffix == ".webp" and (b"EXIF" in data[12:] or b"XMP " in data[12:]):
            metadata_found = True
        if metadata_found:
            add_finding(
                findings,
                "warning",
                "IMAGE_METADATA",
                path.relative_to(root),
                "图片包含常见元数据容器，需要执行项目专用元数据检查",
            )
    return scanned


def audit_repository(
    root: Path,
    zh_name: str = "README.md",
    en_name: str = "README.en.md",
    scan_repository: bool = False,
) -> dict[str, object]:
    """Audit a repository and return a serializable result."""

    root = root.resolve()
    findings: list[Finding] = []
    readme_reports: list[dict[str, object]] = []

    # Both files are required by this bilingual standard unless the caller selects other names.
    readme_paths = [root / zh_name, root / en_name]
    for readme in readme_paths:
        if not readme.is_file():
            add_finding(findings, "error", "MISSING_README", readme.relative_to(root), "缺少要求的 README 文件")
            continue
        readme_reports.append(audit_readme_file(root, readme, findings))

    # Compare structural invariants while allowing natural translation differences.
    if len(readme_reports) == 2:
        zh_report, en_report = readme_reports
        if zh_report["heading_levels"] != en_report["heading_levels"]:
            add_finding(findings, "error", "BILINGUAL_HEADING_DRIFT", Path(en_name), "中英文标题层级或数量不一致")
        if zh_report["section_numbers"] != en_report["section_numbers"]:
            add_finding(findings, "error", "BILINGUAL_SECTION_DRIFT", Path(en_name), "中英文主章节编号不一致")
        for metric in ("images", "tables", "mermaid_blocks"):
            if zh_report[metric] != en_report[metric]:
                add_finding(findings, "error", "BILINGUAL_VISUAL_DRIFT", Path(en_name), f"中英文 {metric} 数量不一致")

    # Default to the README publication surface and offer an explicit full-repository mode.
    audit_scope = set(iter_repository_files(root)) if scan_repository else collect_readme_scope(root, readme_paths)
    allowlist = load_sensitive_allowlist(root, findings, audit_scope)
    text_files_scanned, allowlisted_matches = scan_sensitive_text(root, findings, audit_scope, allowlist)
    vector_images_scanned = scan_svg_safety(root, findings, audit_scope)
    images_scanned = scan_binary_image_metadata(root, findings, audit_scope)
    errors = [asdict(item) for item in findings if item.level == "error"]
    warnings = [asdict(item) for item in findings if item.level == "warning"]

    return {
        "repository": root.as_posix(),
        "status": "PASS" if not errors else "FAIL",
        "summary": {
            "readmes_checked": len(readme_reports),
            "text_files_scanned": text_files_scanned,
            "vector_images_scanned": vector_images_scanned,
            "binary_images_scanned": images_scanned,
            "allowlist_entries": len(allowlist),
            "allowlisted_matches": allowlisted_matches,
            "scan_scope": "repository" if scan_repository else "readme-and-references",
            "error_count": len(errors),
            "warning_count": len(warnings),
        },
        "readmes": readme_reports,
        "errors": errors,
        "warnings": warnings,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command-line options without requiring repository dependencies."""

    parser = argparse.ArgumentParser(description="Audit bilingual GitHub README structure, assets, links, and sensitive patterns")
    parser.add_argument("repository", type=Path, help="Repository root to audit")
    parser.add_argument("--zh", default="README.md", help="Chinese README path relative to the repository")
    parser.add_argument("--en", default="README.en.md", help="English README path relative to the repository")
    parser.add_argument(
        "--scan-repository",
        action="store_true",
        help="Scan all repository text and image files instead of the README publication surface",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the audit and return a failure code when hard gates fail."""

    args = parse_args(argv or sys.argv[1:])
    if not args.repository.is_dir():
        print(json.dumps({"status": "FAIL", "error": "repository path does not exist"}, ensure_ascii=False))
        return 2

    result = audit_repository(args.repository, args.zh, args.en, args.scan_repository)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
