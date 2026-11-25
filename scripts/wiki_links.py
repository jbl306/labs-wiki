"""Wikilink lookup shared by transaction validation and wiki lint."""

from __future__ import annotations

import posixpath
import re
from collections.abc import Iterable
from pathlib import Path


_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_LINK = re.compile(r"\[\[([^\[\]\n]+)\]\]")


def strip_fenced_code(text: str) -> str:
    visible: list[str] = []
    delimiter = ""
    for line in text.splitlines(keepends=True):
        fence = _FENCE.match(line.rstrip("\r\n"))
        if delimiter:
            if fence and fence[1].startswith(delimiter) and not fence[2].strip():
                delimiter = ""
        elif fence:
            delimiter = fence[1]
        else:
            visible.append(line)
    return "".join(visible)


def wikilink_targets(text: str) -> list[str]:
    return [match.strip() for match in _LINK.findall(strip_fenced_code(text))]


def related_wikilinks(frontmatter: dict) -> list[str]:
    """Read folded and quoted YAML related entries using their parsed values."""
    related = frontmatter.get("related")
    if not isinstance(related, list):
        return []
    return [link for entry in related if isinstance(entry, str) for link in wikilink_targets(entry)]


def slugify_wikilink(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower().strip())
    return re.sub(r"[\s_-]+", "-", text).strip("-")


def wiki_markdown_pages(wiki_dir: Path) -> list[Path]:
    """Enumerate graph-eligible Markdown in stable repository-relative order."""
    return sorted(
        page for page in wiki_dir.rglob("*.md")
        if page.name not in {"index.md", "hot.md", "log.md"}
        and not {".obsidian", "meta"}.intersection(page.relative_to(wiki_dir).parts[:-1])
    )


class WikilinkLookup:
    """Resolve a link to a wiki-relative page ID without reading the filesystem."""

    def __init__(self, records: Iterable[tuple[str, str]]) -> None:
        self.titles: dict[str, str] = {}
        self.paths: dict[str, str] = {}
        self.slugs: dict[str, str] = {}
        for node_id, title in records:
            self.paths[node_id.casefold()] = node_id
            self.titles[title.casefold()] = node_id
            self.slugs[slugify_wikilink(title)] = node_id
        for node_id in self.paths.values():
            self.slugs.setdefault(slugify_wikilink(posixpath.basename(node_id)), node_id)
        self.slugs.pop("", None)

    def resolve(self, link: str, source_id: str) -> str | None:
        target = link.replace(r"\|", "|").strip()
        if target.startswith("#"):
            return self.paths.get(source_id.casefold())
        # Some existing titles contain literal pipes. Prefer the longest exact
        # title before interpreting the remaining alias or section delimiters.
        while target:
            exact = self.titles.get(target.casefold())
            if exact is not None:
                return exact
            separator = max(target.rfind("|"), target.rfind("#"))
            if separator == -1:
                break
            target = target[:separator].rstrip()
        path = target.removesuffix(".md")
        if path.startswith(("./", "../")):
            path = posixpath.normpath(posixpath.join(posixpath.dirname(source_id), path))
            return self.paths.get(path.casefold())
        if "/" in path:
            return self.paths.get(path.removeprefix("wiki/").casefold())
        return self.paths.get(path.casefold()) or self.slugs.get(slugify_wikilink(path))


def build_wikilink_lookup(wiki_dir: Path, pages: list[Path]) -> WikilinkLookup:
    from wiki_schema import parse_page_text

    records = []
    for page in pages:
        frontmatter, _, _ = parse_page_text(page.read_text(encoding="utf-8"))
        title = str(frontmatter.get("title") or page.stem.replace("-", " ").title())
        node_id = page.relative_to(wiki_dir).with_suffix("").as_posix()
        records.append((node_id, title))
    return WikilinkLookup(records)
