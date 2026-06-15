# Accessibility Audit Report — March 2026

**Sprint 57: ACCESSIBILITAS**
**Date:** 2026-03-04
**Standard:** WCAG 2.1 Level AA
**Auditor:** AI-assisted (Claude Code) + source code review
**Method:** HTML fetch + source analysis of Astro/Jekyll templates, CSS, and client-side scripts

---

## Executive Summary

Two public-facing properties were audited against WCAG 2.1 AA success criteria. The portfolio site (Astro) demonstrates strong foundational accessibility — it has a skip link, `lang` attribute, semantic landmarks, keyboard-navigable dropdowns with ARIA states, `prefers-reduced-motion` support, and `focus-visible` outlines. However, several issues remain around canvas alternatives and contrast stacking. The public-process site (Jekyll) has critical structural gaps: no skip link, no focus styles, no ARIA landmarks, and missing semantic HTML wrappers. Neither site fully meets WCAG 2.1 AA.

| Site | Critical | Major | Minor | Overall |
|------|----------|-------|-------|---------|
| Portfolio (Astro) | 1 | 4 | 5 | **Partial Compliance** |
| Public Process (Jekyll) | 3 | 4 | 3 | **Non-Compliant** |

---

## Site 1: Portfolio (Astro)

**URL:** https://4444j99.github.io/portfolio/
**Subpage audited:** https://4444j99.github.io/portfolio/omega

### What the site does well

The portfolio site has solid accessibility foundations that many sites lack:

- `<html lang="en">` present on all pages (Layout.astro line 49)
- Skip-to-content link: `<a href="#main-content" class="skip-to-content">` (Layout.astro line 61)
- Semantic structure: `<header>`, `<nav aria-label="Main navigation">`, `<main id="main-content">`, `<footer>`, `<figure>`, `<figcaption>` all used correctly
- Navigation uses `aria-expanded`, `aria-haspopup`, `aria-controls`, `aria-current="page"` throughout (Header.astro lines 76-103)
- Mobile menu has focus trap with Tab wrapping (Header.astro lines 213-226)
- Keyboard navigation: Arrow keys, Home, End in dropdown menus (Header.astro lines 249-256)
- Escape key closes menus and dialogs (Header.astro lines 207-211, 273-283)
- Search dialog uses native `<dialog>` element with `aria-label="Site search"` (Search.astro line 19)
- All decorative SVGs have `aria-hidden="true"` (Header.astro lines 95, 132, 136)
- Flip cards use `inert` attribute to hide back-face content from screen readers (ProjectCard.astro line 35)
- SketchContainer provides `role="img"` or `role="group"`, `aria-label`, `<noscript>` fallback, and `<figcaption>` (SketchContainer.astro lines 39-71)
- `prefers-reduced-motion: reduce` disables flip card animation (ProjectCard.astro lines 498-502)
- Global `focus-visible` outline: `2px solid var(--accent-text)` (global.css line 489)
- All touch targets are minimum 44x44px (Header.astro lines 341, 484-486; Search.astro line 233)
- Theme toggle has dynamic `aria-label` explaining current state and next action (Footer.astro lines 236-240)
- Cmd+K keyboard shortcut for search (Search.astro line 82)

### CRITICAL

#### C-1: Canvas-based generative sketches lack text equivalents for complex content

**WCAG:** 1.1.1 Non-text Content (Level A)
**Location:** SketchContainer.astro, OmegaGalaxy.astro (omega page)

While `SketchContainer.astro` provides `role="img"` and `aria-label` for simple decorative sketches, the Omega page's interactive 3D galaxy visualization ("System Galaxy — 91 Repositories") renders complex data content in a `<canvas>` element. The galaxy shows 91 repository nodes with organ-color coding, interactive drag/zoom/click behavior, and detailed metadata on selection. This data is presented visually only — no accessible data table or text summary accompanies the visualization.

The `aria-label` on the container provides a name but not the data content. Screen reader users cannot access any of the 91 repository names, their organ groupings, or their status information.

**Remediation (P0):**
1. Add a visually-hidden data table below the galaxy canvas listing all repositories by organ, with columns for name, status, and organ. Use `class="sr-only"` or a disclosure widget.
2. Alternatively, add an `aria-describedby` region with a text summary: "Interactive galaxy showing 150 repositories across 8 organs. 4 graduated, 68 candidate, 12 public process."

---

### MAJOR

#### MJ-1: Repetitive link text on project cards — "View project" repeated 20+ times

**WCAG:** 2.4.4 Link Purpose (In Context) (Level A)
**Location:** ProjectCard.astro line 46

Every project card's back face contains `<a class="flip-card__cta">View project &rarr;</a>`. When a screen reader encounters these links out of context (e.g., in a links list), all 20+ links appear identical.

The link *is* within a context where the card title (h3) precedes it, so this may pass under 2.4.4 "in context" interpretation, but fails under 2.4.9 "Link Purpose (Link Only)" (Level AAA) and creates a poor screen reader experience.

**Remediation (P1):**
Add `aria-label` with the project name: `aria-label={`View project: ${title}`}`. This is a one-line template change.

#### MJ-2: Pagefind search input lacks explicit label

**WCAG:** 1.3.1 Info and Relationships / 3.3.2 Labels or Instructions (Level A)
**Location:** Search.astro line 21 (`#pagefind-container`)

The Pagefind UI library dynamically creates an `<input>` element inside `#pagefind-container`. This input does not have an associated `<label>` element or `aria-label`. The parent `<dialog>` has `aria-label="Site search"`, but the input itself lacks a direct label.

**Remediation (P1):**
After Pagefind initializes (Search.astro line 122-124), programmatically add `aria-label="Search the site"` to the generated input:
```js
var input = container.querySelector('input');
if (input) {
  input.setAttribute('aria-label', 'Search the site');
  input.focus();
}
```

#### MJ-3: Stacked opacity on secondary/muted text may fail contrast

**WCAG:** 1.4.3 Contrast (Minimum) (Level AA)
**Location:** global.css lines 25-26, SketchContainer.astro line 109

Dark theme: `--text-muted: rgba(255,255,255,0.75)` renders as approximately `#BFBFBF` on a pure black background. Against `--bg-card: rgba(0,0,0,0.65)` the effective contrast depends on the p5.js canvas behind it, which varies continuously. Worst-case (bright canvas colors bleeding through) could drop contrast below 4.5:1.

Additionally, `.sketch-caption` applies `opacity: 0.8` on top of `--text-secondary: rgba(255,255,255,0.9)`, stacking to an effective ~72% white. On the canvas background, this approaches the 4.5:1 threshold.

Light theme: `--text-muted: #6e6e71` on `#f5f5f0` background = contrast ratio of **3.7:1** — this **fails** the 4.5:1 AA requirement for normal text.

**Remediation (P1):**
1. Light theme: darken `--text-muted` from `#6e6e71` to `#595959` (5.0:1) or darker.
2. Remove `opacity: 0.8` from `.sketch-caption` — the CSS variable already provides the intended lightness.
3. Consider adding a solid fallback background behind text that overlays the dynamic canvas.

#### MJ-4: Placeholder link on omega page

**WCAG:** 2.4.4 Link Purpose (Level A)
**Location:** Omega scorecard page

The omega page contains a "View Intelligence" link with `href="#"` — a non-functional placeholder link. Screen readers will announce this as a link, but activating it does nothing useful.

**Remediation (P1):**
Either remove the link until the destination exists, or replace it with a `<span>` styled as a disabled link with `aria-disabled="true"`.

---

### MINOR

#### MN-1: Sketch controls are 32x32px, below 44px touch target minimum

**WCAG:** 2.5.8 Target Size (Minimum) (Level AA — new in 2.2, recommended in 2.1)
**Location:** SketchContainer.astro lines 147-148

`.sketch-ctrl` buttons (pause, fullscreen) are `width: 32px; height: 32px`. While WCAG 2.1 AA does not mandate 44px, WCAG 2.2 Level AA requires 24px minimum (these pass) and recommends 44px (these do not). Given the site's otherwise excellent 44px targets, these are inconsistent.

**Remediation (P2):** Increase `.sketch-ctrl` to `min-width: 44px; min-height: 44px`.

#### MN-2: RSS link on public-process has reduced opacity without clear purpose

**WCAG:** 1.4.3 Contrast (Level AA)
**Location:** Linked from portfolio footer to public-process

Not a portfolio issue per se, but the footer links to the public-process RSS feed. See public-process findings below.

#### MN-3: Heading hierarchy has minor inconsistencies on index page

**WCAG:** 1.3.1 Info and Relationships (Level A)
**Location:** HeroSection.astro, index.astro

The page uses h1 ("Engineering Creative Practice") followed by h2 ("AI Systems Architect", "System Pulse", "System Artifacts"), then h3 for organ groups and project titles. The structure is generally correct, but the jump from "System Artifacts — Start Here" (h2) to individual organ group headings (h3) within the same section is appropriate. No levels are skipped.

**Status:** Borderline pass. The heading structure is logical but dense. Consider adding `aria-label` to sections for landmark navigation.

#### MN-4: External link indicators are visual-only

**WCAG:** 1.3.1 Info and Relationships (Level A)
**Location:** Header.astro line 106

External links show a visual arrow `&#8599;` with `aria-hidden="true"`, which is correct — but screen reader users receive no indication that a link opens in a new tab. The `target="_blank"` and `rel="noopener noreferrer"` are present but not announced.

**Remediation (P3):** Add `<span class="sr-only">(opens in new tab)</span>` after external link labels.

#### MN-5: `<footer>` element not explicitly present

**WCAG:** 1.3.1 Info and Relationships (Level A)
**Location:** Footer.astro

The component renders `<footer class="footer">` — this is correct. The HTML5 `<footer>` element is present. No issue.

**Status:** Pass (initial WebFetch report was incorrect; source confirms correct usage).

---

### Portfolio Compliance Summary

| WCAG Criterion | Status | Notes |
|----------------|--------|-------|
| 1.1.1 Non-text Content | PARTIAL FAIL | Canvas galaxy lacks data alternative |
| 1.3.1 Info and Relationships | PASS | Semantic HTML, ARIA, headings all solid |
| 1.4.3 Contrast (Minimum) | PARTIAL FAIL | Light theme `--text-muted` below 4.5:1 |
| 1.4.11 Non-text Contrast | PASS | UI components have sufficient contrast |
| 2.1.1 Keyboard | PASS | Full keyboard navigation, focus trap, escape |
| 2.4.1 Bypass Blocks | PASS | Skip-to-content link present |
| 2.4.2 Page Titled | PASS | Dynamic titles on all pages |
| 2.4.3 Focus Order | PASS | Logical tab order, managed focus on flip |
| 2.4.4 Link Purpose | PARTIAL FAIL | "View project" repeated without context |
| 2.4.7 Focus Visible | PASS | `focus-visible` with 2px outline globally |
| 3.1.1 Language of Page | PASS | `<html lang="en">` |
| 3.3.2 Labels or Instructions | PARTIAL FAIL | Pagefind input lacks label |
| 4.1.2 Name, Role, Value | PASS | ARIA states on all interactive elements |

**Overall Assessment: Partial Compliance — 1 critical, 4 major issues. Fixable with moderate effort.**

---

## Site 2: Public Process (Jekyll)

**URL:** https://organvm-v-logos.github.io/public-process/
**Subpage audited:** /public-process/categories/ (the /essays/ path returned 404)

### What the site does well

- `<html lang="en">` present (default.html line 2)
- `<title>` with page-specific prefix (default.html line 6)
- `<meta name="viewport">` present (default.html line 5)
- `<main class="site-content">` wrapping page content (default.html line 28)
- Essay layout includes prev/next navigation with directional labels (essay.html lines 39-52)
- All external links in footer have descriptive text
- Links are all text-based — no icon-only links
- RSS feed provided via `{% feed_meta %}`
- Good color choices for primary content: `#c9d1d9` on `#0d1117` = ~10.5:1 contrast ratio (excellent)
- Heading colors: `#e6edf3` on `#0d1117` = ~13.5:1 (excellent)
- Link color: `#58a6ff` on `#0d1117` = ~5.8:1 (passes AA)

### CRITICAL

#### C-1: No skip navigation link

**WCAG:** 2.4.1 Bypass Blocks (Level A)
**Location:** _layouts/default.html, _includes/header.html

There is no skip link anywhere in the page. The header contains 9 navigation links that must be tabbed through to reach content on every page load. This is a Level A failure — the most basic keyboard accessibility requirement.

**Remediation (P0):**
Add before the header in `default.html`:
```html
<a href="#main-content" class="skip-to-content">Skip to content</a>
```
Add `id="main-content"` to the `<main>` element. Add CSS:
```css
.skip-to-content {
  position: absolute;
  left: -9999px;
  z-index: 999;
  background: var(--accent);
  color: var(--bg);
  padding: 0.5rem 1rem;
  font-weight: 600;
  text-decoration: none;
}
.skip-to-content:focus {
  left: 1rem;
  top: 0.5rem;
}
```

#### C-2: No focus styles defined

**WCAG:** 2.4.7 Focus Visible (Level AA)
**Location:** assets/css/style.css

The entire stylesheet contains zero `:focus` or `:focus-visible` rules. Keyboard users relying on browser default focus indicators get inconsistent (and in some browsers, nearly invisible) outlines on dark backgrounds. On the `#0d1117` background, Chrome's default blue outline may be barely visible.

**Remediation (P0):**
Add global focus styles to style.css:
```css
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

a:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
  border-radius: 2px;
}
```

#### C-3: Navigation lacks `aria-label` and semantic landmark signaling

**WCAG:** 1.3.1 Info and Relationships (Level A), 4.1.2 Name, Role, Value (Level A)
**Location:** _includes/header.html

The `<nav class="site-nav">` element has no `aria-label`. When a page has multiple `<nav>` elements (some pages may via essay prev/next), screen readers cannot distinguish between them. The `<header>` and `<footer>` HTML5 elements are present, which is good, but they lack any ARIA enhancement for complex navigation.

More critically: the header navigation has no mobile menu toggle or hamburger button. On narrow viewports, the nav links simply wrap, potentially creating a wall of links. There is no `aria-expanded`, no toggle mechanism, and no way to collapse the navigation.

**Remediation (P0):**
1. Add `aria-label="Main navigation"` to `<nav class="site-nav">`.
2. Add `aria-label="Previous and next essays"` to the essay prev/next `<nav class="essay-nav">`.
3. Consider adding a mobile hamburger toggle for viewports under 768px.

---

### MAJOR

#### MJ-1: Blockquote text uses muted color with reduced contrast

**WCAG:** 1.4.3 Contrast (Minimum) (Level AA)
**Location:** assets/css/style.css line 98

`blockquote { color: var(--muted); }` where `--muted: #8b949e` on `--bg: #0d1117`. Contrast ratio = **4.0:1** — fails the 4.5:1 minimum for normal text. Blockquotes are used extensively in essays for pull-quotes and cited material.

**Remediation (P1):**
Change blockquote color to `var(--fg)` (`#c9d1d9`, ~10.5:1 contrast) or at minimum `#9ca3ab` (4.6:1).

#### MJ-2: Footer text uses muted color with insufficient contrast for some elements

**WCAG:** 1.4.3 Contrast (Minimum) (Level AA)
**Location:** assets/css/style.css line 179-182

`.footer-inner { color: var(--muted); font-size: 0.85em; }` — the `#8b949e` muted color at 0.85em size fails the 4.5:1 ratio for small text. The separator spans use `color: var(--border)` which is `#30363d` on `#0d1117` = **1.6:1** — extremely low contrast, though these are decorative.

**Remediation (P1):**
Darken footer text to `#9ca3ab` or lighter. Ensure separators remain clearly decorative with `aria-hidden="true"` (they currently lack this).

#### MJ-3: RSS link has opacity:0.7 reducing already-marginal contrast

**WCAG:** 1.4.3 Contrast (Minimum) (Level AA)
**Location:** assets/css/style.css lines 160-162

`.rss-link { opacity: 0.7; }` applied to a link with color `var(--accent)` (`#58a6ff`). At 70% opacity on `#0d1117`, the effective color is approximately `#3d74b2`, giving a contrast ratio of ~3.6:1 — fails AA.

**Remediation (P1):**
Remove the opacity reduction or use a darker explicit color that maintains 4.5:1 contrast.

#### MJ-4: No `<article>` elements wrapping essay content on index page

**WCAG:** 1.3.1 Info and Relationships (Level A)
**Location:** index.md, _layouts/default.html

The homepage lists essays as plain heading + link pairs without `<article>` wrappers. Screen readers cannot identify individual essay entries as distinct content units. The essay layout (essay.html) does use `<article>`, which is correct for individual essay pages.

**Remediation (P1):**
Wrap each essay listing on the index page in `<article>` elements.

---

### MINOR

#### MN-1: Meta/date information lacks semantic time element

**WCAG:** 1.3.1 Info and Relationships (Level A)
**Location:** _layouts/essay.html line 7

Dates are rendered as plain `<span>` text. Using `<time datetime="2026-02-04">February 04, 2026</time>` would provide machine-readable date information.

**Remediation (P3):**
Replace `<span>{{ page.date | date: "%B %d, %Y" }}</span>` with `<time datetime="{{ page.date | date_to_xmlschema }}">{{ page.date | date: "%B %d, %Y" }}</time>`.

#### MN-2: Tag count elements lack context for screen readers

**WCAG:** 1.3.1 Info and Relationships (Level A)
**Location:** Categories and tags pages

Category headings display as "meta-system (21)" where the count is in a span. Screen readers will read this correctly, but `aria-label="meta-system: 21 essays"` would provide clearer context.

**Remediation (P3):** Add descriptive `aria-label` to category headings.

#### MN-3: Footer separator spans lack `aria-hidden`

**WCAG:** 1.3.1 Info and Relationships (Level A)
**Location:** _includes/footer.html lines 6, 8, 10

The `<span class="separator">&middot;</span>` elements are decorative but will be read by screen readers as "middle dot". The portfolio site correctly uses `aria-hidden="true"` on similar separators.

**Remediation (P2):**
Add `aria-hidden="true"` to separator spans:
```html
<span class="separator" aria-hidden="true">&middot;</span>
```

---

### Public Process Compliance Summary

| WCAG Criterion | Status | Notes |
|----------------|--------|-------|
| 1.1.1 Non-text Content | PASS | No images present; text-only site |
| 1.3.1 Info and Relationships | FAIL | No article wrappers, nav lacks label |
| 1.4.3 Contrast (Minimum) | FAIL | Blockquotes, footer, RSS link below 4.5:1 |
| 1.4.11 Non-text Contrast | PASS | Borders and UI elements sufficient |
| 2.1.1 Keyboard | PARTIAL PASS | All links keyboard-accessible, no traps |
| 2.4.1 Bypass Blocks | FAIL | No skip link |
| 2.4.2 Page Titled | PASS | Dynamic titles present |
| 2.4.3 Focus Order | PASS | Source order is logical |
| 2.4.4 Link Purpose | PASS | All links have descriptive text |
| 2.4.7 Focus Visible | FAIL | No focus styles defined |
| 3.1.1 Language of Page | PASS | `<html lang="en">` present |
| 3.3.2 Labels or Instructions | N/A | No forms |
| 4.1.2 Name, Role, Value | FAIL | Nav missing aria-label |

**Overall Assessment: Non-Compliant — 3 critical, 4 major issues. Most are straightforward CSS/HTML fixes.**

---

## Prioritized Remediation Roadmap

### Priority 0 — Must Fix (blocks WCAG 2.1 A compliance)

| ID | Site | Fix | Effort |
|----|------|-----|--------|
| PP-C-1 | Public Process | Add skip-to-content link | 15 min |
| PP-C-2 | Public Process | Add `:focus-visible` styles | 15 min |
| PP-C-3 | Public Process | Add `aria-label` to nav elements | 10 min |

### Priority 1 — Should Fix (blocks WCAG 2.1 AA compliance)

| ID | Site | Fix | Effort |
|----|------|-----|--------|
| PF-C-1 | Portfolio | Canvas galaxy accessible data table | 2 hrs |
| PF-MJ-3 | Portfolio | Fix light theme `--text-muted` contrast | 15 min |
| PF-MJ-2 | Portfolio | Label Pagefind search input | 10 min |
| PF-MJ-1 | Portfolio | Add project name to "View project" links | 10 min |
| PF-MJ-4 | Portfolio | Remove or fix placeholder `#` link | 5 min |
| PP-MJ-1 | Public Process | Fix blockquote contrast | 5 min |
| PP-MJ-2 | Public Process | Fix footer text contrast | 10 min |
| PP-MJ-3 | Public Process | Fix RSS link contrast | 5 min |
| PP-MJ-4 | Public Process | Add `<article>` wrappers on index | 30 min |

### Priority 2 — Nice to Have (improves experience)

| ID | Site | Fix | Effort |
|----|------|-----|--------|
| PF-MN-1 | Portfolio | Increase sketch control buttons to 44px | 5 min |
| PF-MN-4 | Portfolio | Add "(opens in new tab)" to external links | 10 min |
| PP-MN-3 | Public Process | Add `aria-hidden` to footer separators | 5 min |

### Priority 3 — Enhancement

| ID | Site | Fix | Effort |
|----|------|-----|--------|
| PP-MN-1 | Public Process | Use `<time>` elements for dates | 15 min |
| PP-MN-2 | Public Process | Add context to tag counts | 15 min |
| PF-MN-3 | Portfolio | Add `aria-label` to page sections | 20 min |

**Total estimated remediation effort: ~4-5 hours**

---

## Methodology Notes

- **Source analysis:** Astro and Jekyll templates were read directly from the local workspace to verify exact HTML output, ARIA attributes, and CSS values. This is more reliable than live-page inference.
- **Color contrast:** Ratios were calculated using the WCAG relative luminance formula against the declared CSS color values. Dynamic backgrounds (p5.js canvas) introduce variability that cannot be statically measured — worst-case estimates were used.
- **Keyboard testing:** Inferred from source code analysis of event listeners, `tabindex` attributes, `inert` usage, and focus management scripts. Manual keyboard testing is recommended to verify.
- **Screen reader testing:** Not performed. Automated source analysis cannot catch all screen reader interaction patterns. Manual testing with VoiceOver (macOS) is recommended as a follow-up.
- **Pages audited:** 4 total (2 per site). Additional pages share the same layouts and would inherit the same issues.

---

## Recommendations for Future Audits

1. **Integrate axe-core or Lighthouse CI** into the portfolio's Astro build pipeline and the public-process Jekyll build. Both can catch ~60% of WCAG issues automatically.
2. **Manual keyboard walkthrough** with Tab, Shift+Tab, Enter, Space, Escape on each page type — takes 10 minutes per page.
3. **VoiceOver testing** on macOS Safari for both sites — tests actual screen reader experience.
4. **Re-audit after remediation** to confirm fixes and check for regressions.
5. **ORGAN-III product accessibility** should be audited when products ship (per sprint catalog scope).
