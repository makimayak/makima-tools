#!/usr/bin/env python3
"""Simple web content fetcher - extracts readable text from URLs"""
import sys
import urllib.request
import html.parser
import re

class TextExtractor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header'}
    
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip = True
    
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip = False
    
    def handle_data(self, data):
        if not self.skip:
            text = data.strip()
            if text:
                self.text.append(text)

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as r:
        html_content = r.read().decode('utf-8', errors='ignore')
    
    parser = TextExtractor()
    parser.feed(html_content)
    return '\n'.join(parser.text)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: fetch.py <url>")
        sys.exit(1)
    print(fetch(sys.argv[1])[:5000])
