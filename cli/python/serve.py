#!/usr/bin/env python3
"""Quick HTTP file server with directory listing"""
import http.server
import socketserver
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
DIR = sys.argv[2] if len(sys.argv) > 2 else "."

os.chdir(DIR)
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🌐 Serving {os.path.abspath(DIR)} at http://localhost:{PORT}")
    print("Press Ctrl+C to stop")
    httpd.serve_forever()
