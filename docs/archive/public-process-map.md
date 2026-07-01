# ORGAN-V: Public Process Infrastructure

**Status:** Design Document (Ready to Implement)  
**Version:** 1.0  
**Owner:** Public Process Organ  
**Target Launch:** Week 3  

---

## Executive Summary

ORGAN-V is your "building in public" layer. It documents methodology, process, and learnings from ORGAN-I (Theory), ORGAN-II (Art), and ORGAN-III (Commerce).

**Core function:** Transform closed-door work into shareable essays, creating audience visibility and establishing thought leadership.

**Three components:**
1. **Essays & Marginalia** — Long-form process documentation
2. **Changelog & Milestones** — Timestamped project history
3. **Distribution** — RSS, newsletter, social amplification

---

## Table of Contents

1. [Repo Structure](#repo-structure)
2. [Essay System](#essay-system)
3. [Changelog System](#changelog-system)
4. [RSS & Newsletter](#rss--newsletter)
5. [Automation](#automation)
6. [Publishing Workflow](#publishing-workflow)

---

## Repo Structure

### Main ORGAN-V Repo: `public-process`

Location: New repo in `4444J99-organs` org  
Visibility: PUBLIC  
Structure:

```
public-process/
├── README.md                          # Overview + getting started
├── PUBLISHING_GUIDE.md                # How to submit essays
├── essays/                            # Long-form content
│   ├── 2026-02-03--how-we-orchestrate-organs.md
│   ├── 2026-01-15--recursive-engine-at-scale.md
│   └── archive/
│       └── 2025--q4/
├── marginalia/                        # Short-form process notes
│   ├── decision-logs/
│   │   └── 2026-02--orchestration-design-choices.md
│   ├── methodology/
│   │   └── constraint-alchemy-in-practice.md
│   └── lessons-learned/
│       └── what-failed-and-why.md
├── changelog/                         # Project milestones
│   ├── CHANGELOG.md                   # Auto-generated from issues
│   └── MILESTONES.md                  # Major releases/announcements
├── guides/                            # Educational content
│   ├── how-to-think-about-autonomous-systems.md
│   ├── epistemic-tuning-explained.md
│   └── constraint-alchemy-workshop.md
├── case-studies/                      # Detailed project retrospectives
│   ├── classroom-rpg-aetheria--post-mortem.md
│   ├── orchestration-system--design-rationale.md
│   └── crisis-toolkit--community-impact.md
├── data/                              # Supporting JSON/CSV
│   ├── essays-metadata.json           # Article metadata (date, tags, authors)
│   ├── engagement-metrics.json        # Views, shares, discussion stats
│   └── publication-calendar.json      # Scheduled essays
├── _site/                             # Generated static site (Jekyll or Hugo)
│   ├── index.html
│   ├── feed.xml
│   └── sitemap.xml
├── .github/
│   └── workflows/
│       ├── publish-essay.yml          # Validate, publish, distribute
│       ├── generate-changelog.yml     # Auto-generate from repo events
│       └── distribute-to-channels.yml # POSSE automation
└── .github/
    └── CODEOWNERS
        └── (you @4444j99)
```

---

## Essay System

### Essay Anatomy

**Header (YAML frontmatter):**

```markdown
---
title: How We Orchestrate Seven Organs Across 46 GitHub Repositories
subtitle: A System for Coordinating Art, Theory, and Commerce
author: 4444j99
date: 2026-02-03
published: true
tags: [systems, orchestration, github, automation]
excerpt: >
  Building a seven-organ creative system requires automated orchestration.
  Here's how we coordinate 46 repos across theory, art, and commerce using
  governance rules and GitHub Actions.
toc: true
featured_image: images/seven-organs.png
related_repos:
  - orchestration-start-here
  - recursive-engine--generative-entity
  - core-engine
word_count: 4200
reading_time: 18
---
```

**Content (Markdown):**

```markdown
# How We Orchestrate Seven Organs

## Problem

Managing multiple creative systems — theory frameworks, artistic implementations,
and commercial products — is a coordination nightmare...

## Solution

We designed ORGAN-IV: an orchestration layer that...

## Implementation

### Step 1: Central Registry
[code example]

### Step 2: Governance Rules
[code example]

### Step 3: GitHub Actions Automation
[code example]

## Lessons Learned

1. **Start with data, not code.** The registry is more important than workflows.
2. **Governance rules must be explicit.** Automation only works if rules are codified.
3. **Cross-repo automation is hard.** GitHub Actions has limitations; we use custom Python.

## Next Steps

- [ ] Implement monthly organ audit
- [ ] Add promotion workflows
- [ ] Deploy POSSE automation

## Further Reading

- [System Governance Framework](https://github.com/ivviiviivvi/system-governance-framework)
- [Recursive Engine](https://github.com/ivviiviivvi/recursive-engine--generative-entity)

---

**Discussion:** [Open issue on orchestration-start-here](https://github.com/4444J99-orchestration/orchestration-start-here/issues/42)

**Cite:** 4444j99 (2026). "How We Orchestrate Seven Organs..." *Public Process*.
```

### Essay Categories

**By Source:**

| Category | Source Organ | Frequency | Example |
|----------|---|---|---|
| **Methodology** | ORGAN-I, ORGAN-II | Monthly | "How Recursive Systems Generate Novel Outputs" |
| **Implementation** | ORGAN-II, ORGAN-III | Bi-monthly | "Building Orchestration: A Case Study" |
| **Product Retrospectives** | ORGAN-III | Quarterly | "Aetheria RPG: Post-Mortem and Metrics" |
| **Decision Logs** | ORGAN-IV | As-needed | "Why We Chose JSON Over YAML for Registry" |
| **Community Impact** | ORGAN-VI, ORGAN-V | Quarterly | "Crisis Toolkit Year 1: Impact and Lessons" |

**By Format:**

- **Long-form essays** (3,000–5,000 words) — Deep dives into methodology
- **Case studies** (2,000–3,000 words) — Project retrospectives with concrete data
- **Decision logs** (500–1,000 words) — Rationale for architectural choices
- **Marginalia** (100–500 words) — Short notes, observations, quick learnings
- **Guides** (1,500–2,500 words) — Educational or "how-to" content

### Submission & Review Process

**For published repos (you):**

1. Write essay in local branch: `essays/YYYY-MM-DD--slug.md`
2. Commit with metadata in frontmatter
3. Push and open PR with checklist:
   - [ ] Frontmatter complete
   - [ ] Links to source repos work
   - [ ] Spelling/grammar checked
   - [ ] Code examples tested
   - [ ] Related repos tagged
   - [ ] Read time estimated
4. Self-review, merge to `main`
5. GitHub Actions auto-runs publish workflow (see Automation)

**For guest essays (community members):**

1. Fork repo
2. Create essay in `essays/guest/`
3. Open PR with guest credentials in frontmatter
4. Review for coherence + accuracy
5. Request changes or merge
6. Auto-publish and distribute

---

## Changelog System

### Purpose

Every product, framework, and system has a story. The changelog makes it visible.

### Structure

**CHANGELOG.md** (auto-generated):

```markdown
# Changelog

All notable changes to the seven-organ system are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Orchestration system (ORGAN-IV) now live with 5 core workflows
- Monthly organ audit with critical alert detection
- Promotion pipeline: Theory → Art → Commerce → Public Process

### Changed
- Central registry now JSON-based (migrated from YAML)
- Dependency validation now blocks PRs (was advisory)

### Fixed
- Circular dependency in `multi-camera--livestream--framework`
- Broken cross-references in Art organ repos

## [1.0] — 2026-02-01

### Added
- Seven-organ architecture implemented
- 46 repos mapped and organized
- Core governance rules codified
- GitHub Actions automation stack deployed

---

## [0.1] — 2025-12-01

### Added
- System design and audit complete
- Theory and Commerce organs operational

```

**MILESTONES.md** (manual + auto-generated):

```markdown
# Major Milestones

## 2026 Q1: Orchestration Goes Live

- ✅ Central registry created and deployed
- ✅ 5 core GitHub Actions workflows active
- ✅ Monthly organ audit established
- ✅ Promotion pipeline tested end-to-end
- 🔄 Public process infrastructure launched
- 🔄 Marketing/distribution pipeline built

## 2025 Q4: System Architecture Complete

- ✅ Seven-organ model defined and validated
- ✅ All 46 repos audited and mapped
- ✅ Governance rules documented
- ✅ First two organs (Theory, Commerce) operational

## 2025 Q3: Crisis Toolkit Deployed

- ✅ NYC writer crisis resources compiled
- ✅ Interactive navigation system live
- ✅ 1,000+ writers reached

```

### Auto-Generation

**Trigger:** GitHub Actions runs on every release or PR merge  
**Source:** GitHub API (issues, PRs, releases)  
**Script:**

```python
#!/usr/bin/env python3
import json
from github import Github
from datetime import datetime

def generate_changelog(org_list, since=None):
    """Generate CHANGELOG from cross-org GitHub events."""
    
    g = Github(token=os.getenv('GITHUB_TOKEN'))  # allow-secret
    
    all_events = []
    
    for org_name in org_list:
        org = g.get_organization(org_name)
        
        for repo in org.get_repos():
            # Fetch recent PRs and releases
            for pr in repo.get_pulls(state='closed', sort='updated'):
                all_events.append({
                    'date': pr.updated_at,
                    'type': 'merged_pr',
                    'repo': repo.name,
                    'title': pr.title,
                    'labels': [l.name for l in pr.labels]
                })
            
            for release in repo.get_releases():
                all_events.append({
                    'date': release.published_at,
                    'type': 'release',
                    'repo': repo.name,
                    'version': release.tag_name,
                    'notes': release.body
                })
    
    # Group by date and category
    changelog = {}
    for event in sorted(all_events, key=lambda x: x['date'], reverse=True):
        date_key = event['date'].strftime('%Y-%m-%d')
        category = categorize_event(event['labels'])
        
        if date_key not in changelog:
            changelog[date_key] = {}
        if category not in changelog[date_key]:
            changelog[date_key][category] = []
        
        changelog[date_key][category].append(event)
    
    # Render as Markdown
    output = "# Changelog\n\n"
    for date_key, categories in sorted(changelog.items(), reverse=True):
        output += f"## {date_key}\n\n"
        for category, events in categories.items():
            output += f"### {category}\n\n"
            for event in events:
                output += f"- [{event['repo']}] {event['title']}\n"
        output += "\n"
    
    return output

if __name__ == '__main__':
    changelog = generate_changelog([
        'ivviiviivvi',
        'omni-dromenon-machina',
        'labores-profani-crux',
        '4444J99-orchestration'
    ])
    
    with open('CHANGELOG.md', 'w') as f:
        f.write(changelog)
```

---

## RSS & Newsletter

### RSS Feed

**Location:** `_site/feed.xml` (auto-generated)  
**Format:** Atom 1.0 (most compatible)  
**Updated:** Whenever essays published

**Template:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>4444j99 — Public Process</title>
  <link href="https://github.com/4444J99-organs/public-process" rel="alternate"/>
  <link href="https://4444j99.orchestration/feed.xml" rel="self"/>
  <id>https://4444j99.orchestration/</id>
  <updated>2026-02-03T00:00:00Z</updated>
  
  <entry>
    <title>How We Orchestrate Seven Organs Across 46 GitHub Repositories</title>
    <link href="https://github.com/4444J99-organs/public-process/blob/main/essays/2026-02-03--how-we-orchestrate-organs.md"/>
    <link rel="alternate" type="text/html" href="..."/>
    <id>https://github.com/4444J99-organs/public-process/essays/2026-02-03--how-we-orchestrate-organs.md</id>
    <published>2026-02-03T00:00:00Z</published>
    <updated>2026-02-03T00:00:00Z</updated>
    <author>
      <name>4444j99</name>
    </author>
    <summary type="html">Building a seven-organ creative system requires automated orchestration...</summary>
    <content type="html">[full essay content]</content>
    <category term="systems" label="systems"/>
    <category term="orchestration" label="orchestration"/>
  </entry>
</feed>
```

**Generation:** Via Jekyll/Hugo, auto-run on every merge to `main`

**Subscribe:** Users add `https://github.com/4444J99-organs/public-process/feed.xml` to their reader

### Newsletter

**Platform:** Substack or Ghost  
**Frequency:** Weekly  
**Content:** Curated essays + community highlights  
**Subscription link:** Auto-generated in RSS feed description

**Template:**

```markdown
# Public Process — Week of Feb 3, 2026

## This Week's Essays

1. **How We Orchestrate Seven Organs**
   New post on coordinating 46 repos across theory, art, and commerce.
   [Read →](link)

2. **Recursive Engines at Scale**
   Case study: Deploying generative systems to 1,000s of users.
   [Read →](link)

## Community Highlights

- 50+ stars on orchestration-start-here this week
- New contributor: [name] added essays on constraint alchemy
- Discord: 30 active members in #theory discussions

## What's Coming

Next week: Product retrospective on Aetheria RPG, with metrics and learnings.

---

Subscribe here | Unsubscribe | Discuss on Discord | GitHub
```

---

## Automation

### Workflow 1: publish-essay.yml

**Trigger:** PR labeled `ready-to-publish`  
**Actions:**

```yaml
name: Publish Essay

on:
  pull_request:
    types: [labeled]

jobs:
  publish:
    if: contains(github.event.pull_request.labels.*.name, 'ready-to-publish')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate Frontmatter
        run: |
          # Check that YAML frontmatter is valid
          python3 scripts/validate-frontmatter.py essays/*.md
      
      - name: Check Links
        run: |
          # Verify all internal/external links work
          python3 scripts/check-links.py essays/*.md
      
      - name: Generate Reading Time
        run: |
          # Calculate word count and reading time
          python3 scripts/calc-reading-time.py essays/*.md
      
      - name: Build Static Site
        run: |
          # Build HTML via Jekyll/Hugo
          jekyll build --source . --destination _site
      
      - name: Commit Changes
        run: |
          git config user.name "Public Process Bot"
          git config user.email "[email redacted]"
          git add .
          git commit -m "Publish essay: $(date +%Y-%m-%d)"
          git push
      
      - name: Update RSS
        run: |
          # Generate/update feed.xml
          python3 scripts/generate-rss.py
          git add _site/feed.xml
          git commit -m "Update RSS feed"
          git push
      
      - name: Comment Success
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `✅ Essay published!\n\n- Website: [view](https://4444j99.orchestration/essays/...)\n- RSS: [subscribe](https://4444j99.orchestration/feed.xml)\n- Threads ready for distribution`
            });
```

### Workflow 2: generate-changelog.yml

**Trigger:** Cron (daily at midnight) + Manual  
**Actions:** Generate CHANGELOG.md from GitHub events

```yaml
name: Generate Changelog

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Changelog Script
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python3 scripts/generate-changelog.py
      
      - name: Commit
        run: |
          git config user.name "Public Process Bot"
          git config user.email "[email redacted]"
          
          if git diff --quiet CHANGELOG.md; then
            echo "No changes"
          else
            git add CHANGELOG.md
            git commit -m "Auto-update changelog"
            git push
          fi
```

### Workflow 3: distribute-to-channels.yml

**Trigger:** Essay published (PR merged)  
**Actions:** Announce across platforms

```yaml
name: Distribute to Channels

on:
  push:
    branches: [main]
    paths: [essays/**]

jobs:
  distribute:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Extract Metadata
        id: meta
        run: |
          # Get title, excerpt, tags from frontmatter
          python3 scripts/extract-metadata.py
      
      - name: Post to Mastodon
        env:
          MASTODON_TOKEN: ${{ secrets.MASTODON_TOKEN }}
        run: |
          # Thread-based announcement
          python3 scripts/post-mastodon.py \
            --title "${{ steps.meta.outputs.title }}" \
            --excerpt "${{ steps.meta.outputs.excerpt }}"
      
      - name: Post to LinkedIn
        env:
          LINKEDIN_TOKEN: ${{ secrets.LINKEDIN_TOKEN }}
        run: |
          # Professional announcement
          python3 scripts/post-linkedin.py \
            --title "${{ steps.meta.outputs.title }}"
      
      - name: Add to Newsletter Queue
        run: |
          # Append to next week's newsletter
          echo "- [${{ steps.meta.outputs.title }}](...link...)" \
            >> newsletter/queue.md
      
      - name: Discord Announcement
        env:
          DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
        run: |
          # Post to community channel
          curl ${{ env.DISCORD_WEBHOOK }} \
            -X POST \
            -d "{\"content\": \"📝 New essay: ${{ steps.meta.outputs.title }}\"}"
      
      - name: Notify Source Repos
        run: |
          # Open issue in mentioned source repos
          for repo in ${{ steps.meta.outputs.mentioned_repos }}; do
            gh issue create \
              --repo "$repo" \
              --title "Your work featured in public process essay" \
              --body "Read: ${{ steps.meta.outputs.title }}"
          done
```

---

## Publishing Workflow

### Step-by-Step: Publishing an Essay

**1. Write**

```bash
# Create essay in local repo
touch essays/2026-02-03--your-essay-slug.md

# Edit with frontmatter + content
# Test links and code examples locally
```

**2. Commit & Push**

```bash
git checkout -b essays/your-essay-slug
git add essays/2026-02-03--your-essay-slug.md
git commit -m "Essay: Your Essay Title"
git push origin essays/your-essay-slug
```

**3. Open PR**

- Title: "Essay: Your Essay Title"
- Description: Brief summary
- Add label: `ready-to-publish` (or just assign to yourself)
- Self-review checklist in PR body

**4. Merge**

- GitHub Actions auto-runs:
  - Validates frontmatter
  - Checks links
  - Calculates reading time
  - Builds static site
  - Updates RSS feed
  - Posts announcements

**5. Monitor Distribution**

- Essay appears on website
- RSS feed updates
- Mastodon/LinkedIn posts scheduled
- Newsletter queue updated
- Source repos notified

**6. Engage**

- Track engagement metrics
- Pin popular essays
- Link in community channels
- Archive annually

---

## Metrics & Analytics

### Engagement Tracking

**File:** `data/engagement-metrics.json`

```json
{
  "essays": [
    {
      "slug": "2026-02-03--how-we-orchestrate-organs",
      "title": "How We Orchestrate Seven Organs",
      "date": "2026-02-03",
      "status": "published",
      "metrics": {
        "github_views": 145,
        "github_stars": 8,
        "mastodon_boosts": 23,
        "mastodon_replies": 5,
        "linkedin_impressions": 1200,
        "linkedin_engagement": 47,
        "newsletter_clicks": 234,
        "total_discussion_threads": 3
      },
      "related_repos": [
        "orchestration-start-here",
        "recursive-engine--generative-entity"
      ]
    }
  ]
}
```

**Updated via:** Manual logging + GitHub API queries (automated weekly)

### Goals

- **Reach:** 500+ monthly unique readers
- **Engagement:** 5% click-through rate on newsletter
- **Community:** 3+ new contributors per quarter
- **Thought leadership:** Featured in 2+ external publications per year

---

## Content Calendar

### Q1 2026

| Week | Topic | Source | Format | Status |
|------|-------|--------|--------|--------|
| Feb 3 | Orchestration System | ORGAN-IV | Essay | ✅ Published |
| Feb 10 | Theory Foundations | ORGAN-I | Essay | 🟡 Draft |
| Feb 17 | Aetheria Retrospective | ORGAN-III | Case Study | 🔴 Outline |
| Feb 24 | Community Impact | ORGAN-VI | Essay | 🔴 Not started |
| Mar 3 | Constraint Alchemy | ORGAN-I | Guide | 🔴 Not started |
| Mar 10 | Generative Art Pipeline | ORGAN-II | Methodology | 🔴 Not started |

---

## Getting Started

### Week 3 Implementation

**Day 1-2:**
1. Create `public-process` repo
2. Copy directory structure (essays/, changelog/, etc.)
3. Commit sample essays (templates)
4. Set up Jekyll or Hugo for static site

**Day 3-4:**
1. Create GitHub Actions workflows
2. Test on sample essays
3. Deploy to GitHub Pages

**Day 5:**
1. Publish first essay (this orchestration system design)
2. Test RSS generation
3. Test distribution workflows

**Day 6-7:**
1. Set up newsletter/Substack integration
2. Create content calendar
3. Onboard first guest contributors (optional)

---

## Success Criteria

- [ ] Public process repo launched
- [ ] First 3 essays published
- [ ] RSS feed generating correctly
- [ ] Newsletter workflow established
- [ ] Distribution to 3+ platforms automated
- [ ] Engagement metrics dashboard created
- [ ] Monthly publishing cadence established

---

**Status:** Ready to implement  
**Owner:** You (@4444j99)  
**Timeline:** Week 3 (20 hours)  
**Next:** Coordinate with GitHub Actions team on distribution automation
