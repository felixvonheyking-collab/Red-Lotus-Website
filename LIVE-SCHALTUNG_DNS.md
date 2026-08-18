# Live-Schaltung: redlotus-asianfood.com auf Hostinger umstellen

**Durchgeführt und geprüft am 18.08.2026, ca. 21:30 Uhr. Die Seite ist live.**
Das Dokument bleibt als Protokoll und Rückfallplan bestehen.

## Ergebnis

- A `@` → `82.198.229.235`, CNAME `www` → `redlotus-asianfood.com`, beides bei
  Wix gesetzt, alle drei alten Wix-IPs entfernt
- Auflösung binnen Minuten bei 1.1.1.1, 8.8.8.8 und 9.9.9.9 identisch
- Let's-Encrypt-Zertifikat von Hostinger ausgestellt (18.08. 18:27 UTC, gültig
  bis 16.11.2026, gilt für die Domain **und** `www`), Prüfung sauber
- Alle 14 Adressen liefern HTTP 200 (12 Seiten plus `sitemap.xml` und `robots.txt`)
- http leitet auf https um
- Mail unverändert: 5 MX (Google), SPF, beide Google-Verifizierungen, die
  Apple-Verifizierung, DKIM (`google._domainkey` sowie `s1`/`s2`/`sel1`) und der
  `_dmarc`-CNAME

### Wichtigster Stolperstein — HSTS

Zwischen DNS-Umstellung und Zertifikatsausstellung lag ein Fenster, in dem die
Seite für **wiederkehrende Besucher nicht erreichbar** war. Grund: Die alte
Wix-Seite hatte `strict-transport-security: max-age=31556952` gesendet — rund ein
Jahr. Browser, die die Seite in dieser Zeit über https besucht hatten, weigern
sich deshalb, auf http auszuweichen, und https funktionierte mangels Zertifikat
noch nicht. Kein Warnhinweis, sondern eine harte Fehlermeldung.

**Lehre für Site 2 und 3:** Das SSL-Zertifikat direkt nach der DNS-Umstellung
prüfen und, falls nötig, im hPanel unter *Sicherheit → SSL-Zertifikat* sofort
anstoßen. Hier war es rund zwei Minuten später von selbst aktiv.

### Offener Kleinpunkt

`www` leitet nicht auf die Variante ohne `www` um, beide liefern die Seite
gleichwertig aus. Unkritisch, weil alle `canonical`-Angaben und die `sitemap.xml`
auf die Variante ohne `www` zeigen — Suchmaschinen führen das zusammen. Eine
echte Weiterleitung wäre trotzdem sauberer.

---

Stand 18.08.2026. Gemessener IST-Zustand, Ablauf, Rückfallwerte.

## Grundregel

**Nur zwei Einträge werden angefasst: der A-Record der Domain und der
www-Eintrag.** Nameserver bleiben bei Wix. MX, SPF, DKIM und `_dmarc` bleiben
unangetastet — daran hängt die Geschäfts-E-Mail über Google Workspace.

Wenn ein Wix-Dialog anbietet, die Nameserver zu ändern oder „die Domain zu
verbinden/trennen": **abbrechen.** Das ist ein anderer Vorgang und würde die
E-Mail mitreißen.

## IST-Zustand, gemessen am 18.08.2026 gegen 1.1.1.1

Diese Werte sind zugleich der Rückfallplan. Bei Problemen exakt so
wiederherstellen:

| Eintrag | Aktueller Wert |
|---|---|
| Nameserver | `ns6.wixdns.net`, `ns7.wixdns.net` |
| **A (Root)** | `185.230.63.107`, `185.230.63.171`, `185.230.63.186` |
| **CNAME www** | `cdn1.wixdns.net` |
| MX | `aspmx.l.google.com` (10) + `alt1`–`alt4.aspmx.l.google.com` (20–50) |
| TXT Root | `v=spf1 include:_spf.google.com ~all`, `apple-domain-verification=efcQ6E1YIDshHUXL`, zwei `google-site-verification=…` |
| TXT `google._domainkey` | DKIM, 2048 bit |
| `_dmarc` | CNAME auf `_dmarc.wixemails.com` |

Nur die **fett** markierten Zeilen ändern sich.

## Schritt 0 — Domain zuerst in Hostinger anlegen

Ohne diesen Schritt weiß der Server nicht, welche Seite er für
`redlotus-asianfood.com` ausliefern soll — die Umstellung würde in einer
Fehlerseite enden.

Nachgemessen am 18.08.2026: Der Hostinger-Server antwortet auf Anfragen mit dem
Hostnamen `redlotus-asianfood.com` derzeit **gar nicht** (Verbindungsabbruch).
Für die Testdomain antwortet er normal mit HTTP 200. Genau das ändert sich mit
Schritt 0.

In hPanel: **Websites → die Seite → Domains → Domain hinzufügen** (je nach
Ansicht auch „Hauptdomain ändern"), dort `redlotus-asianfood.com` eintragen.
Hostinger zeigt danach die zu setzenden DNS-Werte an — **die dort angezeigte
A-Record-IP ist maßgeblich**, nicht die IP der Testdomain.

> Warum nicht einfach die IP der Testdomain nehmen: `honeydew-eagle-941485.hostingersite.com`
> ist ein CNAME auf Hostingers CDN (`free.cdn.hstgr.net`) und löst je nach
> Standort auf verschiedene Adressen auf (`92.113.23.86`, `88.222.222.16`,
> `84.32.84.1` — alle antworten). Das ist nicht zwingend die IP, die für eine
> eigene Domain gilt.

### Ergebnis Schritt 0 (18.08.2026)

Domain in hPanel verbunden, Weg **„Über DNS-Einträge verbinden"** gewählt (nicht
„Über Nameserver verbinden") — damit bleibt Wix DNS-Anbieter und die
Mail-Einträge bleiben unberührt.

**Von Hostinger genannter A-Record: `82.198.229.235`, TTL 300.**

Die drei aus der Testdomain ermittelten IPs (`92.113.23.86`, `88.222.222.16`,
`84.32.84.1`) sind **nicht** zu verwenden — sie liefern für die echte Domain
eine Seite „Parked Domain name on Hostinger DNS system". Das ist Hostingers
Park-/CDN-Schicht, nicht der Webserver dieser Seite.

## Schritt 1 — Vorabprüfung, bevor DNS angefasst wird

Mit der IP aus Schritt 0 lässt sich vorab testen, ob der Server die Seite für
die echte Domain schon korrekt ausliefert — ohne dass ein einziger DNS-Eintrag
geändert wurde:

```
curl -s -o /dev/null -w "%{http_code}\n" \
  --resolve "redlotus-asianfood.com:443:HIER_DIE_IP" \
  https://redlotus-asianfood.com/
```

Erwartet: `200`. Kommt `000`, `404` oder eine fremde Seite, ist Schritt 0 noch
nicht vollständig — dann **nicht** weitermachen.

### Ergebnis Schritt 1 (18.08.2026): bestanden

Gegen `82.198.229.235` geprüft, mit Browser-Kennung (ohne die greift Hostingers
Bot-Schutz und antwortet irreführend mit 403):

| Hostname | Ergebnis |
|---|---|
| `redlotus-asianfood.com` | HTTP 200, Titel „Red Lotus Asian Food – Catering & Kochkurse in Biberach & Ulm" |
| `www.redlotus-asianfood.com` | HTTP 200, gleicher Titel |

Inhaltsprobe bestätigt die echte Seite (Verweis auf `aktuelles.html`, Schriftart
Bricolage, „Red Lotus" 13×). Der Server liefert also schon korrekt aus, **bevor**
ein DNS-Eintrag geändert wurde — die Umstellung ist damit risikoarm.

## Schritt 2 — DNS bei Wix ändern

Wix-Konto → Domains → `redlotus-asianfood.com` → DNS-Einträge bearbeiten.

Von Hostinger vorgegebene Zielwerte (abgelesen 18.08.2026):

| Typ | Name | Wert | TTL |
|---|---|---|---|
| A | `@` | `82.198.229.235` | 300 |
| CNAME | `www` | `redlotus-asianfood.com` | 300 |

1. **A-Record `@`:** die drei Wix-IPs (`185.230.63.107`, `185.230.63.171`,
   `185.230.63.186`) entfernen, stattdessen `82.198.229.235` eintragen.
2. **CNAME `www`:** `cdn1.wixdns.net` durch `redlotus-asianfood.com` ersetzen.

### Was auf keinen Fall angefasst wird

Hostinger blendet den Hinweis ein: *„Falls vorhanden, entfernen Sie alle anderen
bestehenden A oder CNAME Einträge für @ und www."* Das gilt **ausschließlich für
die Namen `@` und `www`**. Alles andere bleibt stehen:

- **`_dmarc` (CNAME auf `_dmarc.wixemails.com`)** — ist zwar ein CNAME, aber
  nicht für `@` oder `www`. Wird er gelöscht, verliert die Domain ihre
  DMARC-Richtlinie und die Zustellbarkeit der Geschäftsmails leidet.
- MX-Einträge (Google Workspace, 5 Stück)
- TXT auf `@` (SPF, Apple- und Google-Verifizierungen)
- TXT auf `google._domainkey` (DKIM)
- Die Nameserver

**Mögliche Hürde:** Wix lässt den Root-A-Record teils nicht bearbeiten, solange
eine Wix-Seite mit der Domain verbunden ist. Dann in den Wix-Domain-Einstellungen
die *Verbindung zur Wix-Website* lösen — **nicht** die Domain freigeben,
übertragen oder kündigen. Die Domain bleibt bei Wix, nur die Seite hängt nicht
mehr daran.

## Schritt 3 — Warten

DNS-Änderungen brauchen typisch Minuten bis wenige Stunden. Danach stellt
Hostinger automatisch ein Let's-Encrypt-Zertifikat aus; bis das durch ist, kann
der Browser kurzzeitig vor der Verbindung warnen. Das ist normal und erledigt
sich von selbst.

## Schritt 4 — Prüfen

Website:
- `https://redlotus-asianfood.com` zeigt die neue Seite
- `https://www.redlotus-asianfood.com` ebenfalls (oder leitet auf die Version
  ohne www um — die Seite gibt sich in allen `canonical`-Angaben und in der
  `sitemap.xml` als *ohne* www aus, deshalb ist eine Weiterleitung auf die
  Variante ohne www die saubere Einstellung)
- Zertifikat gültig, keine Browserwarnung
- Ein Anfrageformular abschicken → Termin erscheint im Kalender

E-Mail — der wichtigste Test:
- Eine Test-Mail an `info@redlotus-asianfood.com` schicken und eine von dort
  verschicken
- MX/SPF/DKIM/DMARC sollten unverändert sein

## Was mit Wix passiert

Die Wix-Seite ist danach unter der eigenen Domain nicht mehr erreichbar — das
ist beabsichtigt. Das Abo läuft bezahlt bis 17.04.2028 weiter und die Seite
bleibt über ihre Wix-interne Adresse nutzbar (Idee: als Blog-Testfeld).

**Merk-Termin unverändert:** Die Domain muss *vor* einer Kündigung des
Wix-Abos zu einem anderen Registrar transferiert werden, sonst hängt sie fest.

## Rückfall

Die drei A-Records und den www-CNAME aus der Tabelle oben wieder eintragen.
Da Nameserver und alle Mail-Einträge nie angefasst wurden, ist der Rückweg auf
diese zwei Zeilen begrenzt.
