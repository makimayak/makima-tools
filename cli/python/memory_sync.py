#!/usr/bin/env python3
"""
Memory Sync - Auto-ingest new conversations into vector memory.

Tracks what's been ingested and only adds new content.
Run periodically via cron or heartbeat.
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Import from memory_store
import sys
sys.path.insert(0, str(Path(__file__).parent))
from memory_store import store_memory, get_stats

SESSIONS_DIR = Path.home() / ".clawdbot/agents/main/sessions"
STATE_FILE = Path.home() / "clawd/memory/sync-state.json"
MEMORY_DIR = Path.home() / "clawd/memory"


def load_state() -> dict:
    """Load sync state."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_positions": {}, "last_sync": None}


def save_state(state: dict):
    """Save sync state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def sync_session_logs(state: dict) -> int:
    """Sync new messages from session logs."""
    count = 0
    positions = state.get("last_positions", {})
    
    for jsonl_file in SESSIONS_DIR.glob("*.jsonl"):
        if ".deleted." in jsonl_file.name or ".lock" in jsonl_file.name:
            continue
        
        file_key = jsonl_file.name
        last_pos = positions.get(file_key, 0)
        current_size = jsonl_file.stat().st_size
        
        if current_size <= last_pos:
            continue  # No new content
        
        with open(jsonl_file) as f:
            f.seek(last_pos)
            for line in f:
                try:
                    msg = json.loads(line)
                    if msg.get("type") != "message":
                        continue
                    
                    role = msg.get("message", {}).get("role", "")
                    contents = msg.get("message", {}).get("content", [])
                    timestamp = msg.get("timestamp", "")
                    
                    for content in contents:
                        if content.get("type") == "text":
                            text = content.get("text", "")
                            if len(text) > 50 and len(text) < 5000:
                                store_memory(
                                    text=text[:2000],
                                    memory_type="conversation",
                                    source=file_key,
                                    metadata={
                                        "role": role,
                                        "original_timestamp": timestamp,
                                    },
                                )
                                count += 1
                except json.JSONDecodeError:
                    continue
        
        positions[file_key] = current_size
    
    state["last_positions"] = positions
    return count


def sync_memory_files(state: dict) -> int:
    """Sync new/updated memory markdown files."""
    count = 0
    file_hashes = state.get("file_hashes", {})
    
    for md_file in MEMORY_DIR.glob("*.md"):
        file_key = md_file.name
        current_hash = str(md_file.stat().st_mtime)
        
        if file_hashes.get(file_key) == current_hash:
            continue  # No changes
        
        content = md_file.read_text()
        chunks = []
        current_chunk = ""
        
        for line in content.split("\n"):
            if len(current_chunk) + len(line) > 500:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = line + "\n"
            else:
                current_chunk += line + "\n"
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        for chunk in chunks:
            if len(chunk) > 50:
                store_memory(
                    text=chunk,
                    memory_type="document",
                    source=file_key,
                )
                count += 1
        
        file_hashes[file_key] = current_hash
    
    state["file_hashes"] = file_hashes
    return count


def main():
    state = load_state()
    
    session_count = sync_session_logs(state)
    memory_count = sync_memory_files(state)
    
    state["last_sync"] = datetime.now().isoformat()
    save_state(state)
    
    stats = get_stats()
    
    result = {
        "ok": True,
        "new_session_messages": session_count,
        "new_memory_chunks": memory_count,
        "total_memories": stats["points_count"],
        "last_sync": state["last_sync"],
    }
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
