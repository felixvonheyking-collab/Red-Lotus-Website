# -*- coding: utf-8 -*-
"""Lage und Groesse des Tellers in jeder Originalaufnahme.

Von Hand abgelesen an einem 10-Prozent-Raster (outputs/menu-sheets/raster-alle.png),
nachdem zwei automatische Verfahren zu unzuverlaessig waren: Eine Helligkeits-
maske scheiterte am ebenfalls dunklen Holzuntergrund, die Hough-Kreiserkennung
lieferte bei etwa der Haelfte der Bilder Durchmesser zwischen 0,39 und 1,02 —
also offensichtlichen Unsinn. Bei zwanzig Bildern ist Ablesen schneller und
sicher richtig.

  cx, cy  Mittelpunkt des Tellers als Anteil von Bildbreite bzw. -hoehe
  d       Durchmesser als Anteil der Bildbreite
"""

TELLER = {
 "bun-bun-salat":                 (0.51, 0.47, 0.73),
 "chicken-manchurian":            (0.53, 0.47, 0.70),
 "creamy-cajun-chicken":          (0.50, 0.45, 0.76),
 "gelbes-thai-curry":             (0.51, 0.45, 0.87),
 "gruenes-thai-curry":            (0.45, 0.50, 0.74),
 "hoisin-chicken":                (0.51, 0.50, 0.78),
 "indonesische-glasnudelsuppe":   (0.53, 0.50, 0.70),
 # Vorlage am 20.08.2026 in Canva mit Magic Expand nach oben und unten
 # erweitert; vorher (0.51, 0.50, 0.93) und damit das einzige Bild, bei dem
 # der Teller den Ausschnitt randlos fuellte.
 "java-curry":                    (0.51, 0.53, 0.49),
 "kimchi-bacon-udon":             (0.47, 0.52, 0.70),
 "mango-sticky-rice":             (0.57, 0.55, 0.70),   # Mitnahmebox statt Teller
 # Schale leicht schraeg aufgenommen (21.08.2026)
 "ma-yi-shang-shu":               (0.48, 0.555, 0.71),
 "massaman-thai-curry":           (0.52, 0.50, 0.65),
 # rechteckige Platte: d ist hier die Plattenbreite, nicht ein Durchmesser
 "sommerrollen":                  (0.535, 0.435, 0.79),
 "nepalesisches-pilzcurry":       (0.51, 0.50, 0.73),
 "orange-chicken":                (0.50, 0.48, 0.84),
 "pad-thai":                      (0.53, 0.52, 0.83),
 "panang-thai-curry":             (0.51, 0.48, 0.82),
 "pork-adobo":                    (0.58, 0.57, 0.67),
 "ramennudelsalat":               (0.52, 0.52, 0.60),
 "soba-nudelsalat":               (0.51, 0.55, 0.73),
 "thailaendischer-glasnudelsalat":(0.53, 0.52, 0.70),
 "yakisoba":                      (0.53, 0.55, 0.77),
}

# Zielanteil des Tellers an der Bildbreite.
#
# 0,80 war zu formatfuellend — der Teller stand bis fast an den Rand. 0,72 gibt
# spuerbar mehr Luft und ist fuer neun der zwanzig Vorlagen exakt erreichbar;
# die uebrigen bleiben groesser, weil im Original schlicht kein Rand mehr da ist.
#
# Kleinere Werte bringen nichts: Bei 0,65 erreicht nur noch ein einziges Bild
# das Ziel, alle anderen liegen zwischen 0,65 und 1,00 — die Streuung waere also
# groesser statt kleiner. Fehlenden Rand durch eine unscharfe Fortsetzung des
# Bildes zu ergaenzen wurde getestet und verworfen: Beim Java Curry entstand ein
# sichtbarer heller Ring, beim Hoisin Chicken eine senkrechte Kante.
ZIEL_D = 0.72
