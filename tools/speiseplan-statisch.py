#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schreibt den aktuellen Speiseplan als statisches HTML in index.html und aktuelles.html.

Warum das nötig ist
-------------------
Die Seiten laden den Speiseplan per JavaScript aus Firestore. Für Besucher ist
das gut, für Suchmaschinen nur halb: Googlebot rendert JavaScript verzögert,
und die Crawler von ChatGPT, Perplexity und Claude in der Regel gar nicht. Im
ausgelieferten HTML stand deshalb dreimal "Speiseplan folgt in Kürze" — die
einzigen wöchentlich frischen Inhalte der Seite waren für sie unsichtbar.

Dieses Skript holt dieselben Daten über die Firestore-REST-Schnittstelle und
trägt sie zwischen den Markern <!--speiseplan:DOK--> und <!--/speiseplan:DOK-->
ins HTML ein. Das JavaScript bleibt unangetastet und überschreibt den Inhalt im
Browser weiterhin mit dem Live-Stand — statisch ist also nur die Rückfallebene,
die aber jetzt echte Gerichte enthält statt eines Platzhalters.

Das erzeugte Markup entspricht exakt dem, was baueGerichtBlock() im Browser
erzeugt. Ändert sich das eine, muss das andere mit.

Aufruf: python3 tools/speiseplan-statisch.py [--pruefen]
  ohne Argument  schreibt die Dateien
  --pruefen      meldet nur, ob sich etwas ändern würde (Exit 1 = Änderung)
"""

import html
import json
import os
import re
import sys
import urllib.request

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEITEN = ["index.html", "aktuelles.html"]
REFERENZ_SEITE = "catering-firmenevents.html"
# Unter dieser Zahl wird der Abschnitt "Wo wir schon waren" gar nicht erst
# ausgegeben. Eine Referenzliste mit einem einzigen Eintrag wirkt schwaecher
# als die allgemeinen Aussagen, die sie belegen soll.
REFERENZ_MINDESTENS = 3
PROJEKT = "red-lotus-eventkalender"
DATENBANK = "default"          # benannte Datenbank, nicht "(default)" — siehe LIVE-SCHALTUNG_DNS.md
SAMMLUNG = "website"
DOKUMENTE = ["speiseplan_biberach", "speiseplan_laupheim", "speiseplan_warthausen"]

MONATE_OK = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def api_schluessel() -> str:
    """Liest den öffentlichen Web-API-Schlüssel aus index.html.

    Bewusst kein zweiter Ablageort: Der Schlüssel steht ohnehin im
    ausgelieferten Clientcode. Wird er dort getauscht, zieht dieses Skript
    automatisch nach.
    """
    quelle = open(os.path.join(WURZEL, "index.html"), encoding="utf-8").read()
    treffer = re.search(r'apiKey:\s*"([^"]+)"', quelle)
    if not treffer:
        raise SystemExit("Kein apiKey in index.html gefunden — Firebase-Konfiguration geändert?")
    return treffer.group(1)


class Stoerung(Exception):
    """Der Dienst war nicht erreichbar — im Unterschied zu 'Dokument gibt es nicht'."""


def hole(dokument: str, schluessel: str):
    """Ein Speiseplan-Dokument über die REST-Schnittstelle holen.

    Rückgabe None heißt: Das Dokument existiert nicht (404). Für den betroffenen
    Standort ist dann tatsächlich kein Plan hinterlegt, der Platzhalter ist
    richtig.

    Bei allem anderen — Zeitüberschreitung, DNS, 5xx, abgelaufener Schlüssel —
    fliegt Stoerung. Der Aufrufer bricht dann ab, ohne zu schreiben. Sonst würde
    eine halbe Minute Netzstörung den vorhandenen Speiseplan im HTML durch
    "folgt in Kürze" ersetzen und diesen Rückschritt auch noch deployen.
    """
    url = (f"https://firestore.googleapis.com/v1/projects/{PROJEKT}/databases/"
           f"{DATENBANK}/documents/{SAMMLUNG}/{dokument}?key={schluessel}")
    try:
        with urllib.request.urlopen(url, timeout=20) as antwort:
            daten = json.loads(antwort.read().decode("utf-8"))
    except urllib.error.HTTPError as fehler:
        if fehler.code == 404:
            print(f"  {dokument}: kein Dokument hinterlegt")
            return None
        raise Stoerung(f"{dokument}: HTTP {fehler.code}") from fehler
    except Exception as fehler:
        raise Stoerung(f"{dokument}: {fehler}") from fehler

    felder = daten.get("fields", {})
    roh = felder.get("gerichte", {}).get("arrayValue", {}).get("values", [])
    gerichte = []
    for eintrag in roh:
        f = eintrag.get("mapValue", {}).get("fields", {})
        name = f.get("name", {}).get("stringValue", "").strip()
        variante = f.get("variante", {}).get("stringValue", "").strip()
        beschreibung = f.get("beschreibung", {}).get("stringValue", "").strip()
        if name:
            gerichte.append((name, variante, beschreibung))
    datum = felder.get("datum", {}).get("stringValue", "").strip()
    return {"gerichte": gerichte, "datum": datum}


def gruppiere(gerichte):
    """Gleiche Gerichtnamen zusammenfassen, Varianten sammeln.

    Spiegelt gruppiereGerichte() im Browser: "Grünes Curry / Hühnchen" und
    "Grünes Curry / Vegan" werden ein Block mit zwei Varianten, nicht zwei
    Blöcke mit demselben Namen. Reihenfolge des ersten Auftretens bleibt.

    Die Beschreibung hängt am Gericht, nicht an der Variante — die erste
    gefüllte gewinnt, genau wie im Browser.
    """
    gruppen = {}
    for name, variante, beschreibung in gerichte:
        eintrag = gruppen.setdefault(name, {"varianten": [], "beschreibung": ""})
        if variante and variante not in eintrag["varianten"]:
            eintrag["varianten"].append(variante)
        if beschreibung and not eintrag["beschreibung"]:
            eintrag["beschreibung"] = beschreibung
    return gruppen


def datum_deutsch(iso: str) -> str:
    if not MONATE_OK.match(iso or ""):
        return ""
    j, m, t = iso.split("-")
    return f"{t}.{m}.{j}"


# Wörter, die einen organisatorischen Hinweis kennzeichnen statt eines Gerichts.
# Anlass: Am 05.09.2026 stand "Vertretung durch Dominik" mit dem Zusatz "Hühnchen"
# öffentlich als Speise auf der Startseite — eine interne Notiz, die über das
# Gerichte-Feld der Kalender-App durchgeschlagen war.
#
# Bewusst kurz und eindeutig gehalten: Lieber ein Hinweis, der versehentlich als
# Gericht durchrutscht, als ein echtes Gericht, das fälschlich verschwindet.
# Der saubere Weg bleibt das Statusfeld der App (marktstatus_<ort> mit "hinweis") —
# das hier ist nur das Sicherheitsnetz.
HINWEIS_WOERTER = (
    "vertretung", "urlaub", "ausfall", "entfällt", "entfaellt", "kein markt",
    "kein stand", "geschlossen", "feiertag", "krank", "pause",
)


def ist_hinweis(name: str) -> bool:
    n = (name or "").casefold()
    return any(w in n for w in HINWEIS_WOERTER)


def baue_koerper(gruppen) -> str:
    """Erzeugt exakt das Markup von baueGerichtBlock() im Browser."""
    zeilen = []
    for name, eintrag in gruppen.items():
        varianten = eintrag["varianten"]
        beschreibung = eintrag["beschreibung"]
        if ist_hinweis(name):
            # Als Hinweis darstellen, nicht als Speise — und ohne die
            # Variantenzeile, die sonst "Hühnchen" an eine Absage hängt.
            text = html.escape(name.strip(), quote=False)
            zeilen.append(f'          <div class="plan-empty">{text}</div>')
            continue
        zeilen.append('          <div class="plan-dish">')
        zeilen.append(f'            <div class="dish">{html.escape(name, quote=False)}</div>')
        # Reihenfolge wie im Browser: Name, Beschreibung, Varianten.
        if beschreibung:
            text = html.escape(beschreibung, quote=False)
            zeilen.append(f'            <div class="dish-info">{text}</div>')
        if varianten:
            text = html.escape(" · ".join(varianten), quote=False)
            zeilen.append(f'            <div class="dish-desc">{text}</div>')
        zeilen.append('          </div>')
    return "\n".join(zeilen)


def hole_news(schluessel: str):
    """Alle News-Dokumente holen (für die Referenzliste vergangener Einsätze).

    Anders als hole() fragt das die ganze Sammlung ab, weil die News-IDs
    zufällig vergeben werden (news_<zufall>). Das Bildfeld wird bewusst NICHT
    mit ausgelesen: Die Plakate liegen als base64 im Dokument, ein einzelnes
    wog am 05.09.2026 rund 265 KB. Für die Referenzliste brauchen wir nur Text.
    """
    url = (f"https://firestore.googleapis.com/v1/projects/{PROJEKT}/databases/"
           f"{DATENBANK}/documents:runQuery?key={schluessel}")
    abfrage = {
        "structuredQuery": {
            "from": [{"collectionId": SAMMLUNG}],
            "where": {"fieldFilter": {
                "field": {"fieldPath": "type"},
                "op": "EQUAL",
                "value": {"stringValue": "news"},
            }},
            "select": {"fields": [{"fieldPath": f} for f in
                                  ("titel", "text", "tag", "datumVon", "datumBis")]},
        }
    }
    anfrage = urllib.request.Request(
        url, data=json.dumps(abfrage).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(anfrage, timeout=20) as antwort:
            zeilen = json.loads(antwort.read().decode("utf-8"))
    except Exception as fehler:
        raise Stoerung(f"News: {fehler}") from fehler

    news = []
    for zeile in zeilen:
        dok = zeile.get("document")
        if not dok:
            continue
        f = dok.get("fields", {})
        news.append({k: f.get(k, {}).get("stringValue", "").strip()
                     for k in ("titel", "text", "tag", "datumVon", "datumBis")})
    return news


def referenzen(news, heute_iso: str, grenze: int = 8):
    """Vergangene öffentliche Einsätze auswählen, neueste zuerst.

    Drei Bedingungen, alle bewusst eng:
      1. vorbei — Enddatum (ersatzweise Startdatum) liegt vor heute
      2. als "Event" verschlagwortet — Urlaubsmeldungen fallen damit raus
      3. kein organisatorischer Hinweis — fängt Fälle wie
         "Urlaubsvertretung Dominik", die zwar als Event getaggt sind,
         aber keine Referenz darstellen (gleiche Wortliste wie im Speiseplan)

    Felix' Vorgabe: Nur öffentliche Veranstaltungen, keine Privatfeiern. Das
    trägt hier von selbst, weil Privatfeiern gar nicht als News angelegt werden
    — die Auswahl passiert also schon in der Kalender-App.
    """
    treffer = []
    for n in news:
        ende = n["datumBis"] or n["datumVon"]
        if not ende or ende >= heute_iso:
            continue
        if (n["tag"] or "").casefold() != "event":
            continue
        if ist_hinweis(n["titel"]) or ist_hinweis(n["text"]):
            continue
        if not n["titel"]:
            continue
        treffer.append(n)
    treffer.sort(key=lambda n: n["datumBis"] or n["datumVon"], reverse=True)
    return treffer[:grenze]


def baue_referenzen(eintraege) -> str:
    """Erzeugt den kompletten Abschnitt — oder nichts.

    Nichts heisst hier wirklich nichts: Liegen zu wenige Einsaetze vor, wird der
    Abschnitt gar nicht ausgegeben, statt eine duenne Liste zu zeigen.
    """
    if len(eintraege) < REFERENZ_MINDESTENS:
        return ""
    zeilen = ['<section id="wo-wir-waren" style="background:var(--bg-2);">',
              '  <div class="wrap">',
              '    <div class="section-head">',
              '      <span class="eyebrow">Öffentliche Einsätze</span>',
              '      <h2>Wo wir schon waren</h2>',
              '      <p>Ein Auszug aus Veranstaltungen, auf denen wir mit dem Foodtruck standen.</p>',
              '    </div>',
              '    <ul class="ref-list">']
    for n in eintraege:
        datum = datum_deutsch(n["datumBis"] or n["datumVon"])
        titel = html.escape(n["titel"], quote=False)
        zeilen.append('      <li class="ref-item">')
        if datum:
            zeilen.append(f'        <span class="ref-datum">{datum}</span>')
        zeilen.append(f'        <span class="ref-titel">{titel}</span>')
        if n["text"]:
            zeilen.append(f'        <span class="ref-text">{html.escape(n["text"], quote=False)}</span>')
        zeilen.append('      </li>')
    zeilen += ['    </ul>', '  </div>', '</section>']
    return "\n".join(zeilen)


def ersetze(quelle: str, marke: str, inhalt: str) -> str:
    start, ende = f"<!--{marke}-->", f"<!--/{marke}-->"
    i, j = quelle.index(start) + len(start), quelle.index(ende)
    return quelle[:i] + inhalt + quelle[j:]


def main() -> int:
    nur_pruefen = "--pruefen" in sys.argv
    schluessel = api_schluessel()

    print(f"Firestore {PROJEKT}/{DATENBANK}/{SAMMLUNG}")
    daten = {}
    try:
        for dokument in DOKUMENTE:
            satz = hole(dokument, schluessel)
            if satz and satz["gerichte"]:
                gruppen = gruppiere(satz["gerichte"])
                daten[dokument] = (gruppen, satz["datum"])
                print(f"  {dokument}: {len(gruppen)} Gerichte, Stand {satz['datum'] or 'ohne'}")
            else:
                print(f"  {dokument}: keine Gerichte — Platzhalter bleibt")
    except Stoerung as fehler:
        # Nichts anfassen. Lieber ein Lauf ohne Wirkung als ein Rückschritt.
        print(f"Abbruch, Firestore nicht erreichbar: {fehler}")
        print("Dateien bleiben unverändert.")
        return 0

    # Vergangene oeffentliche Einsaetze fuer die Referenzliste.
    # Scheitert das, bleibt nur die Referenzliste unveraendert — der Speiseplan
    # soll deswegen nicht ausfallen.
    referenz_liste = []
    try:
        heute_iso = __import__("datetime").date.today().isoformat()
        referenz_liste = referenzen(hole_news(schluessel), heute_iso)
        print(f"  Referenzen: {len(referenz_liste)} vergangene Einsaetze")
    except Stoerung as fehler:
        print(f"  Referenzen uebersprungen: {fehler}")

    geaendert = []
    for seite in SEITEN:
        pfad = os.path.join(WURZEL, seite)
        quelle = neu = open(pfad, encoding="utf-8").read()

        for dokument in DOKUMENTE:
            if dokument in daten:
                gruppen, datum = daten[dokument]
                koerper = "\n" + baue_koerper(gruppen) + "\n          "
                stand = datum_deutsch(datum)
                # "Gültig für", nicht "Stand": Das Feld "datum" aus Firestore ist
                # der Markttag, an dem es dieses Essen gibt — nicht der Zeitpunkt
                # der letzten Änderung. Als "Stand" gelesen wirkte ein in der
                # Zukunft liegendes Datum wie ein Fehler.
                stand_html = f'<div class="plan-stand">Gültig für {stand}</div>' if stand else ""
            else:
                koerper = ('\n          <div class="plan-empty">Speiseplan folgt in Kürze</div>\n          ')
                stand_html = ""
            neu = ersetze(neu, f"speiseplan:{dokument}", koerper)
            neu = ersetze(neu, f"stand:{dokument}", stand_html)

        if neu != quelle:
            geaendert.append(seite)
            if not nur_pruefen:
                open(pfad, "w", encoding="utf-8").write(neu)

    # Referenzliste vergangener oeffentlicher Einsaetze auf der Firmenseite.
    # Bewusst hier gebacken und nicht nur im Browser nachgeladen: Der Zweck der
    # Liste ist, Erfahrung gegenueber Suchmaschinen und KI-Systemen zu belegen —
    # die rendern aber meist kein JavaScript. Nur im HTML nuetzt sie etwas.
    if True:   # immer anfassen: auch das Entfernen des Abschnitts ist ein Ergebnis
        pfad = os.path.join(WURZEL, REFERENZ_SEITE)
        quelle = open(pfad, encoding="utf-8").read()
        inhalt = baue_referenzen(referenz_liste)
        neu = ersetze(quelle, "referenzen", ("\n" + inhalt + "\n") if inhalt else "")
        if neu != quelle:
            geaendert.append(REFERENZ_SEITE)
            if not nur_pruefen:
                open(pfad, "w", encoding="utf-8").write(neu)

    if geaendert:
        print(("Würde ändern: " if nur_pruefen else "Geschrieben: ") + ", ".join(geaendert))
        return 1 if nur_pruefen else 0
    print("Keine Änderung nötig.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
