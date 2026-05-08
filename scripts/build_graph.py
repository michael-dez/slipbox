#!/usr/bin/env python3
"""Parse zk markdown notes, emit docs/graph.json, and render per-note HTML pages."""

import json
import re
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).parent.parent
DOCS_DIR = ROOT / "docs"
NOTES_DIR = DOCS_DIR / "notes"

# HTML template for individual note pages.
# Placeholders: {id}, {title}, {date}, {tags_html}, {body_html}, {back_url}
_NOTE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #0f0f1a;
      color: #ccc;
      font-family: "Segoe UI", system-ui, sans-serif;
      line-height: 1.7;
      padding: 2rem 1rem 4rem;
    }}
    .container {{
      max-width: 760px;
      margin: 0 auto;
    }}
    nav {{
      margin-bottom: 2rem;
    }}
    nav a {{
      color: #778;
      font-size: 13px;
      text-decoration: none;
    }}
    nav a:hover {{ color: #aab; }}
    h1 {{
      font-size: 1.6rem;
      color: #eee;
      margin-bottom: 0.3rem;
    }}
    .meta {{
      font-size: 12px;
      color: #556;
      margin-bottom: 0.5rem;
    }}
    .tags {{
      font-size: 12px;
      color: #667;
      margin-bottom: 2rem;
    }}
    .tags span {{
      background: rgba(255,255,255,0.06);
      border-radius: 4px;
      padding: 2px 7px;
      margin-right: 4px;
    }}
    hr {{
      border: none;
      border-top: 1px solid rgba(255,255,255,0.08);
      margin-bottom: 2rem;
    }}
    .content h1, .content h2, .content h3, .content h4 {{
      color: #dde;
      margin: 1.6rem 0 0.6rem;
    }}
    .content p {{ margin-bottom: 1rem; }}
    .content ul, .content ol {{
      padding-left: 1.4rem;
      margin-bottom: 1rem;
    }}
    .content li {{ margin-bottom: 0.3rem; }}
    .content a {{ color: #88aadd; }}
    .content a:hover {{ color: #aaccff; }}
    .content code {{
      background: rgba(255,255,255,0.07);
      border-radius: 3px;
      padding: 1px 5px;
      font-size: 0.88em;
      font-family: "Fira Code", "Cascadia Code", monospace;
    }}
    .content pre {{
      background: rgba(255,255,255,0.05);
      border-radius: 6px;
      padding: 1rem;
      overflow-x: auto;
      margin-bottom: 1rem;
    }}
    .content pre code {{
      background: none;
      padding: 0;
      font-size: 0.85em;
    }}
    blockquote {{
      border-left: 3px solid rgba(255,255,255,0.15);
      padding-left: 1rem;
      color: #889;
      margin-bottom: 1rem;
    }}
  </style>
</head>
<body>
  <div class="container">
    <nav><a href="{back_url}">← back to graph</a></nav>
    <h1>{title}</h1>
    <div class="meta">{date}</div>
    <div class="tags">{tags_html}</div>
    <hr />
    <div class="content">
{body_html}
    </div>
  </div>
</body>
</html>
"""


def parse_note(path: Path) -> dict | None:
    """Return a dict with id, title, date, tags, outgoing link ids, and raw body."""
    text = path.read_text(encoding="utf-8")

    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not fm_match:
        return None

    try:
        fm = yaml.safe_load(fm_match.group(1))
    except yaml.YAMLError:
        return None

    if not fm or not isinstance(fm, dict):
        return None

    title = str(fm.get("title") or path.stem)
    note_date = str(fm.get("date") or "")

    raw_tags = fm.get("tags") or []
    if isinstance(raw_tags, str):
        raw_tags = [raw_tags]
    tags = [str(t) for t in raw_tags if t]

    body = text[fm_match.end():]
    # Match standard markdown links whose target is a sibling .md file.
    # Filename characters: letters (any case), digits, hyphens, underscores.
    link_targets = re.findall(r"\[.*?\]\(([a-zA-Z0-9_-]+\.md)\)", body)

    return {
        "id": path.stem,
        "title": title,
        "date": note_date,
        "tags": tags,
        # Outgoing links preserve authoring direction: this note → linked note.
        "links": [t[:-3] for t in link_targets],  # strip .md extension
        "body": body,
    }


def _preprocess_body(body: str, known_ids: set[str]) -> str:
    """Convert zk wiki-style links to standard markdown before rendering.

    zk-nvim converts [[Title]] wiki links to [[[Title](id.md)]] when a match
    exists. Bare [[Text]] links with no note match are stripped to plain text.
    Standard markdown links to .md sibling files are rewritten to point to the
    rendered .html pages in the same notes/ directory.
    """
    # [[[Link text](id.md)]] → [Link text](id.html)
    body = re.sub(
        r"\[\[\[([^\]]+)\]\(([a-zA-Z0-9_-]+)\.md\)\]\]",
        lambda m: f"[{m.group(1)}]({m.group(2)}.html)",
        body,
    )
    # [[plain wiki text]] with no file → just the text
    body = re.sub(r"\[\[([^\]]+)\]\]", r"\1", body)
    # Plain markdown links pointing to .md siblings → .html
    def _md_to_html(m: re.Match) -> str:
        note_id = m.group(2)[:-3]  # strip .md
        if note_id in known_ids:
            return f"[{m.group(1)}]({note_id}.html)"
        return m.group(0)  # leave unknown links unchanged

    body = re.sub(r"\[([^\]]+)\]\(([a-zA-Z0-9_-]+\.md)\)", _md_to_html, body)
    return body


def _render_note_html(note: dict, known_ids: set[str]) -> None:
    """Write docs/notes/<id>.html with the note's markdown rendered to HTML."""
    tags_html = "".join(f"<span>{t}</span>" for t in note["tags"]) if note["tags"] else ""
    processed_body = _preprocess_body(note["body"], known_ids)
    body_html = markdown.markdown(
        processed_body,
        extensions=["fenced_code", "tables", "nl2br"],
    )
    html = _NOTE_TEMPLATE.format(
        id=note["id"],
        title=note["title"],
        date=note["date"] or "no date",
        tags_html=tags_html,
        body_html=body_html,
        back_url="../index.html",
    )
    out = NOTES_DIR / f"{note['id']}.html"
    out.write_text(html, encoding="utf-8")


def build_graph() -> None:
    notes: dict[str, dict] = {}
    for md_file in sorted(ROOT.glob("*.md")):
        note = parse_note(md_file)
        if note:
            notes[note["id"]] = note

    nodes: list[dict] = [
        {
            "id": n["id"],
            "title": n["title"],
            "date": n["date"],
            "tags": n["tags"],
            "type": "note",
        }
        for n in notes.values()
    ]

    # Synthesize a node per unique tag for the optional "show tags" view.
    # Tag node ids use a "tag:" prefix so they cannot collide with note ids
    # (4-char alphanumeric — no colon).
    unique_tags = sorted({t for n in notes.values() for t in n["tags"]})
    for tag in unique_tags:
        nodes.append({
            "id": f"tag:{tag}",
            "title": f"#{tag}",
            "date": "",
            "tags": [],
            "type": "tag",
        })

    # Build directed links that follow the actual authoring direction:
    # if note A contains a link to note B, the edge goes A → B.
    # Both A→B and B→A are kept if they exist independently.
    seen: set[tuple[str, str]] = set()
    links: list[dict] = []
    for note_id, note in notes.items():
        for target_id in note["links"]:
            if target_id not in notes:
                continue
            pair = (note_id, target_id)
            if pair in seen:
                continue
            seen.add(pair)
            links.append({"source": note_id, "target": target_id, "type": "note"})

    # note → tag membership edges
    for note_id, note in notes.items():
        for tag in note["tags"]:
            links.append({
                "source": note_id,
                "target": f"tag:{tag}",
                "type": "tag",
            })

    DOCS_DIR.mkdir(exist_ok=True)
    NOTES_DIR.mkdir(exist_ok=True)

    graph = {"nodes": nodes, "links": links}
    out_path = DOCS_DIR / "graph.json"
    out_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False))
    print(f"Wrote {out_path}  ({len(nodes)} nodes, {len(links)} links)")

    for note in notes.values():
        _render_note_html(note, set(notes.keys()))
    print(f"Rendered {len(notes)} note pages → {NOTES_DIR}")


if __name__ == "__main__":
    build_graph()
