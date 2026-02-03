#!/bin/bash
# Daily check script for Makima
echo "=== Daily Check $(date) ==="

# Check services
echo -e "\n📦 Docker Services:"
docker ps --format "  {{.Names}}: {{.Status}}" 2>/dev/null | head -10

# Check disk space
echo -e "\n💾 Disk Space:"
df -h / | tail -1 | awk '{print "  " $4 " free of " $2 " (" $5 " used)"}'

# Check memory
echo -e "\n🧠 Memory:"
vm_stat 2>/dev/null | head -5 || echo "  (unavailable)"

# Check Ollama models
echo -e "\n🤖 Ollama Models:"
ollama list 2>/dev/null | tail -n +2 | awk '{print "  " $1}' | head -5

# Check for updates
echo -e "\n📥 Package Updates:"
brew outdated 2>/dev/null | head -5 || echo "  (checking...)"

echo -e "\n✅ Daily check complete"
