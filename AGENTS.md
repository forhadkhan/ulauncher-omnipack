# 🤖 AGENTS.md — AI-Optimized Development Guide

> **Project**: uLauncher OmniPack  
> **Repo**: `https://github.com/forhadkhan/ulauncher-omnipack`  
> **Target**: uLauncher Extension API v2  
> **Language**: Python 3.12+  
> **Last Sync**: 2026-05-11  

---

Note: Once you add a new feature or change any file, copy the file or whole root project directory (/home/forhad/projects/ulauncher-omnipack) to the directory of ulauncher extensions: `/home/forhad/.local/share/ulauncher/extensions/com.github.forhadkhan.ulauncher-omnipack`

---

## 🎯 AI Agent Instructions (Read First)

```yaml
# When you receive a task:
1. CHECK feature status table below for current state
2. REVIEW referenced example repos for implementation patterns
3. FOLLOW code standards & project structure strictly
4. TEST locally before committing (see Testing section)
5. UPDATE status + README after implementation
6. COPY files to uLauncher extensions dir post-change

# Decision rules:
- If feature is [PENDING]: implement from scratch using reference repos
- If feature is [WORKING]: review code, fix bugs, improve UX
- If feature is [COMPLETED]: only modify if bug reported or enhancement requested
- Always prefer modular design: one feature = one module file
- Never break existing working features when adding new ones
```

---

## 📊 Feature Matrix (Source of Truth)

| ID | Feature | Keyword | Status | Priority | Dependencies | Reference Repo(s) | Notes |
|----|---------|---------|--------|----------|-------------|-------------------|-------|
| F1 | UUID Generator | `uuid` | ✅ COMPLETED | Low | None | [fsevenm/ulauncher-uuid](https://github.com/fsevenm/ulauncher-uuid) | Supports UUID1/4/5 |
| F2 | File Search (grep/glob) | `f`, `file` | ✅ COMPLETED | High | None | [mariob88/grep-search](https://github.com/mariob88/ulauncher-grep-search), [brpaz/file-search](https://github.com/brpaz/ulauncher-file-search), [fisadev/better-file-browser](https://github.com/fisadev/ulauncher-better-file-browser) | Support recursive search, file previews |
| F3 | Empty Trash | `trash` | ✅ COMPLETED | Low | None | [EstebanForge/empty-trash](https://github.com/EstebanForge/ulauncher-empty-trash) | Added confirmation dialog |
| F4 | YouTube Search | `yt` | ⏳ PENDING | Medium | None | [NastuzziSamy/youtube-search](https://github.com/NastuzziSamy/ulauncher-youtube-search) | Use YouTube Data API v3 |
| F5 | Password Generator | `pass` | ✅ COMPLETED | Low | None | — | Configurable length/charset |
| F6 | Kill Process | `kill`, `ps` | ✅ COMPLETED | High | None | [isacikgoz/ukill](https://github.com/isacikgoz/ukill), [Eckhoff42/Kill-process](https://github.com/Eckhoff42/Ulauncher-Kill-process-on-click) | Modularized + search support |
| F7 | Kill Port | `port` | ✅ COMPLETED | High | F6 | [cosmincraciun97/port-killer](https://github.com/cosmincraciun97/port-killer-ulauncher), [Adii-5442/portKiller](https://github.com/Adii-5442/ulauncher-portKiller) | Modularized + lsof check |
| F8 | Google Search | `g`, `google` | ✅ COMPLETED | Low | None | — | Direct search URL |
| F9 | Google AI Mode | `ai`, `gemini` | ✅ COMPLETED | Medium | F8 | [khurrambhutto/google-ai-mode](https://github.com/khurrambhutto/ulauncher-google-ai-mode) | Link to Gemini/Google AI |
| F10 | Bluetooth Manager | `bt` | ⏳ PENDING | Medium | System: bluetoothctl | [Eckhoff42/Bluetooth-quick-connect](https://github.com/Eckhoff42/Ulauncher-Bluetooth-quick-connect), [elx4vier/UGoogle](https://github.com/elx4vier/UGoogle) | Show status, pair/connect flow |
| F11 | DuckDuckGo Search | `ddg` | ⏳ PENDING | Low | None | [mikebarkmin/ulauncher-duckduckgo](https://github.com/mikebarkmin/ulauncher-duckduckgo) | Privacy-focused search |
| F12 | Bing Search | `bing` | ⏳ PENDING | Low | None | — | Microsoft search engine |
| F13 | AI Aggregator | `ai` | ⏳ PENDING | Medium | None | [IgorVaryvoda/perplexity](https://github.com/IgorVaryvoda/ulauncher-perplexity) | Links to: Perplexity, Gemini, ChatGPT, Claude, Copilot |
| F14 | Calculator | `calc`, `=` | ✅ COMPLETED | High | None | [tchar/albert-calculate-anything](https://github.com/tchar/ulauncher-albert-calculate-anything) | Support math expressions, currency, units |
| F15 | IP Lookup | `ip` | ⏳ PENDING | Medium | None | [manahter/IP-Analysis](https://github.com/manahter/ulauncher-IP-Analysis), [munim/ip-lookup](https://github.com/munim/ulauncher-ip-lookup) | Local + public IP, IPv4/6, geolocation |
| F16 | Browser Profiles | `bbp`, `cbp` | ⏳ PENDING | Medium | OS-specific paths | [SinghRobinKumar/brave-profiles](https://github.com/SinghRobinKumar/ulauncher-brave-profiles), [FloydJohn/chrome-profiles](https://github.com/FloydJohn/ulauncher-chrome-profiles) | Detect installed browsers, list profiles |
| F17 | Word Dictionary | `w`, `ws`, `wa` | ⏳ PENDING | Low | API: dictionaryapi.dev | — | Definition/synonym/antonym via API |
| F18 | VS Code Workspaces | `vs`, `code` | ⏳ PENDING | Medium | User config: workspace files | [barathbheeman/vsw-extension](https://github.com/barathbheeman/vsw-extension/) | Scan `~/*.code-workspace`, recent projects |

### Status Legend
```
✅ COMPLETED  = Fully implemented, tested, documented
🔄 WORKING   = Implemented but needs bug fixes/UX polish
⏳ PENDING   = Not yet started
🚫 BLOCKED   = Cannot proceed (note reason in "Notes")
```

### Priority Legend
```
High   = Core utility, high user value, implement next
Medium = Useful feature, implement after High priority
Low    = Nice-to-have, implement when time permits
```

---

## 🗂️ Project Structure (AI-Readable)

```
ulauncher-omnipack/
├── AGENTS.md                  # [AI] This file: feature matrix, instructions, standards
├── CONTRIBUTING.md            # [HUMAN] Guidelines for human contributors
├── images/
│   └── icon.svg               # [ASSET] Main extension icon (128x128 scalable)
├── LICENSE                    # [LEGAL] MIT License
├── main.py                    # [ENTRY] Extension class + event routing (REQUIRED)
├── manifest.json              # [CONFIG] Metadata, preferences, API version (REQUIRED)
├── README.md                  # [DOCS] User guide: install, usage, keywords, FAQ
├── versions.json              # [RELEASE] API version → git commit mapping (REQUIRED)
├── src/
│   ├── core/
│   │   ├── extension.py       # [CORE] OmniExtension class with module registry
│   │   ├── events.py          # [CORE] Custom event handlers
│   │   └── actions.py         # [CORE] Reusable action helpers (copy, open, etc.)
│   └── modules/               # [FEATURES] One file per feature module
│       ├── base_module.py     # [ABSTRACT] BaseModule interface all modules inherit
│       ├── dev/
│       │   ├── uuid_gen.py    # [F1] UUID generator module
│       │   └── password_gen.py# [F5] Password generator module
│       ├── system/
│       │   ├── kill_process.py# [F6] Process killer module
│       │   ├── kill_port.py   # [F7] Port killer module
│       │   └── empty_trash.py # [F3] Trash empty module
│       ├── web/
│       │   ├── google_search.py   # [F8] Google search
│       │   ├── google_ai.py       # [F9] Google AI mode
│       │   ├── duckduckgo.py      # [F11] DDG search
│       │   ├── bing.py            # [F12] Bing search
│       │   ├── youtube.py         # [F4] YouTube search
│       │   └── ai_aggregator.py   # [F13] AI links aggregator
│       ├── utils/
│       │   ├── calculator.py  # [F14] Expression evaluator
│       │   ├── ip_lookup.py   # [F15] IP info fetcher
│       │   ├── file_search.py # [F2] Grep/glob/file finder
│       │   └── dictionary.py  # [F17] Word definition via API
│       └── apps/
│           ├── browser_profiles.py  # [F16] Brave/Chrome profile launcher
│           ├── vscode_workspaces.py # [F18] VS Code workspace opener
│           └── bluetooth_mgr.py     # [F10] Bluetooth device manager
├── tests/
│   ├── test_modules/          # [TEST] Unit tests per module
│   └── test_integration/      # [TEST] End-to-end event tests
└── docs/
    ├── MODULE_TEMPLATE.md     # [DEV] Copy-paste template for new modules
    └── API_NOTES.md           # [DEV] uLauncher API quirks & workarounds
```

> 💡 **AI Rule**: When adding a new feature → create ONE new file in `src/modules/{category}/` following `base_module.py` interface.

---

## 🧩 Module Implementation Template

```python
# src/modules/{category}/{feature}.py
"""
[FEATURE_ID] {Feature Name}
Keyword: {keyword}
Status: {PENDING|WORKING|COMPLETED}
"""
import logging
from src.modules.base_module import BaseModule
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.{Action} import {Action}  # e.g., CopyToClipboardAction

logger = logging.getLogger(__name__)

class {Feature}Module(BaseModule):
    """{Brief description}"""
    
    def get_keyword(self) -> str:
        """Return sub-keyword (e.g., 'uuid', 'kill')"""
        return "{keyword}"
    
    def get_icon(self) -> str:
        """Return relative path to module icon"""
        return f"images/module_{keyword}.png"  # or reuse extension icon
    
    def is_enabled(self) -> bool:
        """Check if user enabled this module via preferences"""
        prefs = self.extension.preferences
        enabled = prefs.get("enabled_modules", "all")
        return enabled in ["all", "{category}"]
    
    def handle_query(self, query: str) -> list[ExtensionResultItem]:
        """
        Process user input after keyword.
        Args: query: text after "omni {keyword} "
        Returns: list of ExtensionResultItem to display
        """
        items = []
        # TODO: Implement feature logic here
        # Example pattern:
        # 1. Parse/validate query
        # 2. Execute core logic (API call, system command, etc.)
        # 3. Build result items with actions
        # 4. Handle errors gracefully (log + show user-friendly message)
        return items
```

---

## ⚙️ Critical Configuration Files

### `manifest.json` — Must-Have Fields
```json
{
  "required_api_version": "^2.0.0",
  "name": "OmniPack",
  "description": "All-in-one productivity extension for uLauncher",
  "developer_name": "Forhad Khan",
  "icon": "images/icon.svg",
  "options": { "query_debounce": 0.1 },
  "preferences": [
    {
      "id": "omni_kw",
      "type": "keyword",
      "name": "OmniPack",
      "description": "Main trigger keyword",
      "default_value": "omni"
    },
    {
      "id": "enabled_modules",
      "type": "select",
      "name": "Active Module Groups",
      "description": "Enable/disable feature categories",
      "default_value": "all",
      "options": [
        {"value": "all", "text": "All"},
        {"value": "dev", "text": "Developer Tools"},
        {"value": "system", "text": "System Utilities"},
        {"value": "web", "text": "Web Search"},
        {"value": "utils", "text": "Utilities"}
      ]
    }
  ]
}
```

### `versions.json` — Release Mapping
```json
[{"required_api_version": "^2.0.0", "commit": "main"}]
```

---

## ✅ Code Standards (Non-Negotiable)

```python
# TYPE HINTS: Always use them
def process_query(query: str) -> list[ExtensionResultItem]: ...

# DOCSTRINGS: Google-style for public methods
def handle_query(self, query: str) -> list:
    """Process user input and return searchable results.
    
    Args:
        query: Text after the module keyword
        
    Returns:
        List of ExtensionResultItem objects for UI display
    """

# ERROR HANDLING: Never let exceptions crash the extension
try:
    result = risky_operation()
except Exception as e:
    logger.error(f"{self.get_keyword()} failed: {e}", exc_info=True)
    return [ExtensionResultItem(
        icon=self.get_icon(),
        name="Error",
        description="Operation failed. Check logs for details.",
        on_enter=None
    )]

# PATHS: Never hardcode
from pathlib import Path
MODULE_DIR = Path(__file__).parent
ICON_PATH = MODULE_DIR.parent.parent / "images" / "icon.svg"

# LOGGING: Use logger, not print()
logger.debug(f"Processing query: {query}")
logger.info(f"Found {len(items)} results for {self.get_keyword()}")

# EXTERNAL TOOLS: Check availability first
import shutil
if not shutil.which("lsof"):
    logger.warning("lsof not found; port killer may have limited functionality")
```

### Formatting Tools Config
```toml
# pyproject.toml
[tool.black]
line-length = 100
target-version = ["py312"]

[tool.flake8]
max-line-length = 100
exclude = ["__pycache__", "venv", ".git"]
ignore = ["E203", "W503"]
```

---

## 🧪 Testing Protocol (AI Must Follow)

```bash
# 1. Local development setup
ln -sfn $(pwd) ~/.local/share/ulauncher/extensions/com.github.forhadkhan.ulauncher-omnipack

# 2. Start uLauncher in verbose mode (separate terminal)
ulauncher -v 2>&1 | grep -i omnipack

# 3. Test your module manually
#    Type: "omni {keyword} {test_input}"
#    Verify: results appear, actions work, errors handled

# 4. Run unit tests (if writing tests)
python -m pytest tests/test_modules/test_{feature}.py -v

# 5. Check logs for errors
tail -f ~/.local/share/ulauncher/ulauncher.log | grep omnipack
```

### Test Cases Template
```python
# For each new module, test:
[ ] Empty query: handle_query("") → shows help/default options
[ ] Valid input: handle_query("valid") → returns expected results
[ ] Invalid input: handle_query("!@#") → graceful error, no crash
[ ] Special chars: handle_query("test with spaces") → properly escaped
[ ] Action trigger: on_enter executes correct action (copy, open, etc.)
[ ] Preferences: module disables when user toggles it off
```

---

## 🔄 Post-Implementation Checklist (AI: Execute After Coding)

```yaml
# After implementing/fixing a feature:
1. [ ] Update feature matrix status: PENDING→WORKING→COMPLETED
2. [ ] Add/update module entry in README.md "Available Commands" table
3. [ ] Run local test: "omni {keyword}" works as expected
4. [ ] Copy updated files to uLauncher extensions dir:
      cp -r /home/forhad/projects/ulauncher-omnipack/* \
            /home/forhad/.local/share/ulauncher/extensions/com.github.forhadkhan.ulauncher-omnipack/
5. [ ] Restart uLauncher or press Ctrl+R to reload extensions
6. [ ] Verify in UI: feature appears and functions correctly
7. [ ] Commit with descriptive message (see below)
8. [ ] Push to relevant branch (feature/{id}-short-name)

# Commit message format:
feat: add UDP support to port killer module
fix: handle permission denied when killing system processes
docs: update README with new uuid module examples
Note: Keep commits atomic and self-contained.
```

---

## 📚 Reference Repos — Quick Patterns

| Feature | Repo | Key Pattern to Reuse |
|---------|------|---------------------|
| F1 UUID | fsevenm/ulauncher-uuid | Simple generator + clipboard action |
| F2 File Search | brpaz/file-search | Recursive pathlib search + preview |
| F3 Trash | EstebanForge/empty-trash | os.trash() with confirmation dialog |
| F6 Kill Process | isacikgoz/ukill | psutil for process listing + signal |
| F7 Kill Port | cosmincraciun97/port-killer | subprocess + lsof/netstat parsing |
| F10 Bluetooth | Eckhoff42/Bluetooth-quick-connect | bluetoothctl CLI wrapper + state machine |
| F14 Calculator | tchar/albert-calculate-anything | ast.literal_eval for safe math parsing |
| F15 IP Lookup | munim/ip-lookup | requests + ipapi.co/ipleak.net API |
| F16 Browser Profiles | SinghRobinKumar/brave-profiles | OS-specific profile path detection |
| F18 VS Code | barathbheeman/vsw-extension | Scan ~/.config/Code/User/workspaceStorage |

> 🔍 **AI Tip**: Don't copy code directly. Study the pattern → adapt to OmniPack's modular architecture.

---

## 🚨 Troubleshooting Quick Reference

| Symptom | Likely Cause | AI Action |
|---------|-------------|-----------|
| Extension not loading | manifest.json syntax error | Validate JSON, check `required_api_version` |
| Keyword not triggering | Typo in preference default_value | Match `omni_kw` default with user input |
| No results shown | `handle_query()` returns empty list | Add debug logs, check query parsing |
| uLauncher freezes | Blocking I/O in event handler | Add `query_debounce: 1.0` or move to thread |
| Import error | Missing dependency | Add to `requirements.txt` or vendor the code |
| Icon not displaying | Wrong path in manifest/icon field | Use relative path: `images/icon.svg` |
| Preferences not saving | Wrong preference `id` in code | Use `self.preferences['pref_id']` exactly as defined |

### Debug Command
```bash
# Real-time extension logs
journalctl --user -u ulauncher -f  # systemd
# OR
tail -f ~/.local/share/ulauncher/ulauncher.log | grep -A5 -B5 omnipack
```

---

## 🎯 Next Actions for AI Agent

```yaml
# If you just started:
- [ ] Review this entire AGENTS.md file
- [ ] Verify local dev environment matches prerequisites
- [ ] Run existing COMPLETED features to understand baseline

# If implementing a PENDING feature:
- [ ] Pick HIGH priority feature first (F2, F6, F7, F14)
- [ ] Study referenced repo(s) for that feature
- [ ] Create new module file following base_module.py template
- [ ] Implement, test, then follow Post-Implementation Checklist

# If fixing a WORKING feature:
- [ ] Reproduce the reported issue locally
- [ ] Add logging to isolate the problem
- [ ] Fix + add regression test if possible
- [ ] Update status to COMPLETED when verified

# Always:
- [ ] Keep changes atomic: one feature/fix per commit
- [ ] Update documentation alongside code changes
- [ ] Ask for human review before marking COMPLETED
```

---

> ✨ **Golden Rule**: When in doubt, implement the simplest working version first. Refactor later.  
> 🔄 **Sync Reminder**: This file is the single source of truth for feature status. Update it FIRST when status changes.

*Maintainer: @forhadkhan • Auto-updated by AI agents • Last verified: 2026-05-11*