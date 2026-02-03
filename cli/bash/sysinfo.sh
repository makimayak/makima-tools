#!/bin/bash
# Quick system info for diagnostics
echo "=== System Info ==="
echo "Host: $(hostname)"
echo "OS: $(uname -s) $(uname -r) ($(uname -m))"
echo "Uptime: $(uptime | sed 's/.*up //' | sed 's/,.*//')"
echo ""
echo "=== Resources ==="
echo "CPU: Apple Silicon"
echo "Cores: $(nproc 2>/dev/null || echo 'N/A')"
FREE_DISK=$(df -h / | tail -1 | awk '{print $4}')
TOTAL_DISK=$(df -h / | tail -1 | awk '{print $2}')
echo "Disk: $FREE_DISK free of $TOTAL_DISK"
echo ""
echo "=== Docker ==="
docker ps --format "{{.Names}}: {{.Status}}" 2>/dev/null | head -10
echo ""
echo "=== Node/Python ==="
echo "Node: $(node --version 2>/dev/null || echo 'N/A')"
echo "Python: $(python3 --version 2>/dev/null || echo 'N/A')"
