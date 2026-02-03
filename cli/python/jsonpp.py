#!/usr/bin/env python3
"""Pretty print JSON from stdin or file"""
import sys
import json

data = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1]).read()
try:
    print(json.dumps(json.loads(data), indent=2))
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}", file=sys.stderr)
    sys.exit(1)
