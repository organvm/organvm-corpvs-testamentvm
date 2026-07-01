#!/usr/bin/env python3
"""ALCHEMIZER — Identity Transmutation System for Application Materials.

Reads covenant-ark + registry + system-metrics and generates identity-shifted
application materials per opportunity. Deterministic, template-based output.

Usage:
    python3 scripts/alchemizer.py                          # Generate ALL profiles + scripts
    python3 scripts/alchemizer.py --target creative-capital # Single target
    python3 scripts/alchemizer.py --position systems_artist # All targets for position
    python3 scripts/alchemizer.py --profiles-only           # JSON profiles only
    python3 scripts/alchemizer.py --audit                   # Coverage audit
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
COVENANT_ARK_PATH = ROOT / "docs" / "applications" / "00-covenant-ark.md"
REGISTRY_PATH = ROOT / "repo-registry.json"
METRICS_PATH = ROOT / "system-metrics.json"
PROFILES_DIR = ROOT / "docs" / "applications" / "profiles"
SCRIPTS_DIR = ROOT / "docs" / "applications" / "submission-scripts"

# ═══════════════════════════════════════════════════════════════════════════════
# IDENTITY MAP — target_id → (primary_position, secondary_position)
# ═══════════════════════════════════════════════════════════════════════════════

IDENTITY_MAP = {
    # Art grants & residencies → Systems Artist
    "creative-capital": ("systems_artist", "educator"),
    "artadia-nyc": ("systems_artist", None),
    "headlands": ("systems_artist", "community"),
    "eyebeam": ("systems_artist", "community"),
    "fire-island": ("community", "systems_artist"),
    "zkm-rauschenberg": ("systems_artist", "technologist"),
    "watermill": ("systems_artist", "educator"),
    "lacma-art-tech": ("systems_artist", "technologist"),
    "prix-ars": ("systems_artist", "technologist"),
    "starts-prize": ("systems_artist", "technologist"),
    "doris-duke": ("systems_artist", "community"),
    # Writing grants → Systems Artist + Educator
    "whiting-nonfiction": ("systems_artist", "educator"),
    "warhol-arts-writers": ("systems_artist", "educator"),
    "pen-america": ("systems_artist", None),
    # Education → Educator
    "spencer-foundation": ("educator", "systems_artist"),
    "processing-foundation": ("educator", "technologist"),
    "bread-loaf": ("educator", "systems_artist"),
    # Tech → Creative Technologist
    "google-cl5": ("technologist", "systems_artist"),
    "google-fellowship": ("technologist", "systems_artist"),
    "google-ami": ("technologist", "systems_artist"),
    "nlnet-commons": ("technologist", "community"),
    "recurse-center": ("technologist", "systems_artist"),
    # Community → Community Practitioner
    "wff-housing": ("community", "systems_artist"),
    "queer-art": ("community", "systems_artist"),
    "lambda-literary": ("community", "educator"),
    "stimpunks": ("community", "systems_artist"),
    # Employment → Creative Technologist
    "together-ai": ("technologist", "educator"),
    "huggingface": ("technologist", "educator"),
    "anthropic-fde": ("technologist", None),
    "openai-evals": ("technologist", None),
    # Emergency → minimal framing
    "fca-emergency": ("systems_artist", None),
    "rauschenberg-emergency": ("systems_artist", None),
    "awesome-foundation": ("systems_artist", None),
    # Infrastructure
    "github-sponsors": ("systems_artist", "technologist"),
    "fractured-atlas": ("systems_artist", None),
    # Writing income
    "noema": ("systems_artist", "technologist"),
    "logic-magazine": ("technologist", "systems_artist"),
    "gay-lesbian-review": ("community", "systems_artist"),
    "mit-tech-review": ("technologist", "systems_artist"),
    # Career-building
    "new-inc": ("technologist", "systems_artist"),
    "pioneer-works": ("systems_artist", "community"),
    "tulsa-fellowship": ("systems_artist", "community"),
    # Consulting
    "ai-consulting": ("technologist", "educator"),
    "workshop-facilitation": ("educator", "technologist"),
    "documentation-consulting": ("technologist", "educator"),
}

# ═══════════════════════════════════════════════════════════════════════════════
# POSITION TEMPLATES — per-position content generation parameters
# ═══════════════════════════════════════════════════════════════════════════════

POSITION_TEMPLATES = {
    "systems_artist": {
        "label": "Systems Artist",
        "lead_sentence": "I build creative systems — the governance IS the artwork.",
        "statement_emphasis": "process-as-product, governance as creative medium",
        "evidence_order": ["essays", "registry", "portfolio", "generative_art", "recursive_engine"],
        "differentiators_order": [4, 2, 1, 6, 3, 5],
        "work_samples_order": [3, 2, 1, 7, 4, 6, 5, 8],
        "bio_emphasis": ["MFA Creative Writing", "42 published essays", "5+ years sustained practice", "100 repositories"],
        "narrative_frame": (
            "The eight-organ system is a living creative work — 100 repositories across "
            "8 organizations coordinated through automated governance, a formal promotion "
            "state machine, and {essays} published essays documenting the process in real time. "
            "The governance structures aren't bureaucracy — they're generative constraints, "
            "the way a composer's harmonic rules shape what melodies can emerge."
        ),
    },
    "educator": {
        "label": "Educator",
        "lead_sentence": "Teaching complex systems to diverse audiences IS my creative practice.",
        "statement_emphasis": "11 years teaching, curriculum design, knowledge transfer",
        "evidence_order": ["teaching", "essays", "documentation", "portfolio", "community"],
        "differentiators_order": [5, 2, 6, 1, 4, 3],
        "work_samples_order": [3, 1, 2, 6, 7, 4, 5, 8],
        "bio_emphasis": ["11 years teaching", "2,000+ students", "100+ courses", "MFA Creative Writing"],
        "narrative_frame": (
            "Eleven years teaching at 8+ institutions — 2,000+ students across 100+ courses — "
            "taught me that the most powerful pedagogy makes complex systems visible and navigable. "
            "The eight-organ system ({repos} repositories, {essays} essays, {words} of documentation) "
            "is simultaneously a creative work AND a teaching instrument: every architectural decision "
            "is documented, every mistake published, every sprint specified."
        ),
    },
    "technologist": {
        "label": "Creative Technologist",
        "lead_sentence": "Production-grade AI orchestration with creative-artistic applications.",
        "statement_emphasis": "multi-agent orchestration, 2,349+ tests, autonomous governance",
        "evidence_order": ["agentic_titan", "recursive_engine", "ci_cd", "registry", "orchestration"],
        "differentiators_order": [3, 1, 4, 5, 6, 2],
        "work_samples_order": [5, 4, 8, 2, 6, 1, 3, 7],
        "bio_emphasis": ["2,349+ automated tests", "82+ CI/CD workflows", "100 repositories", "multi-agent orchestration"],
        "narrative_frame": (
            "The eight-organ system coordinates {repos} repositories across 8 GitHub organizations "
            "through automated governance: {ci} CI/CD workflows, {edges} dependency edges with zero "
            "violations, a formal promotion state machine, and 2,349+ automated tests across the "
            "flagship frameworks (agentic-titan: 1,095 tests, recursive-engine: 1,254 tests). "
            "Built using the AI-conductor methodology — AI generates volume, human directs architecture."
        ),
    },
    "community": {
        "label": "Community Practitioner",
        "lead_sentence": "Building creative infrastructure from lived experience of precarity.",
        "statement_emphasis": "LGBTQ+, housing-precarious, recovery, community infrastructure",
        "evidence_order": ["community", "essays", "teaching", "portfolio", "public_process"],
        "differentiators_order": [6, 5, 2, 1, 4, 3],
        "work_samples_order": [3, 1, 6, 2, 7, 4, 5, 8],
        "bio_emphasis": ["LGBTQ+", "NYC-based", "housing-precarious", "MFA Creative Writing", "11 years teaching"],
        "narrative_frame": (
            "The eight-organ system grows from lived experience of precarity — housing instability, "
            "recovery, the specific vulnerability of building a creative practice without institutional "
            "support. ORGAN-VI (Community) and ORGAN-V (Public Process) exist because creative "
            "infrastructure should be visible, shared, and governed by the people it serves. "
            "{essays} published essays document this practice transparently, including the failures."
        ),
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# TARGET DATA — all 41 application targets
# ═══════════════════════════════════════════════════════════════════════════════

TARGETS = [
    # Track 1: Art-Tech Grants & Residencies
    {"id": "artadia-nyc", "name": "Artadia NYC Awards", "category": "Grant",
     "amount": "$15,000", "deadline": "March 1, 2026", "fit": 8,
     "url": "https://artadia.org/award_schedule/new-york/",
     "format": "Artist statement + bio + work samples + resume (Submittable)",
     "cliff": {"rating": "safe", "note": "SNAP-safe (lump sum excluded). Below Medicaid with Schedule C deductions."},
     "has_materials": True},
    {"id": "creative-capital", "name": "Creative Capital 2027 Open Call", "category": "Grant",
     "amount": "Up to $50,000", "deadline": "April 2, 2026, 3pm ET", "fit": 9,
     "url": "https://creative-capital.org/creative-capital-award/award-application/",
     "format": "6 short questions + 500-word project description + work samples + bio + resume",
     "cliff": {"rating": "caution", "note": "$50K exceeds Medicaid threshold -> Essential Plan ($0 premium). Call NYLAG [phone redacted])."},
     "has_materials": False},
    {"id": "google-fellowship", "name": "Google Creative Fellowship", "category": "Fellowship",
     "amount": "Stipend (~$50K+)", "deadline": "March 18, 2026, 5pm PST", "fit": 7,
     "url": "https://creativefellowship.google/",
     "format": "Portfolio + artist statement + project description",
     "cliff": {"rating": "caution", "note": "Paid contractor role. Full employment income exceeds all thresholds."},
     "has_materials": True},
    {"id": "google-cl5", "name": "Google Creative Lab Five", "category": "Residency",
     "amount": "Salaried (1 year)", "deadline": "Open (no stated close)", "fit": 8,
     "url": "https://www.creativelab5.com/",
     "format": "3 short-answer questions + portfolio link",
     "cliff": {"rating": "caution", "note": "Full-time employment exits benefits safety net entirely."},
     "has_materials": True},
    {"id": "fire-island", "name": "Fire Island Artist Residency", "category": "Residency",
     "amount": "Stipend + housing", "deadline": "April 1, 2026, 11:59pm", "fit": 7,
     "url": "https://www.fireislandresidency.org/",
     "format": "Artist statement + project proposal + work samples + bio (SlideRoom)",
     "cliff": {"rating": "safe", "note": "SNAP-safe. Stipend likely below thresholds."},
     "has_materials": False},
    {"id": "eyebeam", "name": "Eyebeam Speculating on Plurality", "category": "Residency",
     "amount": "$4,000 + studio", "deadline": "Spring 2026 (TBA)", "fit": 7,
     "url": "https://eyebeam.org/program/speculating-plurality/",
     "format": "Application form + project proposal + work samples",
     "cliff": {"rating": "safe", "note": "SNAP-safe. $4K below all thresholds."},
     "has_materials": False},
    {"id": "processing-foundation", "name": "Processing Foundation Fellowship", "category": "Fellowship",
     "amount": "$10,000 + mentorship", "deadline": "~April-May 2026", "fit": 6,
     "url": "https://processingfoundation.org/fellowships",
     "format": "Project proposal + bio + work samples",
     "cliff": {"rating": "safe", "note": "SNAP-safe (lump sum). $10K on $12K base stays within Medicaid with deductions."},
     "has_materials": False},
    {"id": "prix-ars", "name": "Prix Ars Electronica 2026", "category": "Prize",
     "amount": "EUR 10,000", "deadline": "March 4, 2026", "fit": 8,
     "url": "https://ars.electronica.art/prix/en/opencall/",
     "format": "Project description + documentation + work samples",
     "cliff": {"rating": "safe", "note": "International lump sum = SNAP-safe."},
     "has_materials": True},
    {"id": "starts-prize", "name": "S+T+ARTS Prize 2026", "category": "Prize",
     "amount": "EUR 20,000", "deadline": "March 4, 2026", "fit": 8,
     "url": "https://starts-prize.aec.at/en/open-call/",
     "format": "Project description + documentation + work samples",
     "cliff": {"rating": "safe", "note": "International lump sum = SNAP-safe."},
     "has_materials": True},
    {"id": "wff-housing", "name": "WFF Housing Stability Grant", "category": "Grant",
     "amount": "$30,000 over 3 years ($12K/$10K/$8K)", "deadline": "April 14, 2026, 5pm ET", "fit": 9,
     "url": "https://www.nyfa.org/awards-grants/wff-housing-stability-grant-for-artists/",
     "format": "Artist statement + project narrative + budget + financial documentation + work samples",
     "cliff": {"rating": "caution", "note": "$12K yr 1 + $12K adjunct = $24K -> exceeds Medicaid ($21,597) and Fair Fares ($22,692). Call NYLAG."},
     "has_materials": False},
    {"id": "nlnet-commons", "name": "NLnet NGI Zero Commons Fund", "category": "Grant",
     "amount": "EUR 5,000-50,000+", "deadline": "April 1, 2026", "fit": 7,
     "url": "https://nlnet.nl/commonsfund/",
     "format": "Online application: project description + technical plan + budget",
     "cliff": {"rating": "safe", "note": "International grant = SNAP-safe."},
     "has_materials": False},
    {"id": "whiting-nonfiction", "name": "Whiting Creative Nonfiction Grant", "category": "Grant",
     "amount": "$40,000", "deadline": "~April 2026", "fit": 8,
     "url": "https://www.whiting.org/writers/creative-nonfiction-grant",
     "format": "Writing sample (25 pages) + project description + bio + references",
     "cliff": {"rating": "caution", "note": "$40K -> Essential Plan. Call NYLAG."},
     "has_materials": False},
    {"id": "warhol-arts-writers", "name": "Warhol Foundation Arts Writers Grant", "category": "Grant",
     "amount": "$15,000-$50,000", "deadline": "Opens May 1, 2026", "fit": 7,
     "url": "https://www.artswriters.org",
     "format": "Writing sample + project description + bio",
     "cliff": {"rating": "moderate", "note": "$15K on adjunct base may exceed Medicaid. $50K = Essential Plan. Check with NYLAG."},
     "has_materials": False},
    {"id": "headlands", "name": "Headlands Center for the Arts", "category": "Residency",
     "amount": "Fully funded (airfare + meals + housing + $1K/month)", "deadline": "April 1 - June 1, 2026", "fit": 9,
     "url": "https://www.headlands.org/",
     "format": "Artist statement + project proposal + work samples + bio + references",
     "cliff": {"rating": "safe", "note": "$1K/month stipend is low. SNAP-safe."},
     "has_materials": False},
    {"id": "zkm-rauschenberg", "name": "ZKM Rauschenberg Residencies", "category": "Residency",
     "amount": "Studios/rehearsal rooms, 3 months", "deadline": "April 12, 2026, 11:59pm CET", "fit": 8,
     "url": "https://zkm.de/en/open-call-rauschenberg-residencies-202627",
     "format": "Single PDF: CV + artist statement + project proposal + work samples",
     "cliff": {"rating": "safe", "note": "No stipend. Travel costs only."},
     "has_materials": False},
    {"id": "doris-duke", "name": "Doris Duke / Mozilla Artists Make Technology Lab", "category": "Grant",
     "amount": "Up to $150,000", "deadline": "March 2, 2026, 12:00 ET", "fit": 7,
     "url": "https://www.dorisduke.org/grants/projects/artists-make-technology-lab",
     "format": "Project proposal + budget + work samples + bio",
     "cliff": {"rating": "caution", "note": "$150K well above all thresholds. Call NYLAG before accepting."},
     "has_materials": True},
    {"id": "lacma-art-tech", "name": "LACMA Art + Technology Lab", "category": "Grant",
     "amount": "Up to $50,000 + mentorship", "deadline": "Rolling/annual RFP", "fit": 8,
     "url": "https://www.lacma.org/lab",
     "format": "Project proposal + artist statement + budget + work samples",
     "cliff": {"rating": "caution", "note": "$50K -> Essential Plan. Call NYLAG."},
     "has_materials": False},
    {"id": "google-ami", "name": "Google Artists + Machine Intelligence Grants", "category": "Grant",
     "amount": "$10,000 + technical mentorship", "deadline": "Watch for next cycle", "fit": 9,
     "url": "https://experiments.withgoogle.com/ami-grants",
     "format": "Application form + project description + work samples + bio",
     "cliff": {"rating": "safe", "note": "$10K on adjunct base stays within Medicaid with Schedule C deductions."},
     "has_materials": False},
    # Track 2: Emergency & Rolling
    {"id": "github-sponsors", "name": "GitHub Sponsors", "category": "Infrastructure",
     "amount": "Variable (ongoing)", "deadline": "Activate NOW", "fit": None,
     "url": "https://github.com/sponsors",
     "format": "Profile setup + tier configuration",
     "cliff": {"rating": "safe", "note": "Ongoing income. Monitor monthly against SNAP threshold ($1,580/mo)."},
     "has_materials": True},
    {"id": "fractured-atlas", "name": "Fractured Atlas Fiscal Sponsorship", "category": "Infrastructure",
     "amount": "$10/mo + 8% fee on donations", "deadline": "Apply this week", "fit": None,
     "url": "https://www.fracturedatlas.org/",
     "format": "Online application: project description + budget + artistic statement",
     "cliff": {"rating": "safe", "note": "Infrastructure cost, not income."},
     "has_materials": True},
    {"id": "fca-emergency", "name": "FCA Emergency Grants", "category": "Emergency",
     "amount": "$200-$3,000", "deadline": "Rolling (monthly review)", "fit": None,
     "url": "https://www.foundationforcontemporaryarts.org/grants/emergency-grants/",
     "format": "Application form + proof of public presentation + budget + artist statement",
     "cliff": {"rating": "safe", "note": "SNAP-safe (lump sum, small amount)."},
     "has_materials": False},
    {"id": "rauschenberg-emergency", "name": "Rauschenberg Emergency Cycle 36", "category": "Emergency",
     "amount": "Up to $5,000", "deadline": "April 14 - May 12, 2026", "fit": 6,
     "url": "https://www.rfrfgrants.org/",
     "format": "Short application form + artist statement + documentation of need",
     "cliff": {"rating": "safe", "note": "SNAP-safe (lump sum, <$5K)."},
     "has_materials": False},
    {"id": "pen-america", "name": "PEN America Writers Aid", "category": "Emergency",
     "amount": "Up to $3,500", "deadline": "Rolling", "fit": 9,
     "url": "https://pen.org/us-writers-aid-initiative/",
     "format": "Application form + writing sample + documentation of need",
     "cliff": {"rating": "safe", "note": "SNAP-safe (lump sum)."},
     "has_materials": True},
    {"id": "awesome-foundation", "name": "Awesome Foundation NYC", "category": "Grant",
     "amount": "$1,000", "deadline": "Monthly", "fit": 8,
     "url": "https://www.awesomefoundation.org/en/chapters/nyc",
     "format": "Short application: project description (~300 words)",
     "cliff": {"rating": "safe", "note": "SNAP-safe."},
     "has_materials": False},
    {"id": "stimpunks", "name": "Stimpunks Creator Grant", "category": "Grant",
     "amount": "$3,000", "deadline": "Rolling (5 grants/year)", "fit": 7,
     "url": "https://stimpunks.org/creators/grant/",
     "format": "Application form + project description + work samples",
     "cliff": {"rating": "safe", "note": "SNAP-safe."},
     "has_materials": False},
    # Track 3: Selective Employment
    {"id": "together-ai", "name": "Together AI: Lead DX Engineer, Documentation", "category": "Employment",
     "amount": "$160,000-$240,000 + equity", "deadline": "Rolling", "fit": 6,
     "url": "https://job-boards.greenhouse.io/togetherai/jobs/4903661007",
     "format": "Resume + cover letter + portfolio",
     "cliff": {"rating": "caution", "note": "Full employment exits benefits entirely. Salary sufficient."},
     "has_materials": True},
    {"id": "huggingface", "name": "HuggingFace Developer Advocate Engineer", "category": "Employment",
     "amount": "$120,000-$160,000", "deadline": "Rolling", "fit": 5,
     "url": "https://apply.workable.com/huggingface/j/4C12FB7880",
     "format": "Resume + cover letter + writing samples",
     "cliff": {"rating": "caution", "note": "Full employment exits benefits entirely. Salary sufficient."},
     "has_materials": True},
    {"id": "anthropic-fde", "name": "Anthropic Forward Deployed Engineer", "category": "Employment",
     "amount": "$280,000-$400,000", "deadline": "Rolling", "fit": 4,
     "url": "https://job-boards.greenhouse.io/anthropic/jobs/5074695008",
     "format": "Resume + cover letter + portfolio",
     "cliff": {"rating": "caution", "note": "Full employment exits benefits entirely."},
     "has_materials": True},
    {"id": "openai-evals", "name": "OpenAI Software Engineer, Applied Evals", "category": "Employment",
     "amount": "$230,000-$385,000", "deadline": "Rolling", "fit": 4,
     "url": "https://openai.com/careers/software-engineer-applied-evals-san-francisco/",
     "format": "Resume + cover letter + portfolio",
     "cliff": {"rating": "caution", "note": "Full employment exits benefits entirely."},
     "has_materials": True},
    # Track 4: Consulting
    {"id": "ai-consulting", "name": "AI Systems Consulting", "category": "Consulting",
     "amount": "$100-125/hr (project: $2,500-$15,000)", "deadline": "Ongoing", "fit": None,
     "url": None,
     "format": "Direct outreach + platform registration (Toptal, Contra)",
     "cliff": {"rating": "moderate", "note": "Earned income counts toward SNAP ($1,580/mo). Keep monthly <$1,500 or accept Essential Plan."},
     "has_materials": False},
    {"id": "workshop-facilitation", "name": "Workshop Facilitation", "category": "Consulting",
     "amount": "$500-$2,000/session", "deadline": "Ongoing", "fit": None,
     "url": None,
     "format": "Direct outreach to residency networks + community spaces",
     "cliff": {"rating": "moderate", "note": "Earned income. Monitor monthly totals."},
     "has_materials": False},
    {"id": "documentation-consulting", "name": "Documentation Consulting", "category": "Consulting",
     "amount": "$2,500-$15,000/project", "deadline": "Ongoing", "fit": None,
     "url": None,
     "format": "Direct outreach to startups + open-source projects",
     "cliff": {"rating": "moderate", "note": "Earned income. Monitor against thresholds."},
     "has_materials": False},
    # Track 5: Career-Building
    {"id": "new-inc", "name": "NEW INC (New Museum Incubator)", "category": "Incubator",
     "amount": "~$600/mo membership", "deadline": "Spring/Summer 2026", "fit": 7,
     "url": "https://www.newinc.org/",
     "format": "Application form + project proposal + portfolio",
     "cliff": {"rating": "safe", "note": "Membership cost, not income."},
     "has_materials": False},
    {"id": "pioneer-works", "name": "Pioneer Works Residency", "category": "Residency",
     "amount": "$1,000-$2,500 + studio", "deadline": "Summer 2026 for 2027", "fit": 7,
     "url": "https://pioneerworks.org/",
     "format": "Artist statement + project proposal + work samples + bio",
     "cliff": {"rating": "safe", "note": "Small stipend. SNAP-safe."},
     "has_materials": False},
    {"id": "tulsa-fellowship", "name": "Tulsa Artist Fellowship", "category": "Fellowship",
     "amount": "$230,000+ (3 years: $150K + housing + healthcare)", "deadline": "Spring 2026 app", "fit": 7,
     "url": "https://tulsaartistfellowship.org/",
     "format": "Comprehensive application: statement + proposal + work samples + references + budget",
     "cliff": {"rating": "caution", "note": "$230K+ over 3 years. Full benefits exit. But salary is substantial."},
     "has_materials": False},
    {"id": "queer-art", "name": "Queer|Art Mentorship Program", "category": "Program",
     "amount": "Program-based (mentorship)", "deadline": "~June-July 2026", "fit": 8,
     "url": "https://www.queer-art.org/mentorship",
     "format": "Application form + artist statement + work samples + bio",
     "cliff": {"rating": "safe", "note": "No direct income."},
     "has_materials": False},
    {"id": "lambda-literary", "name": "Lambda Literary Writers Retreat", "category": "Retreat",
     "amount": "Program-based", "deadline": "~November 2026-January 2027", "fit": 7,
     "url": "https://www.lambdaliterary.org/writers-retreat/",
     "format": "Writing sample (15-25 pages) + artist statement + bio",
     "cliff": {"rating": "safe", "note": "No direct income (program fee may apply)."},
     "has_materials": False},
    # Track 6: Writing Income
    {"id": "noema", "name": "Noema Magazine", "category": "Writing",
     "amount": "$1/word (~$3K per essay)", "deadline": "Rolling", "fit": None,
     "url": "mailto:[email redacted]",
     "format": "Pitch email: 2-3 paragraph pitch + writing samples",
     "cliff": {"rating": "moderate", "note": "Earned income. One per quarter = safe on adjunct base. Two per year safest."},
     "has_materials": False},
    {"id": "gay-lesbian-review", "name": "Gay & Lesbian Review", "category": "Writing",
     "amount": "$250/feature, $100/review", "deadline": "Rolling", "fit": 9,
     "url": "https://glreview.org/writers-guidelines/",
     "format": "Pitch email or completed manuscript + bio",
     "cliff": {"rating": "safe", "note": "$250-$350 per piece. Well below thresholds."},
     "has_materials": False},
    {"id": "logic-magazine", "name": "Logic Magazine", "category": "Writing",
     "amount": "$1,200-$2,000/essay", "deadline": "Themed issues", "fit": 8,
     "url": "https://logicmag.io",
     "format": "Pitch email aligned with current theme + writing samples",
     "cliff": {"rating": "moderate", "note": "Earned income. One per quarter is manageable."},
     "has_materials": False},
    {"id": "mit-tech-review", "name": "MIT Technology Review / Wired / Aeon", "category": "Writing",
     "amount": "$1-3/word (MIT TR), $2,500+ (Wired), $500-1,500 (Aeon)", "deadline": "Rolling", "fit": None,
     "url": "https://www.technologyreview.com/",
     "format": "Pitch email: 3-4 paragraph pitch + credentials + writing samples",
     "cliff": {"rating": "moderate", "note": "High per-piece income. Monitor monthly totals."},
     "has_materials": False},
    # Additional targets from funding strategy
    {"id": "spencer-foundation", "name": "Spencer Foundation Small Research Grant", "category": "Grant",
     "amount": "Up to $50,000", "deadline": "April 15, 2026, noon CT", "fit": 6,
     "url": "https://www.spencer.org/grant_types/small-research-grant",
     "format": "Project narrative + literature review + methodology + budget + CV",
     "cliff": {"rating": "caution", "note": "$50K -> Essential Plan. Call NYLAG."},
     "has_materials": False},
    {"id": "recurse-center", "name": "Recurse Center", "category": "Program",
     "amount": "Free (optional living stipend)", "deadline": "Rolling", "fit": 9,
     "url": "https://www.recurse.com/apply",
     "format": "Written application + pair programming interview + conversational interview",
     "cliff": {"rating": "safe", "note": "Free program. Optional stipend available for need."},
     "has_materials": False},
]

# Build lookup by id
TARGET_BY_ID = {t["id"]: t for t in TARGETS}

# ═══════════════════════════════════════════════════════════════════════════════
# CANONICAL WORK SAMPLES (from covenant-ark Section E)
# ═══════════════════════════════════════════════════════════════════════════════

WORK_SAMPLES = [
    {"num": 1, "name": "Portfolio Site", "url": "https://4444j99.github.io/portfolio/",
     "desc": "Interactive portfolio with generative art (p5.js), CMYK design system, 19 curated projects"},
    {"num": 2, "name": "Eight-Organ System Hub", "url": "https://github.com/meta-organvm/organvm-corpvs-testamentvm",
     "desc": "Governance corpus: 410K+ words, registry, orchestration specs, 33 sprint records"},
    {"num": 3, "name": "Public Process Essays", "url": "https://organvm-v-logos.github.io/public-process/",
     "desc": "42 essays documenting creative methodology in real time (~142K words)"},
    {"num": 4, "name": "Recursive Engine", "url": "https://github.com/organvm-i-theoria/recursive-engine--generative-entity",
     "desc": "Symbolic operating system: 1,254 tests, 85% coverage, 21 organ handlers, custom DSL"},
    {"num": 5, "name": "Agentic Titan", "url": "https://github.com/organvm-iv-taxis/agentic-titan",
     "desc": "Multi-agent orchestration framework: 1,095 tests, 18 development phases"},
    {"num": 6, "name": "life-my--midst--in", "url": "https://github.com/organvm-iii-ergon/life-my--midst--in",
     "desc": "Interactive identity platform: 291 tests, 44 DB tables, Inverted Interview paradigm"},
    {"num": 7, "name": "Metasystem Master", "url": "https://github.com/organvm-ii-poiesis/metasystem-master",
     "desc": "Generative art meta-system connecting theory to practice"},
    {"num": 8, "name": "Orchestration Hub", "url": "https://github.com/organvm-iv-taxis/orchestration-start-here",
     "desc": "11 governance workflows, cross-org dispatch, promotion automation"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# CANONICAL LINKS (from covenant-ark Section F)
# ═══════════════════════════════════════════════════════════════════════════════

LINKS = {
    "portfolio": "https://4444j99.github.io/portfolio/",
    "resume": "https://4444j99.github.io/portfolio/resume/",
    "github": "https://github.com/4444J99",
    "essays": "https://organvm-v-logos.github.io/public-process/",
    "rss": "https://organvm-v-logos.github.io/public-process/feed.xml",
    "hub": "https://github.com/meta-organvm/organvm-corpvs-testamentvm",
    "orchestration": "https://github.com/organvm-iv-taxis/orchestration-start-here",
    "registry": "https://github.com/meta-organvm/organvm-corpvs-testamentvm/blob/main/repo-registry.json",
    "meta_org": "https://github.com/meta-organvm",
}

# ═══════════════════════════════════════════════════════════════════════════════
# KEY DIFFERENTIATORS (from covenant-ark Section G, indexed 1-6)
# ═══════════════════════════════════════════════════════════════════════════════

DIFFERENTIATORS = {
    1: "Solo production at institutional scale — one person built and documented a {repos}-repository system across 8 organizations.",
    2: "Process-as-product methodology — the {essays} essays aren't marketing; they ARE the creative work.",
    3: "AI-augmented creative practice, not AI-generated art — AI serves as compositional instrument; the vision is human.",
    4: "Governance as creative medium — registry design, dependency graphs, and promotion pipelines are generative structures.",
    5: "Radical transparency at system scale — {words} of documentation, 33 sprint specs, 12 ADRs, a constitution.",
    6: "Cross-domain integration — the eight-organ model bridges theory, art, commerce, governance, and community.",
}


# ═══════════════════════════════════════════════════════════════════════════════
# LOADERS
# ═══════════════════════════════════════════════════════════════════════════════

def load_covenant_metrics() -> dict:
    """Parse Section A metrics table from covenant-ark.md."""
    metrics = {}
    if not COVENANT_ARK_PATH.exists():
        print(f"WARNING: {COVENANT_ARK_PATH} not found. Using defaults.", file=sys.stderr)
        return {
            "repos": "100", "active": "90", "archived": "10",
            "orgs": "8", "essays": "42", "words": "~410K+",
            "sprints": "33", "ci": "82+", "edges": "31",
            "tests": "2,349+", "scripts": "5",
        }

    text = COVENANT_ARK_PATH.read_text()
    # Parse the metrics table
    table_pattern = re.compile(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|")
    for m in table_pattern.finditer(text):
        key, val = m.group(1).strip(), m.group(2).strip()
        if key == "Metric" or key.startswith("-"):
            continue
        val = val.strip()
        if "Total repositories" in key:
            metrics["repos"] = val
        elif "Implementation status" in key:
            parts = val.split(",")
            for p in parts:
                p = p.strip()
                if "ACTIVE" in p:
                    metrics["active"] = p.split()[0]
                elif "ARCHIVED" in p:
                    metrics["archived"] = p.split()[0]
        elif "Published essays" in key:
            metrics["essays"] = val.split()[0] if " " in val else val
        elif "Total documentation" in key:
            # Strip trailing "words" since templates add context
            metrics["words"] = val.rstrip(" words").rstrip("+") + "+"
        elif "Named development sprints" in key or "sprints" in key.lower():
            metrics["sprints"] = val
        elif "CI/CD" in key:
            metrics["ci"] = val.rstrip(" repos with workflows")
        elif "Dependency edges" in key:
            metrics["edges"] = val.split()[0] if " " in val else val
        elif "Automated tests" in key:
            metrics["tests"] = val
        elif "Validation scripts" in key:
            metrics["scripts"] = val.split()[0] if " " in val else val

    # Defaults for anything not parsed
    metrics.setdefault("repos", "100")
    metrics.setdefault("active", "90")
    metrics.setdefault("archived", "10")
    metrics.setdefault("orgs", "8")
    metrics.setdefault("essays", "42")
    metrics.setdefault("words", "~410K+")
    metrics.setdefault("sprints", "33")
    metrics.setdefault("ci", "82+")
    metrics.setdefault("edges", "31")
    metrics.setdefault("tests", "2,349+")
    metrics.setdefault("scripts", "5")
    return metrics


# ISOTOPE DISSOLUTION: Gate memory--remember G2 (CORPUS_SCRIPTS_DISSOLVED)
try:
    from organvm_engine.registry.loader import load_registry as _engine_load
except ImportError:
    _engine_load = None


def load_registry() -> Optional[dict]:
    """Load repo-registry.json."""
    if not REGISTRY_PATH.exists():
        return None
    if _engine_load is not None:
        return _engine_load(REGISTRY_PATH)
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def load_system_metrics() -> Optional[dict]:
    """Load system-metrics.json for computed values."""
    if not METRICS_PATH.exists():
        return None
    with open(METRICS_PATH) as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# POSITION-SHIFTED CONTENT GENERATORS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_artist_statement(position: str, metrics: dict, length: str = "medium") -> str:
    """Generate a position-shifted artist statement at specified length."""
    pt = POSITION_TEMPLATES[position]

    if length == "short":
        return (
            f"{pt['lead_sentence']} My eight-organ system coordinates {metrics['repos']} repositories "
            f"across 8 organizations — spanning theory, generative art, commerce, governance, "
            f"public process, community, and marketing. {metrics['essays']} published essays document "
            f"the methodology in real time. Solo production using AI tools as compositional instruments."
        )

    if length == "medium":
        return (
            f"{pt['lead_sentence']}\n\n"
            f"My practice centers on the eight-organ system — a documented infrastructure coordinating "
            f"theory, generative art, commercial products, governance, public process, community, and "
            f"marketing across {metrics['repos']} repositories and 8 GitHub organizations. The "
            f"{metrics['essays']} published essays documenting this process aren't reflections on the "
            f"work; they ARE the work — the creative process rendered into prose in real time.\n\n"
            f"I use AI tools as compositional instruments, the way Brian Eno treated the studio. "
            f"The architectural vision, governance design, and editorial judgment are the creative work. "
            f"The result: a documented methodology for solo production at institutional scale, built over "
            f"5+ years and {metrics['sprints']} development sprints."
        )

    # long
    return (
        f"{pt['lead_sentence']}\n\n"
        f"My practice centers on the eight-organ system: a documented infrastructure coordinating "
        f"theory, generative art, commercial products, governance, public process, community, and "
        f"marketing across {metrics['repos']} repositories. I don't produce individual artworks. "
        f"I produce the *systems* that generate, coordinate, and sustain creative work — and the "
        f"visible record of how those systems are built is itself the primary creative output.\n\n"
        f"The process of creation is the product. The {metrics['essays']} essays I've published "
        f"aren't reflections on the work; they ARE the work — the creative process rendered into "
        f"prose in real time. The governance rules — registry design, dependency graphs, promotion "
        f"pipelines — aren't bureaucratic overhead; they're generative constraints, the way a "
        f"composer's harmonic rules shape what melodies can emerge.\n\n"
        f"I work in the tradition of solo producers who became orchestras: Brian Eno treating "
        f"the studio as a compositional instrument, Trent Reznor building entire albums alone "
        f"because nobody else would commit at the necessary intensity. I use AI tools the way "
        f"these practitioners used their technologies — as instruments for realizing an "
        f"architectural vision, not as replacements for creative judgment.\n\n"
        f"The eight-organ system is simultaneously: (a) working infrastructure that produces "
        f"creative work, (b) a documented methodology for solo production at institutional "
        f"scale, (c) an argument that the process of creation — made visible and governable — "
        f"is itself the most interesting thing an artist can produce, and (d) a reusable model "
        f"other practitioners can learn from."
    )


def generate_bio(position: str, metrics: dict, length: str = "medium") -> str:
    """Generate a position-shifted bio at specified length."""
    pt = POSITION_TEMPLATES[position]

    if length == "short":
        ", ".join(pt["bio_emphasis"][:3])
        return (
            f"Systems artist. Creator of the ORGANVM eight-organ system — {metrics['repos']} "
            f"repositories, 8 organizations, {metrics['essays']} essays, {metrics['words']} words. "
            f"Builds creative infrastructure at institutional scale using AI tools as compositional "
            f"instruments. MFA Creative Writing, 18 years professional experience. NYC-based."
        )

    if length == "medium":
        return (
            f"Systems artist and auteur-producer. Creator of the ORGANVM eight-organ system: "
            f"{metrics['repos']} repositories across 8 GitHub organizations coordinating theory, "
            f"art, commerce, governance, and public process through automated governance. "
            f"{metrics['essays']} published essays, {metrics['sprints']} development sprints, "
            f"{metrics['words']} of documentation. 18 years professional experience across "
            f"creative systems design, college instruction (11 years, 2,000+ students), multimedia "
            f"production, and project management. MFA Creative Writing, Meta Full-Stack Developer "
            f"certification. Based in New York City."
        )

    # long
    return (
        f"Systems artist and auteur-producer working at the intersection of creative infrastructure, "
        f"governance design, and AI-augmented methodology. Creator of the ORGANVM eight-organ system: "
        f"{metrics['repos']} repositories across 8 GitHub organizations coordinating theory, generative "
        f"art, commercial products, governance, public process, community, and marketing through automated "
        f"governance and a formal promotion state machine. {metrics['essays']} published essays document "
        f"the creative process in real time.\n\n"
        f"Professional background spans 18 years across four domains: 5 years independent creative "
        f"systems design (the eight-organ system, 2,349+ tests, {metrics['sprints']} "
        f"development sprints), 11 years college instruction at 8+ institutions (2,000+ students), "
        f"15 years multimedia production (AJP Media Arts), and 11 years construction project management. "
        f"MFA Creative Writing (FAU), BA English Literature (CUNY). Meta Full-Stack Developer and Google "
        f"UX/Digital Marketing/Project Management certifications.\n\n"
        f"Based in New York City."
    )


def generate_narrative(position: str, target: dict, metrics: dict) -> str:
    """Generate the 'why this opportunity' paragraph."""
    pt = POSITION_TEMPLATES[position]
    frame = pt["narrative_frame"].format(
        repos=metrics["repos"], essays=metrics["essays"],
        words=metrics["words"], ci=metrics["ci"], edges=metrics["edges"],
    )

    name = target["name"]
    category = target["category"]

    if category in ("Grant", "Prize"):
        return (
            f"{frame}\n\n"
            f"{name} represents a critical opportunity to sustain and extend this practice. "
            f"The work is built, documented, and operational — what it needs now is the time "
            f"and resources to deepen, not to start over."
        )
    elif category == "Residency":
        return (
            f"{frame}\n\n"
            f"A residency at {name} would provide the focused time and creative community "
            f"to advance the most challenging next phase of this work — moving from documented "
            f"infrastructure to active community engagement and public presentation."
        )
    elif category in ("Fellowship", "Program"):
        return (
            f"{frame}\n\n"
            f"{name} aligns precisely with the trajectory of this practice — the combination "
            f"of creative rigor, technical depth, and public documentation that defines the "
            f"eight-organ methodology."
        )
    elif category == "Employment":
        return (
            f"{frame}\n\n"
            f"The skills demonstrated by this system — architecture at scale, documentation "
            f"as infrastructure, autonomous governance design — translate directly to the "
            f"requirements of this role."
        )
    elif category == "Writing":
        return (
            f"{frame}\n\n"
            f"The story is genuinely unusual: one person using AI as a compositional instrument "
            f"to build creative infrastructure at institutional scale, documented transparently "
            f"from day one. The {metrics['essays']} published essays are proof of both the "
            f"methodology and the writing capacity."
        )
    elif category == "Emergency":
        return (
            f"Working artist with an active, documented creative practice: {metrics['repos']} "
            f"repositories, {metrics['essays']} published essays, {metrics['words']} of public "
            f"documentation — all built over 5+ years of sustained work. Currently housing-precarious "
            f"(licensee in parent's home) with limited adjunct income. This emergency support would "
            f"directly enable continued creative production."
        )
    else:
        return frame


def select_work_samples(position: str) -> list:
    """Return work samples reordered for position."""
    pt = POSITION_TEMPLATES[position]
    order = pt["work_samples_order"]
    return [WORK_SAMPLES[i - 1] for i in order if i <= len(WORK_SAMPLES)]


def select_differentiators(position: str, metrics: dict) -> list:
    """Return differentiators reordered for position."""
    pt = POSITION_TEMPLATES[position]
    order = pt["differentiators_order"]
    result = []
    for i in order:
        if i in DIFFERENTIATORS:
            text = DIFFERENTIATORS[i].format(
                repos=metrics["repos"], essays=metrics["essays"],
                words=metrics["words"],
            )
            result.append(text)
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

def generate_profile(target: dict, metrics: dict) -> dict:
    """Generate a complete JSON identity profile for a target."""
    tid = target["id"]
    primary, secondary = IDENTITY_MAP.get(tid, ("systems_artist", None))
    pt = POSITION_TEMPLATES[primary]

    samples = select_work_samples(primary)
    diffs = select_differentiators(primary, metrics)

    profile = {
        "target_id": tid,
        "target_name": target["name"],
        "category": target["category"],
        "amount": target["amount"],
        "deadline": target["deadline"],
        "url": target["url"],
        "fit_score": target["fit"],
        "primary_position": primary,
        "secondary_position": secondary,
        "position_label": pt["label"],
        "identity_narrative": generate_narrative(primary, target, metrics),
        "artist_statement": {
            "long": generate_artist_statement(primary, metrics, "long"),
            "medium": generate_artist_statement(primary, metrics, "medium"),
            "short": generate_artist_statement(primary, metrics, "short"),
        },
        "bio": {
            "long": generate_bio(primary, metrics, "long"),
            "medium": generate_bio(primary, metrics, "medium"),
            "short": generate_bio(primary, metrics, "short"),
        },
        "work_samples": [
            {"name": s["name"], "url": s["url"], "description": s["desc"]}
            for s in samples
        ],
        "evidence_highlights": diffs[:4],
        "differentiators": diffs,
        "benefits_cliff": target["cliff"],
        "submission_format": target["format"],
        "has_existing_materials": target.get("has_materials", False),
        "generated": datetime.now(timezone.utc).isoformat(),
    }
    return profile


# ═══════════════════════════════════════════════════════════════════════════════
# SUBMISSION SCRIPT GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

# Which targets already have scripts (don't regenerate)
EXISTING_SCRIPTS = {
    "artadia-nyc", "google-fellowship", "google-cl5", "prix-ars", "starts-prize",
    "doris-duke", "pen-america", "github-sponsors", "fractured-atlas",
    "together-ai", "huggingface", "anthropic-fde", "openai-evals", "watermill",
}

# Targets that need new scripts
SCRIPT_TARGETS = [t["id"] for t in TARGETS
                  if t["id"] not in EXISTING_SCRIPTS
                  and t["category"] != "Consulting"]

SCRIPT_FILENAMES = {
    "creative-capital": "cc-creative-capital.md",
    "wff-housing": "wff-housing.md",
    "headlands": "headlands.md",
    "fire-island": "fire-island.md",
    "eyebeam": "eyebeam.md",
    "zkm-rauschenberg": "zkm.md",
    "whiting-nonfiction": "whiting.md",
    "warhol-arts-writers": "warhol.md",
    "lacma-art-tech": "lacma.md",
    "google-ami": "google-ami.md",
    "nlnet-commons": "nlnet.md",
    "spencer-foundation": "spencer.md",
    "processing-foundation": "processing.md",
    "recurse-center": "recurse.md",
    "fca-emergency": "fca-emergency.md",
    "rauschenberg-emergency": "rauschenberg-emergency.md",
    "awesome-foundation": "awesome-foundation.md",
    "stimpunks": "stimpunks.md",
    "noema": "noema-pitch.md",
    "logic-magazine": "logic-pitch.md",
    "gay-lesbian-review": "glr-pitch.md",
    "mit-tech-review": "mit-tr-pitch.md",
    "new-inc": "new-inc.md",
    "pioneer-works": "pioneer-works.md",
    "tulsa-fellowship": "tulsa.md",
    "queer-art": "queer-art.md",
    "lambda-literary": "lambda-literary.md",
}


def estimate_time(target: dict) -> str:
    """Estimate completion time based on category."""
    cat = target["category"]
    if cat == "Emergency":
        return "15-20"
    elif cat in ("Writing",):
        return "20-30"
    elif cat in ("Infrastructure", "Program"):
        return "15-30"
    elif cat == "Grant" and target.get("fit") and target["fit"] >= 8:
        return "45-60"
    elif cat == "Residency":
        return "30-45"
    elif cat == "Fellowship":
        return "30-45"
    elif cat == "Prize":
        return "20-30"
    else:
        return "30-45"


def generate_submission_script(target: dict, profile: dict, metrics: dict) -> str:
    """Generate a full submission script markdown file."""
    tid = target["id"]
    primary = profile["primary_position"]
    secondary = profile["secondary_position"]
    pt = POSITION_TEMPLATES[primary]
    est = estimate_time(target)
    cat = target["category"]

    secondary_label = POSITION_TEMPLATES[secondary]["label"] if secondary else "None"

    # Header
    lines = [
        f"# Submission Script — {target['name']}",
        "",
        f"**Created:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        f"**Time to complete:** ~{est} minutes",
    ]
    if target["url"]:
        lines.append(f"**URL:** {target['url']}")
    lines.extend([
        f"**Deadline:** {target['deadline']}",
        f"**Award:** {target['amount']}",
        f"**Identity position:** {pt['label']} (secondary: {secondary_label})",
        f"**Benefits cliff:** {target['cliff']['note']}",
        "",
        "---",
        "",
        "> This is a step-by-step paste-and-submit guide. All answers are pre-written.",
        f"> Identity framing: **{pt['label']}** — {pt['lead_sentence']}",
        "",
        "---",
        "",
    ])

    # Pre-flight
    lines.extend([
        f"## Pre-flight ({_preflight_time(cat)} minutes)",
        "",
    ])
    if target["url"]:
        lines.append(f"- [ ] Open application: {target['url']}")
    lines.extend([
        "- [ ] Confirm eligibility requirements",
        "- [ ] Have ready: portfolio URL, resume PDF, work sample links",
        f"- [ ] Review identity position: **{pt['label']}**",
        "",
        "---",
        "",
    ])

    # Category-specific sections
    if cat in ("Grant", "Residency", "Fellowship", "Prize", "Program", "Incubator"):
        lines.extend(_grant_residency_sections(target, profile, metrics, pt))
    elif cat == "Writing":
        lines.extend(_writing_pitch_sections(target, profile, metrics, pt))
    elif cat == "Emergency":
        lines.extend(_emergency_sections(target, profile, metrics, pt))
    elif cat == "Retreat":
        lines.extend(_retreat_sections(target, profile, metrics, pt))
    else:
        lines.extend(_generic_sections(target, profile, metrics, pt))

    # Common links
    lines.extend([
        "---",
        "",
        "## Links to Submit",
        "",
        "| Resource | URL |",
        "|----------|-----|",
        f"| Portfolio | {LINKS['portfolio']} |",
        f"| Resume | {LINKS['resume']} |",
        f"| Essays | {LINKS['essays']} |",
        f"| System Hub | {LINKS['hub']} |",
        f"| GitHub | {LINKS['github']} |",
        "",
        "---",
        "",
    ])

    # Post-submit
    lines.extend([
        "## Post-submit",
        "",
        "- [ ] Record submission date in 04-application-tracker.md",
        "- [ ] Screenshot confirmation page/email",
        f"- [ ] Update status: `{tid}` → SUBMITTED",
        "- [ ] Note expected response timeline",
        "",
    ])

    return "\n".join(lines)


def _preflight_time(category: str) -> str:
    if category in ("Emergency", "Writing"):
        return "2"
    return "3"


def _grant_residency_sections(target, profile, metrics, pt):
    """Sections for grants, residencies, fellowships, prizes."""
    lines = []
    primary = profile["primary_position"]
    samples = select_work_samples(primary)

    # Artist statement
    statement_len = "long" if target.get("fit", 0) >= 8 else "medium"
    lines.extend([
        "## Artist Statement",
        "",
        f"**~{'300' if statement_len == 'long' else '150'} words — copy between the lines:**",
        "",
        "---",
        "",
        profile["artist_statement"][statement_len],
        "",
        "---",
        "",
    ])

    # Project description / narrative
    lines.extend([
        "## Project Description / Why This Opportunity",
        "",
        "---",
        "",
        profile["identity_narrative"],
        "",
        "---",
        "",
    ])

    # Bio
    lines.extend([
        "## Bio",
        "",
        "**~100 words — copy between the lines:**",
        "",
        "---",
        "",
        profile["bio"]["medium"],
        "",
        "---",
        "",
    ])

    # Work samples
    lines.extend([
        "## Work Samples (ordered for this audience)",
        "",
    ])
    for i, s in enumerate(samples[:5], 1):
        lines.extend([
            f"### Sample {i}: {s['name']}",
            "",
            f"**URL:** `{s['url']}`",
            "",
            s["desc"],
            "",
        ])

    # Key differentiators
    lines.extend([
        "## Key Differentiators (if asked \"what makes you different\")",
        "",
    ])
    for i, d in enumerate(profile["differentiators"][:4], 1):
        lines.append(f"{i}. {d}")
    lines.append("")

    return lines


def _writing_pitch_sections(target, profile, metrics, pt):
    """Sections for writing income pitches."""
    lines = []
    profile["primary_position"]

    # Pitch angles by target
    pitch_angles = {
        "noema": (
            "I built a 100-repository creative system orchestrated by AI — here's what it "
            "reveals about the future of solo creative production.",
            "Technology, governance, AI, culture",
        ),
        "logic-magazine": (
            "Governance as Artistic Medium: When the rules that coordinate 100 repositories "
            "become the artwork.",
            "Technology criticism — must align with current themed issue",
        ),
        "gay-lesbian-review": (
            "Systems art through a queer lens — building creative infrastructure from lived "
            "experience of precarity, recovery, and community.",
            "LGBTQ+ culture, arts, personal essay",
        ),
        "mit-tech-review": (
            "The AI-Conductor Model: How one person used Claude to coordinate 100 repos, "
            "33 sprints, and 410K+ words — and what it reveals about AI-augmented creative work.",
            "AI, creative technology, LLMs, methodology",
        ),
    }
    angle, topic = pitch_angles.get(target["id"], ("The eight-organ system as creative practice.", "Technology and art"))

    lines.extend([
        "## Pitch Email",
        "",
        "**Subject line options (pick one):**",
        "",
        f"1. PITCH: {angle[:60]}...",
        "2. PITCH: Building a 100-Repository Creative System with AI",
        "3. PITCH: The AI-Conductor Model — Solo Production at Institutional Scale",
        "",
        "**Body — copy below the line:**",
        "",
        "---",
        "",
        "Dear Editors,",
        "",
        f"{angle}",
        "",
        f"The essay would explore how the eight-organ system — {metrics['repos']} repositories "
        f"across 8 GitHub organizations, governed by automated dependency validation and a formal "
        f"promotion state machine — challenges assumptions about what solo creative practice can "
        f"achieve when AI tools serve as compositional instruments rather than replacements for "
        f"creative judgment.",
        "",
        f"Topic fit: {topic}",
        "",
        f"I've published {metrics['essays']} essays documenting this methodology ({LINKS['essays']}). "
        f"My MFA is in Creative Writing from Florida Atlantic University, and I've taught writing "
        f"at 8+ institutions over 11 years.",
        "",
        "I'd welcome the chance to discuss scope, angle, and timing.",
        "",
        "Best,",
        "[Name]",
        "",
        "---",
        "",
    ])

    # Writing samples
    lines.extend([
        "## Writing Samples to Attach",
        "",
        f"1. Public Process essay series: {LINKS['essays']}",
        f"2. Portfolio (demonstrates documentation range): {LINKS['portfolio']}",
        f"3. Governance corpus: {LINKS['hub']}",
        "",
    ])

    # Bio
    lines.extend([
        "## Short Bio (if requested)",
        "",
        "---",
        "",
        profile["bio"]["short"],
        "",
        "---",
        "",
    ])

    return lines


def _emergency_sections(target, profile, metrics, pt):
    """Sections for emergency fund applications."""
    lines = []

    lines.extend([
        "## Narrative Description",
        "",
        "---",
        "",
        f"Working artist with an active, documented creative practice: {metrics['repos']} "
        f"repositories, {metrics['essays']} published essays, {metrics['words']} of public "
        f"documentation — all built over 5+ years of sustained work. MFA Creative Writing "
        f"(Florida Atlantic University, 2015-2018). 11 years teaching at 8+ institutions.",
        "",
        "Currently housing-precarious (licensee in parent's home, NYC) with limited adjunct "
        "income (~$12K base). This emergency support would directly enable continued creative "
        "production and professional development.",
        "",
        "---",
        "",
    ])

    # Artist statement (short)
    lines.extend([
        "## Artist Statement (short)",
        "",
        "---",
        "",
        profile["artist_statement"]["short"],
        "",
        "---",
        "",
    ])

    # Evidence of professional practice
    lines.extend([
        "## Evidence of Professional Practice",
        "",
        f"- Portfolio: {LINKS['portfolio']}",
        f"- {metrics['essays']} published essays: {LINKS['essays']}",
        f"- {metrics['repos']}-repository system: {LINKS['hub']}",
        "- MFA Creative Writing, Florida Atlantic University",
        "- 11 years teaching at 8+ NYC-area institutions",
        "",
    ])

    return lines


def _retreat_sections(target, profile, metrics, pt):
    """Sections for writing retreats and workshops."""
    lines = []

    lines.extend([
        "## Writing Sample",
        "",
        "Submit 15-25 pages from published essays. Recommended selections:",
        "",
        f"1. Latest essay from {LINKS['essays']}",
        "2. \"Construction Addiction\" (essay #36 — most narrative)",
        "3. \"Twelve Decisions That Shaped the System\" (essay #40 — most methodological)",
        "",
    ])

    lines.extend([
        "## Artist Statement",
        "",
        "---",
        "",
        profile["artist_statement"]["medium"],
        "",
        "---",
        "",
    ])

    lines.extend([
        "## Bio",
        "",
        "---",
        "",
        profile["bio"]["medium"],
        "",
        "---",
        "",
    ])

    return lines


def _generic_sections(target, profile, metrics, pt):
    """Generic sections for other target types."""
    lines = []

    lines.extend([
        "## Application Content",
        "",
        "---",
        "",
        profile["identity_narrative"],
        "",
        "---",
        "",
    ])

    lines.extend([
        "## Artist Statement",
        "",
        "---",
        "",
        profile["artist_statement"]["medium"],
        "",
        "---",
        "",
    ])

    lines.extend([
        "## Bio",
        "",
        "---",
        "",
        profile["bio"]["medium"],
        "",
        "---",
        "",
    ])

    return lines


# ═══════════════════════════════════════════════════════════════════════════════
# INDEX GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════

def generate_index(profiles: list) -> dict:
    """Generate _index.json manifest."""
    return {
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_profiles": len(profiles),
        "by_position": {
            pos: [p["target_id"] for p in profiles if p["primary_position"] == pos]
            for pos in POSITION_TEMPLATES
        },
        "by_category": {},
        "profiles": [
            {"target_id": p["target_id"], "target_name": p["target_name"],
             "category": p["category"], "primary_position": p["primary_position"],
             "fit_score": p["fit_score"], "has_existing_materials": p["has_existing_materials"]}
            for p in profiles
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# COVERAGE AUDIT
# ═══════════════════════════════════════════════════════════════════════════════

def run_audit():
    """Check coverage: all targets have profiles and scripts."""
    print("=" * 60)
    print("ALCHEMIZER — Coverage Audit")
    print("=" * 60)

    metrics = load_covenant_metrics()
    all_profiles = list(PROFILES_DIR.glob("*.json"))
    profile_ids = {p.stem for p in all_profiles if p.stem != "_index"}

    all_scripts = list(SCRIPTS_DIR.glob("*.md"))
    existing_script_names = {s.name for s in all_scripts}

    target_ids = {t["id"] for t in TARGETS}
    targets_with_materials = {t["id"] for t in TARGETS if t.get("has_materials")}
    targets_needing_scripts = {t["id"] for t in TARGETS
                               if not t.get("has_materials") and t["category"] != "Consulting"}

    print(f"\n  Targets in registry: {len(TARGETS)}")
    print(f"  Targets with existing materials: {len(targets_with_materials)}")
    print(f"  Targets needing new scripts: {len(targets_needing_scripts)}")

    # Profile coverage
    missing_profiles = target_ids - profile_ids
    print(f"\n  Profiles generated: {len(profile_ids)}")
    if missing_profiles:
        print(f"  MISSING profiles: {sorted(missing_profiles)}")
    else:
        print("  Profile coverage: 100%")

    # Script coverage
    script_mapped = set()
    for tid in targets_needing_scripts:
        fname = SCRIPT_FILENAMES.get(tid)
        if fname and fname in existing_script_names:
            script_mapped.add(tid)
    missing_scripts = targets_needing_scripts - script_mapped
    total_scripts = len(targets_with_materials) + len(script_mapped)
    print(f"\n  Total targets with scripts: {total_scripts}/{len(TARGETS)}")
    if missing_scripts:
        print(f"  MISSING scripts: {sorted(missing_scripts)}")
    else:
        print("  Script coverage: 100% (excluding consulting)")

    # Metrics check
    print("\n  Metrics source: covenant-ark")
    print(f"  Repos: {metrics['repos']}")
    print(f"  Active: {metrics['active']}")
    print(f"  Essays: {metrics['essays']}")
    print(f"  Words: {metrics['words']}")

    # Benefits cliff coverage
    high_amount_missing_cliff = []
    for t in TARGETS:
        if t["cliff"]["rating"] == "safe":
            continue
        if "NYLAG" not in t["cliff"]["note"] and t["cliff"]["rating"] == "caution":
            high_amount_missing_cliff.append(t["id"])
    if high_amount_missing_cliff:
        print(f"\n  WARNING: Targets with caution rating but no NYLAG reference: {high_amount_missing_cliff}")
    else:
        print("\n  Benefits cliff: all caution-rated targets reference NYLAG")

    # Identity position distribution
    print("\n  Position distribution:")
    for pos in POSITION_TEMPLATES:
        count = sum(1 for t in TARGETS if IDENTITY_MAP.get(t["id"], (None,))[0] == pos)
        print(f"    {POSITION_TEMPLATES[pos]['label']}: {count} targets")

    ok = not missing_profiles and not missing_scripts
    print(f"\n{'=' * 60}")
    print(f"  AUDIT {'PASSED' if ok else 'FAILED'}")
    print(f"{'=' * 60}")
    return 0 if ok else 1


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="ALCHEMIZER — Identity Transmutation System for Application Materials"
    )
    parser.add_argument("--target", help="Generate for a single target ID")
    parser.add_argument("--position", choices=list(POSITION_TEMPLATES.keys()),
                        help="Generate for all targets with this primary position")
    parser.add_argument("--profiles-only", action="store_true",
                        help="Generate JSON profiles only (no submission scripts)")
    parser.add_argument("--audit", action="store_true",
                        help="Run coverage audit")
    args = parser.parse_args()

    if args.audit:
        sys.exit(run_audit())

    print("=" * 60)
    print("ALCHEMIZER — Identity Transmutation System")
    print("=" * 60)

    # Load sources
    metrics = load_covenant_metrics()
    print("\n  Source: covenant-ark")
    print(f"  Repos: {metrics['repos']} | Active: {metrics['active']} | "
          f"Essays: {metrics['essays']} | Sprints: {metrics['sprints']}")

    # Determine which targets to process
    if args.target:
        targets = [t for t in TARGETS if t["id"] == args.target]
        if not targets:
            print(f"\nERROR: Unknown target '{args.target}'", file=sys.stderr)
            print(f"Available: {', '.join(t['id'] for t in TARGETS)}", file=sys.stderr)
            sys.exit(1)
    elif args.position:
        targets = [t for t in TARGETS
                   if IDENTITY_MAP.get(t["id"], (None,))[0] == args.position]
    else:
        targets = TARGETS

    print(f"\n  Processing {len(targets)} targets...")

    # Create profiles directory
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)

    # Generate profiles
    all_profiles = []
    for target in targets:
        profile = generate_profile(target, metrics)
        all_profiles.append(profile)

        profile_path = PROFILES_DIR / f"{target['id']}.json"
        profile_path.write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n")
        print(f"  [PROFILE] {target['id']} → {pt_label(profile['primary_position'])}")

    # Generate index
    index = generate_index(all_profiles)
    # Compute category counts
    cats = {}
    for p in all_profiles:
        cats.setdefault(p["category"], []).append(p["target_id"])
    index["by_category"] = cats
    (PROFILES_DIR / "_index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    print(f"\n  [INDEX] _index.json ({len(all_profiles)} profiles)")

    # Generate submission scripts
    if not args.profiles_only:
        scripts_generated = 0
        for target in targets:
            tid = target["id"]
            if tid in EXISTING_SCRIPTS:
                continue
            if target["category"] == "Consulting":
                continue
            fname = SCRIPT_FILENAMES.get(tid)
            if not fname:
                continue

            profile = generate_profile(target, metrics)
            script = generate_submission_script(target, profile, metrics)
            script_path = SCRIPTS_DIR / fname
            script_path.write_text(script)
            scripts_generated += 1
            print(f"  [SCRIPT] {fname} → {pt_label(profile['primary_position'])}")

        print(f"\n  Generated {scripts_generated} new submission scripts")

    print(f"\n{'=' * 60}")
    print(f"  Profiles: {PROFILES_DIR}/")
    print(f"  Scripts: {SCRIPTS_DIR}/")
    print(f"{'=' * 60}")


def pt_label(position: str) -> str:
    """Get human-readable label for a position."""
    return POSITION_TEMPLATES.get(position, {}).get("label", position)


if __name__ == "__main__":
    main()
