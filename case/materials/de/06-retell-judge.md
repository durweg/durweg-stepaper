[中文](../zh/06-retell-judge.md) · [English](../en/06-retell-judge.md) · [Deutsch](../de/06-retell-judge.md)

# Wiedergeben und urteilen

Grundlage: Kernaussage, Diskussionsnotizen und Erklärung der Metriken. Wiedergabe und Urteil stammen vom Nutzer; unten in seinen Worten, übersetzt.

### Wiedergabe (A gegen B)

- **A**: U-Net (ganzes Bild auf einmal, U-förmiges Netz + Skip-Verbindungen, mit Augmentierung durch elastische Verformung und einem gewichteten Verlust für die Lücken zwischen Zellen).
- **B**: das Sliding-Window-Netz (Ciresan et al., entscheidet einen kleinen Ausschnitt nach dem anderen).
- **Schluss**: Bei Segmentierungsaufgaben funktioniert U-Net besser.

### Urteil

**Hat das Paper sein Problem gelöst?** Ja, für Segmentierungsaufgaben mit kleinen Datensätzen.

**Wie stark ist die Evidenz?** Alle Metriken und Ranglisten wurden fair von den Veranstaltern der Challenges vergeben, daher ist die Evidenz sehr glaubwürdig.
Ergänzung von Claude (vom Nutzer behalten): Glaubwürdig sind die Punktzahlen selbst. Nach Rand Error schlägt das Sliding Window mit datensatzspezifischer Nachbearbeitung (IDSIA-SCI 0,0189, DIVE-SCI 0,0305) U-Net (0,0382); genauer gilt also: „ohne Nachbearbeitung ist U-Net besser“.

**Mein Vorbehalt**: Es gibt kein Ablationsexperiment, daher lässt sich der Verdienst nicht zwischen Netzarchitektur, elastischer Verformung und gewichtetem Verlust aufteilen. Die Methode auf andere Datensätze zu übertragen, braucht deshalb womöglich mehr Abstimmung (Netzarchitektur, Nachbearbeitung), um das beste Ergebnis zu erreichen.

**Habe ich mein Ziel erreicht (das Paper verstehen)?** Ja. Ich habe das Netzdesign verstanden sowie Training und Ergebnisse in den Challenges; auch ihre „Nachbearbeitungsmethoden“ (Hinweis: U-Net selbst nutzt keine Nachbearbeitung; gemeint sind Trainingsmethoden wie Datenaugmentierung und gewichteter Verlust). Um ihre Methode für meine eigene Aufgabe zu nutzen, sind viele zusätzliche Experimente zur Anpassung nötig.
