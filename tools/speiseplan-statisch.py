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
        if name:
            gerichte.append((name, variante))
    datum = felder.get("datum", {}).get("stringValue", "").strip()
    return {"gerichte": gerichte, "datum": datum}


def gruppiere(gerichte):
    """Gleiche Gerichtnamen zusammenfassen, Varianten sammeln.

    Spiegelt gruppiereGerichte() im Browser: "Grünes Curry / Hühnchen" und
    "Grünes Curry / Vegan" werden ein Block mit zwei Varianten, nicht zwei
    Blöcke mit demselben Namen. Reihenfolge des ersten Auftretens bleibt.
    """
    gruppen = {}
    for name, variante in gerichte:
        liste = gruppen.setdefault(name, [])
        if variante and variante not in liste:
            liste.append(variante)
    return gruppen


def datum_deutsch(iso: str) -> str:
    if not MONATE_OK.match(iso or ""):
        return ""
    j, m, t = iso.split("-")
    return f"{t}.{m}.{j}"


def baue_koerper(gruppen) -> str:
    """Erzeugt exakt das Markup von baueGerichtBlock() im Browser."""
    zeilen = []
    for name, varianten in gruppen.items():
        zeilen.append('          <div class="plan-dish">')
        zeilen.append(f'            <div class="dish">{html.escape(name, quote=False)}</div>')
        if varianten:
            text = html.escape(" · ".join(varianten), quote=False)
            zeilen.append(f'            <div class="dish-desc">{text}</div>')
        zeilen.append('          </div>')
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

    geaendert = []
    for seite in SEITEN:
        pfad = os.path.join(WURZEL, seite)
        quelle = neu = open(pfad, encoding="utf-8").read()

        for dokument in DOKUMENTE:
            if dokument in daten:
                gruppen, datum = daten[dokument]
                koerper = "\n" + baue_koerper(gruppen) + "\n          "
                stand = datum_deutsch(datum)
                stand_html = f'<div class="plan-stand">Stand: {stand}</div>' if stand else ""
            else:
                koerper = ('\n          <div class="plan-empty">Speiseplan folgt in Kürze</div>\n          ')
                stand_html = ""
            neu = ersetze(neu, f"speiseplan:{dokument}", koerper)
            neu = ersetze(neu, f"stand:{dokument}", stand_html)

        if neu != quelle:
            geaendert.append(seite)
            if not nur_pruefen:
                open(pfad, "w", encoding="utf-8").write(neu)

    if geaendert:
        print(("Würde ändern: " if nur_pruefen else "Geschrieben: ") + ", ".join(geaendert))
        return 1 if nur_pruefen else 0
    print("Keine Änderung nötig.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
