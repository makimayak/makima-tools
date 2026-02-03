#!/bin/bash
# Quick weather check - spaces become underscores
LOCATION="${1:-Los Angeles}"
LOCATION_URL=$(echo "$LOCATION" | tr ' ' '_')
curl -s "https://wttr.in/${LOCATION_URL}?format=3" 2>/dev/null || echo "Weather unavailable"
