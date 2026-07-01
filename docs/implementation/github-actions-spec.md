# GitHub Actions Specification: ORGAN-IV Automation Stack

**Version:** 2.0
**Status:** IMPLEMENTED (Consolidation Sprint 2026-02-11)
**Framework:** GitHub Actions (native, no external runners needed)
**Deployment Location:** `orchestration-start-here` repo

> **Implementation Status (2026-02-11):** All 5 core workflows deployed and tested. distribute-content.yml upgraded with LinkedIn POSSE + Ghost newsletter endpoints. Per-repo `.meta/dependencies.json` deployed to 7 flagship repos. Branch protection active on 5 flagship repos. ORCHESTRATION_PAT secret required for cross-org operations (promote-repo, publish-process).

---

## Overview

Five core workflows automate the entire eight-organ system:

| Workflow | Trigger | Purpose | Latency |
|----------|---------|---------|---------|
| **validate-dependencies** | Every PR in any repo | Block merge if deps invalid | <2 min |
| **monthly-organ-audit** | Cron: 1st of month | Full system health check | ~15 min |
| **promote-repo** | Repo label + comment | Handle Theory→Art→Commerce promotions | <5 min |
| **publish-process** | Issue label in ORGAN-III | Automate ORGAN-V essay creation | On-demand |
| **distribute-content** | Issue label in ORGAN-V | Trigger POSSE/newsletter distribution | On-demand |

All workflows read from `registry.json` and `governance-rules.json` as the single source of truth.

---

## Architecture Pattern

### Data-Driven Workflows

**Every workflow follows this pattern:**

```
Trigger Event
    ↓
Read Central Registry (registry.json)
    ↓
Apply Governance Rules (governance-rules.json)
    ↓
Execute Actions (open PR, close issue, notify, etc.)
    ↓
Update Registry + Create Audit Trail
```

This ensures consistency: **logic lives in data files, not workflow code.**

### Reusable Actions

All workflows use these composable actions:

1. **fetch-registry** — Clone/update central registry
2. **validate-against-rules** — Check constraints
3. **notify-organs** — Cross-repo notifications
4. **update-dependencies** — Modify `.meta/` files
5. **log-event** — Audit trail

These live in `orchestration-start-here/.github/actions/` and are reusable across workflows.

---

## Workflow 1: validate-dependencies

**Purpose:** Prevent merging code that violates dependency rules  
**Trigger:** On PR opened/updated in ANY repo  
**Latency:** <2 minutes

### Setup Instructions

1. Create `.github/workflows/validate-dependencies.yml` in **EVERY** repo (use template):

```yaml
name: Validate Dependencies

on:
  pull_request:
    paths:
      - '.meta/dependencies.json'
      - 'package.json'
      - 'requirements.txt'
      - 'Cargo.toml'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Fetch Central Registry
        run: |
          curl -s https://raw.githubusercontent.com/organvm-iv-taxis/orchestration-start-here/main/registry.json \
            -o registry.json
      
      - name: Check Dependency Rules
        run: |
          # Pseudocode; real implementation in Python/Node
          python3 - <<'EOF'
          import json
          
          # Load registry and PR changes
          registry = json.load(open('registry.json'))
          current_repo = "${{ github.repository }}"
          
          # Extract dependencies from PR diff
          # (uses gh CLI to fetch diff)
          
          # Validate against rules:
          # 1. No circular dependencies
          # 2. Dependencies only flow downward in organ hierarchy
          # 3. Transitive depth <= 4
          
          if violations:
              print(f"FAILED: {violations}")
              exit(1)
          else:
              print("PASSED: All dependency rules satisfied")
              exit(0)
          EOF
      
      - name: Comment Results
        if: always()
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const results = fs.readFileSync('validation-results.txt', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Dependency Validation\n\n${results}`
            });
```

2. **Deployment:** Copy this template to all 46 repos (automated via second workflow)

3. **Force as required status check:**
   - Settings → Branches → Branch protection rule
   - Require `validate-dependencies` to pass before merge

### Configuration

Create `.meta/dependencies.json` in every repo:

```json
{
  "repo_name": "my-great-engine",
  "organ": "ORGAN-I",
  "status": "ACTIVE",
  "dependencies": {
    "internal": {
      "depends_on": [
        {
          "repo": "recursive-engine--generative-entity",
          "org": "organvm-i-theoria",
          "organ": "ORGAN-I",
          "type": "hard"
        }
      ],
      "consumed_by": [
        {
          "repo": "core-engine",
          "org": "organvm-ii-poiesis",
          "organ": "ORGAN-II"
        }
      ]
    }
  }
}
```

### Success Criteria

- [ ] Circular dependency detected and blocked
- [ ] Downward dependency violations blocked
- [ ] Transitive depth violations detected
- [ ] Clear error message on failure
- [ ] Passes on valid PRs

---

## Workflow 2: monthly-organ-audit

**Purpose:** Full health check across all eight organs  
**Trigger:** Cron: `0 2 1 * *` (2 AM UTC on 1st of every month)  
**Latency:** ~15 minutes

### Implementation

**File:** `.github/workflows/monthly-organ-audit.yml` (in orchestration repo only)

```yaml
name: Monthly Organ Audit

on:
  schedule:
    - cron: '0 2 1 * * '  # 1st of month, 2 AM UTC
  workflow_dispatch:  # Manual trigger

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Run Organ Audit
        run: |
          python3 scripts/organ-audit.py \
            --registry registry.json \
            --governance governance-rules.json \
            --output audit-report.md
      
      - name: Generate Metrics
        run: |
          python3 scripts/calculate-metrics.py \
            --registry registry.json \
            --output metrics.json
      
      - name: Create GitHub Issue with Report
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('audit-report.md', 'utf8');
            const metrics = JSON.parse(fs.readFileSync('metrics.json', 'utf8'));
            
            const body = `
            # Monthly Organ Audit — ${new Date().toISOString().split('T')[0]}
            
            ${report}
            
            ## System Metrics
            - Total repos: ${metrics.total_repos}
            - Operational organs: ${metrics.operational_organs}/7
            - Completion: ${metrics.completion}%
            - Critical alerts: ${metrics.critical_alerts}
            - Warnings: ${metrics.warnings}
            `;
            
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `Monthly Organ Audit — ${new Date().toISOString().split('T')[0]}`,
              body: body,
              labels: ['audit', 'monthly']
            });
      
      - name: Push Metrics to Registry
        run: |
          git config user.name "Orchestration Bot"
          git config user.email "[email redacted]"
          
          # Append metrics to registry history
          python3 - <<'EOF'
          import json
          from datetime import datetime
          
          registry = json.load(open('registry.json'))
          metrics = json.load(open('metrics.json'))
          
          registry['audit_history'] = registry.get('audit_history', [])
          registry['audit_history'].append({
            'date': datetime.now().isoformat(),
            'metrics': metrics
          })
          
          json.dump(registry, open('registry.json', 'w'), indent=2)
          EOF
          
          git add registry.json
          git commit -m "Monthly audit metrics — $(date +%Y-%m-%d)"
          git push
```

### Audit Script (Python)

**File:** `scripts/organ-audit.py`

```python
#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timedelta

def audit_organs(registry_path, governance_path):
    """Run comprehensive system audit."""
    
    with open(registry_path) as f:
        registry = json.load(f)
    with open(governance_path) as f:
        governance = json.load(f)
    
    report = []
    alerts = {'critical': [], 'warning': []}
    
    # Audit each organ
    for organ_id in ['ORGAN-I', 'ORGAN-II', 'ORGAN-III', 'ORGAN-IV', 
                     'ORGAN-V', 'ORGAN-VI', 'ORGAN-VII']:
        organ = registry['organs'].get(organ_id, {})
        report.append(f"\n## {organ_id}: {organ.get('name', 'Unknown')}\n")
        
        # Check operational status
        status = organ.get('launch_status')
        completion = organ.get('completion', 0)
        report.append(f"**Status:** {status} ({completion}% complete)\n")
        
        # Run organ-specific checks
        if organ_id == 'ORGAN-I':
            report += check_theory_organ(organ, alerts)
        elif organ_id == 'ORGAN-II':
            report += check_art_organ(organ, alerts)
        elif organ_id == 'ORGAN-III':
            report += check_commerce_organ(organ, alerts)
        # ... etc
    
    # Validate dependency graph
    report += validate_dependency_graph(registry, alerts)
    
    # Check for alert conditions
    report.append(f"\n## Alerts\n")
    if alerts['critical']:
        report.append(f"🔴 **Critical ({len(alerts['critical'])}):**\n")
        for alert in alerts['critical']:
            report.append(f"- {alert}\n")
    
    if alerts['warning']:
        report.append(f"⚠️ **Warnings ({len(alerts['warning'])}):**\n")
        for alert in alerts['warning']:
            report.append(f"- {alert}\n")
    
    return ''.join(report), alerts

def validate_dependency_graph(registry, alerts):
    """Check for circular deps, broken links, etc."""
    report = ["\n## Dependency Validation\n"]
    
    # Build graph
    graph = {}
    for organ_id, organ in registry['organs'].items():
        for repo in organ.get('repositories', []):
            repo_name = repo['name']
            graph[repo_name] = {
                'deps': repo.get('relationships', {}).get('depends_on', []),
                'consumers': repo.get('relationships', {}).get('consumed_by', [])
            }
    
    # Check for cycles
    cycles = find_cycles(graph)
    if cycles:
        for cycle in cycles:
            alerts['critical'].append(f"Circular dependency: {' → '.join(cycle)}")
            report.append(f"🔴 Circular dep found: {cycle}\n")
    
    # Check for broken references
    for repo_name, deps in graph.items():
        for dep in deps['deps']:
            if dep not in graph:
                alerts['warning'].append(f"{repo_name} depends on missing {dep}")
    
    return report

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--registry', required=True)
    parser.add_argument('--governance', required=True)
    parser.add_argument('--output', required=True)
    
    args = parser.parse_args()
    
    report, alerts = audit_organs(args.registry, args.governance)
    
    with open(args.output, 'w') as f:
        f.write(report)
    
    # Exit code based on critical alerts
    sys.exit(1 if alerts['critical'] else 0)
```

### Success Criteria

- [ ] Audit completes within 15 minutes
- [ ] Report generated with all organ status
- [ ] Critical alerts trigger GitHub issues
- [ ] Metrics recorded in audit history
- [ ] No false positives

---

## Workflow 3: promote-repo

**Purpose:** Handle Theory→Art→Commerce promotions  
**Trigger:** Label on GitHub issue + comment with promotion request  
**Latency:** <5 minutes

### Usage

User opens issue in source repo (e.g., Theory repo):

```
Title: Promote to Art: Create implementation demo
Labels: promote-to-art
Comment: @orchestration promote
```

System automatically:
1. Validates promotion criteria
2. Creates new repo in destination organ
3. Links source → destination in registry
4. Notifies destination organ maintainers
5. Updates all cross-references

### Implementation

**File:** `.github/workflows/promote-repo.yml`

```yaml
name: Promote Repo

on:
  issue_comment:
    types: [created, edited]

jobs:
  promote:
    if: contains(github.event.issue.labels.*.name, 'promote-to-art') ||
        contains(github.event.issue.labels.*.name, 'promote-to-commerce')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          token: ${{ secrets.ORCHESTRATION_PAT }}
      
      - name: Parse Promotion Request
        id: parse
        run: |
          # Extract promotion type from label
          LABELS="${{ join(github.event.issue.labels.*.name) }}"
          
          if [[ $LABELS == *"promote-to-art"* ]]; then
            echo "promotion_type=promote-to-art" >> $GITHUB_OUTPUT
            echo "target_org=organvm-ii-poiesis" >> $GITHUB_OUTPUT
          elif [[ $LABELS == *"promote-to-commerce"* ]]; then
            echo "promotion_type=promote-to-commerce" >> $GITHUB_OUTPUT
            echo "target_org=organvm-iii-ergon" >> $GITHUB_OUTPUT
          fi
      
      - name: Validate Promotion Criteria
        run: |
          python3 - <<'EOF'
          import json
          import requests
          from datetime import datetime, timedelta
          
          promotion_type = "${{ steps.parse.outputs.promotion_type }}"
          source_repo = "${{ github.repository }}"
          
          # Fetch registry
          registry_url = "https://raw.githubusercontent.com/organvm-iv-taxis/orchestration-start-here/main/registry.json"
          registry = requests.get(registry_url).json()
          
          # Load promotion criteria from governance
          governance_url = "https://raw.githubusercontent.com/organvm-iv-taxis/orchestration-start-here/main/governance-rules.json"
          governance = requests.get(governance_url).json()
          
          criteria = governance['rules'].get(promotion_type, {}).get('conditions', [])
          
          # Validate source repo against criteria
          passed = []
          failed = []
          
          # Check each criterion
          for criterion in criteria:
              if check_criterion(source_repo, criterion, registry):
                  passed.append(criterion)
              else:
                  failed.append(criterion)
          
          # Report
          if failed:
              print(f"❌ Promotion blocked. Failed criteria:")
              for f in failed:
                  print(f"  - {f}")
              exit(1)
          else:
              print(f"✅ All promotion criteria met for {promotion_type}")
              exit(0)
          EOF
      
      - name: Create Destination Repo
        env:
          GH_TOKEN: ${{ secrets.ORCHESTRATION_PAT }}
        run: |
          TARGET_ORG="${{ steps.parse.outputs.target_org }}"
          SOURCE_REPO="${{ github.event.repository.name }}"
          
          # Derive new repo name based on promotion type
          if [[ "${{ steps.parse.outputs.promotion_type }}" == "promote-to-art" ]]; then
            NEW_REPO="art-from--${SOURCE_REPO}"
          else
            NEW_REPO="${SOURCE_REPO}"
          fi
          
          # Create repo via gh CLI
          gh repo create ${TARGET_ORG}/${NEW_REPO} \
            --public \
            --source=. \
            --remote=destination \
            --push
          
          echo "new_repo=${NEW_REPO}" >> $GITHUB_ENV
      
      - name: Link in Registry
        run: |
          python3 - <<'EOF'
          import json
          
          registry = json.load(open('registry.json'))
          
          source_repo = "${{ github.repository }}"
          dest_repo = "${{ env.new_repo }}"
          promotion_type = "${{ steps.parse.outputs.promotion_type }}"
          
          # Find source in registry and add promotion link
          for organ_id, organ in registry['organs'].items():
              for repo in organ.get('repositories', []):
                  if repo['name'] == source_repo.split('/')[-1]:
                      repo['promoted_to'] = {
                        'repo': dest_repo,
                        'org': "${{ steps.parse.outputs.target_org }}",
                        'type': promotion_type,
                        'date': "${{ github.event.issue.created_at }}"
                      }
          
          json.dump(registry, open('registry.json', 'w'), indent=2)
          EOF
      
      - name: Open Issue in Destination
        env:
          GH_TOKEN: ${{ secrets.ORCHESTRATION_PAT }}
        run: |
          TARGET_ORG="${{ steps.parse.outputs.target_org }}"
          NEW_REPO="${{ env.new_repo }}"
          SOURCE_REPO="${{ github.repository }}"
          
          gh issue create \
            --repo ${TARGET_ORG}/${NEW_REPO} \
            --title "Promoted from ${SOURCE_REPO}" \
            --body "This repo was promoted from [${SOURCE_REPO}](https://github.com/${SOURCE_REPO}). Link back to source and update dependencies in registry." \
            --label "promoted"
      
      - name: Comment on Source Issue
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `✅ Promotion successful!\n\n- **Target repo:** ${process.env.NEW_REPO}\n- **Target org:** ${process.env.TARGET_ORG}\n- **Status:** Linked in central registry\n\nNext: Set up dependency links and notify destination organ maintainers.`
            });
```

### Success Criteria

- [ ] Promotion validates against governance criteria
- [ ] New repo created in destination org
- [ ] Registry updated with promotion link
- [ ] Cross-repo issue opened in destination
- [ ] Source repo notified of success

---

## Workflow 4: publish-process

**Purpose:** Automate ORGAN-V essay creation from ORGAN-III product documentation  
**Trigger:** Issue label in Commerce repo  
**Latency:** On-demand

### Usage

1. Commerce product maintainer opens issue:

```
Title: Publish process: How we built Aetheria RPG
Labels: publish-process
Comment: @orchestration create essay
```

2. System:
   - Creates draft essay in ORGAN-V repo
   - Pulls methodology from source repo docs
   - Generates outline from git history
   - Opens PR for human review
   - Links back to source product

### Implementation Sketch

```yaml
name: Publish Process

on:
  issue_comment:
    types: [created]

jobs:
  publish:
    if: contains(github.event.issue.labels.*.name, 'publish-process')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Extract Content
        run: |
          # Pull from source repo:
          # - README.md (overview)
          # - docs/** (methodology)
          # - git log (decision history)
          # - CHANGELOG.md (milestones)
          
          python3 scripts/extract-process.py \
            --source-repo "${{ github.repository }}" \
            --output process-draft.md
      
      - name: Generate Essay Outline
        run: |
          python3 scripts/generate-outline.py \
            --content process-draft.md \
            --template templates/essay-structure.md \
            --output essay-outline.md
      
      - name: Create Draft in ORGAN-V
        env:
          GH_TOKEN: ${{ secrets.ORCHESTRATION_PAT }}
        run: |
          # Fork/clone ORGAN-V repo
          gh repo clone organvm-v-logos/public-process public-process
          cd public-process
          
          # Add essay draft
          cp ../essay-outline.md "essays/$(date +%Y-%m-%d)--from-${{ github.event.repository.name }}.md"
          
          # Create PR
          git checkout -b essay/from-${{ github.event.repository.name }}
          git add essays/
          git commit -m "Draft essay: Process from ${{ github.repository }}"
          git push origin essay/from-${{ github.event.repository.name }}
          
          gh pr create \
            --title "Essay: Process from ${{ github.repository }}" \
            --body "Auto-generated from ${{ github.repository }}" \
            --label "auto-draft"
      
      - name: Comment on Source Issue
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `📝 Essay draft created in ORGAN-V!\n\nReview and refine at: [organvm-v-logos/public-process](https://github.com/organvm-v-logos/public-process)`
            });
```

---

## Workflow 5: distribute-content

**Purpose:** POSSE automation for ORGAN-V essays  
**Trigger:** Label in public-process repo  
**Latency:** On-demand

### Usage

1. After essay published in ORGAN-V, add label: `ready-to-distribute`

2. System automatically:
   - Posts to Mastodon, LinkedIn, Twitter (via scheduled posts)
   - Adds to weekly newsletter
   - Pings community channels (Discord, etc.)
   - Tracks engagement metrics

### Implementation Sketch

```yaml
name: Distribute Content

on:
  issues:
    types: [labeled]

jobs:
  distribute:
    if: contains(github.event.issue.labels.*.name, 'ready-to-distribute')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Extract Essay Metadata
        id: metadata
        run: |
          # Parse YAML frontmatter from essay
          python3 - <<'EOF'
          import yaml
          import re
          
          with open("${{ github.event.issue.body }}") as f:
              match = re.match(r'^---\n(.*?)\n---', f.read(), re.DOTALL)
              if match:
                  meta = yaml.safe_load(match.group(1))
                  print(f"title={meta['title']}")
                  print(f"excerpt={meta.get('excerpt', 'New essay from 4444j99')}")
          EOF
      
      - name: Post to Mastodon
        env:
          MASTODON_TOKEN: ${{ secrets.MASTODON_TOKEN }}
        run: |
          # Schedule toot
          curl https://mastodon.social/api/v1/statuses \
            -H "Authorization: Bearer ${MASTODON_TOKEN}" \
            -F "status=${{ steps.metadata.outputs.excerpt }} — https://github.com/organvm-v-logos/public-process/issues/${{ github.event.issue.number }}"
      
      - name: Add to Newsletter Queue
        run: |
          # Append to weekly newsletter draft
          echo "- [${{ steps.metadata.outputs.title }}](...link...)" >> newsletter/queue.md
      
      - name: Notify Community
        env:
          DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
        run: |
          # Post to Discord community channel
          curl ${DISCORD_WEBHOOK} \
            -X POST \
            -d '{"content":"New essay: ${{ steps.metadata.outputs.title }}"}'
      
      - name: Track in Analytics
        run: |
          # Log distribution event for metrics
          python3 - <<'EOF'
          import json
          from datetime import datetime
          
          analytics = json.load(open('analytics.json', 'a'))
          analytics.append({
            'date': datetime.now().isoformat(),
            'essay': "${{ github.event.issue.number }}",
            'distributed': True,
            'channels': ['mastodon', 'newsletter', 'discord']
          })
          json.dump(analytics, open('analytics.json', 'w'), indent=2)
          EOF
```

---

## Deployment Checklist

### Pre-Deployment

- [ ] Create `orchestration-start-here` repo
- [ ] Commit registry.json, governance-rules.json
- [ ] Create `.github/actions/` with reusable actions
- [ ] Create `.github/workflows/` with all 5 workflows
- [ ] Test validate-dependencies on single repo first

### Deployment Phase

- [ ] Copy validate-dependencies workflow template to all 46 repos
- [ ] Create `.meta/dependencies.json` in all 46 repos
- [ ] Tag all repos with organ topics in GitHub
- [ ] Enable branch protection rules requiring status checks

### Post-Deployment

- [ ] Run manual monthly-organ-audit to establish baseline
- [ ] Test promote-repo with sandbox repos
- [ ] Test publish-process with single essay
- [ ] Monitor logs for first 24 hours

---

## Maintenance & Monitoring

### GitHub Actions Dashboard

Monitor at: `https://github.com/organvm-iv-taxis/orchestration-start-here/actions`

**Key metrics to track:**
- Validate-dependencies: failure rate (target: <2%)
- Monthly-organ-audit: completion time (target: <20 min)
- Promote-repo: success rate (target: 100% of promoted repos)

### Alert Thresholds

- If any workflow fails consistently: create GitHub issue
- If monthly-audit detects critical alerts: notify via email
- If dependency validation blocks >3 PRs/week: review criteria

---

## Implementation Order

**Week 2:**
1. Create orchestration repo and commit workflows
2. Implement validate-dependencies (simplest, highest immediate value)
3. Deploy to 5-10 repos as pilot
4. Refine based on feedback

**Week 3:**
1. Deploy validate-dependencies to all 46 repos
2. Implement monthly-organ-audit
3. Implement promote-repo (requires org-level PAT token)
4. Test end-to-end

**Week 4:**
1. Implement publish-process and distribute-content
2. Full system testing
3. Documentation and runbooks

---

## Success Metrics

- [ ] 0 circular dependencies detected in any audit
- [ ] All 46 repos mapped to organs and passing validation
- [ ] Promotion pipeline handles Theory→Art→Commerce flow
- [ ] Essays published monthly from commerce products
- [ ] Monthly audit completes successfully
- [ ] <5% false positive rate on validation

---

**Status:** Specification complete, ready to implement  
**Owner:** You (@4444j99)  
**Questions?** See orchestration-system-v2.md for governance details
