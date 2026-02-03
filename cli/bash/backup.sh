#!/bin/bash
# Quick backup script
BACKUP_DIR="${HOME}/clawd/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup clawd workspace
tar -czf "$BACKUP_DIR/clawd_${TIMESTAMP}.tar.gz" \
    --exclude="backups" \
    --exclude="node_modules" \
    --exclude=".git" \
    -C "$HOME" clawd 2>/dev/null

echo "✓ Backup created: $BACKUP_DIR/clawd_${TIMESTAMP}.tar.gz"
ls -lh "$BACKUP_DIR/clawd_${TIMESTAMP}.tar.gz"
