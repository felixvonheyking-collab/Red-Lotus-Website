# Support-Anfrage an Hostinger — GPTBot erhält HTTP 429

Erstellt am 05.09.2026 aus dem GEO-Check. Text unten kopierfertig.
Deutsche und englische Fassung — Hostinger antwortet über den englischen
Kanal erfahrungsgemäß schneller.

---

## Deutsche Fassung

**Betreff:** Bot-Schutz blockiert GPTBot mit HTTP 429 – bitte für zwei Domains freigeben

Guten Tag,

auf meinen beiden bei Ihnen gehosteten Domains wird der Crawler **GPTBot**
(OpenAI) durchgängig mit **HTTP 429** abgewiesen. Andere Crawler kommen
problemlos durch. Ich vermute eine Regel im serverseitigen Bot-Schutz und
bitte darum, GPTBot freizugeben.

**Betroffene Domains**
- redlotus-asianfood.com
- redlotusstreetfood.com

**Was ich gemessen habe (05.09.2026)**

Anfrage mit der Kennung von GPTBot:

```
User-Agent: Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.2; +https://openai.com/gptbot
```

Ergebnis: **HTTP 429** auf *jeder* angefragten Adresse, auch auf
`/robots.txt` und `/llms.txt`, und auf beiden Domains. Der Antworttext ist
leer, ein `Retry-After`-Header wird nicht mitgeschickt. Als Server meldet
sich `LiteSpeed`.

Drei Versuche mit jeweils acht Sekunden Abstand ergaben dreimal 429. Ein
normaler Browser-Zugriff unmittelbar danach lieferte **HTTP 200**. Es handelt
sich also nicht um eine allgemeine Überlastung oder eine Ratenbegrenzung
durch zu viele Anfragen, sondern um eine Reaktion auf die Kennung.

**Zum Vergleich — diese Crawler erhalten alle HTTP 200:**

| Crawler | Ergebnis |
|---|---|
| OAI-SearchBot (OpenAI) | 200 |
| ChatGPT-User (OpenAI) | 200 |
| ClaudeBot (Anthropic) | 200 |
| Claude-User (Anthropic) | 200 |
| Googlebot | 200 |
| Bingbot | 200 |
| PerplexityBot | 200 |

Auffällig ist, dass ausgerechnet GPTBot als einziger der geprüften Crawler
abgewiesen wird, während zwei andere OpenAI-Crawler durchkommen.

**Meine eigene Konfiguration erlaubt den Zugriff ausdrücklich.**
Die `robots.txt` beider Domains enthält:

```
User-agent: *
Allow: /
```

In meiner `.htaccess` gibt es keine Regel, die auf User-Agents reagiert.

**Meine Bitte**

Bitte prüfen Sie, ob der Bot-Schutz beziehungsweise die WAF auf Ihrer Seite
GPTBot blockiert, und nehmen Sie den Crawler für die beiden genannten Domains
von der Sperre aus. Falls die Einstellung im hPanel selbst vorgenommen werden
kann, sagen Sie mir bitte, wo ich sie finde.

Vielen Dank und viele Grüße
Felix von Heyking

---

## Englische Fassung

**Subject:** Bot protection blocks GPTBot with HTTP 429 – please allow it for two domains

Hello,

on my two domains hosted with you, the crawler **GPTBot** (OpenAI) is
consistently rejected with **HTTP 429**, while other crawlers pass without
any problem. I suspect a rule in the server-side bot protection and would
like to ask you to allow GPTBot.

**Affected domains**
- redlotus-asianfood.com
- redlotusstreetfood.com

**What I measured (5 September 2026)**

Request using GPTBot's user agent:

```
User-Agent: Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.2; +https://openai.com/gptbot
```

Result: **HTTP 429** on *every* URL requested, including `/robots.txt` and
`/llms.txt`, and on both domains. The response body is empty and no
`Retry-After` header is sent. The server identifies itself as `LiteSpeed`.

Three attempts, eight seconds apart, returned 429 every time. A normal browser
request immediately afterwards returned **HTTP 200**. So this is not general
load or rate limiting caused by too many requests — it is a reaction to the
user agent string.

**For comparison — all of these crawlers receive HTTP 200:**
OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User, Googlebot, Bingbot,
PerplexityBot.

It is notable that GPTBot is the only crawler being rejected, while two other
OpenAI crawlers pass.

**My own configuration explicitly allows access.** The `robots.txt` of both
domains contains `User-agent: *` and `Allow: /`, and my `.htaccess` has no
user-agent-based rules.

**My request**

Please check whether your bot protection or WAF is blocking GPTBot, and
exclude it from the block for the two domains above. If this can be changed
in hPanel myself, please tell me where to find the setting.

Thank you and best regards,
Felix von Heyking

---

## Hintergrund für dich (nicht mitschicken)

**Warum das überhaupt wichtig ist — und warum nur mäßig dringend.**
OpenAI betreibt drei getrennte Crawler. `GPTBot` sammelt Trainingsdaten,
`OAI-SearchBot` baut den Index, aus dem ChatGPT beim Suchen zitiert, und
`ChatGPT-User` holt eine Seite live ab, wenn ein Nutzer sie verlangt. Bei dir
funktionieren die beiden letzten. ChatGPT kann die Seite also finden und
zitieren — sie fließt nur nicht ins Modellwissen ein.

**Falls Hostinger ablehnt oder nicht reagiert:** Das ist verschmerzbar. Der
Zitierweg ist offen, und die Trainingsaufnahme ist ohnehin nichts, worauf man
sich verlassen sollte. Kein Grund, den Anbieter deswegen zu wechseln.

**Falls Hostinger zurückfragt, ob du den Bot wirklich willst:** Ja. Die Seite
ist öffentlich, es gibt nichts zu schützen, und ein zusätzlicher Crawler
erzeugt bei einer Seite dieser Größe keine nennenswerte Last.
