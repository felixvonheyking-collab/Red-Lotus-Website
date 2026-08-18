---
target: gesamte Website (12 Seiten)
total_score: 29
max_score: 36
na_heuristics: 7
p0_count: 1
p1_count: 3
timestamp: 2026-08-18T12-36-21Z
slug: gesamte-website-12-seiten
---
Method: dual-agent (A: a1d9644025c4dfb96 · B: a96658e49e1991a68)

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 2 | All 4 lead forms show an unconditional "Danke!" success message on `mailto:` submit, even with no mail client configured — a false-positive success state |
| 2 | Match System / Real World | 4 | Real market days/times/locations, regional tone, informal ihr/euch throughout |
| 3 | User Control and Freedom | 3 | Solid breadcrumbs/home links; gallery links dead-end to bare image files, no lightbox |
| 4 | Consistency and Standards | 3 | Three verified drift instances (nav gap, form/input background pairing, section-head spacing) — see synthesis below |
| 5 | Error Prevention | 3 | Native browser validation only; no confirmation before the mailto app-switch |
| 6 | Recognition Rather Than Recall | 4 | Persistent nav with active state, breadcrumbs on every subpage |
| 7 | Flexibility and Efficiency | n/a | One-time-conversion marketing site has no meaningful expert/repeat-user acceleration surface |
| 8 | Aesthetic and Minimalist Design | 4 | Strongest heuristic — disciplined, restrained, matches DESIGN.md exactly |
| 9 | Error Recovery | 2 | No styled error states anywhere; compounds the mailto false-success problem |
| 10 | Help and Documentation | 4 | FAQ's Veranstalter power/water/footprint spec table is genuinely excellent anticipatory documentation |
| **Total** | | **29/36** | **Good (80.6%)** |

## Design Specificity Verdict

**LLM assessment:** Authored for this specific business, not a swappable dark-mode food template. Real market days/times, a real Impressum (address, tax number, insurer), named founders with defined roles, truck nicknames, exact CEE power specs and footprint per truck, real named 5-star reviews with unpolished German phrasing, a consistent "seit Sommer 2022" origin thread. The one place generic-template energy creeps in: header/footer social icons are plain Unicode glyphs, OS/font-dependent.

**Deterministic scan:** The CLI detector (`detect.mjs --json`, regex-fallback mode — the tool's own htmlparser2/css-select/css-tree/domutils modules are unavailable, so it explicitly warns findings are an undercount) returned 218 advisory findings across all 12 files: 200 `design-system-font-size`, 18 `design-system-color`. Cross-checking against DESIGN.md's source shows most of this is noise, not real drift: DESIGN.md's frontmatter (which the detector parses) is missing a documented "Title" typography role (1.15–1.5rem) and hardcodes label/body to single values where the prose describes them as ranges (0.7–0.78rem, 0.88–1.08rem) — so values like `.value-card h3{font-size:1.15rem}` and `.btn{font-size:0.78rem}` get flagged despite matching the system's own documented intent. Of the 18 color findings, the `rgba(0,0,0,0.4)` mobile-nav shadow is explicitly named in DESIGN.md's prose as one of only two intentional shadow exceptions (false positive); the `rgba(20,17,14,0.5/0.6)` hero-overlay tints are a defensible, consistent convention just not listed in the frontmatter's color table. **Net finding: the 218-count headline number overstates the problem by roughly two orders of magnitude — DESIGN.md's frontmatter needs to catch up to its own prose, not the site's CSS.**

The real consistency issues are the three Assessment A found by direct code diffing across all 12 pages, not the detector's output: `nav{gap:34px}` on 10 pages vs `gap:28px` on faq.html/aktuelles.html; form-section/input background pairing inverted on kochkurse.html relative to the three catering pages; and `.section-head{margin-bottom}` drifting across four different values (48/56/60/64px) for one repeated component.

**Visual overlays:** Not available this run — the Claude in Chrome extension isn't connected (checked twice), so no live rendering/screenshot evidence could be gathered. This is a genuine tool-availability gap, not a skipped step; findings below rest on direct source reading, not rendered inspection.

## Overall Impression

This is a well-executed, specific piece of work — the "Candlelit Buffet" system is followed with real discipline and the content is unmistakably this business, not a template. The biggest opportunity isn't visual polish (the aesthetic is already the strongest-scoring heuristic); it's that the site's actual conversion mechanism — four `mailto:`-only forms with an unconditional success message — has no way to know whether an inquiry ever reached anyone, which undermines the one metric PRODUCT.md defines as success.

## What's Working

1. **The 4-step "Ablauf" process module**, repeated across all three catering pages plus Kochkurse with genuinely different, segment-appropriate language (Hochzeiten: "Menüverkostung"; Firmenevents: "Planungsgespräch") rather than templated filler.
2. **The FAQ Veranstalter spec table** (exact amperage, footprint, water requirements per truck), cross-linked from every catering form. Content a generic template could not produce.
3. **Real, named, imperfectly-phrased Google reviews with schema.org markup** — reads as authentic evidence rather than marketing copy; the site's strongest trust moment.

## Priority Issues

**[P0] Mailto-only forms produce a false-positive success state**
Why it matters: All 4 lead forms (Firmenevents, Hochzeiten, Private Feiern, Kochkurs) build a `mailto:` link and immediately show "Danke!" regardless of whether the visitor's device has a mail client configured. PRODUCT.md defines success as inquiry volume through these exact forms — on any device without a configured mail client, the inquiry is silently lost while both sides believe it succeeded.
Fix: Replace/supplement mailto with a real submission endpoint (the planned Firebase `website`-adjacent collection, or a lightweight form service); if mailto stays, detect likely failure and offer an explicit WhatsApp/copy-to-clipboard fallback inside the same confirmation state.
Suggested command: `/impeccable harden`

**[P1] `catering-hochzeiten.html` has no wedding-specific reassurance**
Why it matters: The highest-stakes, highest-budget purchase on the site shows only food-only photography and zero wedding-specific testimonials or stats — the thinnest trust page on the site, at the exact page where PRODUCT.md says this audience needs the most reassurance.
Fix: Add a wedding-specific proof element (adapted testimonial or "X Hochzeiten begleitet seit 2022") near `#referenz`/`#anfrage`; pull in a wedding-filtered version of the review block.
Suggested command: `/impeccable shape`

**[P1] Keyboard-focus dropdown bug, identical on all 12 pages**
Why it matters: The "Catering ▾" nav dropdown only reveals on `:hover` with no `:focus-within` equivalent, so keyboard-only users can Tab onto invisible, `opacity:0` menu links they can't see are focused — a real interaction break for keyboard/screen-reader users, not just a polish gap, present sitewide since the header markup is shared.
Fix: Add `:focus-within` alongside `:hover` on `.nav-dropdown`, and strengthen `.field input:focus` beyond a 1px border shift (currently no glow/box-shadow, borderline against WCAG 2.4.7 visible-focus expectations) across all 4 forms.
Suggested command: `/impeccable harden`

**[P1] Verified cross-page style drift (nav gap, form/input background pairing, section-head spacing)**
Why it matters: Confirmed by direct code diff, not detector noise (see Design Specificity Verdict) — three concrete inconsistencies a repeat visitor would perceive as the header/forms/sections subtly "jumping" between pages, since each page repeats its own inline `<style>` block with no shared source of truth.
Fix: Extract nav gap, the form-section/input background pair, and the section-head spacing scale into one canonical reference; diff each page against it. While in there, update DESIGN.md's frontmatter to include the "Title" typography role and the label/body ranges already documented in its own prose, so the next detector run isn't 99% noise.
Suggested command: `/impeccable polish`

**[P2] `foodtruck-paew.jpg` reused across two structurally incompatible aspect ratios**
Why it matters: The same portrait-oriented photo of Pearl sits in a narrow 0.9fr column on foodtruck.html `#am-truck` (a good fit) and gets forced into a wider ~1.3fr, more landscape-shaped column on ueber-uns.html `#story` — the About page, the page most responsible for building trust in the two founders. Not a systemic layout flaw (the split module itself is legitimate and already correctly patched once, on `#live-cooking`) — a single asset/crop-matching problem.
Fix: Source or crop an alternate landscape-oriented frame for the `ueber-uns.html #story` wide column rather than relying on `object-fit:cover` to reconcile two different ratios from one portrait source.
Suggested command: `/impeccable layout`

**[P2] Gallery links dead-end to bare image files instead of an in-page lightbox**
Why it matters: foodtruck.html, kochkurse.html, and galerie.html all wrap gallery images in plain `<a href="img/xxx.jpg">`, fully exiting the styled site to a chrome-less browser image view at the exact moment a visitor is engaging deepest with a photo — undercutting "photography does the persuading."
Fix: A minimal `<dialog>`-based lightbox keeps photo engagement inside the branded experience.
Suggested command: `/impeccable polish`

**[P3] Homepage hero front-loads 3 competing CTAs before any trust content**
Why it matters: Firmenevents (primary), Hochzeiten (outline), and private Feiern (text link) all compete before the visitor has seen the proof section/reviews further down — a small but real cognitive-load add at the first decision point.
Fix: Defer the 3-way segmentation to where it already exists further down the page; give the hero one lower-commitment primary action.
Suggested command: `/impeccable layout`

**[P3] No styled error states; weak focus indicators sitewide**
Why it matters: Native browser validation bubbles would look visually jarring against the fully custom anthracite/serif system — the one place native browser chrome would visibly break the visual language — and compounds the P1 keyboard-focus issue above.
Fix: Style form validation states to match the system (gold/red accent, not browser default); add a visible focus ring beyond the current 1px border shift.
Suggested command: `/impeccable harden`

## Persona Red Flags

**Jordan (confused first-timer, lands on `catering-hochzeiten.html`)**: Sees a food-only hero with no people, no wedding atmosphere, reaches `#referenz` — still no third-party validation before the form. Fills the 8-field form; if on a device with no default mail app, sees "Danke!" and believes contact was made while the business receives nothing (this is the P0, landing directly on the exact persona the page is built for). No pricing signal anywhere means Jordan invests full form-fill effort with zero cost-anchoring first.

**Riley (stress-tester)**: Clicks a gallery photo on foodtruck.html → dumped onto a bare image file with no nav (P2). Tabs through the header via keyboard and lands on invisible Catering-dropdown links (P1). Notes `.field input:focus` only shifts border color 1px, no glow — a weak focus indicator on every input, sitewide.

**Casey (distracted mobile user, wants this week's market location)**: On a phone, the hero is `min-height:100vh`, so on a short mobile viewport with browser chrome Casey scrolls 1.5–2 screen-heights before reaching the market-strip — working against PRODUCT.md's own principle that market location "must be easy to find on the homepage, not buried." No longer buried in an FAQ (a real improvement over the old Wix site) but still buried below a full-viewport hero on mobile. The market-strip lists all 3 days with no "today" highlighting, so Casey has to manually cross-reference the current weekday.

## Minor Observations

- `catering-hochzeiten.html`, `catering-private-feiern.html`, faq/galerie/aktuelles/impressum/datenschutz all fall back to `og-default.jpg` for social sharing, while firmenevents/kochkurse/foodtruck/ueber-uns got dedicated OG images — odd that the wedding page, arguably highest-value, didn't get its own.
- Homepage's Kochkurs teaser CTA links to `kochkurse.html` (hero) rather than `kochkurse.html#anfrage`, adding an avoidable extra scroll for a visitor who already expressed form-filling intent.
- The Firebase-backed Speiseplan on aktuelles.html degrades gracefully and silently to the static placeholder on any fetch failure — good defensive engineering.
- The custom-built `.g-badge` "G" review-source mark is a nice example of the "no stock icons" rule done properly, in contrast to the plain Unicode social glyphs (✆ ◎ ✉) elsewhere.
- DESIGN.md documentation gap (see Design Specificity Verdict) is worth fixing on its own merits even outside the detector-noise angle — a Title role and label/body ranges belong in the frontmatter, not just the prose.

## Questions to Consider

1. If weddings are the highest-margin, highest-stakes conversion on the site, is the missing wedding-specific proof a photography-supply gap (per PRODUCT.md's own acknowledged gap in guest/event photos) or a site-structure oversight independent of having more photos?
2. The entire conversion mechanism is a client-side mailto hand-off with an unconditional success message — has anyone checked how many submissions have been silently lost on devices with no configured mail client since the site's been live?
3. Now that two independent assessments found real drift purely by diffing 12 independently-authored `<style>` blocks, is manual copy-paste discipline still viable, or does the next iteration need one canonical token file every page is checked against?
