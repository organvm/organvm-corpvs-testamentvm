# Talk Proposal: The AI-Conductor Model

## Title

**The AI-Conductor Model: Building Institutional-Scale Systems Solo**

## Target Venues

- Strange Loop (St. Louis) — technology conference, systems-thinking audience
- XOXO (Portland) — independent creators, art+tech intersection
- Processing Community Day — creative coding, educational tools
- Local meetups: Creative Coding NYC, Papers We Love

## Abstract (200 words)

What happens when you treat an AI not as a replacement for a developer, but as an orchestra responding to a conductor? In nine days, I built a 113-repository system spanning 8 organizations — 739K+ words of documentation, 49 published essays, 33+ sprints — as a solo operator directing AI generation with human strategic judgment.

This talk introduces the AI-conductor methodology: a structured approach where the human sets direction, defines quality gates, and reviews output, while the AI generates volume at institutional scale. I'll cover the token-based effort model (measuring work in TE, not hours), the quality risks specific to AI-generated content (hallucinated code examples, generic phrasing, incorrect cross-references), and the governance structures that make it work (registries, state machines, dependency graphs).

This is not a talk about prompt engineering. It is a talk about organizational design — how one person can operate a system that would normally require a team, by treating AI as infrastructure rather than intelligence. I'll share the actual decision records, the failures, and the metrics from 33 sprints of sustained operation.

## Outline (30-minute talk)

### 1. The Problem (5 min)
- Solo operators face institutional-scale demands: documentation, governance, distribution
- Traditional approach: "just hire someone" is not always an option
- The gap between what one person can write and what a system needs

### 2. The Model (8 min)
- Human as conductor, AI as orchestra
- The three phases: direct, generate, review
- Token-based effort model (TE budgets instead of hours)
- Live example: generating a 3,000-word README in 15 minutes of human review time

### 3. The Governance Layer (7 min)
- Why volume without governance creates chaos
- Registry-as-JSON: single source of truth for 149 registry entries
- Unidirectional dependency flow (DAG enforcement)
- Promotion state machine: when work becomes visible

### 4. The Failure Modes (5 min)
- Hallucinated code examples in AI-generated documentation
- Generic phrasing that makes every README sound the same
- Future-dated essays (VERITAS sprint discovery)
- Billing overruns from automated workflows (48,880 minutes)

### 5. The Evidence (5 min)
- 33+ sprints completed, 149 registry entries documented
- 32-day soak test COMPLETE (autonomous operation verified)
- Distribution pipeline: essays auto-deploy to social channels
- What "done" looks like: omega criteria and exit conditions

## Speaker Bio

@4444j99 designed the organvm eight-organ system — a 113-repository institutional system coordinated across 8 GitHub organizations, built solo using AI-conductor methodology. 33+ sprints, 739K+ words, 104 CI/CD workflows, 4,015+ automated tests. MFA. Based in New York City.

## Technical Requirements

- Screen sharing / HDMI output for slides
- Audio not required (no demos with sound)
- Ideal format: 30 min talk + 10 min Q&A
- Can be adapted to: lightning talk (10 min), workshop (90 min)
