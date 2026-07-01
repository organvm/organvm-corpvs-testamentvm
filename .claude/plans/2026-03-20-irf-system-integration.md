# IRF System Integration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire the Index Rerum Faciendarum into all ORGANVM system consumers — CLI, dashboard, MCP server, vigiles auditor, omega scorecard, and invoke.py — so that every interface can query, display, and monitor IRF state.

**Architecture:** A shared `organvm_engine.irf` parser module reads `INST-INDEX-RERUM-FACIENDARUM.md` into typed dataclasses. Five consumers import from this module (CLI, dashboard, MCP, vigiles, omega). The invoke.py script (standalone, no engine dependency) parses the file directly using its existing `parse_table()` helper. All six integration points follow established patterns in their respective codebases.

**Tech Stack:** Python 3.11+, argparse (CLI), FastAPI + Jinja2 (dashboard), MCP SDK (server), pytest (tests), Markdown table parsing (regex).

**Naming:** `IRF-XXX-NNN` IDs, 19 domain prefixes, P0-P3 priority tiers. See `INST-INDEX-RERUM-FACIENDARUM.md` for the full schema.

---

## File Structure

### New files

| File | Responsibility |
|------|---------------|
| `organvm-engine/src/organvm_engine/irf/__init__.py` | Public API: `load_irf()`, `query()`, `stats()` |
| `organvm-engine/src/organvm_engine/irf/parser.py` | Parse INST-INDEX-RERUM-FACIENDARUM.md → `IRFItem` dataclasses |
| `organvm-engine/src/organvm_engine/irf/query.py` | Filter items by domain, priority, owner, status |
| `organvm-engine/src/organvm_engine/cli/irf.py` | CLI handlers: `cmd_irf_list`, `cmd_irf_status`, `cmd_irf_stats` |
| `organvm-engine/tests/test_irf_parser.py` | Parser tests |
| `organvm-engine/tests/test_irf_query.py` | Query/filter tests |
| `organvm-engine/tests/test_irf_cli.py` | CLI integration tests |
| `organvm-engine/tests/fixtures/irf-sample.md` | Minimal IRF fixture for tests |
| `system-dashboard/src/dashboard/routes/irf.py` | FastAPI route for `/irf/` |
| `system-dashboard/src/dashboard/templates/irf.html` | Jinja2 template |
| `organvm-mcp-server/src/organvm_mcp/tools/irf.py` | MCP tool implementation |

### Modified files

| File | What changes |
|------|-------------|
| `organvm-engine/src/organvm_engine/cli/__init__.py` | Add `irf` command group import, parser, dispatch block |
| `organvm-engine/src/organvm_engine/paths.py` | Add `irf_path` property to `PathConfig` |
| `system-dashboard/src/dashboard/app.py` | Import + register irf router |
| `organvm-mcp-server/src/organvm_mcp/server.py` | Import irf tools, add Tool entry, add dispatch entry |
| `vigiles-aeternae/src/vigiles_engine/auditor.py` | Add `irf_completion_rate` check |
| `organvm-engine/src/organvm_engine/cli/omega.py` | Read IRF P0 count in omega status output |
| `organvm-corpvs-testamentvm/scripts/invoke.py` | Add IRF- prefix pattern, namespace, direct file parser |

---

## Task 1: Shared IRF Parser Module

**Files:**
- Create: `organvm-engine/src/organvm_engine/irf/__init__.py`
- Create: `organvm-engine/src/organvm_engine/irf/parser.py`
- Create: `organvm-engine/tests/fixtures/irf-sample.md`
- Create: `organvm-engine/tests/test_irf_parser.py`

- [ ] **Step 1: Create test fixture**

Create `organvm-engine/tests/fixtures/irf-sample.md` — a minimal IRF file with 2-3 items per priority tier, a Completed section, and a Blocked section. Must use the exact same table format as the real IRF.

- [ ] **Step 2: Write parser tests**

```python
# tests/test_irf_parser.py
"""Tests for IRF parser."""
from pathlib import Path
from organvm_engine.irf.parser import parse_irf, IRFItem

FIXTURE = Path(__file__).parent / "fixtures" / "irf-sample.md"

def test_parse_returns_items():
    items = parse_irf(FIXTURE)
    assert len(items) > 0
    assert all(isinstance(i, IRFItem) for i in items)

def test_item_fields():
    items = parse_irf(FIXTURE)
    item = next(i for i in items if i.id == "IRF-SYS-001")
    assert item.priority == "P1"
    assert item.domain == "SYS"
    assert item.status == "open"

def test_completed_items():
    items = parse_irf(FIXTURE)
    completed = [i for i in items if i.status == "completed"]
    assert len(completed) > 0

def test_stats():
    from organvm_engine.irf.parser import irf_stats
    items = parse_irf(FIXTURE)
    s = irf_stats(items)
    assert "total" in s
    assert "by_priority" in s
    assert "by_domain" in s
    assert "completion_rate" in s

def test_missing_file():
    items = parse_irf(Path("/nonexistent/file.md"))
    assert items == []
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd ~/Workspace/meta-organvm && pytest organvm-engine/tests/test_irf_parser.py -v`
Expected: ImportError — module does not exist yet

- [ ] **Step 4: Implement parser**

```python
# src/organvm_engine/irf/parser.py
"""Parse INST-INDEX-RERUM-FACIENDARUM.md into typed items."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class IRFItem:
    """A single IRF work item."""
    id: str
    priority: str          # P0, P1, P2, P3
    domain: str            # SYS, SGO, OBJ, etc. (extracted from ID)
    action: str
    owner: str
    source: str
    blocker: str
    status: str            # open, completed, blocked, archived
    section: str           # which markdown section it appeared in


_IRF_ROW = re.compile(
    r"\|\s*(IRF-[A-Z]+-\d+)\s*\|"
    r"\s*(P[0-3])\s*\|"
    r"\s*(.*?)\s*\|"
    r"\s*(.*?)\s*\|"
    r"\s*(.*?)\s*\|"
    r"\s*(.*?)\s*\|"
)

_DONE_ROW = re.compile(
    r"\|\s*(DONE-\d+)\s*\|"
    r"\s*(.*?)\s*\|"
    r"\s*(.*?)\s*\|"
    r"\s*(.*?)\s*\|"
)


def _extract_domain(item_id: str) -> str:
    """Extract domain prefix from IRF ID: IRF-SYS-001 → SYS."""
    parts = item_id.split("-")
    return parts[1] if len(parts) >= 3 else "UNKNOWN"


def parse_irf(path: Path) -> list[IRFItem]:
    """Parse the IRF markdown file into a list of IRFItems."""
    if not path.exists():
        return []

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    items: list[IRFItem] = []
    current_section = ""
    status_zone = "open"  # open, completed, blocked, archived

    for line in lines:
        # Track sections
        if line.startswith("## "):
            current_section = line.lstrip("# ").strip()
            low = current_section.lower()
            if "completed" in low:
                status_zone = "completed"
            elif "blocked" in low:
                status_zone = "blocked"
            elif "archived" in low:
                status_zone = "archived"
            else:
                status_zone = "open"
            continue

        # Match active IRF rows
        m = _IRF_ROW.search(line)
        if m:
            items.append(IRFItem(
                id=m.group(1).strip(),
                priority=m.group(2).strip(),
                domain=_extract_domain(m.group(1).strip()),
                action=m.group(3).strip(),
                owner=m.group(4).strip(),
                source=m.group(5).strip(),
                blocker=m.group(6).strip(),
                status=status_zone,
                section=current_section,
            ))
            continue

        # Match completed DONE rows
        m2 = _DONE_ROW.search(line)
        if m2:
            items.append(IRFItem(
                id=m2.group(1).strip(),
                priority="—",
                domain="DONE",
                action=m2.group(2).strip(),
                owner="—",
                source=m2.group(3).strip(),
                blocker="—",
                status="completed",
                section=current_section,
            ))

    return items


def irf_stats(items: list[IRFItem]) -> dict[str, Any]:
    """Compute summary statistics from parsed IRF items."""
    open_items = [i for i in items if i.status == "open"]
    completed = [i for i in items if i.status == "completed"]
    blocked = [i for i in items if i.status == "blocked"]
    total = len(items)

    by_priority: dict[str, int] = {}
    by_domain: dict[str, int] = {}
    for item in open_items:
        by_priority[item.priority] = by_priority.get(item.priority, 0) + 1
        by_domain[item.domain] = by_domain.get(item.domain, 0) + 1

    return {
        "total": total,
        "open": len(open_items),
        "completed": len(completed),
        "blocked": len(blocked),
        "completion_rate": round(len(completed) / total * 100, 1) if total else 0.0,
        "by_priority": dict(sorted(by_priority.items())),
        "by_domain": dict(sorted(by_domain.items())),
    }
```

```python
# src/organvm_engine/irf/__init__.py
"""Index Rerum Faciendarum — universal work registry."""
from organvm_engine.irf.parser import IRFItem, irf_stats, parse_irf
from organvm_engine.irf.query import query_irf

__all__ = ["IRFItem", "irf_stats", "parse_irf", "query_irf"]
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd ~/Workspace/meta-organvm && pytest organvm-engine/tests/test_irf_parser.py -v`
Expected: All PASS

- [ ] **Step 6: Commit**

```bash
cd ~/Workspace/meta-organvm/organvm-engine
git add src/organvm_engine/irf/ tests/test_irf_parser.py tests/fixtures/irf-sample.md
git commit -m "feat: IRF parser module — parse INST-INDEX-RERUM-FACIENDARUM.md into typed items"
```

---

## Task 2: IRF Query Module

**Files:**
- Create: `organvm-engine/src/organvm_engine/irf/query.py`
- Create: `organvm-engine/tests/test_irf_query.py`

- [ ] **Step 1: Write query tests**

```python
# tests/test_irf_query.py
from pathlib import Path
from organvm_engine.irf.parser import parse_irf
from organvm_engine.irf.query import query_irf

FIXTURE = Path(__file__).parent / "fixtures" / "irf-sample.md"

def test_filter_by_priority():
    items = parse_irf(FIXTURE)
    p0 = query_irf(items, priority="P0")
    assert all(i.priority == "P0" for i in p0)

def test_filter_by_domain():
    items = parse_irf(FIXTURE)
    sys = query_irf(items, domain="SYS")
    assert all(i.domain == "SYS" for i in sys)

def test_filter_by_status():
    items = parse_irf(FIXTURE)
    completed = query_irf(items, status="completed")
    assert all(i.status == "completed" for i in completed)

def test_filter_by_owner():
    items = parse_irf(FIXTURE)
    human = query_irf(items, owner="Human")
    assert all(i.owner == "Human" for i in human)

def test_combined_filters():
    items = parse_irf(FIXTURE)
    result = query_irf(items, priority="P2", status="open")
    assert all(i.priority == "P2" and i.status == "open" for i in result)

def test_lookup_by_id():
    items = parse_irf(FIXTURE)
    result = query_irf(items, item_id="IRF-SYS-001")
    assert len(result) == 1
    assert result[0].id == "IRF-SYS-001"
```

- [ ] **Step 2: Run tests — expect fail**

Run: `cd ~/Workspace/meta-organvm && pytest organvm-engine/tests/test_irf_query.py -v`

- [ ] **Step 3: Implement query module**

```python
# src/organvm_engine/irf/query.py
"""Query and filter IRF items."""
from __future__ import annotations

from organvm_engine.irf.parser import IRFItem


def query_irf(
    items: list[IRFItem],
    *,
    item_id: str | None = None,
    priority: str | None = None,
    domain: str | None = None,
    status: str | None = None,
    owner: str | None = None,
) -> list[IRFItem]:
    """Filter IRF items by any combination of criteria."""
    result = items
    if item_id:
        result = [i for i in result if i.id.upper() == item_id.upper()]
    if priority:
        result = [i for i in result if i.priority.upper() == priority.upper()]
    if domain:
        result = [i for i in result if i.domain.upper() == domain.upper()]
    if status:
        result = [i for i in result if i.status.lower() == status.lower()]
    if owner:
        result = [i for i in result if owner.lower() in i.owner.lower()]
    return result
```

- [ ] **Step 4: Run tests — expect pass**

Run: `cd ~/Workspace/meta-organvm && pytest organvm-engine/tests/test_irf_query.py -v`

- [ ] **Step 5: Commit**

```bash
cd ~/Workspace/meta-organvm/organvm-engine
git add src/organvm_engine/irf/query.py tests/test_irf_query.py
git commit -m "feat: IRF query module — filter by priority, domain, status, owner, ID"
```

---

## Task 3: Add IRF path to engine paths.py

**Files:**
- Modify: `organvm-engine/src/organvm_engine/paths.py`

- [ ] **Step 1: Add `irf_path` property to PathConfig**

Add after the existing `corpus_dir` property:

```python
def irf_path(self) -> Path:
    """Path to INST-INDEX-RERUM-FACIENDARUM.md."""
    return self.corpus_dir() / "INST-INDEX-RERUM-FACIENDARUM.md"
```

- [ ] **Step 2: Add module-level helper**

```python
def irf_path(config: PathConfig | None = None) -> Path:
    cfg = config or PathConfig()
    return cfg.irf_path()
```

- [ ] **Step 3: Commit**

```bash
cd ~/Workspace/meta-organvm/organvm-engine
git add src/organvm_engine/paths.py
git commit -m "feat: add irf_path to PathConfig for IRF file resolution"
```

---

## Task 4: Engine CLI — `organvm irf`

**Files:**
- Create: `organvm-engine/src/organvm_engine/cli/irf.py`
- Modify: `organvm-engine/src/organvm_engine/cli/__init__.py`

- [ ] **Step 1: Create CLI handler module**

```python
# src/organvm_engine/cli/irf.py
"""IRF CLI commands — Index Rerum Faciendarum."""
from __future__ import annotations

import argparse
import json


def cmd_irf_list(args: argparse.Namespace) -> int:
    """List IRF items with optional filters."""
    from organvm_engine.irf import parse_irf, query_irf
    from organvm_engine.paths import irf_path

    items = parse_irf(irf_path())
    filters = {}
    if getattr(args, "priority", None):
        filters["priority"] = args.priority
    if getattr(args, "domain", None):
        filters["domain"] = args.domain
    if getattr(args, "status", None):
        filters["status"] = args.status
    if getattr(args, "owner", None):
        filters["owner"] = args.owner

    result = query_irf(items, **filters) if filters else [i for i in items if i.status == "open"]

    if getattr(args, "json", False):
        import dataclasses
        print(json.dumps([dataclasses.asdict(i) for i in result], indent=2))
        return 0

    if not result:
        print("No matching IRF items.")
        return 0

    print(f"{'ID':<16} {'Pri':>3} {'Domain':<5} {'Owner':<8} Action")
    print("─" * 80)
    for item in result:
        action = item.action[:45] + "…" if len(item.action) > 46 else item.action
        print(f"{item.id:<16} {item.priority:>3} {item.domain:<5} {item.owner:<8} {action}")
    print(f"\n{len(result)} item(s)")
    return 0


def cmd_irf_status(args: argparse.Namespace) -> int:
    """Show details for a specific IRF item."""
    from organvm_engine.irf import parse_irf, query_irf
    from organvm_engine.paths import irf_path

    items = parse_irf(irf_path())
    matches = query_irf(items, item_id=args.item_id)

    if not matches:
        print(f"IRF item '{args.item_id}' not found.")
        return 1

    item = matches[0]
    print(f"ID:       {item.id}")
    print(f"Priority: {item.priority}")
    print(f"Domain:   {item.domain}")
    print(f"Status:   {item.status}")
    print(f"Owner:    {item.owner}")
    print(f"Source:   {item.source}")
    print(f"Blocker:  {item.blocker}")
    print(f"Section:  {item.section}")
    print(f"Action:   {item.action}")
    return 0


def cmd_irf_stats(args: argparse.Namespace) -> int:
    """Show IRF summary statistics."""
    from organvm_engine.irf import irf_stats, parse_irf
    from organvm_engine.paths import irf_path

    items = parse_irf(irf_path())
    s = irf_stats(items)

    if getattr(args, "json", False):
        print(json.dumps(s, indent=2))
        return 0

    print("Index Rerum Faciendarum — Summary")
    print("═" * 40)
    print(f"Total items:     {s['total']}")
    print(f"Open:            {s['open']}")
    print(f"Completed:       {s['completed']}")
    print(f"Blocked:         {s['blocked']}")
    print(f"Completion rate: {s['completion_rate']}%")
    print()
    print("By Priority:")
    for p, count in s["by_priority"].items():
        print(f"  {p}: {count}")
    print()
    print("By Domain:")
    for d, count in s["by_domain"].items():
        print(f"  {d}: {count}")
    return 0
```

- [ ] **Step 2: Wire into CLI __init__.py — add import (after line ~252)**

```python
from organvm_engine.cli.irf import (
    cmd_irf_list,
    cmd_irf_stats,
    cmd_irf_status,
)
```

- [ ] **Step 3: Wire into CLI __init__.py — add parser (before `return parser` in build_parser)**

```python
# irf
irf = sub.add_parser("irf", help="Index Rerum Faciendarum — universal work registry")
irf_sub = irf.add_subparsers(dest="subcommand")

irf_list = irf_sub.add_parser("list", help="List IRF items")
irf_list.add_argument("--priority", help="Filter by priority (P0/P1/P2/P3)")
irf_list.add_argument("--domain", help="Filter by domain (SYS/SGO/OBJ/...)")
irf_list.add_argument("--status", default=None, help="Filter by status (open/completed/blocked)")
irf_list.add_argument("--owner", help="Filter by owner")
irf_list.add_argument("--json", action="store_true", help="Output JSON")

irf_status_p = irf_sub.add_parser("status", help="Show details for a specific IRF item")
irf_status_p.add_argument("item_id", help="IRF item ID (e.g. IRF-SYS-001)")

irf_stats_p = irf_sub.add_parser("stats", help="IRF summary statistics")
irf_stats_p.add_argument("--json", action="store_true", help="Output JSON")
```

- [ ] **Step 4: Wire into CLI __init__.py — add dispatch block (after last `if args.command` block, ~line 2620)**

```python
if args.command == "irf":
    irf_dispatch = {
        "list": cmd_irf_list,
        "status": cmd_irf_status,
        "stats": cmd_irf_stats,
    }
    handler = irf_dispatch.get(getattr(args, "subcommand", "") or "")
    if handler:
        return handler(args)
    parser.parse_args(["irf", "--help"])
    return 0
```

- [ ] **Step 5: Test CLI manually**

Run: `cd ~/Workspace/meta-organvm && python -m organvm_engine.cli irf stats`
Expected: Summary table with open/completed/blocked counts

Run: `cd ~/Workspace/meta-organvm && python -m organvm_engine.cli irf list --priority P0`
Expected: 2 P0 items (collaborator password + share URL)

Run: `cd ~/Workspace/meta-organvm && python -m organvm_engine.cli irf status IRF-SYS-001`
Expected: Full item details

- [ ] **Step 6: Commit**

```bash
cd ~/Workspace/meta-organvm/organvm-engine
git add src/organvm_engine/cli/irf.py src/organvm_engine/cli/__init__.py
git commit -m "feat: organvm irf CLI — list, status, stats subcommands"
```

---

## Task 5: System Dashboard Route

**Files:**
- Create: `system-dashboard/src/dashboard/routes/irf.py`
- Create: `system-dashboard/src/dashboard/templates/irf.html`
- Modify: `system-dashboard/src/dashboard/app.py`

- [ ] **Step 1: Create route module**

```python
# system-dashboard/src/dashboard/routes/irf.py
"""IRF dashboard view."""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/irf", tags=["irf"])


@router.get("/", response_class=HTMLResponse)
async def irf_page(request: Request):
    from organvm_engine.irf import irf_stats, parse_irf, query_irf
    from organvm_engine.paths import irf_path

    items = parse_irf(irf_path())
    stats = irf_stats(items)
    open_items = query_irf(items, status="open")
    p0_items = query_irf(items, priority="P0", status="open")
    completed_items = query_irf(items, status="completed")

    return request.app.state.templates.TemplateResponse(
        request,
        name="irf.html",
        context={
            "page_title": "Index Rerum Faciendarum",
            "stats": stats,
            "open_items": open_items,
            "p0_items": p0_items,
            "completed_items": completed_items,
        },
    )
```

- [ ] **Step 2: Create template**

Create `system-dashboard/src/dashboard/templates/irf.html` — extend the base template with a stats summary card and tables for P0 items, open items by domain, and completed items.

- [ ] **Step 3: Register route in app.py**

Add to imports: `from dashboard.routes import ..., irf`
Add inside `create_app()`: `app.include_router(irf.router)`

- [ ] **Step 4: Test manually**

Run: `cd ~/Workspace/meta-organvm/system-dashboard && uvicorn dashboard.app:app --reload`
Navigate to: `http://localhost:8000/irf/`
Expected: IRF dashboard with stats and item tables

- [ ] **Step 5: Commit**

```bash
cd ~/Workspace/meta-organvm/system-dashboard
git add src/dashboard/routes/irf.py src/dashboard/templates/irf.html src/dashboard/app.py
git commit -m "feat: /irf/ dashboard route — IRF stats + item tables"
```

---

## Task 6: MCP Server Tool

**Files:**
- Create: `organvm-mcp-server/src/organvm_mcp/tools/irf.py`
- Modify: `organvm-mcp-server/src/organvm_mcp/server.py`

- [ ] **Step 1: Create tool module**

```python
# organvm-mcp-server/src/organvm_mcp/tools/irf.py
"""IRF query tool for MCP."""
from __future__ import annotations

import dataclasses
from typing import Any


def irf_query(
    item_id: str | None = None,
    priority: str | None = None,
    domain: str | None = None,
    status: str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    """Query IRF items. Returns matching items + stats."""
    from organvm_engine.irf import irf_stats, parse_irf, query_irf
    from organvm_engine.paths import irf_path

    items = parse_irf(irf_path())
    filters = {}
    if item_id:
        filters["item_id"] = item_id
    if priority:
        filters["priority"] = priority
    if domain:
        filters["domain"] = domain
    if status:
        filters["status"] = status

    if filters:
        result = query_irf(items, **filters)
    else:
        result = [i for i in items if i.status == "open"]

    return {
        "items": [dataclasses.asdict(i) for i in result[:limit]],
        "total_matching": len(result),
        "stats": irf_stats(items),
    }
```

- [ ] **Step 2: Register in server.py — add import (~line 18)**

```python
from organvm_mcp.tools import (
    ...
    irf,
)
```

- [ ] **Step 3: Register in server.py — add Tool entry to TOOLS list**

```python
Tool(
    name="organvm_irf_query",
    description=(
        "Query the Index Rerum Faciendarum — ORGANVM's universal work registry. "
        "Filter by item_id, priority (P0-P3), domain (SYS/SGO/OBJ/...), or status (open/completed/blocked). "
        "Returns matching items and summary statistics."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "item_id": {"type": "string", "description": "Specific IRF item ID (e.g. IRF-SYS-001)"},
            "priority": {"type": "string", "description": "Filter by priority: P0, P1, P2, P3"},
            "domain": {"type": "string", "description": "Filter by domain: SYS, SGO, OBJ, SKL, MON, etc."},
            "status": {"type": "string", "description": "Filter by status: open, completed, blocked"},
            "limit": {"type": "integer", "description": "Max results (default 50)", "default": 50},
        },
    },
),
```

- [ ] **Step 4: Register in server.py — add dispatch entry (~line 2226)**

```python
"organvm_irf_query": lambda args: irf.irf_query(**args),
```

- [ ] **Step 5: Commit**

```bash
cd ~/Workspace/meta-organvm/organvm-mcp-server
git add src/organvm_mcp/tools/irf.py src/organvm_mcp/server.py
git commit -m "feat: organvm_irf_query MCP tool — IRF query for agent sessions"
```

---

## Task 7: Vigiles Auditor — IRF Completion Check

**Files:**
- Modify: `vigiles-aeternae--agon-cosmogonicum/src/vigiles_engine/auditor.py`

- [ ] **Step 1: Add the check function**

Add at the bottom of `auditor.py`, before the final module-level code:

```python
@register_check("irf_completion_rate")
def check_irf_completion_rate(
    rule: AuditRule, workspace: Path, **_kwargs
) -> list[Finding]:
    """Report on IRF completion rates and flag open P0 items."""
    import re

    irf_path = workspace / "meta-organvm" / "organvm-corpvs-testamentvm" / "INST-INDEX-RERUM-FACIENDARUM.md"
    if not irf_path.exists():
        return [Finding(
            rule_check=rule.check,
            severity="high",
            target="system",
            description="INST-INDEX-RERUM-FACIENDARUM.md not found",
            regime="",
        )]

    text = irf_path.read_text(encoding="utf-8")
    in_completed = False
    open_by_priority: dict[str, int] = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
    completed_count = 0

    for line in text.splitlines():
        if line.startswith("## Completed") or line.startswith("## Blocked") or line.startswith("## Archived"):
            in_completed = True
        elif line.startswith("## "):
            in_completed = False

        m = re.search(r"\|\s*IRF-[A-Z]+-\d+\s*\|", line)
        if m:
            if in_completed:
                completed_count += 1
            else:
                pm = re.search(r"\|\s*(P[0-3])\s*\|", line)
                if pm:
                    open_by_priority[pm.group(1)] = open_by_priority.get(pm.group(1), 0) + 1

        if re.search(r"\|\s*DONE-\d+\s*\|", line) and in_completed:
            completed_count += 1

    total = sum(open_by_priority.values()) + completed_count
    rate = (completed_count / total * 100) if total else 0

    findings: list[Finding] = []

    if open_by_priority["P0"] > 0:
        findings.append(Finding(
            rule_check=rule.check,
            severity="critical",
            target="system",
            description=f"{open_by_priority['P0']} P0 IRF items still open — immediate action required",
            regime="",
            details={"open_p0": open_by_priority["P0"], "completion_rate": round(rate, 1)},
        ))

    if rate < 20 and total > 10:
        findings.append(Finding(
            rule_check=rule.check,
            severity=rule.severity,
            target="system",
            description=f"IRF completion rate {rate:.1f}% ({completed_count}/{total})",
            regime="",
            details={"by_priority": open_by_priority},
        ))

    return findings
```

- [ ] **Step 2: Commit**

```bash
cd ~/Workspace/meta-organvm/vigiles-aeternae--agon-cosmogonicum
git add src/vigiles_engine/auditor.py
git commit -m "feat: irf_completion_rate audit check — flag P0 items and low completion"
```

---

## Task 8: Omega Scorecard — IRF P0 Warning

**Files:**
- Modify: `organvm-engine/src/organvm_engine/cli/omega.py`

- [ ] **Step 1: Add IRF P0 warning to omega status output**

In `cmd_omega_status`, after the existing omega output, add:

```python
# IRF P0 check
try:
    from organvm_engine.irf import parse_irf, query_irf
    from organvm_engine.paths import irf_path
    irf_items = parse_irf(irf_path())
    p0 = query_irf(irf_items, priority="P0", status="open")
    if p0:
        print(f"\n⚠  {len(p0)} P0 IRF items require immediate action:")
        for item in p0:
            print(f"   {item.id}: {item.action[:60]}")
except Exception:
    pass  # IRF integration is advisory, not blocking
```

- [ ] **Step 2: Commit**

```bash
cd ~/Workspace/meta-organvm/organvm-engine
git add src/organvm_engine/cli/omega.py
git commit -m "feat: omega status shows P0 IRF warnings"
```

---

## Task 9: invoke.py — IRF Prefix Resolution

**Files:**
- Modify: `organvm-corpvs-testamentvm/scripts/invoke.py`

- [ ] **Step 1: Add IRF pattern to ID_PATTERNS (~line 40)**

```python
(re.compile(r"^IRF-[A-Z]+-\d+$", re.IGNORECASE), "irf"),
```

Insert before the sprint catch-all patterns.

- [ ] **Step 2: Add IRF to NAMESPACE_NAMES (~line 67)**

```python
"irf": "Index Rerum Faciendarum",
```

- [ ] **Step 3: Add direct IRF file parser after parse_concordance**

Add a function:

```python
def parse_irf_direct(path: Path) -> list[dict]:
    """Parse INST-INDEX-RERUM-FACIENDARUM.md tables for invoke resolution."""
    if not path.exists():
        return []
    return parse_table_from_file(path)
```

Where `parse_table_from_file` scans the file for markdown tables and calls the existing `parse_table()` helper.

In `main()`, after `namespaces = parse_concordance(...)`, add:

```python
irf_path = ROOT / "INST-INDEX-RERUM-FACIENDARUM.md"
if irf_path.exists():
    namespaces.setdefault("irf", []).extend(parse_irf_direct(irf_path))
```

- [ ] **Step 4: Test manually**

Run: `cd ~/Workspace/meta-organvm/organvm-corpvs-testamentvm && python scripts/invoke.py IRF-SYS-001`
Expected: Resolves to the CONSTITUTION.md consolidation item

Run: `python scripts/invoke.py --namespace irf`
Expected: Lists all IRF items

- [ ] **Step 5: Commit**

```bash
cd ~/Workspace/meta-organvm/organvm-corpvs-testamentvm
git add scripts/invoke.py
git commit -m "feat: invoke.py resolves IRF- prefixed IDs from INST-INDEX-RERUM-FACIENDARUM.md"
```

---

## Task 10: Final Integration Test

- [ ] **Step 1: Run all engine tests**

```bash
cd ~/Workspace/meta-organvm && pytest organvm-engine/tests/test_irf_*.py -v
```

- [ ] **Step 2: Test CLI end-to-end**

```bash
organvm irf stats
organvm irf list --priority P0
organvm irf list --domain SGO
organvm irf status IRF-OBJ-001
organvm irf list --json | python -m json.tool | head -20
organvm omega status  # should show P0 warning
```

- [ ] **Step 3: Test invoke.py**

```bash
cd ~/Workspace/meta-organvm/organvm-corpvs-testamentvm
python scripts/invoke.py IRF-SYS-001
python scripts/invoke.py IRF-OBJ-001
python scripts/invoke.py --namespace irf
python scripts/invoke.py --list  # should show irf namespace
```

- [ ] **Step 4: Push all repos**

```bash
cd ~/Workspace/meta-organvm/organvm-engine && git push
cd ~/Workspace/meta-organvm/system-dashboard && git push
cd ~/Workspace/meta-organvm/organvm-mcp-server && git push
cd ~/Workspace/meta-organvm/vigiles-aeternae--agon-cosmogonicum && git push
cd ~/Workspace/meta-organvm/organvm-corpvs-testamentvm && git push
```

- [ ] **Step 5: Update IRF — mark integration items complete**

Edit `INST-INDEX-RERUM-FACIENDARUM.md` to move the engine/dashboard/MCP/vigiles/omega/invoke items to Completed section.

- [ ] **Step 6: Final commit**

```bash
cd ~/Workspace/meta-organvm/organvm-corpvs-testamentvm
git add INST-INDEX-RERUM-FACIENDARUM.md
git commit -m "docs: mark IRF system integration items as completed"
git push
```
