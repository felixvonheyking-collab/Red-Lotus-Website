# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML/CSS, custom-coded (no framework, no CMS-as-a-platform). Fonts via Google Fonts (Cormorant Garamond, Bricolage Grotesque). Planned: Firebase (Firestore) as a lightweight headless data source for dynamic content only (see Capabilities and Constraints).

## Users

Two primary audiences, both in the Biberach/Ulm/Baden-Württemberg region:
- Firmenkunden planning catering for company events (Weihnachtsfeiern, Teamevents, Meetings mit Verpflegung, Sommerfeste mit Foodtruck vor Ort).
- Privatkunden planning a wedding or a private celebration (Geburtstage, Jubiläen) who have a higher per-person budget than average and are choosing a premium catering partner.

A secondary, lower-intent audience: passers-by / regulars checking the current weekly market location and lunch menu (Wochenmarkt/Mittagstisch).

## Product Purpose

The website for "Red Lotus Asian Food" (Site 1 of three planned Red Lotus sites), the original business Felix and his wife Paew have run since summer 2022. Its job is to convert catering/event inquiries (Firmenevents, Hochzeiten, private Feiern) and Kochkurs bookings, while also serving as the reference point for the weekly Foodtruck/Wochenmarkt schedule. Success = more qualified inquiries via the three catering forms and the Kochkurs form, replacing the current Wix site.

## Positioning

Premium positioning within the Red Lotus family: authentic, hand-cooked Thai/Asian catering for people who want a well-planned, well-presented event, not casual street food. This is the deliberate opposite pole to the sibling site "Red Lotus Streetfood" (Site 2), which is casual, playful, and aimed at a younger audience. Mechanism a generic caterer or Site 2 could not truthfully copy: real event photography (not stock/AI), a specific 4-step catering process already proven on the old site, and Kochkurse positioned as a team-building format for corporate clients as well as a private activity.

## Operating Context

- Wochenmärkte at fixed weekly locations (Mittwoch Biberach, Donnerstag Laupheim, Freitag Warthausen) — the current location/day must be easy to find, not buried in an FAQ as on the old site.
- Catering delivered on-site for company events, weddings, and private parties, booked via three separate segment-specific inquiry forms.
- Kochkurse run as hands-on group sessions (dumpling-folding, shared prep), bookable by private groups and companies (team event framing).
- Contact happens via WhatsApp, Instagram, and email — no dedicated contact page, just header/footer icons (WhatsApp must link to a real wa.me URL, a bug on the old site).

## Capabilities and Constraints

- No traditional CMS. Static, hand-built HTML/CSS pages. Content that changes often (weekly menu, current market location) is not meant to be hardcoded — the plan is a dedicated `website` collection in the existing Firebase project "red-lotus-eventkalender" (already in production for the internal Kalender/Bestellstatus/Küchendisplay/Kundendisplay/Inventar/Löhne tooling), read via a small admin page in the same internal style. Not yet implemented.
- Hard security constraint: the public website may only ever get **read-only** access to the new `website` Firestore collection. It must never have access to the internal collections (Löhne, Inventar, Bestellungen). This must be enforced with Firestore security rules before the Firebase integration ships.
- Three separate catering landing pages (Firmenevents / Hochzeiten / Private Feiern) instead of one page with sections, each with its own inquiry form and its own URL, for targeted local SEO and clearer user paths per audience.
- Kochkurse gets its own page and own form (a real gap on the old Wix site — the old link to it was broken).
- No traditional Kontakt page with a form; contact is WhatsApp/Instagram/email icons in header/footer only.

## Brand Commitments

- Name: Red Lotus Asian Food (Site 1 of a three-site family: Site 1 Asian Food/catering, Site 2 Streetfood, Site 3 hub/blog — all must feel like "eine Familie, klar erkennbar" while Site 1 stays visually premium/distinct from Site 2's playfulness).
- Logo: final decision is the **wordmark only** (lotus icon + "Red Lotus" script + "Asian Food" line), no circular badge. The round Maneki-Neko-cat badge is explicitly rejected for the website (mismatched symbolism: Japanese luck cat vs. Thai-leaning food offering; 3D badge vs. flat line-art wordmark) and is reserved for social media only. The two standalone lotus icons are approved for favicon / recurring divider use.
- Imagery must be real photography of the business's own events and food — explicitly not stock or AI-generated imagery (a flaw identified and rejected on the old Wix site, where some food photos were visibly AI-generated).
- Voice/character: warm, moody, candlelit — not corporate-clinical.

## Evidence on Hand

- 92 photos in the connected Lightroom folder, all reviewed. Strong existing material for Site 1: red-lantern-lit spring roll display against red velvet, canapé/betel-leaf appetizers, Thai-tea pudding jars, a fruit platter with edible flowers, a night shot of two trucks with string lights and guests at standing tables (social proof for events), and a warm ingredient-prep / dumpling-folding group photo for Kochkurse.
- Known gap: few photos of actual guests at the buffet/truck during a wedding or upscale corporate event (current material is mostly food/truck without people). More photos can be supplied later; layout should tolerate adding them.
- Reference for what NOT to repeat: the live Wix site at www.redlotus-asianfood.com, critiqued for inconsistent nav/URLs, a broken Kochkurse link, AI-looking food photos, market locations hidden in an FAQ, repetitive text, no testimonials/social proof, a broken WhatsApp link, and leftover old-agency/Wix branding in the footer. Its 4-step catering process, local-SEO meta text, and city list are the parts worth keeping.
- Full project briefing with all confirmed decisions: `Red Lotus - Projektbriefing Seite 1.md` in the user's Lightroom folder.

## Product Principles

1. Premium and calm over busy and salesy — the site should read like a well-run event caterer, not a generic food truck flyer.
2. Every claim needs a real photo behind it — no stock or AI imagery, ever, per the explicit brand rejection of the old site's AI-generated food shots.
3. Segment the ask: each customer type (Firmenevent, Hochzeit, private Feier, Kochkurs) gets its own path and its own form rather than one generic contact form.
4. Don't hide operational facts — current market day/location must be easy to find on the homepage, not buried in an FAQ.
5. Keep Site 1 visually distinct from Site 2 (premium vs. playful) while staying recognizably part of the same Red Lotus family.

## Accessibility & Inclusion

No product-specific accessibility requirement has been established yet; standard web accessibility practice applies by default.
