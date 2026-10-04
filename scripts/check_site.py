"""Validate the generated Pages artifact before publishing it."""

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])


site = Path(sys.argv[1]).resolve()
base = sys.argv[2].rstrip("/")
pages = {}
errors = []
for path in site.rglob("*.html"):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    pages[path] = parser


def resolve(url):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc:
        return None, None
    path = unquote(parsed.path)
    if path == base:
        path = "/"
    elif path.startswith(base + "/"):
        path = path[len(base):]
    else:
        return None, "Internal URL is outside the site's base path: " + url
    target = (site / path.lstrip("/")).resolve()
    if not target.is_relative_to(site):
        return None, "Internal URL leaves the site: " + url
    if target.is_dir():
        target /= "index.html"
    if not target.is_file():
        return None, "Missing target: " + url
    if parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
        return None, "Missing heading: " + url
    return target, None


for path, parser in pages.items():
    relative = path.relative_to(site).as_posix()
    page_url = base + "/" + (relative[:-10] if relative.endswith("index.html") else relative)
    for link in parser.links:
        _, error = resolve(urljoin(page_url, link))
        if error:
            errors.append(f"{relative}: {error}")

index = json.loads((site / "search.json").read_text(encoding="utf-8"))
if not index:
    errors.append("Search index has no documents")
for item in index:
    _, error = resolve(item["url"])
    if error:
        errors.append("Search index: " + error)

if errors:
    print("\n".join(sorted(set(errors))))
    sys.exit(1)
print(f"Checked {len(pages)} HTML pages and {len(index)} search documents.")
