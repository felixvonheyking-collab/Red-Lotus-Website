---
name: Red Lotus Asian Food
description: Premium asiatisches Catering & Kochkurse in Biberach & Ulm
colors:
  bg: "#1c1a17"
  bg-2: "#232019"
  red: "#c8382b"
  red-bright: "#e0473a"
  gold: "#d3b78c"
  gold-soft: "#bfa274"
  cream: "#f5f0e6"
  cream-dim: "#cdc6b8"
  line: "rgba(211,183,140,0.22)"
typography:
  display:
    fontFamily: "Cormorant Garamond, Georgia, serif"
    fontSize: "clamp(2.6rem, 5.4vw, 4.4rem)"
    fontWeight: 500
    lineHeight: 1.08
  headline:
    fontFamily: "Cormorant Garamond, Georgia, serif"
    fontSize: "clamp(2rem, 3.6vw, 2.8rem)"
    fontWeight: 500
  title:
    fontFamily: "Cormorant Garamond, Georgia, serif"
    fontSize: "1.15rem–1.5rem"
    fontWeight: 500
  label:
    fontFamily: "Bricolage Grotesque, sans-serif"
    fontSize: "0.7rem–0.78rem"
    fontWeight: 600
    letterSpacing: "0.32em"
  body:
    fontFamily: "Bricolage Grotesque, sans-serif"
    fontSize: "0.88rem–1.08rem"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  sm: "2px"
  full: "50%"
spacing:
  sm: "16px"
  md: "32px"
  lg: "64px"
  xl: "120px"
components:
  button-primary:
    backgroundColor: "{colors.red}"
    textColor: "{colors.cream}"
    rounded: "{rounded.sm}"
    padding: "16px 30px"
  button-primary-hover:
    backgroundColor: "{colors.red-bright}"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.cream}"
    rounded: "{rounded.sm}"
    padding: "16px 30px"
---

# Design System: Red Lotus Asian Food

## Overview

**Creative North Star: "The Candlelit Buffet"**

Red Lotus Asian Food reads like walking into a private evening event: near-black anthracite rooms, warm lantern-red and champagne-gold accents, and real photography doing the persuading instead of copy or iconography. The system is deliberately quiet — flat surfaces, hairline dividers, generous dark space — so that food and event photography stay the loudest thing on every screen. It exists to feel like a premium event caterer's own material, not a food-truck flyer: no bright primary colors, no playful iconography, no stock imagery. That louder, younger register belongs to the sibling site (Red Lotus Streetfood) and is an explicit anti-reference here.

Two typefaces carry the whole voice: an italic-capable serif for anything that needs warmth or occasion (headlines, the em-emphasis word in the hero), and a wide-tracked uppercase sans for anything structural (nav, labels, buttons, eyebrows). The pairing does the work that decoration would otherwise do.

**Key Characteristics:**
- Near-black backgrounds with warm cream text — always dark-mode, never a light section.
- Lantern-red as a rare, deliberate accent (primary CTAs, numerals, list markers) — not a background color.
- Full-bleed photography as the primary content, not decoration behind text.
- Hairline (1px, low-opacity gold) dividers instead of shadows or cards-on-white.
- Wide-tracked uppercase labels/eyebrows as the system's structural rhythm.

## Colors

A near-monochrome anthracite palette lit by exactly two warm accents; color is spent sparingly and always on purpose.

### Primary
- **Lotus Red** (`#c8382b`): the CTA and emphasis color — primary buttons, hero em-word, section numerals, list bullets (❊). Used sparingly; its rarity is the point.
- **Lotus Red Bright** (`#e0473a`): hover/active state for Lotus Red, never used at rest.

### Secondary
- **Champagne Gold** (`#d3b78c`): eyebrows, labels, dropdown/nav hover states, icon strokes, footer headings — the "structural" accent that marks navigation and metadata.
- **Gold Soft** (`#bfa274`): a muted variant of Champagne Gold used for outline-button borders and the proof section's city list — where gold needs to recede slightly.

### Neutral
- **Anthracite** (`#1c1a17`): the primary page background (`--bg`).
- **Anthracite Deep** (`#232019`): the secondary/panel background (`--bg-2`) — used for header dropdowns, the proof-text panel, catering path cards, footer, and mobile nav.
- **Warm Cream** (`#f5f0e6`): primary text color on dark backgrounds, and headline color.
- **Cream Dim** (`#cdc6b8`): secondary/body text color — paragraphs, nav links at rest, footer copy.
- **Hairline Gold** (`rgba(211,183,140,0.22)`): the system's only border/divider color, at low opacity — used for the 1px grid lines between value cards and catering cards, section dividers, and card borders.

### Named Rules
**The One Accent Rule.** Lotus Red never appears as a background or fill beyond buttons and small marks (numerals, bullets). If red starts covering more than a button or a few characters, it's being overused.

## Typography

**Display Font:** Cormorant Garamond (with Georgia, serif fallback)
**Body Font:** Bricolage Grotesque (with sans-serif fallback)

**Character:** A restrained, editorial pairing — the serif brings occasion and warmth to headlines (including an italic emphasis treatment), while the grotesque sans stays cool, wide-tracked, and structural everywhere else (navigation, labels, buttons). Neither font is decorative on its own; the contrast between them carries the personality.

### Hierarchy
- **Display** (weight 500, `clamp(2.6rem, 5.4vw, 4.4rem)`, line-height 1.08): hero h1 only. Uses an italicized `<em>` span in Lotus Red Bright for the one emphasized word per hero.
- **Headline** (weight 500, `clamp(2rem, 3.6vw, 2.8rem)`): section h2s (section-head, proof-text, kochkurs).
- **Title** (weight 500, `1.15–1.5rem`): card-level h3s (value cards, catering path cards).
- **Body** (weight 400, `0.88–1.08rem`, line-height 1.6): paragraph copy in Cream Dim.
- **Label** (weight 600, `0.7–0.78rem`, letter-spacing `0.08em–0.32em`, uppercase): eyebrows, nav links, buttons, footer column headings — always uppercase, always wide-tracked.

### Named Rules
**The Serif-Only-For-Headlines Rule.** Cormorant Garamond never appears in body copy, buttons, or labels — it is reserved entirely for h1/h2/h3. Everything structural or interactive stays in the sans.

## Layout

Content sits in two container widths: a `1180px` reading-width wrap (`.wrap`) for most sections, and a `1440px` wide wrap (`.wrap-wide`) for the gallery, where photography needs more room to breathe. Sections default to `120px` vertical padding on desktop, dropping to `80px` at the `960px` mobile breakpoint — the system's one breakpoint, below which multi-column grids (values, catering paths, gallery, proof, kochkurs, footer) collapse to one or two columns and the header switches from an inline nav to a slide-down mobile panel.

Grid sections (`.values`, `.paths`) use a distinctive "hairline grid" technique: a `1px` gap filled with the Hairline Gold border color, so cards appear to share thin dividers rather than sitting in boxes with margins. The proof section is an asymmetric two-column split (`0.9fr` text / `1.3fr` image) that becomes a stacked single column on mobile. The gallery is a fixed-height `3×2` (desktop) / `2×3` (mobile) photo grid, not a masonry — every tile crops to fill via `object-fit: cover`.

## Elevation & Depth

Flat by default — the system does not use box-shadows for cards, buttons, or panels; depth comes from background-color layering (Anthracite vs. Anthracite Deep) and the hairline grid technique, not from shadows. The two exceptions are functional, not decorative: the logo has a soft `drop-shadow` purely for legibility over photography, and the mobile nav panel gets a `box-shadow: 0 12px 24px rgba(0,0,0,0.4)` because it floats above page content and needs to visually separate from what's beneath it.

### Named Rules
**The Flat-By-Default Rule.** Surfaces are flat at rest. The only shadows in the system exist to solve a legibility or stacking-order problem (logo-over-photo, floating nav-over-content), never for generic "card" polish.

## Shapes

Almost square throughout — `2px` border-radius on buttons is the only rectangular rounding in the system (`--rounded: sm`). The one recurring circular shape is the icon-button: header social icons, footer social icons, and the mobile nav-toggle button are all perfect circles (`border-radius: 50%`) with a 1px hairline border. No card in the system uses a visible corner radius; cards are defined by background color and hairline dividers, not by rounded containers.

## Components

### Buttons
- **Shape:** Barely rounded (`2px` radius) — reads as squared-off, not soft.
- **Primary:** Lotus Red background, Cream text, `16px 30px` padding, uppercase label typography (`0.78rem`, `0.14em` tracking, weight 600).
- **Hover/Focus:** Primary shifts to Lotus Red Bright and lifts 1px (`translateY(-1px)`), `0.25s ease` transition.
- **Outline:** Transparent background, Gold Soft border, Cream text; hover brightens the border to full Gold and adds a faint gold background wash (`rgba(211,183,140,0.08)`).
- **Ghost:** Text-only link in Gold with a hairline bottom border (used for secondary CTAs like "Hier entlang für private Feiern").

### Cards / Containers
- **Corner Style:** None — square edges throughout.
- **Background:** Value cards and catering path cards sit on Anthracite (`--bg`) or Anthracite Deep (`--bg-2`) depending on section; separated from siblings by the 1px hairline-grid technique rather than individual borders.
- **Shadow Strategy:** None (see Elevation & Depth — flat by default).
- **Internal Padding:** Generous — `44px 32px` (value cards) to `54px 40px` (catering path cards).
- **Hover:** Catering path cards darken slightly on hover (`background: #26221c`) as the only card-level interactive feedback.

### Navigation
- **Desktop:** Inline uppercase label links (`0.72rem`, `0.14em` tracking) in Cream Dim, turning Gold on hover. The "Catering" item is a hover-triggered dropdown (Anthracite Deep panel, hairline border, no shadow) listing the three catering sub-pages.
- **Mobile (≤960px):** Desktop nav hides entirely; a circular hamburger toggle button reveals a full-width slide-down panel (`position: absolute`, opacity/transform transition, hardcoded `#1c1a17` background to avoid the header's gradient bleeding through) stacking every nav link full-width with hairline top borders between them.
- **Header behavior:** Fixed position, dark-to-transparent gradient background on desktop (so it can sit over the hero image), collapsing to a flat solid Anthracite bar on mobile.

### Icon Buttons (Signature Component)
Circular, 30–44px depending on context (header vs. footer vs. nav-toggle), 1px Hairline Gold border, Gold icon glyph, no fill at rest. Used identically for WhatsApp/Instagram/email in the header and footer, and for the mobile nav-toggle. This is the system's one consistently reused "chrome" component outside of buttons and cards.

## Do's and Don'ts

### Do:
- **Do** keep every background dark (Anthracite or Anthracite Deep) — there is no light-mode section anywhere in the system.
- **Do** spend Lotus Red only on CTAs, numerals, and small marks; let photography and Champagne Gold carry the rest of the warmth.
- **Do** use the hairline-grid technique (1px gap filled with `--line`) for any new multi-card grid instead of individual card borders or shadows.
- **Do** keep all structural/interactive text (nav, labels, buttons, eyebrows) in uppercase Bricolage Grotesque with wide letter-spacing.
- **Do** use real, on-brand event/food photography for any new image slot — never a placeholder that looks like stock art.

### Don't:
- **Don't** introduce a light background or a bright, saturated secondary color — that register belongs to the Streetfood sibling site, not this one.
- **Don't** add box-shadows to cards or buttons for generic "polish" — depth here comes from background layering, not shadows.
- **Don't** round corners beyond the established `2px` button radius or the circular icon-buttons; square-edged cards are intentional.
- **Don't** use the serif (Cormorant Garamond) outside headlines — it never appears in body copy, labels, or buttons.
- **Don't** use stock or AI-generated imagery anywhere on the site (a rejected trait of the previous Wix site) — every photo must be real Red Lotus event/food photography.
