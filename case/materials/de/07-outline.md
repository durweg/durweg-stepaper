[中文](../zh/07-outline.md) · [English](../en/07-outline.md) · [Deutsch](../de/07-outline.md)

# Foliengliederung

Abbildungen aus dem Paper tragen ihre Quelle: Ronneberger et al., MICCAI 2015, arXiv:1505.04597, nur für das eigene Verständnis.

10 Folien (Standard sind 8; „Methode“ ist auf 3 Folien aufgeteilt, damit jede nur eine Sache behandelt). Jede Folie: Titel = ihre Schlussfolgerung in einem Satz; darunter, was auf die Folie kommt.

| # | Beantwortete Frage | Titel (Schlussfolgerung in einem Satz) | Inhalt |
|---|---|---|---|
| 1 | Welches Problem löst das Paper? | Ein paar Dutzend annotierte Bilder reichen, um ein präzises Segmentierungsnetz zu trainieren | Titel, Autoren, Venue; die Kernaussage in einem Satz |
| 2 | Was war an der bisherigen Methode schlecht? | Das Sliding Window entscheidet Ausschnitt für Ausschnitt: langsam, und „weit sehen“ und „genau lokalisieren“ ziehen gegeneinander | Eigene Skizze: ein Ausschnitt wandert schrittweise über das Bild; eine Zeile pro Nachteil |
| 3 | Methode 1: Wie sieht das Netz aus? | U-Net = Encoder–Decoder + eine Skip-Verbindung auf jeder Ebene, das ganze Bild in einem Durchgang | Paper Abb. 1; markiert: verkleinernde linke Seite, vergrößernde rechte Seite, hinübergereichte Details |
| 4 | Methode 2: Was, wenn es zu wenige Bilder gibt? | Elastische Verformung macht aus vorhandenen Bildern neue, ohne neue Annotation | Original gegen drei verformte Versionen; warum Gewebe zu elastischer Verformung passt |
| 5 | Methode 3: Wie werden sich berührende Zellen getrennt? | Die schmalen Lücken zwischen Zellen gewichten, damit das Netz sie trennen lernt | Paper Abb. 3 (c Segmentierungskarte, d Gewichtskarte) |
| 6 | Was löst jeder Teil? | Jeder Teil beantwortet eines der ursprünglichen Probleme | Drei Zeilen: U-Form → Zielkonflikt und Geschwindigkeit; Augmentierung → wenige Daten; Gewichtung → verschmolzene Zellen |
| 7 | Wie wurde getestet? | Drei öffentliche Challenges, die Lösungen liegen bei den Veranstaltern | Tabelle: Datensatz, Bildart, Trainingsbilder (30 / 35 / 20), Metrik |
| 8 | Wie sind die Ergebnisse (A gegen B)? | Ohne Nachbearbeitung schlägt U-Net das Sliding Window bereits | Auszug Tabelle 1: U-Net gegen IDSIA (Warping 0,000353 gegen 0,000420, Rand 0,0382 gegen 0,0504); Tabelle 2: IOU 0,92 gegen 0,83, 0,78 gegen 0,46 |
| 9 | Wie verlässlich ist der Schluss? | Die Punktzahlen sind glaubwürdig, aber es gibt keine Evidenz dafür, warum es besser ist | Vier Vorbehalte: Sliding Window mit Nachbearbeitung hat besseren Rand Error (0,0189, 0,0305); keine Ablation; „schneller“ nicht unter gleichen Bedingungen gemessen; nur Mikroskopie |
| 10 | Was nehmen wir mit? | Die Architektur ist direkt nutzbar; eine neue Aufgabe braucht eigene Experimente | Wiedergabe A gegen B in einem Satz; offene Fragen: ① Welche Ablationen zuerst auf neuen Daten? ② Padding oder kein Padding? |
