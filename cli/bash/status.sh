#!/bin/bash
# Makima Status Report
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🔴 MAKIMA STATUS REPORT                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📅 $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo ""
echo "=== 🐳 Docker Services ==="
docker ps --format "  ✓ {{.Names}}: {{.Status}}" 2>/dev/null | head -10

echo ""
echo "=== 🤖 Ollama Models ==="
ollama list 2>/dev/null | tail -n +2 | awk '{print "  • " $1}'

echo ""
echo "=== 📁 Projects Built ==="
ls -1 ~/clawd/projects/*.{py,sh} 2>/dev/null | xargs -I{} basename {} | sed 's/^/  • /'

echo ""
echo "=== 📋 Tasks ==="
if [ -f ~/clawd/data/tasks.json ]; then
    python3 -c "
import json
tasks = json.load(open('$HOME/clawd/data/tasks.json'))
for t in tasks:
    status = '✓' if t['done'] else '○'
    prio = '!' if t.get('priority') == 'high' else ''
    print(f'  {status} [{t[\"id\"]}] {prio}{t[\"description\"]}')"
fi

echo ""
echo "=== 💾 Storage ==="
df -h / | tail -1 | awk '{print "  Disk: " $4 " free of " $2 " (" $5 " used)"}'

echo ""
echo "══════════════════════════════════════════════════════════════"
