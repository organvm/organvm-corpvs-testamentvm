# Universal Orchestrator Architecture
## omni-dromenon-machina as Global Repo Manager

**Date**: 2025-12-26
**Revision**: Based on clarification that omni-drom orchestrates ALL repos

---

## Core Insight

**omni-dromenon-machina** is not project-specific—it's a **universal autonomous development orchestrator** that manages multiple repositories across your entire workspace.

This is architecturally superior because:
1. ✅ **Single orchestrator** for all projects (DRY principle)
2. ✅ **Reusable agent system** across repos
3. ✅ **Centralized quality enforcement**
4. ✅ **Shared learning** across projects
5. ✅ **Consistent development patterns**

---

## Architectural Model

```
┌─────────────────────────────────────────────────────────────┐
│  omni-dromenon-machina (Universal Orchestrator)             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Multi-Agent System                                   │  │
│  │  • Architect  • Implementer  • Reviewer              │  │
│  │  • Tester     • Maintainer                           │  │
│  └───────────────────────────────────────────────────────┘  │
│                            ↓                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Discovery & Configuration Engine                     │  │
│  │  • Scans workspace for seed.yaml files               │  │
│  │  • Reads project constraints                         │  │
│  │  • Routes work to appropriate agents                 │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┴───────────────────┐
        ↓                   ↓                   ↓
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ Project 1     │  │ Project 2     │  │ Project N     │
│               │  │               │  │               │
│ life-my--     │  │ [your-next-   │  │ [future-      │
│ midst--in     │  │  project]     │  │  project]     │
│               │  │               │  │               │
│ seed.yaml     │  │ seed.yaml     │  │ seed.yaml     │
└───────────────┘  └───────────────┘  └───────────────┘
```

Each project has its own `seed.yaml` (genome).
The orchestrator discovers and manages them all.

---

## Recommended Structure: Flat with Discovery

### Option 1: Flat Structure (Simplest)

```
~/Workspace/
├── omni-dromenon-machina/           # The universal orchestrator
│   ├── config/
│   │   └── orchestrator.yaml        # Global config
│   ├── agents/                      # Shared agent system
│   ├── core/                        # Orchestration logic
│   └── README.md
│
├── life-my--midst--in/              # Managed project 1
│   ├── seed.yaml                    # Project genome
│   └── ...
│
├── [your-other-project]/            # Managed project 2
│   ├── seed.yaml
│   └── ...
│
└── [another-project]/               # Managed project 3
    ├── seed.yaml
    └── ...
```

**orchestrator.yaml** in omni-drom:
```yaml
discovery:
  mode: "auto"
  workspace_root: "~/Workspace"
  exclude_patterns:
    - "omni-dromenon-machina"
    - ".*"              # Hidden folders
    - "node_modules"

managed_projects:
  auto_discover: true
  genome_file: "seed.yaml"

  # Or explicit registration:
  # explicit:
  #   - path: "../life-my--midst--in"
  #     name: "in-midst-my-life"
```

**Pros**:
- ✅ Simplest structure
- ✅ All projects at same level
- ✅ Easy to navigate
- ✅ Auto-discovery of any project with seed.yaml

**Cons**:
- Projects mixed with orchestrator at root level
- Could get cluttered with many projects

---

### Option 2: Organized with Projects Folder

```
~/Workspace/
├── omni-dromenon-machina/           # The orchestrator
│   └── config/orchestrator.yaml
│
└── projects/                        # All managed projects
    ├── life-my--midst--in/
    │   └── seed.yaml
    ├── [project-2]/
    │   └── seed.yaml
    └── [project-3]/
        └── seed.yaml
```

**Pros**:
- ✅ Clean separation
- ✅ Clear "these are managed projects"
- ✅ Scales to many projects

**Cons**:
- Extra nesting
- Requires path adjustment

---

### Option 3: Hybrid with Categories

```
~/Workspace/
├── omni-dromenon-machina/           # The orchestrator
│
├── identity-systems/                # Category: Identity projects
│   └── life-my--midst--in/
│
├── web-apps/                        # Category: Web applications
│   └── [some-web-project]/
│
└── tools/                           # Category: Tools
    └── [some-tool]/
```

**Pros**:
- ✅ Organized by domain
- ✅ Logical grouping
- ✅ Easy to find related projects

**Cons**:
- More structure to maintain
- Orchestrator needs to scan multiple dirs

---

## My Recommendation: **Option 1 (Flat) + Smart Discovery**

Keep it simple:

```
~/Workspace/
├── omni-dromenon-machina/           # THE orchestrator
├── life-my--midst--in/              # Project with seed.yaml
├── [any-other-project]/             # Any project with seed.yaml
└── [random-stuff]/                  # No seed.yaml = ignored
```

**omni-drom discovers and manages any repo with `seed.yaml`**

---

## How omni-drom Would Work

### Discovery Process

```typescript
// In omni-dromenon-machina/core/discovery.ts

async function discoverManagedProjects(workspaceRoot: string): Promise<Project[]> {
  const projects: Project[] = [];

  // Scan workspace
  for (const dir of await fs.readdir(workspaceRoot)) {
    const projectPath = path.join(workspaceRoot, dir);
    const seedPath = path.join(projectPath, 'seed.yaml');

    // Skip orchestrator itself
    if (dir === 'omni-dromenon-machina') continue;

    // Check for seed.yaml
    if (await fs.exists(seedPath)) {
      const seed = await parseYaml(seedPath);
      projects.push({
        name: seed.project.name,
        path: projectPath,
        genome: seed,
      });
    }
  }

  return projects;
}
```

### Orchestration Flow

1. **Scan workspace** → Find all `seed.yaml` files
2. **Parse genomes** → Understand constraints for each project
3. **Route tasks** → Assign agent work based on project rules
4. **Execute** → Run agents within project-specific boundaries
5. **Report** → Aggregate status across all projects

---

## Configuration Architecture

### Global Config: omni-dromenon-machina/config/orchestrator.yaml

```yaml
version: 1
orchestrator:
  name: "omni-dromenon-machina"
  description: "Universal autonomous development orchestrator"

discovery:
  workspace_root: "~/Workspace"
  auto_discover: true
  genome_filename: "seed.yaml"
  exclude_dirs:
    - "omni-dromenon-machina"
    - "node_modules"
    - ".git"

agents:
  architect:
    model: "claude-sonnet-4.5"
    max_concurrent: 1
  implementer:
    model: "claude-sonnet-4.5"
    max_concurrent: 3
  reviewer:
    model: "claude-sonnet-4.5"
    max_concurrent: 2
  tester:
    model: "claude-haiku-4"
    max_concurrent: 5
  maintainer:
    model: "claude-opus-4.5"
    max_concurrent: 1

github:
  enabled: true
  webhook_secret: "${GITHUB_WEBHOOK_SECRET}"
  create_issues: true
  create_prs: true
  auto_merge_criteria:
    - "all_ci_pass"
    - "coverage_maintained"
    - "within_project_constraints"

quality_enforcement:
  global_minimums:
    test_coverage: 0.70           # 70% global minimum
    max_complexity: 15
    max_file_lines: 500

  # Projects can be stricter in their seed.yaml
  allow_project_override: "stricter_only"

monitoring:
  log_level: "info"
  metrics_export: "prometheus"
  dashboard_port: 3000
```

### Per-Project Config: life-my--midst--in/seed.yaml

```yaml
# Each project maintains its own genome
version: 1
project:
  name: "in--midst--my-life"

# ... (existing seed.yaml content)

# Orchestration hooks (optional)
orchestration:
  enabled: true
  priority: "normal"          # normal | high | low
  agent_preferences:
    architect: "claude-opus-4.5"  # Can request specific models

  notifications:
    slack_channel: "#cv-project"
    email: "[email redacted]"
```

---

## Benefits of This Architecture

### 1. Universal Agent System
- Same agents work across all projects
- Learning/improvements benefit everything
- Consistent quality standards

### 2. Project Autonomy
- Each project defines its own constraints (seed.yaml)
- Orchestrator respects project-specific rules
- Can have different tech stacks, patterns, etc.

### 3. Centralized Intelligence
- One place to improve agent behavior
- Cross-project insights (e.g., "this pattern works well")
- Shared knowledge base

### 4. Easy Scaling
- Add new project? Just create seed.yaml
- Orchestrator auto-discovers it
- No configuration needed in orchestrator

### 5. Clear Separation
- Orchestrator = mechanism (how to develop)
- Projects = policy (what constraints to follow)

---

## Implementation Approach

### Phase 1: Enhance omni-drom for Discovery

```bash
cd omni-dromenon-machina

# Add discovery module
mkdir -p core/discovery
touch core/discovery/scanner.ts
touch core/discovery/genome-parser.ts

# Add global config
mkdir -p config
touch config/orchestrator.yaml

# Update to scan workspace
# Implement auto-discovery logic
```

### Phase 2: Update life-my--midst--in

```bash
cd life-my--midst--in

# seed.yaml already exists ✓
# Add orchestration hooks to seed.yaml
# Configure project-specific preferences
```

### Phase 3: Add More Projects

```bash
cd ~/Workspace

# Create any new project
mkdir my-new-project
cd my-new-project

# Add seed.yaml
cp ../life-my--midst--in/seed.yaml ./seed.yaml
# Customize for this project

# omni-drom auto-discovers it!
```

---

## Monitoring Dashboard Concept

```
┌─────────────────────────────────────────────────────────────┐
│  omni-dromenon-machina Dashboard                            │
├─────────────────────────────────────────────────────────────┤
│  Managed Projects: 3                                        │
│  Active Tasks: 7                                            │
│  Agents Running: 5                                          │
├─────────────────────────────────────────────────────────────┤
│  Project                    Status      Coverage   Tasks    │
│  ─────────────────────────────────────────────────────────  │
│  life-my--midst--in         🟢 Active   82%        3        │
│  other-project              🟡 Review   76%        2        │
│  new-project                🔵 Setup    45%        2        │
└─────────────────────────────────────────────────────────────┘
```

---

## Cross-Project Features

With multiple projects, omni-drom can:

1. **Share Patterns**
   - "This testing pattern works well in project A, suggest for B"

2. **Detect Duplication**
   - "Projects X and Y have similar utilities, extract to shared package?"

3. **Coordinate Updates**
   - "New security patch needed in all TypeScript projects"

4. **Resource Management**
   - "Project A is critical, allocate more agent time"

5. **Learning Transfer**
   - Agent improvements benefit all projects immediately

---

## Recommendation: Flat Structure + Smart Discovery

**Keep it simple**:

```
~/Workspace/
├── omni-dromenon-machina/     # Universal orchestrator
├── life-my--midst--in/        # Project 1 (has seed.yaml)
├── [project-2]/               # Project 2 (has seed.yaml)
└── [random-stuff]/            # No seed.yaml = ignored
```

**omni-drom config**:
- Scans `~/Workspace`
- Finds any directory with `seed.yaml`
- Manages those projects automatically
- Ignores everything else

**To add a new project**:
1. Create directory in workspace
2. Add `seed.yaml`
3. Done! omni-drom finds it

---

## Next Steps

1. ✅ Keep flat structure in `~/Workspace`
2. Enhance omni-drom with discovery system
3. Ensure life-my--midst--in seed.yaml is complete
4. Test orchestration on one project
5. Add more projects as needed

**No folder reorganization needed!** The current structure is perfect.

---

**Thoughts on this architecture?** Does this match your vision for omni-drom as a universal orchestrator?
