#!/usr/bin/env python3
"""Create a new static blog article for this GitHub Pages site."""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from string import Template


TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parents[1]
ARTICLE_DIR = REPO_ROOT / "article"
DEFAULT_TEMPLATE = TOOL_DIR / "templates" / "article.html"


def today_label() -> str:
    return date.today().strftime("%b %d, %Y").replace(" 0", " ")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "new-blog"


def normalize_filename(title: str, filename: str | None) -> str:
    name = filename or slugify(title)
    if not name.endswith(".html"):
        name += ".html"
    return Path(name).name


def split_tags(raw_tags: list[str]) -> list[str]:
    tags: list[str] = []
    for raw_tag in raw_tags:
        tags.extend(tag.strip() for tag in raw_tag.split(",") if tag.strip())
    return tags or ["Tags"]


def build_tag_html(tags: list[str]) -> str:
    labels = []
    for index, tag in enumerate(tags):
        label_class = "label-primary" if index == 0 else "label-default"
        labels.append(f'<span class="label {label_class}">{html.escape(tag)}</span>')
    return "\n                    ".join(labels)


def build_content_html(content: str) -> str:
    paragraphs = [part.strip() for part in content.split("\n\n") if part.strip()]
    if not paragraphs:
        paragraphs = ["Start writing here..."]
    return "\n\n".join(f"                    <p>{html.escape(part)}</p>" for part in paragraphs)


def build_pager(args: argparse.Namespace) -> str:
    if args.previous_title and args.previous_url:
        previous = (
            f'<li class="previous"><a href="{html.escape(args.previous_url)}">'
            f'<span aria-hidden="true">&lt;</span> {html.escape(args.previous_title)}</a></li>'
        )
    else:
        previous = (
            '<li class="previous disabled"><a href="#">'
            '<span aria-hidden="true">&lt;</span> No previous</a></li>'
        )

    if args.next_title and args.next_url:
        next_link = (
            f'<li class="next"><a href="{html.escape(args.next_url)}">'
            f'{html.escape(args.next_title)} <span aria-hidden="true">&gt;</span></a></li>'
        )
    else:
        next_link = '<li class="next disabled"><a href="#">No more <span aria-hidden="true">&gt;</span></a></li>'

    return f"{previous}\n                        {next_link}"


def open_in_editor(path: Path) -> None:
    editor = None
    try:
        import os

        editor = os.environ.get("EDITOR")
    except Exception:
        editor = None

    if editor:
        subprocess.run([editor, str(path)], check=False)
        return

    if sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a new article HTML file.")
    parser.add_argument("title", help="Article title.")
    parser.add_argument("-f", "--filename", help="Output filename, for example first_blog.html.")
    parser.add_argument("-d", "--date", default=today_label(), help="Display date, for example Nov 21, 2016.")
    parser.add_argument("-t", "--tag", action="append", default=[], help="Article tag. Can be repeated or comma-separated.")
    parser.add_argument("-c", "--content", default="", help="Initial article text. Blank lines become paragraphs.")
    parser.add_argument("--previous-title", help="Previous article title.")
    parser.add_argument("--previous-url", help="Previous article URL relative to article/.")
    parser.add_argument("--next-title", help="Next article title.")
    parser.add_argument("--next-url", help="Next article URL relative to article/.")
    parser.add_argument("--force", action="store_true", help="Overwrite the article if it already exists.")
    parser.add_argument("--open", action="store_true", help="Open the generated file after writing it.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    filename = normalize_filename(args.title, args.filename)
    output_path = ARTICLE_DIR / filename

    if output_path.exists() and not args.force:
        print(f"Article already exists: {output_path}")
        print("Use --force to overwrite it.")
        return 1

    template = Template(DEFAULT_TEMPLATE.read_text(encoding="utf-8"))
    tags = split_tags(args.tag)
    html_text = template.substitute(
        title=html.escape(args.title),
        date=html.escape(args.date),
        tags=build_tag_html(tags),
        content=build_content_html(args.content),
        pager=build_pager(args),
        canonical_url=f"https://micown.com/article/{filename}",
        disqus_identifier=Path(filename).stem,
    )

    output_path.write_text(html_text, encoding="utf-8")
    print(f"Created {output_path.relative_to(REPO_ROOT)}")

    if args.open:
        open_in_editor(output_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
