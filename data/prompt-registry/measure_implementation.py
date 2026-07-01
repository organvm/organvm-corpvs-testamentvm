#!/usr/bin/env python3
"""Implementation Measurement Engine for ORGANVM prompt-atoms.

Reads prompt-atoms.json (29,671 atoms) and auto-triages implementation status
by cross-referencing against actual system state:
  1. Git history — commit messages across all workspace repos
  2. IRF entries — DONE and open items in INST-INDEX-RERUM-FACIENDARUM.md
  3. GitHub issues/PRs — closed issues, merged PRs, and open items via gh CLI
  4. Hook existence — hooks in ~/.claude/settings.json
  5. Memory existence — topics in ~/.claude/projects/-Users-[user]/memory/MEMORY.md
  6. File/directory existence — check if referenced files/repos exist
  7. Git file-path evidence — changed filenames in recent commits

Usage:
    python3 measure_implementation.py
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WORKSPACE = Path.home() / "Workspace"
SCRIPT_DIR = Path(__file__).resolve().parent
ATOMS_PATH = SCRIPT_DIR / "prompt-atoms.json"
IRF_PATH = WORKSPACE / "meta-organvm" / "organvm-corpvs-testamentvm" / "INST-INDEX-RERUM-FACIENDARUM.md"
HOOKS_PATH = Path.home() / ".claude" / "settings.json"
MEMORY_PATH = Path.home() / ".claude" / "projects" / "-Users-[user]" / "memory" / "MEMORY.md"
SCORECARD_PATH = SCRIPT_DIR / "IMPLEMENTATION-SCORECARD.md"
GITHUB_CACHE_PATH = SCRIPT_DIR / "github-evidence-cache.json"
GITHUB_CACHE_TTL = 3600  # 1 hour in seconds

# Regex to detect file-path-like strings in atom content
FILE_PATH_PATTERN = re.compile(r"[\w-]+\.(py|yaml|json|md|sh|ts|js|toml|zsh)")

# Minimum keyword length for meaningful matching
MIN_KEYWORD_LEN = 4

# Git: minimum overlapping keywords for a single commit line to match an atom
MIN_KEYWORD_OVERLAP_GIT = 3

# Git: minimum Jaccard similarity between atom keywords and a commit message
# Measured as overlap / min(atom_kw, commit_kw) (asymmetric: we want
# the commit to be "about" the atom, not just share a few words)
MIN_JACCARD_GIT = 0.25

# IRF: minimum Jaccard similarity (intersection/union) to count as a match
# This prevents high-keyword-count IRF entries from matching everything
MIN_JACCARD_IRF = 0.15

# IRF: absolute minimum overlap count (Jaccard alone isn't enough for tiny sets)
MIN_OVERLAP_IRF = 3

# Words too common to be meaningful signals
STOP_WORDS = frozenset({
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "this", "that", "are", "was",
    "were", "be", "been", "being", "have", "has", "had", "do", "does",
    "did", "will", "would", "shall", "should", "may", "might", "must",
    "can", "could", "not", "no", "all", "each", "every", "both", "few",
    "more", "most", "other", "some", "such", "than", "too", "very",
    "just", "also", "now", "then", "when", "where", "how", "what",
    "which", "who", "whom", "why", "here", "there", "about", "above",
    "after", "again", "against", "below", "between", "into", "through",
    "during", "before", "until", "while", "use", "used", "using",
    "make", "made", "need", "needs", "new", "get", "set", "add", "run",
    "file", "files", "see", "like", "only", "over", "same", "work",
    "if", "so", "up", "out", "any", "its", "they", "them", "their",
    "you", "your", "we", "our", "my", "me", "he", "she", "his", "her",
    "one", "two", "first", "last", "next", "well", "way", "even",
})

# Domain-specific words that appear in nearly every IRF entry and
# therefore carry no discriminating signal for matching
DOMAIN_STOP_WORDS = frozenset({
    "agent", "completed", "done", "session", "audit", "commit", "vacuum",
    "claude", "none", "resolved", "added", "yaml", "created", "json",
    "seed", "tests", "repo", "human", "github", "repos", "meta-organvm",
    "docs", "organvm", "governance", "registry", "entry", "data", "closed",
    "across", "entries", "organ", "system", "update", "status", "build",
    "deploy", "spec", "sprint", "phase", "check", "pass", "rule", "rules",
    "implement", "implemented", "implementation", "config", "configure",
    "configured", "ensure", "verified", "fixed", "test", "merged",
    "pushed", "remaining", "advanced", "partially", "further",
    # Git commit boilerplate
    "chore", "feat", "sync", "context", "submodule", "auto-generated",
    "refresh", "dependabot", "remove", "checkpoint", "workflow",
    "pointers", "changes", "readme", "updates", "local", "bump",
    "standards", "plans", "version", "deps", "initial", "merge",
    "branch", "revert", "release", "moved", "rename", "renamed",
    "refactor", "cleanup", "minor", "style", "format",
    # Generic action/process words that pollute theme extraction
    "create", "review", "these", "output", "start", "proceed",
    "write", "clean", "users", "project", "state", "source",
    "should", "given", "based", "using", "every", "follow",
    "apply", "point", "define", "include", "current", "specific",
    "existing", "running", "right", "within", "keep", "thing",
    "things", "type", "types", "must", "want", "back", "full",
    "takes", "look", "show", "move", "step", "ensure", "require",
})


# ---------------------------------------------------------------------------
# Utility: extract keywords from text
# ---------------------------------------------------------------------------

def extract_keywords(text: str, include_domain: bool = True) -> set[str]:
    """Extract meaningful lowercase keywords from text.

    Args:
        text: Raw text to extract keywords from.
        include_domain: If False, also filter out domain-specific stop words.
            Use False for IRF matching where domain words cause false positives.
    """
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]+", text.lower())
    stop = STOP_WORDS if include_domain else (STOP_WORDS | DOMAIN_STOP_WORDS)
    return {w for w in words if len(w) >= MIN_KEYWORD_LEN and w not in stop}


# ---------------------------------------------------------------------------
# Evidence Source 1: Git History
# ---------------------------------------------------------------------------

@dataclass
class GitCorpus:
    """Aggregated commit messages from all workspace repos."""
    raw_lines: list[str] = field(default_factory=list)
    line_keywords: list[set[str]] = field(default_factory=list)
    keyword_index: dict[str, set[int]] = field(default_factory=lambda: defaultdict(set))
    file_index: set[str] = field(default_factory=set)

    def build(self) -> None:
        """Walk ~/Workspace/*/* and collect git log --oneline -100 from each."""
        print("[1/6] Building git history corpus...", flush=True)
        repo_count = 0
        line_count = 0

        for org_dir in sorted(WORKSPACE.iterdir()):
            if not org_dir.is_dir():
                continue
            # Skip non-repo directories at workspace root
            if org_dir.name in {"intake", "export", "alchemia-ingestvm"}:
                continue

            # Check if org_dir itself is a repo
            candidates = []
            if (org_dir / ".git").exists():
                candidates.append(org_dir)

            # Check subdirectories
            try:
                for sub in sorted(org_dir.iterdir()):
                    if sub.is_dir() and (sub / ".git").exists():
                        candidates.append(sub)
            except PermissionError:
                continue

            for repo_path in candidates:
                try:
                    result = subprocess.run(
                        ["git", "-C", str(repo_path), "log", "--all", "--oneline", "-100"],
                        capture_output=True, text=True, timeout=10,
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        for line in result.stdout.strip().splitlines():
                            # Strip the commit hash prefix
                            msg = line.split(" ", 1)[1] if " " in line else line
                            idx = len(self.raw_lines)
                            self.raw_lines.append(msg.lower())
                            # Use domain-filtered keywords for indexing
                            kw_set = extract_keywords(msg, include_domain=False)
                            self.line_keywords.append(kw_set)
                            for kw in kw_set:
                                self.keyword_index[kw].add(idx)
                            line_count += 1
                        repo_count += 1
                    # Also collect changed file paths for git-file evidence
                    file_result = subprocess.run(
                        ["git", "-C", str(repo_path), "log", "--all",
                         "--name-only", "--format=", "-100"],
                        capture_output=True, text=True, timeout=10,
                    )
                    if file_result.returncode == 0 and file_result.stdout.strip():
                        for fline in file_result.stdout.strip().splitlines():
                            fline = fline.strip()
                            if fline:
                                self.file_index.add(os.path.basename(fline).lower())
                except (subprocess.TimeoutExpired, OSError):
                    continue

        print(f"  -> {repo_count} repos, {line_count} commit messages, "
              f"{len(self.file_index)} unique file paths indexed", flush=True)

    def match(self, atom_keywords: set[str]) -> bool:
        """Return True if a commit message is sufficiently similar to the atom.

        Uses asymmetric similarity: overlap / len(commit_keywords).
        This asks "what fraction of the commit's distinct words does this
        atom explain?" — a short, specific commit that shares 3 of its 4
        keywords with the atom is strong evidence.
        """
        # Filter atom keywords with domain stop words
        filtered = atom_keywords - DOMAIN_STOP_WORDS
        if len(filtered) < MIN_KEYWORD_OVERLAP_GIT:
            return False

        # Find candidate lines via inverted index
        line_hits: Counter[int] = Counter()
        for kw in filtered:
            for line_idx in self.keyword_index.get(kw, set()):
                line_hits[line_idx] += 1

        for line_idx, hit_count in line_hits.items():
            if hit_count < MIN_KEYWORD_OVERLAP_GIT:
                continue
            commit_kw = self.line_keywords[line_idx]
            if not commit_kw:
                continue
            # Asymmetric: what fraction of the commit is covered by the atom?
            similarity = hit_count / len(commit_kw)
            if similarity >= MIN_JACCARD_GIT:
                return True

        return False

    def match_files(self, content: str) -> bool:
        """Return True if file-path-like strings in content appear in the file-change index.

        Extracts filenames matching common source extensions from atom content
        and checks whether any of those filenames were changed in recent commits.
        """
        if not self.file_index:
            return False
        matches = FILE_PATH_PATTERN.findall(content)
        if not matches:
            return False
        # FILE_PATH_PATTERN captures the extension group; re-extract full filenames
        for m in FILE_PATH_PATTERN.finditer(content):
            filename = m.group(0).lower()
            if filename in self.file_index:
                return True
        return False


# ---------------------------------------------------------------------------
# Evidence Source 2: IRF Entries
# ---------------------------------------------------------------------------

@dataclass
class IRFEntry:
    """A parsed IRF item."""
    irf_id: str
    is_done: bool
    text: str
    keywords: set[str]


@dataclass
class IRFIndex:
    """Parsed INST-INDEX-RERUM-FACIENDARUM.md."""
    done_entries: list[IRFEntry] = field(default_factory=list)
    open_entries: list[IRFEntry] = field(default_factory=list)

    def build(self) -> None:
        """Parse the IRF markdown for DONE and open items."""
        print("[2/6] Parsing IRF entries...", flush=True)

        if not IRF_PATH.exists():
            print("  -> IRF file not found, skipping", flush=True)
            return

        text = IRF_PATH.read_text(encoding="utf-8")

        # Match table rows with IRF IDs: | IRF-XXX-NNN | ... | ... |
        # Also detect strikethrough (~~) as DONE, and "DONE" or "RESOLVED" in text
        irf_pattern = re.compile(
            r"\|\s*(~~)?(IRF-[A-Z]+-\d+)(~~)?\s*\|(.+)",
            re.MULTILINE,
        )

        for m in irf_pattern.finditer(text):
            struck_open = m.group(1)
            irf_id = m.group(2)
            struck_close = m.group(3)
            rest = m.group(4)

            is_done = bool(struck_open and struck_close)
            if not is_done:
                is_done = bool(re.search(r"\b(DONE|RESOLVED|COMPLETED|CLOSED)\b", rest, re.IGNORECASE))

            # Use domain-filtered keywords to avoid false positives from
            # high-frequency system vocabulary appearing in every IRF entry
            entry = IRFEntry(
                irf_id=irf_id,
                is_done=is_done,
                text=rest,
                keywords=extract_keywords(rest, include_domain=False),
            )

            if is_done:
                self.done_entries.append(entry)
            else:
                self.open_entries.append(entry)

        # Also parse DONE-NNN completion log entries
        done_pattern = re.compile(r"DONE-\d+[:\s](.+)", re.MULTILINE)
        for m in done_pattern.finditer(text):
            entry = IRFEntry(
                irf_id=m.group(0).split(":")[0].split()[0],
                is_done=True,
                text=m.group(1),
                keywords=extract_keywords(m.group(1), include_domain=False),
            )
            self.done_entries.append(entry)

        print(f"  -> {len(self.done_entries)} DONE entries, {len(self.open_entries)} open entries", flush=True)

    @staticmethod
    def _jaccard_match(atom_kw: set[str], entry_kw: set[str]) -> bool:
        """Check if two keyword sets are similar enough using Jaccard index.

        Requires both a minimum absolute overlap AND a minimum Jaccard
        ratio to prevent both tiny-set noise and large-set dilution.
        """
        overlap = atom_kw & entry_kw
        overlap_count = len(overlap)
        if overlap_count < MIN_OVERLAP_IRF:
            return False
        union_count = len(atom_kw | entry_kw)
        if union_count == 0:
            return False
        jaccard = overlap_count / union_count
        return jaccard >= MIN_JACCARD_IRF

    def match_done(self, atom_keywords: set[str]) -> bool:
        """Return True if atom keywords match a DONE IRF entry."""
        # Filter atom keywords with domain stop words for fair comparison
        filtered = atom_keywords - DOMAIN_STOP_WORDS
        if len(filtered) < MIN_OVERLAP_IRF:
            return False
        return any(self._jaccard_match(filtered, e.keywords) for e in self.done_entries)

    def match_open(self, atom_keywords: set[str]) -> bool:
        """Return True if atom keywords match an open IRF entry."""
        filtered = atom_keywords - DOMAIN_STOP_WORDS
        if len(filtered) < MIN_OVERLAP_IRF:
            return False
        return any(self._jaccard_match(filtered, e.keywords) for e in self.open_entries)


# ---------------------------------------------------------------------------
# Evidence Source 3: File/Directory Existence
# ---------------------------------------------------------------------------

# Patterns that suggest a file/repo/directory reference
FILE_PATTERNS = [
    re.compile(r"(?:create|build|add|deploy|write)\s+(?:a\s+)?(?:file|script|module)\s+(?:at\s+|called\s+|named\s+)?[`'\"]?([~./]\S+)", re.IGNORECASE),
    re.compile(r"(?:create|build|add)\s+(?:a\s+)?(?:repo|repository)\s+(?:called\s+|named\s+)?[`'\"]?(\S+)", re.IGNORECASE),
    re.compile(r"[`'\"]?(~/\S+)[`'\"]?", re.IGNORECASE),
    re.compile(r"[`'\"]?(\./\S+)[`'\"]?", re.IGNORECASE),
]

REPO_NAME_PATTERN = re.compile(r"(?:repo|repository)\s+(?:called\s+|named\s+)[`'\"]?([a-zA-Z0-9_-]+(?:--[a-zA-Z0-9_-]+)?)", re.IGNORECASE)


def check_file_existence(content: str) -> bool:
    """Check if files/repos mentioned in atom content actually exist."""
    # Check explicit file paths
    for pattern in FILE_PATTERNS:
        for m in pattern.finditer(content):
            path_str = m.group(1).rstrip("'\"`,.")
            path = Path(os.path.expanduser(path_str))
            if path.exists():
                return True

    # Check repo names against workspace
    for m in REPO_NAME_PATTERN.finditer(content):
        repo_name = m.group(1)
        for org_dir in WORKSPACE.iterdir():
            if org_dir.is_dir() and (org_dir / repo_name).is_dir():
                return True

    return False


# ---------------------------------------------------------------------------
# Evidence Source 4: Hook Inventory
# ---------------------------------------------------------------------------

@dataclass
class HookInventory:
    """Parsed hooks from ~/.claude/settings.json.

    Instead of keyword matching (which produces massive false positives
    because hook command strings contain full English sentences), this
    uses a concept-based approach: each hook is reduced to a short
    descriptor phrase, and atom content is checked for those phrases.
    """
    hook_concepts: list[tuple[str, ...]] = field(default_factory=list)
    hook_event_types: set[str] = field(default_factory=set)

    def build(self) -> None:
        """Parse settings.json for hook definitions and extract concepts."""
        print("[4/6] Building hook inventory...", flush=True)

        if not HOOKS_PATH.exists():
            print("  -> settings.json not found, skipping", flush=True)
            return

        try:
            data = json.loads(HOOKS_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            print("  -> Failed to parse settings.json", flush=True)
            return

        hooks = data.get("hooks", {})
        for event_name, event_hooks in hooks.items():
            self.hook_event_types.add(event_name.lower())
            for hook_group in event_hooks:
                matcher = hook_group.get("matcher", "")
                if_clause = hook_group.get("if", "")

                # Extract the concept from the matcher/if clause, which is
                # the structural part (e.g., "Bash(gh pr comment *)")
                # rather than the verbose command output
                concept_parts = []
                if matcher:
                    concept_parts.append(matcher.lower())
                if if_clause:
                    # Extract the meaningful part from patterns like "Bash(gh pr comment *)"
                    m = re.search(r"\w+\((.+)\)", if_clause)
                    if m:
                        inner = m.group(1).replace("*", "").strip()
                        concept_parts.extend(inner.split())

                if concept_parts:
                    self.hook_concepts.append(tuple(concept_parts))

        # Semantic concepts that are actually enforced by hooks in settings.json.
        # Each tuple requires ALL words to be present as distinct words in the
        # atom content. Use 3+ word tuples to avoid false positives.
        self._semantic_concepts = [
            ("force", "push", "guard"),
            ("force", "push", "warning"),
            ("force", "push", "protect"),
            ("outbound", "preflight"),
            ("memory", "hygiene"),
            ("session", "hygiene"),
            ("registry", "write", "integrity"),
            ("registry", "write", "guard"),
            ("destruction", "guard"),
            ("data", "integrity", "guard"),
            ("data", "integrity", "write"),
            ("1password", "discipline"),
            ("execution", "discipline"),
            ("branch", "delete", "guard"),
            ("issue", "close", "guard"),
            ("hook", "enforcement"),
            ("hook", "guard"),
            ("pretooluse", "guard"),
            ("pretooluse", "hook"),
        ]

        print(f"  -> {len(self.hook_concepts)} hook matchers, {len(self._semantic_concepts)} semantic concepts indexed", flush=True)

    def matches(self, atom_content: str) -> bool:
        """Check if a governance-rule atom is implemented as a hook.

        Uses phrase-based matching with word boundaries: the atom must
        contain ALL words in at least one concept tuple as distinct words,
        not as substrings of other words.
        """
        content_lower = atom_content.lower()
        # Extract word set once for efficient lookup
        content_words = set(re.findall(r"[a-z][a-z0-9_-]+", content_lower))

        for concept in self._semantic_concepts:
            if all(word in content_words for word in concept):
                return True

        return False


# ---------------------------------------------------------------------------
# Evidence Source 5: Memory Inventory
# ---------------------------------------------------------------------------

@dataclass
class MemoryInventory:
    """Parsed topics from MEMORY.md."""
    topic_keywords: list[set[str]] = field(default_factory=list)
    raw_topics: list[str] = field(default_factory=list)

    def build(self) -> None:
        """Parse MEMORY.md for topic entries."""
        print("[5/6] Building memory inventory...", flush=True)

        if not MEMORY_PATH.exists():
            print("  -> MEMORY.md not found, skipping", flush=True)
            return

        text = MEMORY_PATH.read_text(encoding="utf-8")

        # Each line starting with "- " is a topic entry
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("- "):
                topic_text = line[2:]
                self.raw_topics.append(topic_text)
                self.topic_keywords.append(extract_keywords(topic_text))

        print(f"  -> {len(self.raw_topics)} memory topics indexed", flush=True)

    def matches(self, atom_keywords: set[str]) -> bool:
        """Check if atom keywords overlap with memory topics.

        Uses Jaccard similarity to prevent generic vocabulary from
        causing false matches.
        """
        # Filter with domain stop words
        filtered = atom_keywords - DOMAIN_STOP_WORDS
        if len(filtered) < 3:
            return False
        for topic_kw in self.topic_keywords:
            topic_filtered = topic_kw - DOMAIN_STOP_WORDS
            if not topic_filtered:
                continue
            overlap = filtered & topic_filtered
            if len(overlap) < 3:
                continue
            union = len(filtered | topic_filtered)
            if union > 0 and (len(overlap) / union) >= 0.2:
                return True
        return False


# ---------------------------------------------------------------------------
# Evidence Source 6: GitHub Issues/PRs
# ---------------------------------------------------------------------------

def _parse_github_remote(repo_path: Path) -> str | None:
    """Extract org/repo from a git remote URL. Returns None on failure."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return None
        url = result.stdout.strip()
        # SSH: [email redacted]:org/repo.git
        m = re.match(r"git@github\.com:(.+?)(?:\.git)?$", url)
        if m:
            return m.group(1)
        # HTTPS: https://github.com/org/repo.git
        m = re.match(r"https?://github\.com/(.+?)(?:\.git)?$", url)
        if m:
            return m.group(1)
        return None
    except (subprocess.TimeoutExpired, OSError):
        return None


@dataclass
class GitHubEvidence:
    """Issues and PRs from GitHub as implementation evidence."""
    done_keywords: list[set[str]] = field(default_factory=list)
    open_keywords: list[set[str]] = field(default_factory=list)

    def build(self) -> None:
        """Fetch GitHub issues/PRs, using a cache to avoid repeated API calls."""
        print("[3/6] Building GitHub evidence index...", flush=True)

        # Check if gh CLI is available
        if shutil.which("gh") is None:
            print("  -> gh CLI not found, skipping GitHub evidence", flush=True)
            return

        # Check cache freshness
        cache_data = self._load_cache()
        if cache_data is not None:
            self._index_from_cache(cache_data)
            return

        # Walk repos and fetch issues/PRs
        cache_data = {"timestamp": time.time(), "repos": {}}
        repo_count = 0
        issue_count = 0
        pr_count = 0

        for org_dir in sorted(WORKSPACE.iterdir()):
            if not org_dir.is_dir():
                continue
            if org_dir.name in {"intake", "export", "alchemia-ingestvm"}:
                continue

            candidates: list[Path] = []
            if (org_dir / ".git").exists():
                candidates.append(org_dir)
            try:
                for sub in sorted(org_dir.iterdir()):
                    if sub.is_dir() and (sub / ".git").exists():
                        candidates.append(sub)
            except PermissionError:
                continue

            for repo_path in candidates:
                slug = _parse_github_remote(repo_path)
                if not slug:
                    continue

                repo_entry: dict[str, list[dict[str, str]]] = {"issues": [], "prs": []}

                # Fetch issues
                try:
                    result = subprocess.run(
                        ["gh", "issue", "list", "--repo", slug, "--state", "all",
                         "--limit", "100", "--json", "title,state"],
                        capture_output=True, text=True, timeout=30,
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        items = json.loads(result.stdout)
                        repo_entry["issues"] = items
                        issue_count += len(items)
                except (subprocess.TimeoutExpired, OSError, json.JSONDecodeError):
                    pass

                # Fetch PRs
                try:
                    result = subprocess.run(
                        ["gh", "pr", "list", "--repo", slug, "--state", "all",
                         "--limit", "100", "--json", "title,state"],
                        capture_output=True, text=True, timeout=30,
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        items = json.loads(result.stdout)
                        repo_entry["prs"] = items
                        pr_count += len(items)
                except (subprocess.TimeoutExpired, OSError, json.JSONDecodeError):
                    pass

                if repo_entry["issues"] or repo_entry["prs"]:
                    cache_data["repos"][slug] = repo_entry
                    repo_count += 1

        # Write cache
        try:
            GITHUB_CACHE_PATH.write_text(
                json.dumps(cache_data, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        except OSError:
            pass

        self._index_from_cache(cache_data)
        print(f"  -> {repo_count} repos, {issue_count} issues, {pr_count} PRs indexed",
              flush=True)

    def _load_cache(self) -> dict[str, Any] | None:
        """Load cache if it exists and is fresher than GITHUB_CACHE_TTL."""
        if not GITHUB_CACHE_PATH.exists():
            return None
        try:
            data = json.loads(GITHUB_CACHE_PATH.read_text(encoding="utf-8"))
            ts = data.get("timestamp", 0)
            if time.time() - ts < GITHUB_CACHE_TTL:
                print(f"  -> Using cached GitHub evidence "
                      f"({int(time.time() - ts)}s old)", flush=True)
                return data
        except (json.JSONDecodeError, OSError, KeyError):
            pass
        return None

    def _index_from_cache(self, cache_data: dict[str, Any]) -> None:
        """Build keyword indices from cached issue/PR data."""
        for slug, repo_entry in cache_data.get("repos", {}).items():
            for issue in repo_entry.get("issues", []):
                title = issue.get("title", "")
                state = issue.get("state", "").upper()
                kw = extract_keywords(title, include_domain=False)
                if not kw:
                    continue
                if state == "CLOSED":
                    self.done_keywords.append(kw)
                else:
                    self.open_keywords.append(kw)

            for pr in repo_entry.get("prs", []):
                title = pr.get("title", "")
                state = pr.get("state", "").upper()
                kw = extract_keywords(title, include_domain=False)
                if not kw:
                    continue
                if state in ("CLOSED", "MERGED"):
                    self.done_keywords.append(kw)
                else:
                    self.open_keywords.append(kw)

    @staticmethod
    def _jaccard_match(atom_kw: set[str], entry_kw: set[str]) -> bool:
        """Jaccard similarity check, same thresholds as IRF matching."""
        overlap = atom_kw & entry_kw
        overlap_count = len(overlap)
        if overlap_count < MIN_OVERLAP_IRF:
            return False
        union_count = len(atom_kw | entry_kw)
        if union_count == 0:
            return False
        return (overlap_count / union_count) >= MIN_JACCARD_IRF

    def match_done(self, atom_keywords: set[str]) -> bool:
        """Return True if atom keywords match a closed issue or merged PR."""
        filtered = atom_keywords - DOMAIN_STOP_WORDS
        if len(filtered) < MIN_OVERLAP_IRF:
            return False
        return any(self._jaccard_match(filtered, kw) for kw in self.done_keywords)

    def match_open(self, atom_keywords: set[str]) -> bool:
        """Return True if atom keywords match an open issue or PR."""
        filtered = atom_keywords - DOMAIN_STOP_WORDS
        if len(filtered) < MIN_OVERLAP_IRF:
            return False
        return any(self._jaccard_match(filtered, kw) for kw in self.open_keywords)


# ---------------------------------------------------------------------------
# Main Measurement Engine
# ---------------------------------------------------------------------------

@dataclass
class MeasurementResult:
    """Result of measuring a single atom."""
    atom_id: str
    old_status: str
    new_status: str
    evidence_source: str  # "git", "git-file", "github", "github-open", "irf-done", "irf-open", "file", "hook", "memory", "none"


def run_measurement() -> list[MeasurementResult]:
    """Execute the full measurement pipeline."""
    print(f"Loading {ATOMS_PATH.name}...", flush=True)
    atoms: list[dict[str, Any]] = json.loads(ATOMS_PATH.read_text(encoding="utf-8"))
    print(f"  -> {len(atoms)} atoms loaded", flush=True)

    # Build all evidence indices
    git_corpus = GitCorpus()
    git_corpus.build()

    irf_index = IRFIndex()
    irf_index.build()

    github_ev = GitHubEvidence()
    github_ev.build()

    hook_inv = HookInventory()
    hook_inv.build()

    memory_inv = MemoryInventory()
    memory_inv.build()

    # Phase: check each atom against all sources
    print("[6/6] Measuring implementation status...", flush=True)
    results: list[MeasurementResult] = []

    status_counts: Counter[str] = Counter()
    evidence_counts: Counter[str] = Counter()

    for i, atom in enumerate(atoms):
        if (i + 1) % 5000 == 0:
            print(f"  -> {i + 1}/{len(atoms)} atoms processed...", flush=True)

        atom_id = atom.get("atom_id", "")
        old_status = atom.get("status", "UNREVIEWED")
        content = atom.get("content", "")
        atom_type = atom.get("type", "")
        keywords = extract_keywords(content)

        new_status = old_status
        evidence_source = "none"

        # Re-verify ALL atoms — no skipping.
        # Previously this skipped DONE and CLOSED atoms, which meant
        # no evidence was ever recorded for them. Now every atom gets
        # checked against all evidence sources on every run.
        # Status is only UPGRADED (OPEN→DONE), never downgraded
        # (DONE atoms keep their status even if evidence isn't found
        # this run — evidence may have been from a previous check).

        # Check evidence sources in priority order

        # 1. IRF DONE match — strongest signal
        if irf_index.match_done(keywords):
            new_status = "DONE"
            evidence_source = "irf-done"

        # 2. Git history match (commit messages)
        elif git_corpus.match(keywords):
            new_status = "DONE"
            evidence_source = "git"

        # 3. Git file-path match (changed files in recent commits)
        elif git_corpus.match_files(content):
            new_status = "DONE"
            evidence_source = "git-file"

        # 4. GitHub closed issues / merged PRs
        elif github_ev.match_done(keywords):
            new_status = "DONE"
            evidence_source = "github"

        # 5. Hook existence (only for governance-rule atoms)
        elif atom_type == "governance-rule" and hook_inv.matches(content):
            new_status = "DONE"
            evidence_source = "hook"

        # 6. File/directory existence
        elif check_file_existence(content):
            new_status = "DONE"
            evidence_source = "file"

        # 7. Memory coverage (for governance-rule and constraint atoms)
        elif atom_type in ("governance-rule", "constraint") and memory_inv.matches(keywords):
            new_status = "DONE"
            evidence_source = "memory"

        # 8. GitHub open issues/PRs — mark as OPEN
        elif github_ev.match_open(keywords):
            new_status = "OPEN"
            evidence_source = "github-open"

        # 9. IRF open match — mark as OPEN, not DONE
        elif irf_index.match_open(keywords):
            new_status = "OPEN"
            evidence_source = "irf-open"

        # Otherwise: no evidence found this run
        else:
            # Never downgrade: DONE stays DONE (evidence may be from prior run)
            if old_status == "DONE":
                new_status = "DONE"
            else:
                new_status = old_status if old_status != "N/A" else "UNREVIEWED"
            evidence_source = "none"

        # Never downgrade DONE → OPEN (only upgrade OPEN → DONE)
        if old_status == "DONE" and new_status != "DONE":
            new_status = "DONE"
        atom["status"] = new_status
        # Record evidence source in the atom for audit trail
        if evidence_source != "none":
            produced = atom.get("produced", [])
            if evidence_source not in produced:
                produced.append(evidence_source)
            atom["produced"] = produced
        results.append(MeasurementResult(atom_id, old_status, new_status, evidence_source))
        status_counts[new_status] += 1
        evidence_counts[evidence_source] += 1

    print(f"\nStatus distribution:", flush=True)
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}", flush=True)
    print(f"\nEvidence sources:", flush=True)
    for source, count in sorted(evidence_counts.items()):
        print(f"  {source}: {count}", flush=True)

    # Write updated atoms
    print(f"\nWriting updated {ATOMS_PATH.name}...", flush=True)
    ATOMS_PATH.write_text(
        json.dumps(atoms, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"  -> {len(atoms)} atoms written", flush=True)

    return results


# ---------------------------------------------------------------------------
# Scorecard Generation
# ---------------------------------------------------------------------------

def generate_scorecard(atoms: list[dict[str, Any]], results: list[MeasurementResult]) -> None:
    """Generate IMPLEMENTATION-SCORECARD.md from measurement results."""
    print(f"\nGenerating {SCORECARD_PATH.name}...", flush=True)

    total = len(atoms)
    status_counts: Counter[str] = Counter()
    by_source: dict[str, Counter[str]] = defaultdict(Counter)
    by_type: dict[str, Counter[str]] = defaultdict(Counter)
    by_universe: dict[str, Counter[str]] = defaultdict(Counter)
    by_evidence: Counter[str] = Counter()

    # Collect unimplemented directive themes for top-20
    unimplemented_directives: list[str] = []

    for atom, result in zip(atoms, results):
        status = atom.get("status", "UNREVIEWED")
        source = atom.get("source", "unknown")
        atom_type = atom.get("type", "unknown")
        universes = atom.get("universes", ["unscoped"])

        status_counts[status] += 1
        by_source[source][status] += 1
        by_type[atom_type][status] += 1
        for u in universes:
            by_universe[u][status] += 1
        by_evidence[result.evidence_source] += 1

        if status in ("UNREVIEWED", "N/A") and atom_type == "directive":
            # Normalize content for theme extraction
            content = atom.get("content", "").strip()
            if len(content) > 10:
                unimplemented_directives.append(content)

    # Extract top themes from unimplemented directives using keyword clustering
    # Use domain-filtered keywords to exclude boilerplate system vocabulary
    theme_keywords: Counter[str] = Counter()
    for content in unimplemented_directives:
        for kw in extract_keywords(content, include_domain=False):
            if len(kw) >= 5:  # Slightly higher threshold for themes
                theme_keywords[kw] += 1

    def pct(n: int) -> str:
        return f"{n / total * 100:.1f}%" if total > 0 else "0.0%"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines: list[str] = []
    lines.append("# Implementation Scorecard")
    lines.append("")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Source:** `prompt-atoms.json` ({total:,} atoms)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Overall
    lines.append("## Overall")
    lines.append("")
    done_total = status_counts.get("DONE", 0)
    open_total = status_counts.get("OPEN", 0)
    closed_total = sum(v for k, v in status_counts.items() if k.startswith("CLOSED-"))
    unrev_total = status_counts.get("UNREVIEWED", 0) + status_counts.get("N/A", 0)
    lines.append(f"| Metric | Count | Percentage |")
    lines.append(f"|--------|-------|------------|")
    lines.append(f"| Total atoms | {total:,} | 100% |")
    lines.append(f"| DONE | {done_total:,} | {pct(done_total)} |")
    lines.append(f"| OPEN (IRF/GitHub tracked) | {open_total:,} | {pct(open_total)} |")
    lines.append(f"| CLOSED-* | {closed_total:,} | {pct(closed_total)} |")
    lines.append(f"| UNREVIEWED | {unrev_total:,} | {pct(unrev_total)} |")
    lines.append("")

    # Evidence source breakdown
    lines.append("### Evidence Sources")
    lines.append("")
    lines.append("| Source | Atoms Matched |")
    lines.append("|--------|--------------|")
    for source, count in sorted(by_evidence.items(), key=lambda x: -x[1]):
        lines.append(f"| {source} | {count:,} |")
    lines.append("")

    # By source (chatgpt, claude-code, codex)
    lines.append("## By Source")
    lines.append("")
    lines.append("| Source | Total | DONE | OPEN | CLOSED | UNREVIEWED |")
    lines.append("|--------|-------|------|------|--------|------------|")
    for source in sorted(by_source.keys()):
        counts = by_source[source]
        src_total = sum(counts.values())
        done = counts.get("DONE", 0)
        open_n = counts.get("OPEN", 0)
        closed = sum(v for k, v in counts.items() if k.startswith("CLOSED-"))
        unrev = counts.get("UNREVIEWED", 0) + counts.get("N/A", 0)
        d_pct = f"{done / src_total * 100:.1f}%" if src_total > 0 else "0%"
        o_pct = f"{open_n / src_total * 100:.1f}%" if src_total > 0 else "0%"
        c_pct = f"{closed / src_total * 100:.1f}%" if src_total > 0 else "0%"
        u_pct = f"{unrev / src_total * 100:.1f}%" if src_total > 0 else "0%"
        lines.append(f"| {source} | {src_total:,} | {done:,} ({d_pct}) | {open_n:,} ({o_pct}) | {closed:,} ({c_pct}) | {unrev:,} ({u_pct}) |")
    lines.append("")

    # By type
    lines.append("## By Type")
    lines.append("")
    lines.append("| Type | Total | DONE | OPEN | CLOSED | UNREVIEWED |")
    lines.append("|------|-------|------|------|--------|------------|")
    for atom_type in sorted(by_type.keys()):
        counts = by_type[atom_type]
        t_total = sum(counts.values())
        done = counts.get("DONE", 0)
        open_n = counts.get("OPEN", 0)
        closed = sum(v for k, v in counts.items() if k.startswith("CLOSED-"))
        unrev = counts.get("UNREVIEWED", 0) + counts.get("N/A", 0)
        d_pct = f"{done / t_total * 100:.1f}%" if t_total > 0 else "0%"
        o_pct = f"{open_n / t_total * 100:.1f}%" if t_total > 0 else "0%"
        c_pct = f"{closed / t_total * 100:.1f}%" if t_total > 0 else "0%"
        u_pct = f"{unrev / t_total * 100:.1f}%" if t_total > 0 else "0%"
        lines.append(f"| {atom_type} | {t_total:,} | {done:,} ({d_pct}) | {open_n:,} ({o_pct}) | {closed:,} ({c_pct}) | {unrev:,} ({u_pct}) |")
    lines.append("")

    # By universe
    lines.append("## By Universe")
    lines.append("")
    lines.append("| Universe | Total | DONE | OPEN | CLOSED | UNREVIEWED |")
    lines.append("|----------|-------|------|------|--------|------------|")
    for universe in sorted(by_universe.keys()):
        counts = by_universe[universe]
        u_total = sum(counts.values())
        done = counts.get("DONE", 0)
        open_n = counts.get("OPEN", 0)
        closed = sum(v for k, v in counts.items() if k.startswith("CLOSED-"))
        unrev = counts.get("UNREVIEWED", 0) + counts.get("N/A", 0)
        d_pct = f"{done / u_total * 100:.1f}%" if u_total > 0 else "0%"
        o_pct = f"{open_n / u_total * 100:.1f}%" if u_total > 0 else "0%"
        c_pct = f"{closed / u_total * 100:.1f}%" if u_total > 0 else "0%"
        u_pct = f"{unrev / u_total * 100:.1f}%" if u_total > 0 else "0%"
        lines.append(f"| {universe} | {u_total:,} | {done:,} ({d_pct}) | {open_n:,} ({o_pct}) | {closed:,} ({c_pct}) | {unrev:,} ({u_pct}) |")
    lines.append("")

    # Top 20 unimplemented directive themes
    lines.append("## Top 20 Unimplemented Directive Themes")
    lines.append("")
    lines.append("Keywords extracted from directives still at UNREVIEWED status,")
    lines.append("ranked by frequency across all unimplemented directives.")
    lines.append("")
    lines.append("| Rank | Keyword | Occurrences |")
    lines.append("|------|---------|-------------|")
    for rank, (keyword, count) in enumerate(theme_keywords.most_common(20), 1):
        lines.append(f"| {rank} | {keyword} | {count:,} |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"*Engine: `measure_implementation.py` | Run: {now}*")
    lines.append("")

    SCORECARD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"  -> Scorecard written to {SCORECARD_PATH}", flush=True)


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the full measurement pipeline."""
    print("=" * 60)
    print("  ORGANVM Implementation Measurement Engine")
    print("=" * 60)
    print()

    if not ATOMS_PATH.exists():
        print(f"ERROR: {ATOMS_PATH} not found", file=sys.stderr)
        sys.exit(1)

    results = run_measurement()

    # Reload atoms after mutation for scorecard
    atoms = json.loads(ATOMS_PATH.read_text(encoding="utf-8"))
    generate_scorecard(atoms, results)

    print("\nDone.")


if __name__ == "__main__":
    main()
