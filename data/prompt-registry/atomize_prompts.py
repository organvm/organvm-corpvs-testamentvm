#!/usr/bin/env python3
"""Atomize prompts into micro-units.

Reads prompt-registry.json and decomposes each macro prompt into discrete
micro-units (directives, rules, questions, signals). Outputs prompt-atoms.json.

Ontology:
  PROMPT (macro) → MICRO-UNIT (atom) → UNIVERSE INSTANCES (expansion)

This script handles macro → micro. Universe expansion is separate.
"""

import json
import re
from pathlib import Path

REGISTRY_DIR = Path(__file__).parent
INPUT_FILE = REGISTRY_DIR / "prompt-registry.json"
OUTPUT_FILE = REGISTRY_DIR / "prompt-atoms.json"
OUTPUT_MD = REGISTRY_DIR / "PROMPT-ATOMS-SUMMARY.md"

# Atom types
DIRECTIVE = "directive"
GOVERNANCE = "governance-rule"
QUESTION = "question"
CONSTRAINT = "constraint"
IMPLICIT = "implicit-signal"
EMOTIONAL = "emotional"
DATA = "data"
CORRECTION = "correction"
COMMAND = "command"


def split_on_thought_separators(text: str) -> list[str]:
    """Split on the user's thought separators: --, ;, numbered lists."""
    segments = []

    # First: numbered lists like [1], [2] or 1., 2.
    numbered = re.split(r"(?:^|\n)\s*(?:\[(\d+)\]|\((\d+)\)|(\d+)[\.\)])\s*", text)
    if len(numbered) > 3:  # has numbered items
        for chunk in numbered:
            if chunk and not chunk.strip().isdigit():
                segments.append(chunk.strip())
        return [s for s in segments if s]

    # Second: double-dash separator
    if "--" in text and text.count("--") <= 10:
        parts = re.split(r"\s*--\s*", text)
        if len(parts) > 1 and all(len(p) > 5 for p in parts if p.strip()):
            return [p.strip() for p in parts if p.strip()]

    # Third: semicolons
    if ";" in text and text.count(";") <= 8:
        parts = text.split(";")
        if len(parts) > 1 and all(len(p) > 5 for p in parts if p.strip()):
            return [p.strip() for p in parts if p.strip()]

    # Fourth: sentence-level splitting for multi-sentence prompts
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    if len(sentences) > 1:
        return [s.strip() for s in sentences if len(s.strip()) > 10]

    # Single unit
    return [text.strip()] if text.strip() else []


def classify_atom(text: str) -> str:
    """Classify a single micro-unit by type."""
    lower = text.lower().strip()

    # Commands
    if text.startswith("/"):
        return COMMAND

    # Questions — check for ? anywhere, not just at end
    if "?" in text:
        rhetorical_markers = [
            "how many times", "how many fucking", "what am i doing wrong",
            "is that not true", "right?", "correct?",
        ]
        if any(m in lower for m in rhetorical_markers):
            return GOVERNANCE
        return QUESTION

    # Questions — interrogative starts
    if re.match(r"^(how do|what is|where is|why is|can we|should we|does |is there|are there|what'?s|how)", lower):
        return QUESTION

    # Governance rules — expanded
    gov_patterns = [
        r"\bmust\b", r"\bnever\b", r"\balways\b", r"\brule\b",
        r"\bnon-negotiable\b", r"\brequire[ds]?\b", r"\bmandat",
        r"\bevery single\b", r"\bno exception", r"\bfail",
        r"vacuum", r"persist", r"enforce",
        # Temporal governance markers
        r"\bfrom now on\b", r"\bgoing forward\b", r"\bhenceforth\b",
        r"\bevery time\b", r"\beach time\b", r"\bwhenever\b",
        # Rule declarations
        r"\bthe rule is\b", r"\bthe law is\b", r"\bthe principle is\b",
        # Arrow rules (user uses → and => for rules)
        r"→", r"=>", r"->",
    ]
    for pat in gov_patterns:
        if re.search(pat, lower):
            return GOVERNANCE

    # Corrections
    if any(w in lower for w in ["wrong", "not that", "actually", "no--", "not correct"]):
        return CORRECTION

    # Emotional signals
    if any(w in lower for w in ["fuck", "shit", "sick of", "frustrated", "idiot", "moron"]):
        return EMOTIONAL

    # Constraints — expanded
    constraint_words = [
        "without", "don't", "stop", "not",
        r"\bonly\b", r"\bjust\b", r"\bno more than\b", r"\bat most\b", r"\bat least\b",
        r"\bexcept\b", r"\bunless\b", r"\bbut not\b", r"\bother than\b",
    ]
    for w in constraint_words:
        if w.startswith(r"\b"):
            if re.search(w, lower):
                return CONSTRAINT
        elif w in lower:
            return CONSTRAINT

    # Directives — expanded with modal verbs and imperative detection
    directive_words = [
        r"\bsolve\b", r"\bbuild\b", r"\bcreate\b", r"\bimplement\b",
        r"\bfix\b", r"\bwrite\b", r"\bdesign\b", r"\bwe need\b",
        r"\blet'?s\b", r"\bmake\b", r"\bensure\b", r"\bwire\b",
        r"\bfind\b", r"\bcheck\b", r"\breview\b", r"\bgo\b",
        r"\bstart\b", r"\bdo\b", r"\brun\b", r"\badd\b",
        r"\bremove\b", r"\bdelete\b", r"\bclean\b",
        r"\bi want\b", r"\bi need\b",
        # Modal verbs
        r"\bshould\b", r"\bought to\b", r"\bneed to\b", r"\bhave to\b",
        # Additional imperatives
        r"\bproceed\b", r"\bcontinue\b", r"\bdeploy\b", r"\bpush\b",
        r"\bcommit\b", r"\binstall\b", r"\bset up\b", r"\bconfigure\b",
        r"\bupdate\b", r"\bupgrade\b", r"\bmigrate\b", r"\bscaffold\b",
        r"\brefactor\b", r"\btest\b", r"\baudit\b", r"\bverify\b",
    ]
    for pat in directive_words:
        if re.search(pat, lower):
            return DIRECTIVE

    # Imperative mood — segment starts with a common verb
    imperative_verbs = [
        "check", "fix", "build", "find", "make", "ensure", "wire", "run",
        "go", "start", "stop", "remove", "add", "update", "create", "review",
        "proceed", "continue", "solve", "design", "implement", "deploy",
        "set", "get", "put", "move", "copy", "read", "write", "show",
        "list", "search", "open", "close", "merge", "push", "pull",
    ]
    first_word = lower.split()[0] if lower.split() else ""
    if first_word in imperative_verbs:
        return DIRECTIVE

    # Data/pasted content
    if len(text) > 500 and text.count("\n") > 5:
        return DATA

    # Rescue: long segments with verbs are likely directives, not implicit
    if len(text) > 50:
        common_verbs = ["is", "are", "was", "were", "have", "has", "do", "does",
                        "make", "take", "get", "give", "go", "come", "see", "know",
                        "want", "need", "use", "find", "tell", "work", "call", "try"]
        if any(f" {v} " in f" {lower} " for v in common_verbs):
            return DIRECTIVE

    # Implicit signals (catch-all for what's left)
    if len(text) > 20:
        return IMPLICIT

    return IMPLICIT


def detect_universe_hints(text: str) -> list[str]:
    """Detect which universes/contexts a micro-unit might apply to."""
    hints = []
    lower = text.lower()

    # Organs
    organ_patterns = {
        "organ-i": r"\borgan.?i\b|\btheoria\b|\btheory\b|\brecursive\b",
        "organ-ii": r"\borgan.?ii\b|\bpoiesis\b|\bart\b|\bgenerative\b|\bperformance\b",
        "organ-iii": r"\borgan.?iii\b|\bergon\b|\bcommerce\b|\bproduct\b|\bsaas\b|\bstripe\b|\bincome\b",
        "organ-iv": r"\borgan.?iv\b|\btaxis\b|\borchestrat\b|\bagent\b|\bconductor\b",
        "organ-v": r"\borgan.?v\b|\blogos\b|\bessay\b|\bpublic.?process\b",
        "organ-vi": r"\borgan.?vi\b|\bkoinonia\b|\bcommunity\b|\bsalon\b",
        "organ-vii": r"\borgan.?vii\b|\bkerygma\b|\bdistribut\b|\bposse\b",
        "meta": r"\bmeta\b|\bregistry\b|\birf\b|\bgovernance\b|\bdashboard\b",
        "personal": r"\bdomus\b|\bdotfile\b|\bchezmoi\b|\bportfolio\b|\bpadavano\b|\bresume\b",
    }
    for universe, pattern in organ_patterns.items():
        if re.search(pattern, lower):
            hints.append(universe)

    # Life domains
    life_patterns = {
        "employment": r"\bjob\b|\bemploy\b|\bhiring\b|\bapplication\b|\bresume\b|\binterview\b",
        "housing": r"\bhous\b|\brent\b|\bshelter\b|\bapartment\b|\blive\b",
        "financial": r"\bmoney\b|\bbill\b|\bpay\b|\bdebt\b|\btax\b|\bincome\b|\brevenue\b",
        "health": r"\bhealth\b|\bdiet\b|\bwork.?out\b|\bsubstance\b|\brecovery\b",
        "relationships": r"\bbecka\b|\bfamily\b|\bmother\b|\bfriend\b",
        "education": r"\bmfa\b|\bfau\b|\bteach\b|\badjunct\b|\bacademi\b",
    }
    for domain, pattern in life_patterns.items():
        if re.search(pattern, lower):
            hints.append(domain)

    # System domains
    system_patterns = {
        "naming": r"\bnam[ei]\b|\bslug\b|\btitle\b|\brename\b",
        "persistence": r"\bpersist\b|\bsave\b|\bcommit\b|\bpush\b|\bbackup\b|\blocal.*remote\b",
        "enforcement": r"\bhook\b|\benforc\b|\bguard\b|\brule\b|\bconstraint\b",
        "security": r"\bsecret\b|\bpassword\b|\bkey\b|\b1password\b|\bcredential\b",
        "automation": r"\blaunchagent\b|\bdaemon\b|\bcron\b|\bautomat\b|\bschedul\b",
    }
    for domain, pattern in system_patterns.items():
        if re.search(pattern, lower):
            hints.append(domain)

    # Universal hints
    if any(w in lower for w in ["every", "all", "universal", "everywhere", "always", "system"]):
        hints.append("UNIVERSAL")

    return hints if hints else ["unscoped"]


def inherit_universe_from_project(project_path: str) -> list[str]:
    """Inherit universe tags from the project directory path."""
    inherited = []
    lower = project_path.lower()

    mappings = [
        (["organvm-i-theoria", "/theoria/"], "organ-i"),
        (["organvm-ii-poiesis", "/poiesis/"], "organ-ii"),
        (["organvm-iii-ergon", "/ergon/"], "organ-iii"),
        (["organvm-iv-taxis", "/taxis/"], "organ-iv"),
        (["organvm-v-logos", "/logos/"], "organ-v"),
        (["organvm-vi-koinonia", "/koinonia/"], "organ-vi"),
        (["organvm-vii-kerygma", "/kerygma/"], "organ-vii"),
        (["meta-organvm", "/meta/"], "meta"),
        (["4444j99", "domus", "portfolio"], "personal"),
        (["application-pipeline"], "employment"),
    ]

    for patterns, universe in mappings:
        if any(p in lower for p in patterns):
            inherited.append(universe)

    return inherited


def atomize_prompt(prompt: dict) -> list[dict]:
    """Decompose a macro prompt into micro-unit atoms."""
    content = prompt.get("content", "")
    if not content or len(content.strip()) < 3:
        return []

    # Inherit universes from project directory
    project_path = prompt.get("project_path", "")
    inherited_universes = inherit_universe_from_project(project_path)

    # Skip pure slash commands — they're already atomic
    if content.strip().startswith("/") and len(content.strip()) < 30:
        return [{
            "atom_id": "",
            "parent_prompt_id": prompt.get("id", ""),
            "type": COMMAND,
            "content": content.strip(),
            "summary": content.strip(),
            "universes": inherited_universes or [],
            "status": "N/A",
            "produced": [],
            "source": prompt.get("source", "unknown"),
            "date": prompt.get("date", ""),
            "timestamp": prompt.get("timestamp", ""),
            "response_summary": prompt.get("response_summary", ""),
        }]

    # Split into segments
    segments = split_on_thought_separators(content)

    atoms = []
    for i, segment in enumerate(segments):
        if len(segment.strip()) < 3:
            continue

        atom_type = classify_atom(segment)
        universe_hints = detect_universe_hints(segment)

        # Merge inherited universes from project directory
        for u in inherited_universes:
            if u not in universe_hints:
                universe_hints.append(u)

        # Governance rules get UNIVERSAL by default
        if atom_type == GOVERNANCE and "UNIVERSAL" not in universe_hints:
            universe_hints.append("UNIVERSAL")

        # Remove "unscoped" if we now have real universe hints
        if len(universe_hints) > 1 and "unscoped" in universe_hints:
            universe_hints.remove("unscoped")

        summary = segment[:150].replace("\n", " ").strip()
        if len(segment) > 150:
            summary += "..."

        atoms.append({
            "atom_id": "",  # assigned after collection
            "parent_prompt_id": prompt.get("id", ""),
            "type": atom_type,
            "content": segment,
            "summary": summary,
            "universes": universe_hints,
            "status": "UNREVIEWED",
            "produced": [],
            "source": prompt.get("source", "unknown"),
            "date": prompt.get("date", ""),
            "timestamp": prompt.get("timestamp", ""),
            "response_summary": prompt.get("response_summary", ""),
        })

    return atoms


def generate_summary(all_atoms: list[dict]) -> str:
    """Generate a markdown summary of the atomized corpus."""
    lines = []
    lines.append("# Prompt Atoms — Micro-Unit Registry")
    lines.append("")
    from datetime import datetime
    lines.append(f"**Generated:** {datetime.now().isoformat()}")
    lines.append(f"**Total atoms:** {len(all_atoms)}")

    # By type
    type_counts: dict[str, int] = {}
    for a in all_atoms:
        type_counts[a["type"]] = type_counts.get(a["type"], 0) + 1

    lines.append("")
    lines.append("## By Type")
    lines.append("")
    lines.append("| Type | Count | % |")
    lines.append("|------|-------|---|")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {t} | {c} | {c/len(all_atoms)*100:.1f}% |")

    # By source
    source_counts: dict[str, int] = {}
    for a in all_atoms:
        source_counts[a["source"]] = source_counts.get(a["source"], 0) + 1

    lines.append("")
    lines.append("## By Source")
    lines.append("")
    lines.append("| Source | Atoms |")
    lines.append("|--------|-------|")
    for s, c in sorted(source_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {s} | {c} |")

    # Universe distribution
    universe_counts: dict[str, int] = {}
    for a in all_atoms:
        for u in a["universes"]:
            universe_counts[u] = universe_counts.get(u, 0) + 1

    lines.append("")
    lines.append("## Universe Distribution")
    lines.append("")
    lines.append("| Universe | Atoms |")
    lines.append("|----------|-------|")
    for u, c in sorted(universe_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {u} | {c} |")

    # Status
    status_counts: dict[str, int] = {}
    for a in all_atoms:
        status_counts[a["status"]] = status_counts.get(a["status"], 0) + 1

    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|--------|-------|")
    for s, c in sorted(status_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {s} | {c} |")

    # Directive atoms (the implementation tracking surface)
    directives = [a for a in all_atoms if a["type"] == DIRECTIVE]
    lines.append("")
    lines.append(f"## Directives — {len(directives)} atoms requiring implementation")
    lines.append("")
    lines.append("| ID | Date | Source | Universes | Summary |")
    lines.append("|----|------|--------|-----------|---------|")
    for a in directives[:200]:  # first 200 for readability
        universes = ", ".join(a["universes"][:3])
        summary = a["summary"][:80].replace("|", "\\|")
        lines.append(f"| {a['atom_id']} | {a['date']} | {a['source']} | {universes} | {summary} |")
    if len(directives) > 200:
        lines.append(f"| ... | ... | ... | ... | ({len(directives)-200} more) |")

    # Governance rules
    rules = [a for a in all_atoms if a["type"] == GOVERNANCE]
    lines.append("")
    lines.append(f"## Governance Rules — {len(rules)} atoms")
    lines.append("")
    for a in rules[:100]:
        lines.append(f"- **{a['atom_id']}** [{a['date']}] {a['summary']}")
    if len(rules) > 100:
        lines.append(f"- ... and {len(rules)-100} more")

    return "\n".join(lines)


def main():
    # Load prompts
    prompts = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    print(f"Loaded {len(prompts)} prompts")

    # Atomize
    all_atoms = []
    for prompt in prompts:
        atoms = atomize_prompt(prompt)
        all_atoms.extend(atoms)

    # Assign sequential IDs
    for i, atom in enumerate(all_atoms, 1):
        atom["atom_id"] = f"ATM-{i:06d}"

    print(f"Generated {len(all_atoms)} atoms ({len(all_atoms)/len(prompts):.1f} avg per prompt)")

    # Write JSON
    OUTPUT_FILE.write_text(
        json.dumps(all_atoms, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"JSON → {OUTPUT_FILE}")

    # Write summary
    md = generate_summary(all_atoms)
    OUTPUT_MD.write_text(md, encoding="utf-8")
    print(f"Summary → {OUTPUT_MD}")

    # Stats
    types = {}
    for a in all_atoms:
        types[a["type"]] = types.get(a["type"], 0) + 1
    print("\nAtom types:")
    for t, c in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()
