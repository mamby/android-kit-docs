"""Import selected public usage documentation, never library implementation files."""

import argparse
import re
from pathlib import Path

GUIDES = {
    "theme": ("Themes and colors", "Configure the palette and supported colors while preserving Kit's shared design.", "Foundations"),
    "navigation": ("Navigation", "Connect host-owned routes and back stacks to Kit's immediate page renderer.", "Foundations"),
    "button": ("Buttons", "Choose a text button variant and configure its colors.", "Components"),
    "list": ("Lists and selection", "Declare list and grid items, context actions, swipe deletion and bulk selection.", "Components"),
    "section-card": ("Section cards", "Present actions, switches, sliders and information through typed entries.", "Components"),
    "settings": ("Settings", "Declare one complete settings catalog with persistent values and global search.", "Components"),
    "search-page": ("Search pages", "Search typed application content with shared chrome and page-scoped history.", "Components"),
    "floating-search": ("Floating search", "Use controlled search input with supported submission modes and device speech input.", "Components"),
    "action-flyout": ("Action flyouts", "Declare anchored menus and submenus using Kit's typed action DSL.", "Components"),
    "context-menu": ("Context menus", "Open item actions with touch, mouse, keyboard and accessibility input.", "Components"),
    "floating-tooltip": ("Tooltips", "Present text and optional actions inside Material's tooltip positioning and state.", "Components"),
    "lock-page": ("Lock pages", "Present unlock, progress and retry states while your application owns authentication.", "Components"),
    "support-prompt": ("Support prompts", "Add an optional support card to page content with host-owned eligibility and callbacks.", "Components"),
}

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source", type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
known = set(GUIDES) | {"localization", "component-contract"}


def convert_links(match):
    name = match.group(1)
    anchor = match.group(2) or ""
    if name not in known:
        raise ValueError(f"Unpublished documentation link: {name}.md")
    return "({{ site.baseurl }}{% link guides/" + name + ".md %}" + anchor + ")"


for name, (title, description, section) in GUIDES.items():
    content = (args.source / "docs" / f"{name}.md").read_text(encoding="utf-8")
    content = re.sub(r"\A# [^\n]+\n+", "", content)
    content = re.sub(r"\(([a-z][a-z0-9-]*)\.md(#[^)]*)?\)", convert_links, content)
    header = f"---\ntitle: {title}\ndescription: {description}\npermalink: /guides/{name}/\nsection: {section}\n---\n"
    (root / "guides" / f"{name}.md").write_text(header + content, encoding="utf-8", newline="\n")

notices = (args.source / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
notices = notices.replace(
    "(compose/src/main/resources/META-INF/LICENSE-MATERIAL-SYMBOLS)",
    "(https://www.apache.org/licenses/LICENSE-2.0)",
)
(root / "THIRD_PARTY_NOTICES.md").write_text(notices, encoding="utf-8", newline="\n")
license_text = (root / "LICENSE").read_text(encoding="utf-8")
license_header = """---
title: License and notices
description: MIT licensing for Android Kit and applicable third-party notices.
permalink: /license/
section: Distribution
---
Android Kit binaries, these documents and usage examples are distributed under
the MIT license. The implementation repository is maintained privately; MIT does
not require source publication.

Retain the copyright and permission notice when redistributing Kit. The notices
below also apply to the identified third-party material and do not change the
license of an application's own code.

## Android Kit

```text
"""
notices = notices.replace("# Third-party notices", "## Third-party notices", 1).replace("## Lucide", "### Lucide", 1)
(root / "license.md").write_text(license_header + license_text.rstrip() + "\n```\n\n" + notices, encoding="utf-8", newline="\n")
print(f"Imported {len(GUIDES)} usage guides and third-party notices.")
