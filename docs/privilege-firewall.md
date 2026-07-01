# Privilege Firewall

**Date:** 2026-04-28
**Status:** Active operational firewall
**Scope:** All artifacts produced under ORGANVM, chezmoi, `~/.claude/`, `~/Workspace/a-i--skills/`, and any externally-facing surface.
**Privilege classification of this doc:** SAFE — meta-level only; no case content.

## Purpose

[name redacted] is in active litigation, with attorney Micah Longo as counsel. The substrate Anthony builds (ORGANVM + skills + memory + plans) must NEVER encode privileged content from this case. The legal-domain skill (and any product that derives from this work — Praxis Curia, the post-trigger pitch) must be reproducible by a practitioner who never met Micah, never read a discovery doc, never heard a privileged word.

**Operational test:** If a sentence in a shipped artifact would not have existed had this case never happened, it is contaminated. Cut, or rewrite from public sources.

## The five categories

| Category | Status | Rule |
|----------|--------|------|
| Generic legal-practice domain (FRCP, ABA model rules, public bar opinions, public scholarship) | SAFE | Cite to public sources; no Micah-attribution. |
| Anything case-specific (claims, parties, dates, theories of liability, settlement posture, opposing counsel, witness identities) | UNSAFE | Never enters any shipped artifact, ever. Stays in case-only Drive folder; never in chezmoi, never in GitHub, never in iCloud-shared, never in `~/.claude/` memory. |
| Patterns observed working with Micah, stripped of identifying facts | GREY | SAFE only when (a) the pattern exists in 2+ public sources independently, AND (b) the artifact does not name Micah as the source. UNSAFE if the pattern was learned uniquely from this case or only fits this fact pattern. **Default action: cut.** |
| Citations to public legal scholarship / industry analysis | SAFE | Standard citation hygiene. |
| Fact that Anthony has worked with Micah | SAFE | Already in public memory; can appear in pitch deck cover, LinkedIn, etc. |

## Auto-deny patterns

Terms/patterns that trigger automatic rejection in any committed file:
- Specific case-party names (stored privately in `~/Library/PrivilegeAuditDB/blocklist.txt`, chmod 600, OUTSIDE chezmoi)
- Document names from discovery (PDFs, exhibits, exhibit numbers)
- Specific docket numbers
- Specific motion captions
- Settlement figures
- Names of opposing parties / counsel / witnesses
- Specific dates of hearings, depositions, filings (when paired with case-context)

The blocklist itself lives outside chezmoi by design — committing the blocklist to chezmoi would *publish* the very terms it's meant to seal.

## Chezmoi exclusion list

Add to `~/Workspace/4444J99/domus-semper-palingenesis/.chezmoiignore`:

```
**/lawsuit/**
**/litigation/**
**/case-files/**
**/discovery/**
**/depo*/**
**/*-privileged.*
~/Dropbox/Lawsuit-*
~/Documents/Legal-Active/
```

## Pre-commit hook (W4 deliverable, not yet built)

**Path:** `~/Workspace/4444J99/domus-semper-palingenesis/.chezmoiscripts/pre-commit-privilege-scan.sh`

**Behavior:**
1. On every chezmoi auto-commit, scan staged files for any term in `~/Library/PrivilegeAuditDB/blocklist.txt`.
2. If match found: HARD BLOCK with exit 1, error message "PRIVILEGE FIREWALL VIOLATION: case content detected in [file]:[line]. Review and remove before commit."
3. If clean: pass through to commit.

**Critical:** Hook is **on-demand** (fires at git-commit time only), NOT a LaunchAgent. Per `feedback_no_launchagents.md`: every prior LaunchAgent froze the machine. Hard rule.

## Trigger conditions for post-litigation pitch

The Micah pitch (Praxis Curia productization conversation) is gated until first to occur of:

- **(a) Settlement signed and on the public docket** — verifiable via public PACER or state-court docket
- **(b) Case dismissed or judgment entered AND any appeal window closed** — verifiable via public docket + calendar
- **(c) Micah explicitly invites the conversation in writing** — email or text from Micah explicitly opening the topic

Until any trigger fires: pitch deck v0 stays at `DRAFT-LOCKED-UNTIL-TRIGGER`. System refuses to send. If user impulses to pitch early, hold the deck and re-surface this firewall doc.

**Decision cascade — no anxiety.** The trigger is the trigger. Don't deliberate. Don't pitch early. Don't send a "soft test" message. Hold until.

## Non-circumvention rules

1. **Never paraphrase privileged content** — even paraphrase carries provenance.
2. **Never attribute** — patterns observed cannot name Micah as source.
3. **Never anchor to case dates** — examples must use synthetic dates, not real ones.
4. **Never use case docket as exemplar** — even with redaction, the shape leaks.
5. **No drift from public sources** — every legal example traces to FRCP / public reporters / ABA / academic legal scholarship.
6. **No "by way of analogy to my case"** phrasing — break the analogy entirely.
7. **No memory of privileged conversations** — if a conversation contained privileged content, the *memory of that conversation* is forbidden, not just its specific words.
8. **No counsel-shaped reasoning** — do not encode reasoning that exists because Micah's counsel shaped it; encode reasoning that any competent practitioner could derive from public sources.

## Audit trail

When firewall integrity is questioned, run this on-demand command (NOT a LaunchAgent):

```bash
grep -rE -f ~/Library/PrivilegeAuditDB/blocklist.txt \
  ~/.claude/ \
  ~/Workspace/organvm/ \
  ~/Workspace/4444J99/domus-semper-palingenesis/ \
  ~/Workspace/a-i--skills/
```

Zero hits expected. Any hit = HARD BLOCK incident:
1. Quarantine the offending artifact (move to `~/Library/PrivilegeAuditDB/quarantine/YYYY-MM-DD/`)
2. Audit recent commits (last 30 days) for related leakage
3. Rotate the blocklist with new terms if the leak suggests a pattern not yet covered
4. File the incident as a CURIA case (when Phase 1 lands)

## What this is NOT

- **Not legal advice.** This is an operational firewall by Anthony for Anthony's own substrate. Bar obligations are Micah's; this firewall protects substrate, not the bar.
- **Not professional ethics counsel.** If a question of ethics arises (e.g., is X privileged?), ask Micah, not this doc.
- **Not retroactive.** Pre-2026-04-28 commits exist in git history; if any contain leaked content, that is a separate incident requiring git history audit and possible rebase. This firewall is forward-acting.
- **Not infallible.** A sufficiently subtle leak (paraphrased pattern with no auto-deny match) can slip through. The audit + manual review caught what auto-deny missed. Triple-check before shipping any artifact that touches legal practice.

## Cross-references

- CURIA Phase 0 spec: `~/.claude/plans/2026-04-28-curia-organ-viii-specification.md`
- Plan file: `~/.claude/plans/going-through-a-lawsuit-fizzy-moth.md` (duplicated to canonical name `~/.claude/plans/2026-04-28-curia-organ-viii-and-legal-domain-instancing.md` per Plan File Discipline — both retained, never overwrite)
- Collaborator memory: `~/.claude/projects/-Users-[user]/memory/collaborator_micah.md` + `_PRIVILEGE_BOUNDARY.md`
- Legal-practice-domain skill: `~/Workspace/a-i--skills/legal-practice-domain/SKILL.md`
- Pre-commit hook (W4, not yet built): `~/Workspace/4444J99/domus-semper-palingenesis/.chezmoiscripts/pre-commit-privilege-scan.sh`
- LaunchAgent rule: `feedback_no_launchagents.md` (HARD; this firewall's hook is on-demand only)

---

*Filed under operational governance. The firewall is the load-bearing piece — every downstream artifact (legal-practice-domain skill, CURIA, post-trigger Micah pitch, Praxis Curia productization) assumes this exists and is enforced.*
