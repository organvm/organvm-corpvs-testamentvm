# Key Workflows

**Purpose:** Step-by-step guides for common operations in the eight-organ system.
**Audience:** A competent developer with GitHub experience but no prior knowledge of this system.
**Last updated:** 2026-03-07

> **Note:** Sections 2 (Promote a Repo), 3 (Publish an Essay), and 6 (Add a New Repo) have been formalized as governed SOPs in `praxis-perpetua/standards/`. The canonical procedures are:
> - Section 2 -> `SOP--promotion-and-state-transitions.md`
> - Section 3 -> `SOP--essay-publishing-and-distribution.md`
> - Section 6 -> `SOP--repo-onboarding-and-habitat-creation.md`
>
> The steps below are retained as quick-reference operational guides tied to this corpus's specific scripts and toolchain.

---

## Table of Contents

1. [Update the Registry](#1-update-the-registry)
2. [Promote a Repo](#2-promote-a-repo)
3. [Publish an Essay](#3-publish-an-essay)
4. [Submit an Application](#4-submit-an-application)
5. [Run the Soak Test Monitor](#5-run-the-soak-test-monitor)
6. [Add a New Repo to the System](#6-add-a-new-repo-to-the-system)
7. [Run a Document Audit & Feature Extraction](#7-run-a-document-audit--feature-extraction)

---

## 1. Update the Registry

The registry (`repo-registry.json`) is the single source of truth for all repo state. Any change to a repo's status, metadata, or dependencies must be reflected here.

### When to update
- Repo implementation status changes (e.g., SKELETON -> PROTOTYPE -> ACTIVE)
- New repo added to the system
- Repo archived or removed
- Dependencies change
- Documentation status changes

### Steps

1. **Open the registry:**
   ```bash
   cd ~/Workspace/meta-organvm/organvm-corpvs-testamentvm
   ```
   Edit `repo-registry.json` in your editor.

2. **Find the repo entry.** Repos are nested under `organs.<ORGAN-KEY>.repositories[]`. Each entry has:
   ```json
   {
     "name": "repo-name",
     "org": "organvm-i-theoria",
     "implementation_status": "ACTIVE",
     "documentation_status": "DEPLOYED",
     "description": "...",
     "public": true,
     "portfolio_relevance": "CRITICAL|HIGH|MEDIUM|LOW"
   }
   ```

3. **Make your change.** Common updates:
   - `implementation_status`: ACTIVE | PROTOTYPE | SKELETON | DESIGN_ONLY | ARCHIVED
   - `documentation_status`: DEPLOYED | SKELETON | EMPTY
   - ORGAN-III repos also need: `type` (SaaS/B2B/B2C/internal), `revenue_model`, `revenue_status`

4. **Update aggregate counts** if you added/removed a repo:
   - `total_repos` (top-level field)
   - `total_repos_note` (description of count)
   - The relevant organ's `repository_count`
   - `implementation_status_distribution` (top-level summary)

5. **Validate:**
   ```bash
   python3 scripts/organ-audit.py \
       --registry repo-registry.json \
       --governance governance-rules.json \
       --output /tmp/audit-check.md
   ```
   Expect: `AUDIT PASSED`

6. **Commit and push:**
   ```bash
   git add repo-registry.json
   git commit -m "chore: update registry — <describe change>"
   git push origin main
   ```

---

## 2. Promote a Repo

Promotion moves work between organs following the state machine: LOCAL -> CANDIDATE -> PUBLIC_PROCESS -> GRADUATED -> ARCHIVED.

There are three promotion paths (defined in `governance-rules.json`):
- **Theory -> Art:** ORGAN-I repo inspires an ORGAN-II creative project
- **Art -> Commerce:** ORGAN-II project becomes an ORGAN-III product
- **Any -> Public Process:** Any repo's work becomes an ORGAN-V essay topic

### Steps

1. **Verify preconditions** (from `governance-rules.json`):
   - Source repo has `documentation_status != EMPTY`
   - Source repo has documented use cases in README
   - Source repo has `implementation_status` of PROTOTYPE or ACTIVE
   - No unresolved critical audit alerts for the source

2. **Create the destination repo** (if it doesn't exist):
   ```bash
   gh repo create <destination-org>/<new-repo-name> --public --description "..."
   ```

   Naming conventions:
   - Theory -> Art: `art-from--<source-name>` in `organvm-ii-poiesis`
   - Art -> Commerce: `<source-name>` in `organvm-iii-ergon`
   - Any -> Public Process: `essay-from--<source-name>` in `organvm-v-logos`

3. **Update the registry:**
   - Add the new repo entry to the destination organ
   - Add a dependency edge from the new repo to the source repo
   - Update `promotion_status` on the source repo

4. **Create a `seed.yaml`** in the new repo (if the system uses them):
   ```yaml
   schema_version: "1.0"
   organ: "ORGAN-II"
   org: "organvm-ii-poiesis"
   repo: "art-from--recursive-engine"
   metadata:
     description: "Creative interpretation of recursive-engine concepts"
   consumes:
     - type: "theory"
       from: "organvm-i-theoria/recursive-engine--generative-entity"
   produces:
     - type: "creative-artifact"
   ```

5. **Validate the dependency graph** (no back-edges allowed):
   ```bash
   python3 scripts/v4-dependency-validation.py
   ```

---

## 3. Publish an Essay

Essays live in ORGAN-V (`organvm-v-logos/public-process`) as Jekyll posts in the `_posts/` directory.

### Steps

1. **Write the essay.** Draft it locally or in `docs/essays/` of this corpus. Target: 3,000–5,000 words.

2. **Format as Jekyll post.** Filename: `YYYY-MM-DD-slug-title.md`
   ```markdown
   ---
   layout: post
   title: "Your Essay Title"
   date: 2026-02-16
   categories: [meta-system]
   ---

   Essay content here...
   ```

3. **Deploy to public-process:**
   ```bash
   cd ~/Workspace/organvm-v-logos/public-process
   cp <draft-path> _posts/2026-02-16-your-essay-slug.md
   git add _posts/2026-02-16-your-essay-slug.md
   git commit -m "essay: your essay title"
   git push origin main
   ```

4. **Verify deployment:** The essay-monitor workflow (daily 09:00 UTC) will detect it, or trigger manually:
   ```bash
   gh workflow run essay-monitor.yml --repo organvm-iv-taxis/orchestration-start-here
   ```

5. **Update system metrics** (if the portfolio dashboard tracks essay counts):
   ```bash
   cd ~/Workspace/meta-organvm/organvm-corpvs-testamentvm
   python3 scripts/praxis-metrics-dashboard.py --output system-metrics.json
   ```

---

## 4. Submit an Application

Application materials live in `docs/applications/` of this corpus. Three audience tracks are pre-built:
- **AI Engineering:** `01-track-ai-engineering.md` + cover letters in `cover-letters/`
- **Grants:** `02-track-grants.md`
- **Residencies:** `03-track-residencies.md`

### Steps

1. **Choose a target** from `04-application-tracker.md`. Each entry has: deadline, framing, lead projects, materials status.

2. **Review the submission bundle** in `07-submission-bundles.md` — this maps targets to pre-assembled evidence packages.

3. **Prepare materials:**
   - Confirm all URLs resolve (portfolio, GitHub repos, essays)
   - Verify claims against `repo-registry.json` (repo counts, status, etc.)
   - Run link check: `grep -oP 'https?://[^\s)]+' docs/applications/<file>.md | while read url; do curl -sI "$url" | head -1; done`

4. **Submit** via the target's application portal (browser — not automatable).

5. **Update the tracker:**
   ```bash
   # Edit docs/applications/04-application-tracker.md
   # Change status to SUBMITTED, add submission date
   git add docs/applications/04-application-tracker.md
   git commit -m "chore: mark <target> as submitted"
   git push origin main
   ```

6. **Follow up:** Note confirmation emails, expected response timeline in the tracker.

---

## 5. Run the Soak Test Monitor

The soak test monitor collects daily system health snapshots and generates 30-day reports.

### Daily Collection

```bash
cd ~/Workspace/meta-organvm/organvm-corpvs-testamentvm

# Full collection (hits GitHub API — takes 3-5 minutes)
python3 scripts/soak-test-monitor.py collect

# Dry run (validates registry only, no API calls)
python3 scripts/soak-test-monitor.py collect --dry-run
```

Output: `data/soak-test/daily-YYYY-MM-DD.json`

### Generate Report

```bash
# Generate 30-day summary
python3 scripts/soak-test-monitor.py report

# Or specify a different window
python3 scripts/soak-test-monitor.py report --days 7
```

Output: `data/soak-test/report.md`

### Automating Collection

For true 30-day soak testing, schedule daily collection. On macOS:

```bash
# Option 1: crontab
crontab -e
# Add: 0 10 * * * cd ~/Workspace/meta-organvm/organvm-corpvs-testamentvm && python3 scripts/soak-test-monitor.py collect >> /tmp/soak-test.log 2>&1

# Option 2: launchd (preferred on macOS)
# Create ~/Library/LaunchAgents/com.organvm.soak-test.plist
# (see macOS launchd documentation for plist format)
```

---

## 6. Add a New Repo to the System

### Steps

1. **Create the repo on GitHub:**
   ```bash
   gh repo create <org>/<repo-name> --public --description "..."
   ```

2. **Add a README.md** — every README is a portfolio piece. Use existing repos in the same organ as style reference. Target: 2,500+ words for portfolio-relevant repos.

3. **Add to the registry:**
   Edit `repo-registry.json` and add the repo entry under the appropriate organ:
   ```json
   {
     "name": "repo-name",
     "org": "organvm-ii-poiesis",
     "implementation_status": "SKELETON",
     "documentation_status": "DEPLOYED",
     "public": true,
     "description": "What this repo does",
     "portfolio_relevance": "MEDIUM",
     "tier": "silver",
     "dependencies": []
   }
   ```

4. **Update counts:**
   - Increment `total_repos`
   - Increment the organ's `repository_count`
   - Update `implementation_status_distribution` if needed

5. **Add a `seed.yaml`** (for orchestration integration):
   ```yaml
   schema_version: "1.0"
   organ: "ORGAN-II"
   org: "organvm-ii-poiesis"
   repo: "repo-name"
   metadata:
     description: "What this repo does"
   produces:
     - type: "creative-artifact"
   consumes:
     - type: "theory"
       from: "organvm-i-theoria/some-dependency"
   ```

6. **Set GitHub topics** (for discoverability):
   ```bash
   gh api "repos/<org>/<repo>/topics" --method PUT --input - <<EOF
   {"names": ["organvm", "organ-ii", "generative-art"]}
   EOF
   ```

7. **Validate:**
   ```bash
   python3 scripts/organ-audit.py \
       --registry repo-registry.json \
       --governance governance-rules.json \
       --output /tmp/new-repo-audit.md
   ```

8. **Commit registry changes:**
   ```bash
   git add repo-registry.json
   git commit -m "feat: add <repo-name> to ORGAN-II"
   git push origin main
   ```

---

## 7. Run a Document Audit & Feature Extraction

Systematically read every document in a repo's `docs/` directory, extract product/feature ideas, deduplicate against existing tracking, and create GitHub issues for everything genuinely new.

**Full SOP:** [`sop--document-audit-feature-extraction.md`](./sop--document-audit-feature-extraction.md)

### When to run

- New repo with existing documentation enters the system
- Major bulk import of research, brainstorm, or reference materials
- Quarterly review (Week 4 of the monthly cadence)
- Pre-beta audit for an ORGAN-III product

### Steps (summary — v2.0, 8 phases)

0. **Scope & Classify** — determine repo topology (single/multi-repo), classify document types (authored, transcript, reference, RFC/ADR, code/wiki), build routing table if multi-repo, plan agent allocation.

1. **Inventory & Triage** — list all files, classify format, convert unreadable formats (pandoc/Calibre), assign thematic cohorts or folder order, cluster shared-prompt docs, flag high-density docs, build `MANIFEST.md`.

2. **Read & Extract** — read every document word-for-word using type-specific heuristics. Double-read high-density docs. Self-estimate coverage per document; re-read any below 70%.

3. **Completeness Proof (mandatory gate)** — fresh agents re-read all docs adversarially. Produce coverage table, detect antagonistic tensions. Gate: >=80% overall, >=50% per-doc, all tensions identified. Fail -> return to Phase 2.

4. **Dedup & Tension Resolution** — cross-ref against backlog, issues, codebase. Merge source-cluster overlaps. Classify: SKIP / ENHANCE / CREATE / TENSION. Resolve each tension.

5. **Synthesis** — identify cross-cutting themes (3+ docs or 2+ repos). Map theme dependencies, integrate tensions, compile risk data, produce execution order.

6. **Create Issues** — route by Phase 0 routing table. Sequential creation (>=2s delay). Title: `feat: ...`. Body: Source, Problem, Proposed Feature, Tensions, Cross-References. Batch by category, maintain running tally.

7. **Post-Audit Artifacts** — update `FEATURE-BACKLOG.md`, `MANIFEST.md`, `SYLLABUS.md` (variant: academic/tooling/mixed). Commit synthesis doc + completeness proof. Write audit summary with retrospective. File SOP amendment recommendations.

### Quick commands

```bash
# Pre-audit: inventory existing issues
gh issue list --repo <org>/<repo> --state open --limit 500

# During audit: create issues
gh issue create --repo <org>/<repo> --title "feat: ..." --body "..." --label "enhancement"

# During audit: enhance existing issues
gh issue comment <N> --repo <org>/<repo> --body "Additional context from audit..."

# Format conversion
pandoc -f epub -t plain input.epub -o output.txt
pandoc -f pdf -t plain input.pdf -o output.txt
```

See the full SOP for the issue body template, label taxonomy, parallelization guide, format conversion reference, document type heuristics, multi-repo routing guide, completeness proof methodology, SYLLABUS variants, and retrospective template.

---

## Quick Reference: Common Commands

```bash
# Audit the system
python3 scripts/organ-audit.py --registry repo-registry.json --governance governance-rules.json --output audit.md --github

# Validate dependencies only
python3 scripts/v4-dependency-validation.py

# Generate metrics dashboard
python3 scripts/praxis-metrics-dashboard.py --output system-metrics.json

# Collect soak test snapshot
python3 scripts/soak-test-monitor.py collect

# List essays in public-process
gh api repos/organvm-v-logos/public-process/git/trees/HEAD?recursive=1 --jq '[.tree[] | select(.path | startswith("_posts/")) | .path] | sort[]'

# Check workflow status
gh run list --repo organvm-iv-taxis/orchestration-start-here --limit 10
```
