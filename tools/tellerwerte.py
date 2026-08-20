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
 "java-curry":                    (0.51, 0.50, 0.93),
 "kimchi-bacon-udon":             (0.47, 0.52, 0.70),
 "mango-sticky-rice":             (0.57, 0.55, 0.70),   # Mitnahmebox statt Teller
 "massaman-thai-curry":           (0.52, 0.50, 0.65),
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

# Zielanteil des Tellers an der Bildbreite. 0,80 liegt oberhalb des Medians
# (0,73) und ist fuer 15 der 20 Vorlagen ohne Anschnitt erreichbar. Die fuenf
# darueber (0,82 bis 0,93) behalten ihren groesseren Teller — dort ist im
# Original schlicht kein Rand mehr uebrig.
ZIEL_D = 0.80
