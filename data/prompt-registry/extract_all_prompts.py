#!/usr/bin/env python3
"""Extract every user prompt from ALL Claude Code sessions into a structured registry.

Reads JSONL files from ~/.claude/projects/*/ (the authoritative source for all sessions).
Parses each human message with full metadata and outputs:
1. A JSON registry (prompt-registry.json) — machine-readable, full metadata
2. A markdown registry (INST-INDEX-PROMPTORUM.md) — human-readable, grouped views
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"
CHATGPT_EXPORT = Path.home() / "Workspace/meta-organvm/intake/data-2026-02-16-00-20-00-batch-0000/conversations.json"
CODEX_HISTORY = Path.home() / ".codex" / "history.jsonl"
SPECSTORY_DIRS = [
    # Post-cutover homes (2026-06-05 cartridge migration); ~/Code symlinks
    # into the cartridge, so these survive a cartridge relocation.
    Path.home() / "Code/organvm-i-theoria/linguistic-atomization-framework/.specstory",
    Path.home() / "Code/organvm/cognitive-archaelogy-tribunal/.config/.specstory",
    Path.home() / "Code/organvm/cognitive-archaelogy-tribunal/.specstory",
    Path.home() / "Code/organvm/cognitive-archaelogy-tribunal/.history/.specstory",
    Path.home() / "Workspace/limen-work/public-record-data-scrapper/.specstory",
]
CORPUS_SITE_DIR = Path.home() / "Workspace/organvm-i-theoria/conversation-corpus-site"
ZSH_HISTORY = Path.home() / ".config/zsh/.zsh_history"
REGISTRY_DIR = Path(__file__).parent
OUTPUT_JSON = REGISTRY_DIR / "prompt-registry.json"
OUTPUT_MD = REGISTRY_DIR / "INST-INDEX-PROMPTORUM.md"


def extract_project_path(dir_name: str) -> str:
    """Convert project directory name back to a readable path."""
    # Format: -Users-[user]-Workspace-meta-organvm → ~/Workspace/meta-organvm
    return "/" + dir_name.replace("-", "/").lstrip("/")


def parse_jsonl_session(filepath: Path, project_dir: str) -> list[dict]:
    """Parse a JSONL session file and extract all human messages."""
    prompts = []
    project_path = extract_project_path(project_dir)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (OSError, UnicodeDecodeError):
        return []

    # Pre-parse all lines for index-based lookahead (response linking)
    entries = []
    for line_text in lines:
        line_text = line_text.strip()
        if not line_text:
            continue
        try:
            entries.append(json.loads(line_text))
        except json.JSONDecodeError:
            continue

    prompt_num = 0
    for idx, entry in enumerate(entries):
        # Look for user messages
        if entry.get("type") != "user":
            continue

        # Skip sidechain/meta messages
        if entry.get("isSidechain") or entry.get("isMeta"):
            continue

        # Extract content
        content_parts = entry.get("message", {}).get("content", [])
        if isinstance(content_parts, str):
            raw_content = content_parts
        elif isinstance(content_parts, list):
            text_parts = []
            for part in content_parts:
                if isinstance(part, dict) and part.get("type") == "text":
                    text_parts.append(part.get("text", ""))
                elif isinstance(part, str):
                    text_parts.append(part)
            raw_content = "\n".join(text_parts)
        else:
            continue

        if not raw_content or not raw_content.strip():
            continue

        # Skip system-generated messages (local-command-caveat wrappers)
        if "<local-command-caveat>" in raw_content and len(raw_content) < 200:
            continue
        if "<local-command-stdout>" in raw_content and len(raw_content) < 200:
            continue
        # Skip harness/runtime sentinels and notification echoes (not user-authored)
        # Why: these flow through user-message slots in JSONL but originate from the
        # harness, not from the human. Without this filter they tag as "user prompts"
        # and pollute downstream classification (corpus run 2026-04-26 surfaced
        # autonomous-loop sentinels and task-notification echoes as hanging vacuums).
        stripped = raw_content.strip()
        if stripped.startswith("<<autonomous-loop") or stripped == "<<autonomous-loop-dynamic>>":
            continue
        if stripped.startswith("<task-notification>") or "<task-notification>" in stripped[:50]:
            continue
        if raw_content.strip().startswith("<command-name>") and len(raw_content) < 200:
            # Extract slash command
            cmd_match = re.search(r"<command-name>([^<]+)</command-name>", raw_content)
            if cmd_match:
                raw_content = f"/{cmd_match.group(1)}"
            else:
                continue

        prompt_num += 1

        # Get timestamp (ISO string format: 2026-04-16T12:35:26.621Z)
        timestamp_raw = entry.get("timestamp", "")
        if isinstance(timestamp_raw, str) and timestamp_raw:
            try:
                dt = datetime.fromisoformat(timestamp_raw.replace("Z", "+00:00"))
                timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                date_str = dt.strftime("%Y-%m-%d")
            except ValueError:
                timestamp_str = timestamp_raw
                date_str = timestamp_raw[:10] if len(timestamp_raw) >= 10 else ""
        elif isinstance(timestamp_raw, (int, float)) and timestamp_raw > 0:
            dt = datetime.fromtimestamp(timestamp_raw / 1000)
            timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            date_str = dt.strftime("%Y-%m-%d")
        else:
            timestamp_str = ""
            date_str = ""

        # Classify
        categories = classify_prompt(raw_content)

        # Summary (first 150 chars, single line)
        summary = raw_content[:150].replace("\n", " ").strip()
        if len(raw_content) > 150:
            summary += "..."

        session_id = filepath.stem  # UUID from filename

        # Response linking: look ahead for the assistant's response
        response_summary = ""
        for lookahead in range(idx + 1, min(idx + 5, len(entries))):
            next_entry = entries[lookahead]
            if next_entry.get("type") == "assistant":
                next_content = next_entry.get("message", {}).get("content", [])
                if isinstance(next_content, str):
                    response_summary = next_content[:200].replace("\n", " ").strip()
                elif isinstance(next_content, list):
                    for part in next_content:
                        if isinstance(part, dict) and part.get("type") == "text":
                            response_summary = part.get("text", "")[:200].replace("\n", " ").strip()
                            break
                        elif isinstance(part, str) and part.strip():
                            response_summary = part[:200].replace("\n", " ").strip()
                            break
                break
            elif next_entry.get("type") == "user":
                break  # next user message before any assistant response

        prompts.append({
            "session_id": session_id,
            "project_dir": project_dir,
            "project_path": project_path,
            "prompt_number": prompt_num,
            "timestamp": timestamp_str,
            "date": date_str,
            "content": raw_content,
            "summary": summary,
            "categories": categories,
            "status": "UNREVIEWED",
            "content_length": len(raw_content),
            "source": "claude-code",
            "response_summary": response_summary,
        })

    return prompts


def parse_chatgpt_export(filepath: Path) -> list[dict]:
    """Parse a ChatGPT conversations.json export and extract all human messages."""
    prompts = []
    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    for conv in data:
        conv_name = conv.get("name", "untitled")
        conv_uuid = conv.get("uuid", "")
        messages = conv.get("chat_messages", [])

        prompt_num = 0
        for msg in messages:
            if msg.get("sender") != "human":
                continue

            text = msg.get("text") or ""
            if not text.strip():
                continue

            prompt_num += 1

            ts_raw = msg.get("created_at", "")
            if ts_raw:
                try:
                    dt = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
                    timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                    date_str = dt.strftime("%Y-%m-%d")
                except ValueError:
                    timestamp_str = ts_raw
                    date_str = ts_raw[:10]
            else:
                timestamp_str = ""
                date_str = ""

            summary = text[:150].replace("\n", " ").strip()
            if len(text) > 150:
                summary += "..."

            prompts.append({
                "session_id": conv_uuid,
                "project_dir": "chatgpt",
                "project_path": "ChatGPT",
                "prompt_number": prompt_num,
                "timestamp": timestamp_str,
                "date": date_str,
                "content": text,
                "summary": summary,
                "categories": classify_prompt(text),
                "status": "UNREVIEWED",
                "content_length": len(text),
                "source": "chatgpt",
                "conversation_name": conv_name,
            })

    return prompts


_SHELL_PROMPT_RE = re.compile(r"^\s*[\w.-]+@[\w.-]+\s+[~/].*?[%$#]\s")
_BREW_OUTPUT_RE = re.compile(r"^==>\s|^Pouring\s|^Caveats\s|^Error: (No available formula|Cannot install)")
_LOGIN_BANNER_RE = re.compile(r"^Last login:\s")


def _is_scrollback_paste(text: str) -> bool:
    """Heuristic: detect when text is a pasted terminal scrollback rather than a user prompt.

    Why: Codex's history.jsonl captures user-typed text, but users frequently paste
    raw terminal output (often including `[user]@Mac ~ % brew upgrade` followed by
    Homebrew "==> Pouring..." banners). The atomizer then shreds this into dozens
    of fake "prompt atoms" (43 found in run 2026-05-13). This filter drops pastes
    where shell-output patterns dominate, while preserving real prompts that
    happen to quote one or two error lines.
    """
    body_lines = text.splitlines()
    if len(body_lines) < 5:
        return False
    shell_signal = 0
    for line in body_lines:
        if _LOGIN_BANNER_RE.match(line) or _SHELL_PROMPT_RE.match(line) or _BREW_OUTPUT_RE.match(line):
            shell_signal += 1
            if shell_signal >= 3:
                return True
    return False


def parse_codex_history(filepath: Path) -> list[dict]:
    """Parse Codex history.jsonl and extract all user prompts."""
    prompts = []
    session_counters: dict[str, int] = {}
    skipped_scrollback = 0

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return []

    for line_text in lines:
        line_text = line_text.strip()
        if not line_text:
            continue
        try:
            entry = json.loads(line_text)
        except json.JSONDecodeError:
            continue

        text = entry.get("text", "")
        if not text or not text.strip():
            continue

        if _is_scrollback_paste(text):
            skipped_scrollback += 1
            continue

        session_id = entry.get("session_id", "unknown")
        session_counters[session_id] = session_counters.get(session_id, 0) + 1

        ts_raw = entry.get("ts", 0)
        if ts_raw:
            dt = datetime.fromtimestamp(ts_raw)
            timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            date_str = dt.strftime("%Y-%m-%d")
        else:
            timestamp_str = ""
            date_str = ""

        summary = text[:150].replace("\n", " ").strip()
        if len(text) > 150:
            summary += "..."

        prompts.append({
            "session_id": session_id,
            "project_dir": "codex",
            "project_path": "Codex",
            "prompt_number": session_counters[session_id],
            "timestamp": timestamp_str,
            "date": date_str,
            "content": text,
            "summary": summary,
            "categories": classify_prompt(text),
            "status": "UNREVIEWED",
            "content_length": len(text),
            "source": "codex",
        })

    if skipped_scrollback:
        print(f"Codex: skipped {skipped_scrollback} scrollback-paste entries")
    return prompts


def parse_specstory_files(specstory_dirs: list[Path]) -> list[dict]:
    """Parse Specstory (Cursor IDE) conversation logs and extract user messages.

    Specstory markdown format uses `_**User (YYYY-MM-DD HH:MMZ)**_` lines
    to mark user messages, with content following until the next `---` separator.
    """
    prompts = []

    for specstory_dir in specstory_dirs:
        history_dir = specstory_dir / "history"
        if not history_dir.is_dir():
            continue

        # Derive project path from the specstory dir location
        # e.g. .../organvm-i-theoria/linguistic-atomization-framework/.specstory
        # project is the parent before .specstory (or .config/.specstory, etc.)
        parts = specstory_dir.parts
        # Walk up past .specstory, .config, .history to find the project root
        project_root = specstory_dir.parent
        while project_root.name in (".config", ".history", ".specstory"):
            project_root = project_root.parent
        project_path = str(project_root)
        project_dir = project_root.name

        md_files = sorted(history_dir.glob("*.md"))
        for md_file in md_files:
            try:
                content = md_file.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue

            # Extract session ID from the file header comment
            session_match = re.search(
                r"Session\s+([0-9a-f-]+)", content
            )
            session_id = session_match.group(1) if session_match else md_file.stem

            # Extract date from filename: YYYY-MM-DD_HH-MMZ-slug.md
            date_match = re.match(r"(\d{4}-\d{2}-\d{2})", md_file.name)
            file_date = date_match.group(1) if date_match else ""

            # Find all user messages using the pattern:
            # _**User (YYYY-MM-DD HH:MMZ)**_
            user_pattern = re.compile(
                r'_\*\*User\s*\((\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}Z?)\)\*\*_'
            )

            # Split content by --- separators to isolate message blocks
            blocks = re.split(r'\n---\n', content)

            prompt_num = 0
            for block in blocks:
                user_match = user_pattern.search(block)
                if not user_match:
                    continue

                # Extract timestamp
                ts_raw = user_match.group(1)
                try:
                    dt = datetime.strptime(ts_raw.rstrip("Z"), "%Y-%m-%d %H:%M")
                    timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                    date_str = dt.strftime("%Y-%m-%d")
                except ValueError:
                    timestamp_str = ts_raw
                    date_str = file_date

                # Extract message text: everything after the User line
                text_start = user_match.end()
                raw_content = block[text_start:].strip()

                if not raw_content:
                    continue

                prompt_num += 1
                summary = raw_content[:150].replace("\n", " ").strip()
                if len(raw_content) > 150:
                    summary += "..."

                prompts.append({
                    "session_id": session_id,
                    "project_dir": project_dir,
                    "project_path": project_path,
                    "prompt_number": prompt_num,
                    "timestamp": timestamp_str,
                    "date": date_str,
                    "content": raw_content,
                    "summary": summary,
                    "categories": classify_prompt(raw_content),
                    "status": "UNREVIEWED",
                    "content_length": len(raw_content),
                    "source": "specstory",
                })

    return prompts


def parse_corpus_site(corpus_dir: Path) -> list[dict]:
    """Parse conversation corpus site markdowns and extract user messages.

    These files use varied formats for user messages including:
    - `## Q:` / `## A:` pairs (ChatGPT-style exports)
    - `_**User (...)**_` blocks (Claude-style transcripts)
    - `## Entry N -- user -- TIMESTAMP` blocks (raw session transcripts)
    Excludes repo metadata files (CLAUDE.md, AGENTS.md, GEMINI.md, README.md).
    """
    prompts = []
    exclude_names = {"CLAUDE.md", "AGENTS.md", "GEMINI.md", "README.md", "formation.yaml"}

    md_files = []
    for root, dirs, files in os.walk(str(corpus_dir)):
        depth = root.replace(str(corpus_dir), "").count(os.sep)
        if depth > 1:
            dirs.clear()
            continue
        for f in sorted(files):
            if f.endswith(".md") and f not in exclude_names:
                md_files.append(Path(root) / f)

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        session_id = md_file.stem
        rel_path = str(md_file.relative_to(corpus_dir))

        # Try to extract a date from the filename (YYYY-MM-DD prefix)
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", md_file.name)
        file_date = date_match.group(1) if date_match else ""

        prompt_num = 0
        user_messages: list[tuple[str, str, str]] = []  # (text, timestamp, date)

        # Strategy 1: ## Q: / ## A: pairs
        qa_blocks = re.split(r'\n## [QA]:\s*\n?', content)
        if len(qa_blocks) > 2:
            # File uses Q:/A: format — odd-indexed blocks (1, 3, 5...) are user Qs
            # qa_blocks[0] is before first ## Q:
            # qa_blocks[1] is content after first ## Q: (user)
            # qa_blocks[2] is content after first ## A: (assistant)
            # etc.
            for i in range(1, len(qa_blocks), 2):
                text = qa_blocks[i].strip()
                if text:
                    user_messages.append((text, "", file_date))
        else:
            # Strategy 2: _**User (timestamp)**_ blocks (specstory-like)
            user_pattern = re.compile(
                r'_\*\*User\s*\((\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}Z?)\)\*\*_'
            )
            blocks = re.split(r'\n---\n', content)
            found_user_blocks = False
            for block in blocks:
                user_match = user_pattern.search(block)
                if user_match:
                    found_user_blocks = True
                    ts_raw = user_match.group(1)
                    try:
                        dt = datetime.strptime(ts_raw.rstrip("Z"), "%Y-%m-%d %H:%M:%S")
                        ts_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                        d_str = dt.strftime("%Y-%m-%d")
                    except ValueError:
                        ts_str = ts_raw
                        d_str = file_date
                    text = block[user_match.end():].strip()
                    if text:
                        user_messages.append((text, ts_str, d_str))

            # Strategy 3: ## Entry N — user — TIMESTAMP blocks
            if not found_user_blocks:
                entry_pattern = re.compile(
                    r'## Entry \d+\s*(?:—|--)\s*user\s*(?:—|--)\s*'
                    r'(\d{4}-\d{2}-\d{2}T[\d:.]+Z?)'
                )
                entry_splits = re.split(r'(?=## Entry \d+)', content)
                for block in entry_splits:
                    entry_match = entry_pattern.search(block)
                    if entry_match:
                        ts_raw = entry_match.group(1)
                        try:
                            dt = datetime.fromisoformat(
                                ts_raw.replace("Z", "+00:00")
                            )
                            ts_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                            d_str = dt.strftime("%Y-%m-%d")
                        except ValueError:
                            ts_str = ts_raw
                            d_str = file_date
                        # Text is everything after the header line(s)
                        lines = block.split("\n")
                        # Skip the header line and any metadata lines (- cwd:, etc.)
                        text_lines = []
                        past_header = False
                        for line in lines:
                            if past_header:
                                text_lines.append(line)
                            elif line.startswith("## Entry"):
                                continue
                            elif line.startswith("- cwd:"):
                                continue
                            elif line.strip() == "":
                                if not past_header:
                                    past_header = True
                            else:
                                past_header = True
                                text_lines.append(line)
                        text = "\n".join(text_lines).strip()
                        # Skip system-generated messages
                        if text and "<local-command-caveat>" not in text and "<local-command-stdout>" not in text:
                            if "<command-name>" in text and len(text) < 200:
                                cmd_match = re.search(
                                    r"<command-name>([^<]+)</command-name>", text
                                )
                                if cmd_match:
                                    text = f"/{cmd_match.group(1)}"
                                else:
                                    continue
                            user_messages.append((text, ts_str, d_str))

        # If no structured user messages found, treat the whole file as a single entry
        # (summaries, plans, etc. — still valuable as prompts provenance)
        if not user_messages and len(content.strip()) > 100:
            # Skip files that are clearly not conversation transcripts
            # Only include if they have some conversational markers
            lower = content.lower()
            if any(marker in lower for marker in [
                "## q:", "user", "human", "prompt", "you:", "me:",
            ]):
                user_messages.append((content[:2000].strip(), "", file_date))

        for text, ts_str, d_str in user_messages:
            if not text.strip():
                continue
            prompt_num += 1
            summary = text[:150].replace("\n", " ").strip()
            if len(text) > 150:
                summary += "..."

            prompts.append({
                "session_id": session_id,
                "project_dir": "conversation-corpus-site",
                "project_path": str(corpus_dir),
                "prompt_number": prompt_num,
                "timestamp": ts_str,
                "date": d_str,
                "content": text,
                "summary": summary,
                "categories": classify_prompt(text),
                "status": "UNREVIEWED",
                "content_length": len(text),
                "source": "corpus-site",
            })

    return prompts


def parse_shell_history(history_path: Path) -> list[dict]:
    """Parse zsh history for AI-relevant commands.

    Format: `: timestamp:0;command` (extended_history format).
    Filters to commands containing AI-related keywords or git commit messages.
    """
    prompts = []
    ai_keywords = [
        "claude", "codex", "organvm", "cce", "gemini",
        "gpt", "openai", "anthropic",
    ]
    history_pattern = re.compile(r'^: (\d+):\d+;(.+)$')

    try:
        with open(history_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return []

    prompt_num = 0
    for line_text in lines:
        line_text = line_text.rstrip("\n")
        match = history_pattern.match(line_text)
        if not match:
            continue

        ts_epoch = int(match.group(1))
        command = match.group(2).strip()

        if not command:
            continue

        # Check AI relevance
        lower_cmd = command.lower()
        is_ai_relevant = any(kw in lower_cmd for kw in ai_keywords)
        is_git_commit = "git commit -m" in lower_cmd

        if not is_ai_relevant and not is_git_commit:
            continue

        prompt_num += 1

        try:
            dt = datetime.fromtimestamp(ts_epoch)
            timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            date_str = dt.strftime("%Y-%m-%d")
        except (OSError, ValueError, OverflowError):
            timestamp_str = ""
            date_str = ""

        summary = command[:150].replace("\n", " ").strip()
        if len(command) > 150:
            summary += "..."

        prompts.append({
            "session_id": f"shell-{ts_epoch}",
            "project_dir": "shell",
            "project_path": "~/.config/zsh/.zsh_history",
            "prompt_number": prompt_num,
            "timestamp": timestamp_str,
            "date": date_str,
            "content": command,
            "summary": summary,
            "categories": classify_prompt(command),
            "status": "UNREVIEWED",
            "content_length": len(command),
            "source": "shell-history",
        })

    return prompts


def classify_prompt(content: str) -> list[str]:
    """Classify a prompt into categories."""
    categories = []
    lower = content.lower()

    if content.startswith("/"):
        categories.append("command")
        return categories

    # Close-out litany
    if "provide an overview of all that was" in lower or "are we certain, sisyphus" in lower:
        categories.append("close-out")
    if "commit[all] push[origin]" in lower:
        categories.append("close-out")
    if "(local):(remote)" in lower:
        categories.append("close-out")
    if "nothing will be lost" in lower:
        categories.append("close-out")

    # Governance rules
    if "vacuum" in lower and ("n/a" in lower or "none-knowledge" in lower):
        categories.append("governance")
    if "persistent memory must" in lower:
        categories.append("governance")
    if "every single thing you ingest" in lower:
        categories.append("governance")
    if "must be universally" in lower:
        categories.append("governance")

    # Directives
    directive_words = [
        r"\bsolve\b", r"\bbuild\b", r"\bcreate\b", r"\bimplement\b",
        r"\bfix\b", r"\bwrite\b", r"\bdesign\b", r"\bwe need to\b",
        r"\blet'?s\b", r"\bmake\b", r"\bensure\b", r"\bwire\b",
    ]
    for pat in directive_words:
        if re.search(pat, lower):
            categories.append("directive")
            break

    # Questions
    if content.rstrip().endswith("?") or re.match(r"^(what|why|how|is |does |did |can |where)", lower):
        categories.append("question")

    # Emotional
    if any(w in lower for w in ["fuck", "shit", "retard", "sick of", "frustrated", "idiot", "moron"]):
        categories.append("emotional")

    # Resume/carry-forward
    if "last session" in lower or "pick this back up" in lower or "continue" in lower:
        categories.append("carry-forward")

    # Pasted content (large blocks)
    if len(content) > 500 and content.count("\n") > 10:
        categories.append("pasted-content")

    # Personal
    if any(w in lower for w in ["becka", "housing", "employment", "income", "money"]):
        categories.append("personal")

    if not categories:
        categories.append("uncategorized")

    return list(set(categories))


def generate_markdown(all_prompts: list[dict]) -> str:
    """Generate the full markdown registry."""
    lines = []
    lines.append("# Index Promptorum — Complete Prompt Registry")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().isoformat()}")
    lines.append(f"**Total prompts:** {len(all_prompts)}")
    sessions = set(p["session_id"] for p in all_prompts)
    lines.append(f"**Total sessions:** {len(sessions)}")
    dates = [p["date"] for p in all_prompts if p["date"]]
    if dates:
        lines.append(f"**Date range:** {min(dates)} → {max(dates)}")
    lines.append("")
    lines.append("**Automation:** SessionEnd hook at `~/.claude/hooks/session-prompt-capture.sh`")
    lines.append("**Machine-readable:** `data/prompt-registry/prompt-registry.json`")
    lines.append("")

    # Category stats
    cat_counts: dict[str, int] = {}
    for p in all_prompts:
        for c in p["categories"]:
            cat_counts[c] = cat_counts.get(c, 0) + 1

    lines.append("## Statistics")
    lines.append("")
    lines.append("| Category | Count | % |")
    lines.append("|----------|-------|---|")
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        pct = count / len(all_prompts) * 100
        lines.append(f"| {cat} | {count} | {pct:.1f}% |")
    lines.append("")

    # Status counts
    status_counts: dict[str, int] = {}
    for p in all_prompts:
        s = p["status"]
        status_counts[s] = status_counts.get(s, 0) + 1
    lines.append("| Status | Count |")
    lines.append("|--------|-------|")
    for s, count in sorted(status_counts.items()):
        lines.append(f"| {s} | {count} |")
    lines.append("")

    # Daily activity
    daily: dict[str, int] = {}
    for p in all_prompts:
        if p["date"]:
            daily[p["date"]] = daily.get(p["date"], 0) + 1

    lines.append("## Daily Activity")
    lines.append("")
    lines.append("| Date | Prompts |")
    lines.append("|------|---------|")
    for date in sorted(daily.keys()):
        lines.append(f"| {date} | {daily[date]} |")
    lines.append("")

    # Directives view (the implementation tracking board)
    directives = [p for p in all_prompts if "directive" in p["categories"]]
    lines.append("---")
    lines.append(f"## Directives — Implementation Tracking ({len(directives)})")
    lines.append("")
    lines.append("| ID | Date | Project | Status | Prompt |")
    lines.append("|----|------|---------|--------|--------|")
    for i, p in enumerate(directives, 1):
        proj = p["project_path"].split("/")[-1] if "/" in p["project_path"] else p["project_path"]
        summary = p["summary"][:80].replace("|", "\\|")
        lines.append(f"| D-{i:04d} | {p['date']} | {proj} | {p['status']} | {summary} |")
    lines.append("")

    # Governance rules view
    governance = [p for p in all_prompts if "governance" in p["categories"]]
    lines.append("---")
    lines.append(f"## Governance Rules ({len(governance)})")
    lines.append("")
    for p in governance:
        lines.append(f"- **[{p['date']}]** {p['summary']}")
    lines.append("")

    # By project directory
    lines.append("---")
    lines.append("## By Project Directory")
    lines.append("")
    by_proj: dict[str, list] = {}
    for p in all_prompts:
        by_proj.setdefault(p["project_path"], []).append(p)

    for proj in sorted(by_proj.keys()):
        prompts = by_proj[proj]
        lines.append(f"### `{proj}` ({len(prompts)} prompts)")
        lines.append("")
        for p in prompts[:10]:  # Show first 10 per project
            lines.append(f"- [{p['date']}] {p['summary']}")
        if len(prompts) > 10:
            lines.append(f"- ... and {len(prompts)-10} more")
        lines.append("")

    return "\n".join(lines)


def main():
    all_prompts = []

    # Walk ALL project directories
    for project_dir in sorted(PROJECTS_DIR.iterdir()):
        if not project_dir.is_dir():
            continue

        project_name = project_dir.name

        # Find all JSONL files (sessions)
        jsonl_files = sorted(project_dir.glob("*.jsonl"))
        for jsonl_file in jsonl_files:
            prompts = parse_jsonl_session(jsonl_file, project_name)
            all_prompts.extend(prompts)

    # ChatGPT export
    if CHATGPT_EXPORT.exists():
        chatgpt_prompts = parse_chatgpt_export(CHATGPT_EXPORT)
        all_prompts.extend(chatgpt_prompts)
        print(f"ChatGPT: {len(chatgpt_prompts)} prompts")

    # Codex history
    if CODEX_HISTORY.exists():
        codex_prompts = parse_codex_history(CODEX_HISTORY)
        all_prompts.extend(codex_prompts)
        print(f"Codex: {len(codex_prompts)} prompts")

    # Specstory (Cursor IDE) conversation logs
    specstory_prompts = parse_specstory_files(SPECSTORY_DIRS)
    if specstory_prompts:
        all_prompts.extend(specstory_prompts)
        print(f"Specstory: {len(specstory_prompts)} prompts")

    # Corpus site markdowns (conversation transcripts)
    if CORPUS_SITE_DIR.is_dir():
        corpus_prompts = parse_corpus_site(CORPUS_SITE_DIR)
        all_prompts.extend(corpus_prompts)
        print(f"Corpus site: {len(corpus_prompts)} prompts")

    # Shell history (AI-relevant commands)
    if ZSH_HISTORY.exists():
        shell_prompts = parse_shell_history(ZSH_HISTORY)
        all_prompts.extend(shell_prompts)
        print(f"Shell history: {len(shell_prompts)} prompts")

    if not all_prompts:
        print("No prompts found.")
        return

    # Sort by timestamp
    all_prompts.sort(key=lambda p: p["timestamp"] or "0")

    # Assign sequential IDs
    for i, p in enumerate(all_prompts, 1):
        p["id"] = f"PRM-{i:05d}"

    # Write JSON
    OUTPUT_JSON.write_text(
        json.dumps(all_prompts, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"JSON: {len(all_prompts)} prompts → {OUTPUT_JSON}")

    # Write Markdown
    md = generate_markdown(all_prompts)
    OUTPUT_MD.write_text(md, encoding="utf-8")
    print(f"Markdown: → {OUTPUT_MD}")

    # Stats
    cats = {}
    for p in all_prompts:
        for c in p["categories"]:
            cats[c] = cats.get(c, 0) + 1
    print(f"\nCategories:")
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")


if __name__ == "__main__":
    main()
