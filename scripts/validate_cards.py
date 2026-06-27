#!/usr/bin/env python3
"""Validate landing page card structure. Run before every push."""
import re, sys

with open('index.html') as f:
    c = f.read()

errors = []

# Check 1: No orphan locked div wrapping a live <a>
bad = re.findall(r'<div class="card locked"[^>]*><a href=', c)
if bad:
    errors.append(f"Orphan locked+live div wrapping live <a>: {len(bad)} found")

# Check 2: No stray card-title/tags divs after a card close tag
stray = re.findall(r'(?:</a>|</div></div>)\s*<div class="card-title">', c)
if stray:
    errors.append(f"Stray card-title immediately after card close tag: {len(stray)} found")

# Check 3: Every card-title preceded by card-top
for m in re.finditer(r'<div class="card-title">', c):
    pos = m.start()
    before = c[max(0, pos-300):pos]
    if '<div class="card-top">' not in before:
        errors.append(f"card-title with no card-top at {pos}: {repr(c[pos:pos+50])}")

# Check 4: No </a></div> on the same line (grid close merged onto card close)
# This puts subsequent cards outside the grid
merged = re.findall(r'</a></div>', c)
if merged:
    errors.append(f"</a></div> on same line (grid close merged onto card): {len(merged)} found — breaks grid layout")

# Inventory
live   = re.findall(r'<a href="/day(\d+)" class="card live"', c)
locked = re.findall(r'class="card locked"', c)
print(f"Live  ({len(live)}): {sorted(int(d) for d in live)}")
print(f"Locked: {len(locked)}")

if errors:
    print("\nERRORS:")
    for e in errors: print(f"  ✗ {e}")
    sys.exit(1)
else:
    print("✓ All cards clean")
