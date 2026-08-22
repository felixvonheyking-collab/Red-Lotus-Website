---
name: Red Lotus Asian Food
description: Premium asiatisches Catering & Kochkurse in Biberach & Ulm
colors:
  bg: "#131110"
  bg-2: "#1e1a16"
  bg-3: "#242019"
  red: "#c8382b"
  red-bright: "#e0473a"
  gold: "#d3b78c"
  gold-soft: "#bfa274"
  cream: "#f5f0e6"
  cream-dim: "#c9c2b4"
  scrollbar-thumb: "#3a322a"
  line: "rgba(211,183,140,0.16)"
  glass: "rgba(245,240,230,0.07)"
  glass-line: "rgba(245,240,230,0.16)"
  # Halbtransparente Werte: Scrims verdunkeln Fotos für Textlesbarkeit
  # (Verläufe 0.06–0.94 über rgba(19,17,16,ALPHA)); Glass-Flächen liegen
  # mit backdrop-blur über Fotos oder dem Canvas.
typography:
  display:
    fontFamily: "Cormorant Garamond, Georgia, serif"
    fontSize: "clamp(2.9rem, 6.4vw, 5.6rem)"
    fontWeight: 400
    lineHeight: 1.02
  headline:
    fontFamily: "Cormorant Garamond, Georgia, serif"
    fontSize: "clamp(2.1rem, 3.9vw, 3rem)"
    fontWeight: 400
  title:
    fontFamily: "Cormorant Garamond, Georgia, serif"
    fontSize: "1.2rem–1.7rem"
    fontWeight: 400
  em-accent:
    fontFamily: "Cormorant Garamond, Georgia, serif"
    fontStyle: italic
    fontWeight: 500
    color: "{colors.red-bright}"
  label:
    fontFamily: "Bricolage Grotesque, sans-serif"
    fontSize: "0.6rem–0.78rem"
    fontWeight: 600
    letterSpacing: "0.22em"
  body:
    fontFamily: "Bricolage Grotesque, sans-serif"
    fontSize: "0.88rem–1.08rem"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  focus: "4px"
  scrollbar: "5px"
  card: "10px"
  img: "10px"
  menu: "14px"
  pill: "999px"
  full: "50%"
spacing:
  sm: "18px"
  md: "32px"
  lg: "64px"
  xl: "120px"
components:
  button-primary:
    backgroundColor: "{colors.red}"
    textColor: "{colors.cream}"
    rounded: "{rounded.pill}"
    padding: "16px 32px"
    shadow: "0 4px 20px rgba(0,0,0,0.35)"
  button-primary-hover:
    backgroundColor: "{colors.red-bright}"
  button-outline:
    backgroundColor: "transparent"
    borderColor: "rgba(245,240,230,0.35)"
    textColor: "{colors.cream}"
    rounded: "{rounded.pill}"
    padding: "16px 32px"
  chip:
    backgroundColor: "{colors.glass}"
    borderColor: "{colors.glass-line}"
    textColor: "{colors.gold}"
    rounded: "{rounded.pill}"
    padding: "8px 18px"
    effect: "backdrop-blur(14px) saturate(1.3), inset 0 1px 0 rgba(245,240,230,0.08)"
---

# Design System: Red Lotus Asian Food

## Overview

**Creative North Star: „Der private Vorführraum" (The Private Screening)**

Redesign vom 22.08.2026 (Referenz: Sequel „Private screening after dark", styles.refero.design; von Felix gewählt). Die Seite liest sich wie ein privater Vorführraum nach Einbruch der Dunkelheit: Das Foto ist die Bühne — der Hero füllt den kompletten ersten Bildschirm und wird nur so weit abgedunkelt, wie der Text es braucht. Ein tieferes Warmschwarz als zuvor bildet den Saal, eine einzige ruhige Flächen-Stufe darüber trägt Karten und Panels. Lotus-Rot bleibt der einzige gefüllte Akzent (CTA-Pille, kursives Akzentwort, Heute-Markierung), Champagner-Gold ist die Meta-Ebene (Chips, Labels, Hairlines, Icons). Der frühere „lautere" Anteil — kantige 2px-Buttons, Hairline-Grid-Raster, nackte Eyebrow-Zeilen — ist Pillen, weichen 10px-Karten und Frosted-Glass-Chips gewichen.

**Key Characteristics:**
- Fotografie zuerst: Vollbild-Hero und Vollbild-Referenzband („Kinoband") mit Text **im** Bild, unten links, über einem Verlaufs-Scrim.
- Ein kursives Serif-Wort in Lotus-Rot-Bright pro wichtiger Headline — die typografische Signatur (`<em>` in h1/h2).
- Frosted-Glass-Chips (Pille, Blur, Gold-Text) für alle kleinen Info-Etiketten — nie nackte Label-Zeilen über Überschriften.
- Karten sind stille Flächen: bg-2 auf bg, 10px Radius, kein Rand, kein Schatten; Hover hebt minimal (translateY -3/-4px) und hellt zur bg-3 auf.
- Orchestrierte, abschaltbare Bewegung: Hero-Auftritt (Zeilen steigen, Ken-Burns-Zoom), Scroll-Reveal gestaffelt, Parallax-Drift auf Galerie-/Kinoband-Fotos, Zähl-Chip und Sternen-Sweep bei den Bewertungen.

## Colors

- **Lotus Red** (`#c8382b`): einziger gefüllter Akzent — Primär-CTA-Pille, Heute-Linie der Wochenkarte. **Lotus Red Bright** (`#e0473a`): Hover des CTAs und Farbe des kursiven Akzentworts.
- **Champagne Gold** (`#d3b78c`) / **Gold Soft** (`#bfa274`): Chips, Labels, Icon-Strokes, Footer-Spaltentitel, Sterne, Meta-Angaben.
- **Anthrazit-Nacht** (`#131110`): Canvas. **Fläche** (`#1e1a16`, `--bg-2`): Karten, Panels, Footer, Markt-Zeile. **Fläche hell** (`#242019`, `--bg-3`): Hover-Zustand von Karten.
- **Warm Cream** (`#f5f0e6`): Primärtext/Headlines. **Cream Dim** (`#c9c2b4`): Fließtext.
- **Hairline Gold** (`rgba(211,183,140,0.16)`): einzige Linienfarbe. **Glass** (`rgba(245,240,230,0.07)`) + **Glass Line** (`rgba(245,240,230,0.16)`): Chips, Icon-Buttons, gescrollter Header, Dropdowns.

**The One Accent Rule (unverändert):** Rot nie als Fläche jenseits von Buttons und kleinen Marken. **Neu — The Photo Rule:** Scrims nur so stark, wie Text-Lesbarkeit es verlangt (4.5:1); das Foto bleibt erkennbar Hauptdarsteller.

## Typography

**Display:** Cormorant Garamond, Gewicht 400 (leichter als früher: Autorität durch Zurückhaltung), Display bis clamp 5.6rem, line-height 1.02, letter-spacing -0.01em. Ein `<em>` (kursiv, Gewicht 500, Lotus Red Bright) pro zentraler Headline. **Body/UI:** Bricolage Grotesque; Labels uppercase mit 0.22em Tracking leben fast ausschließlich in Chips. **Serif-Only-For-Headlines-Regel gilt weiter.** Beide Schriften selbst gehostet (`fonts/`, Latein-Subset).

## Layout & Depth

Container 1180px (`.wrap`) / 1440px (`.wrap-wide`), Sektionen 120px (Desktop) / 80px (Mobil, Breakpoint 960px). Karten-Grids nutzen 18px-Lücken auf dem Canvas — **kein 1px-Hairline-Grid mehr**. Tiefe entsteht durch Flächen-Stufen (bg → bg-2 → bg-3) und Glas (backdrop-blur), nicht durch Schatten; Ausnahmen: CTA-Pille (0 4px 20px), Dropdown/Mobile-Nav (Stapelordnung), Chip-Innenkante (inset 1px Highlight).

## Components

- **Buttons:** Pillen (999px). Primär rot gefüllt, Outline mit Cream-35%-Rand (Hover: Gold), Ghost = Gold-Text mit wanderndem Pfeil (`.arr`).
- **Chips:** Glas-Pille mit Gold-Text — Standard für alle kleinen Etiketten (Sektionseinleitungen, Kartenzielgruppen, Bewertungs-Kennzahl).
- **Header:** fixiert, transparent über dem Hero, ab 40px Scroll Milchglas (blur 18px) mit Hairline; Logo schrumpft mit. Mobil immer Milchglas. Dropdowns als Glas-Panels (14px Radius).
- **Icon-Buttons:** Kreise mit Glas-Füllung und Glass-Line-Rand; Icons sind gezeichnete Stroke-SVGs (WhatsApp, Instagram, Facebook, Mail, Lotus-Listenpunkt) — **nie Unicode-Glyphen**.
- **Karten** (Werte, Wochenkarte, Bewertungen, Catering-Wege): bg-2, 10px, randlos; Bewertungs-Grid mit versetzter Mittelkarte (Desktop +48px).
- **Bilder:** 10px Radius in Grids/Splits, Vollbild (0px) für Hero und Kinoband; innen 1px Cream-8%-Ring via ::after.

## Motion

Gated: `html.js` (sonst alles sichtbar) und `prefers-reduced-motion` (alles aus). Muster: Hero-Rise (0.9s, gestaffelt), Ken-Burns (12s, einmalig), Scroll-Reveal (`.reveal` + IntersectionObserver, translateY 26px, Stagger via `--d`), Parallax-Drift (nur transform, rAF, Faktor 0.05/0.07 mit Basis-Scale 1.12–1.14), Count-up (1.2s, Endstand = HTML-Text), Sternen-Sweep (clip-path). Timing-Kurve überall cubic-bezier(.16,.84,.28,1).

## Do's and Don'ts

### Do
- Fotos die Bühne geben: Vollbild-Sektionen mit Text im Bild statt Bild-neben-Text, wo die Seite einen Höhepunkt braucht.
- Jedes kleine Etikett als Glas-Chip setzen; jede wichtige Headline darf genau ein kursives rotes `<em>`-Wort tragen.
- Karten flach und randlos auf bg-2 halten; Tiefe über Flächen-Stufen und Glas.
- Alle Bewegung hinter `.js` + reduced-motion absichern; Inhalte müssen ohne JavaScript vollständig sichtbar sein.
- Marker-Kommentare (`<!--speiseplan:...-->`) und Klassen der Wochenkarte unangetastet lassen — Werkzeuge und Firestore-Skript hängen daran.

### Don't
- Keine 2px-Kanten-Buttons, kein 1px-Hairline-Grid, keine nackten Eyebrow-Zeilen mehr — das war das alte System.
- Kein Unicode-Zeichen als Icon (✆ ◎ ✉ ⓕ ❊ sind abgelöst); Icons sind Stroke-SVGs in einheitlicher Strichstärke.
- Rot nicht als Flächenfarbe, Gold nicht als Fließtextfarbe; Body-Text nie unter 4.5:1 Kontrast.
- Keine Schatten als Karten-Schmuck; kein Parallax auf Text; keine Endlos-Animationen.
- Kein Stock- oder KI-Bildmaterial für Menschen, Trucks, Events (unverändert; Gerichtefotos in `img/gerichte/` dürfen retuschierte Studiokulisse haben).
