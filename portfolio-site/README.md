# ORGANVM Portfolio Site

The unified front door for the eight-organ creative-institutional system.

## Architecture

- **Framework**: Astro (static site generator)
- **Data source**: `repo-registry.json` via `praxis-portfolio-generate.py`
- **Design tokens**: Derived from `taste.yaml` aesthetic pillars
- **Deploy target**: Vercel or GitHub Pages

## Pages

| Page | Path | Data Source |
|------|------|-------------|
| Landing | `/` | `src/data/landing.json` |
| Projects | `/projects/` | `src/data/projects.json` |
| Essays | `/essays/` | `src/data/essays.json` |
| Architecture | `/architecture/` | `src/data/graph.json` |
| Dashboard | `/dashboard/` | `src/data/system-metrics.json` |
| About | `/about/` | `src/data/about.json` |

## Development

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Production build using committed data snapshot
npm run build

# Regenerate committed data snapshot intentionally
npm run generate-data

# Regenerate data, then build
npm run build:fresh
```

## Data Policy

`src/data/*.json` is a committed snapshot, not an ephemeral build artifact.

- `npm run build` is non-mutating and verifies snapshot integrity before Astro builds.
- `npm run generate-data` is the explicit refresh path.
- Refreshes should be reviewed and committed intentionally.

## Data Pipeline

```
repo-registry.json
       |
       v
praxis-portfolio-generate.py  -->  src/data/*.json (committed snapshot)
       |
       v
    Astro build  -->  dist/  -->  Vercel/GitHub Pages
```

## Design

The visual language follows the `taste.yaml` aesthetic pillars:
- **Density**: Information-rich layouts, no wasted space
- **Structure**: Clear hierarchy, organ-based color coding
- **Reference**: Links to source repos, essays, registry
- **Precision**: Monospace metrics, exact counts
- **Warmth**: Serif body text, warm color palette
