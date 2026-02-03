#!/usr/bin/env python3
"""
Makima's Vector Memory System 🔴

Stores and retrieves memories using Qdrant + Ollama embeddings.
Everything I learn, remember, and experience goes here.
"""

import argparse
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

import httpx

QDRANT_URL = "http://localhost:6333"
OLLAMA_URL = "http://localhost:11434"
COLLECTION = "makima_memory"


def get_embedding(text: str) -> list[float]:
    """Get embedding from Ollama's nomic-embed-text."""
    resp = httpx.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]


def store_memory(
    text: str,
    memory_type: str = "general",
    source: str = "manual",
    metadata: dict | None = None,
) -> str:
    """Store a memory in Qdrant."""
    memory_id = str(uuid.uuid4())
    embedding = get_embedding(text)
    
    payload = {
        "text": text,
        "type": memory_type,
        "source": source,
        "timestamp": datetime.now().isoformat(),
        "id": memory_id,
    }
    if metadata:
        payload.update(metadata)
    
    resp = httpx.put(
        f"{QDRANT_URL}/collections/{COLLECTION}/points",
        json={
            "points": [
                {
                    "id": memory_id,
                    "vector": embedding,
                    "payload": payload,
                }
            ]
        },
        timeout=30,
    )
    resp.raise_for_status()
    return memory_id


def search_memories(query: str, limit: int = 5) -> list[dict]:
    """Search memories by semantic similarity."""
    embedding = get_embedding(query)
    
    resp = httpx.post(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/search",
        json={
            "vector": embedding,
            "limit": limit,
            "with_payload": True,
        },
        timeout=30,
    )
    resp.raise_for_status()
    
    results = []
    for hit in resp.json()["result"]:
        results.append({
            "score": hit["score"],
            "text": hit["payload"].get("text", ""),
            "type": hit["payload"].get("type", ""),
            "source": hit["payload"].get("source", ""),
            "timestamp": hit["payload"].get("timestamp", ""),
        })
    return results


def ingest_file(filepath: str, chunk_size: int = 500) -> int:
    """Ingest a file into memory, chunking if needed."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    content = path.read_text()
    filename = path.name
    
    # Simple chunking by paragraphs or size
    chunks = []
    current_chunk = ""
    
    for line in content.split("\n"):
        if len(current_chunk) + len(line) > chunk_size:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    count = 0
    for i, chunk in enumerate(chunks):
        if len(chunk) > 50:  # Skip very short chunks
            store_memory(
                text=chunk,
                memory_type="document",
                source=filename,
                metadata={"chunk_index": i, "filepath": str(path)},
            )
            count += 1
    
    return count


def ingest_session_logs(sessions_dir: str) -> int:
    """Ingest session logs from Clawdbot."""
    sessions_path = Path(sessions_dir)
    if not sessions_path.exists():
        raise FileNotFoundError(f"Sessions directory not found: {sessions_dir}")
    
    count = 0
    for jsonl_file in sessions_path.glob("*.jsonl"):
        if ".deleted." in jsonl_file.name:
            continue
        
        with open(jsonl_file) as f:
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
                            if len(text) > 50:
                                store_memory(
                                    text=text[:2000],  # Limit size
                                    memory_type="conversation",
                                    source=jsonl_file.name,
                                    metadata={
                                        "role": role,
                                        "original_timestamp": timestamp,
                                    },
                                )
                                count += 1
                except json.JSONDecodeError:
                    continue
    
    return count


def get_stats() -> dict:
    """Get collection statistics."""
    resp = httpx.get(f"{QDRANT_URL}/collections/{COLLECTION}", timeout=10)
    resp.raise_for_status()
    data = resp.json()["result"]
    return {
        "vectors_count": data.get("vectors_count", 0),
        "points_count": data.get("points_count", 0),
        "status": data.get("status", "unknown"),
    }


def main():
    parser = argparse.ArgumentParser(description="Makima's Vector Memory System 🔴")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Store command
    store_parser = subparsers.add_parser("store", help="Store a memory")
    store_parser.add_argument("text", help="Memory text to store")
    store_parser.add_argument("-t", "--type", default="general", help="Memory type")
    store_parser.add_argument("-s", "--source", default="manual", help="Source")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search memories")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("-n", "--limit", type=int, default=5, help="Max results")
    
    # Ingest file command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest a file")
    ingest_parser.add_argument("filepath", help="File to ingest")
    
    # Ingest sessions command
    sessions_parser = subparsers.add_parser("ingest-sessions", help="Ingest session logs")
    sessions_parser.add_argument("sessions_dir", help="Sessions directory")
    
    # Stats command
    subparsers.add_parser("stats", help="Show collection stats")
    
    args = parser.parse_args()
    
    if args.command == "store":
        memory_id = store_memory(args.text, args.type, args.source)
        print(json.dumps({"ok": True, "id": memory_id}))
    
    elif args.command == "search":
        results = search_memories(args.query, args.limit)
        print(json.dumps(results, indent=2))
    
    elif args.command == "ingest":
        count = ingest_file(args.filepath)
        print(json.dumps({"ok": True, "chunks_stored": count}))
    
    elif args.command == "ingest-sessions":
        count = ingest_session_logs(args.sessions_dir)
        print(json.dumps({"ok": True, "messages_stored": count}))
    
    elif args.command == "stats":
        stats = get_stats()
        print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
