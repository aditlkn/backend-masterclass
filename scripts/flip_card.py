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
    for m in re.finditer(r'<(div|a)\b[^>]*class="card[^"]*"[^>]*>', before):
        card_open = m
    if not card_open:
        print(f"ERROR: no card wrapper found before {day_str}"); return False

    base = max(0, idx-400)
    open_pos = base + card_open.start()
    open_end = base + card_open.end()
    tag = card_open.group(1)

    # Find matching close tag by scanning forward with proper tag boundary
    # Use regex to find all open/close tags of this type
    depth = 1  # we start after the opening tag
    i = open_end
    close_pos = len(c)
    open_re  = re.compile(r'<' + tag + r'\b')
    close_re = re.compile(r'</' + tag + r'>')
    while i < len(c):
        om = open_re.match(c, i)
        cm = close_re.match(c, i)
        if cm:
            depth -= 1
            if depth == 0:
                close_pos = cm.end()
                break
            i = cm.end()
        elif om:
            depth += 1
            i = om.end()
        else:
            i += 1

    old = c[open_pos:close_pos]
    print(f"Old ({len(old)}b): {repr(old[:70])}...")
    new_c = c[:open_pos] + new_card + c[close_pos:]

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
