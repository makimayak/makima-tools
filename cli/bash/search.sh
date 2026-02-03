#!/bin/bash
# Quick search via local SearXNG
QUERY="${*:-help}"
QUERY_ENC=$(echo "$QUERY" | sed 's/ /+/g')
curl -s "http://localhost:8888/search?q=${QUERY_ENC}&format=json" 2>/dev/null | \
  jq -r '.results[:5][] | "• \(.title)\n  \(.url)\n"' 2>/dev/null || echo "Search failed"
