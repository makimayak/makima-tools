#!/usr/bin/env python3
"""Simple link/bookmark manager"""
import sys
import json
import os
from datetime import datetime

LINKS_FILE = os.path.expanduser("~/clawd/data/links.json")

def load_links():
    os.makedirs(os.path.dirname(LINKS_FILE), exist_ok=True)
    if os.path.exists(LINKS_FILE):
        return json.load(open(LINKS_FILE))
    return []

def save_links(links):
    json.dump(links, open(LINKS_FILE, 'w'), indent=2)

def add_link(url, title="", tags=""):
    links = load_links()
    links.append({
        "url": url,
        "title": title or url,
        "tags": tags.split(",") if tags else [],
        "added": datetime.now().isoformat()
    })
    save_links(links)
    print(f"✓ Added: {title or url}")

def list_links(tag=None):
    links = load_links()
    for link in links:
        if tag is None or tag in link.get("tags", []):
            tags = " ".join(f"[{t}]" for t in link.get("tags", []))
            print(f"• {link['title']} {tags}")
            print(f"  {link['url']}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: links.py add <url> [title] [tags]")
        print("       links.py list [tag]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) >= 3:
        add_link(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "", sys.argv[4] if len(sys.argv) > 4 else "")
    elif cmd == "list":
        list_links(sys.argv[2] if len(sys.argv) > 2 else None)
