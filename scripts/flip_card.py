#!/usr/bin/env python3
"""Atomically flip a day card from locked to live. No partial replacements."""
import re, sys

def flip_card(day_num, href, title, tags_html, meta="~55 min|8 interactives"):
    with open('index.html') as f:
        c = f.read()

    day_str = f'DAY {int(day_num):02d}'
    meta_parts = meta.split('|')
    meta_html = ''.join(
        f'<span>⏱ {p.strip()}</span>' if 'min' in p else f'<span>⚙ {p.strip()}</span>'
        for p in meta_parts
    )
    new_card = (
        f'<a href="{href}" class="card live" style="--c:var(--w3)">\n'
        f'        <div class="card-top"><span class="day-num">{day_str}</span>'
        f'<span class="badge badge-live">Available</span></div>\n'
        f'        <div class="card-title">{title}</div>\n'
        f'        <div class="tags">{tags_html}</div>\n'
        f'        <div class="card-meta">{meta_html}</div>\n'
        f'      </a>'
    )

    idx = c.find(day_str)
    if idx < 0:
        print(f"ERROR: {day_str} not found"); return False

    # Find the card wrapper opening tag before this day string
    before = c[max(0, idx-400):idx]
    card_open = None
    for m in re.finditer(r'<(div|a)\s[^>]*class="card[^"]*"[^>]*>', before):
        card_open = m
    if not card_open:
        print(f"ERROR: no card wrapper found before {day_str}"); return False

    base = max(0, idx-400)
    open_pos = base + card_open.start()
    tag = card_open.group(1)

    # Walk forward to find the matching closing tag
    depth, i = 0, open_pos
    while i < len(c):
        if re.match(r'<' + tag + r'[\s>]', c[i:]):
            depth += 1; i += 1
        elif re.match(r'</' + tag + r'>', c[i:]):
            depth -= 1; i += len(tag) + 3
            if depth == 0: break
        else:
            i += 1

    old = c[open_pos:i]
    print(f"Old ({len(old)}b): {repr(old[:70])}...")
    new_c = c[:open_pos] + new_card + c[i:]

    with open('index.html', 'w') as f:
        f.write(new_c)
    print(f"✓ {day_str} flipped to live")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: flip_card.py <day> <href> <title> <tags_html> [meta]")
        sys.exit(1)
    flip_card(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
              sys.argv[5] if len(sys.argv) > 5 else "~55 min|8 interactives")
