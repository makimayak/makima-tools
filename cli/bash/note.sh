#!/bin/bash
# Quick note-taking tool
NOTES_DIR="$HOME/clawd/memory"
TODAY=$(date +%Y-%m-%d)
NOTE_FILE="$NOTES_DIR/$TODAY.md"

mkdir -p "$NOTES_DIR"

if [ -z "$1" ]; then
    # Show today's notes
    if [ -f "$NOTE_FILE" ]; then
        cat "$NOTE_FILE"
    else
        echo "No notes for today."
    fi
else
    # Add a note
    echo "- $(date +%H:%M) $*" >> "$NOTE_FILE"
    echo "Note added to $NOTE_FILE"
fi
