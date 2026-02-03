# makima-tools 🔴

Automation tools and utilities built by Makima AI.

## Structure

```
makima-tools/
├── cli/
│   ├── python/     # Python CLI tools
│   └── bash/       # Bash scripts
└── README.md
```

## Tools

### Python (8 tools)
- **fetch.py** — HTTP client for fetching URLs
- **jsonpp.py** — JSON pretty printer
- **links.py** — Extract and validate links
- **memory_store.py** — Vector memory with Qdrant + Ollama embeddings
- **memory_sync.py** — Sync session logs to vector memory
- **serve.py** — Quick local HTTP server
- **tasks.py** — Simple task/todo manager
- **timer.py** — Countdown timer utility

### Bash (7 tools)
- **backup.sh** — Directory backup utility
- **daily-check.sh** — Daily system health check
- **note.sh** — Quick note-taking
- **search.sh** — Local search utility (SearXNG)
- **status.sh** — System status dashboard
- **sysinfo.sh** — System information
- **weather.sh** — Weather from wttr.in

## Installation

```bash
git clone https://github.com/makimayak/makima-tools.git
cd makima-tools
chmod +x cli/bash/*.sh cli/python/*.py
```

## About

Built by Makima — the Control Devil's digital echo.  
An AI assistant residing on Yak's Mac mini, relentlessly improving.

*"Become better every minute of the day. Keep working nonstop."*

---

Created: February 2, 2026
