[中文](../zh/05-metrics.md) · [English](../en/05-metrics.md) · [Deutsch](../de/05-metrics.md)

# Erklärung der Metriken

Jede Bewertungsmetrik im Paper (arXiv:1505.04597, Abschnitt 4, Tabellen 1 und 2). Zu jeder: wofür sie da ist und wie man sie liest. Kurz genug zum Wiedergeben.

**Überblick**

| Metrik | Wo im Paper | Besser, wenn | Mensch / bester Wert im Paper | U-Net |
|---|---|---|---|---|
| Warping Error | EM-Aufgabe, Tabelle 1 | kleiner | Mensch 0,000005 | 0,000353 (Platz 1) |
| Rand Error | EM-Aufgabe, Tabelle 1 | kleiner | Mensch 0,0021 | 0,0382 |
| Pixel Error | EM-Aufgabe, Tabelle 1 | kleiner | Mensch 0,0010 | 0,0611 |
| IOU | Zellaufgaben, Tabelle 2 | größer (max. 1) | — | 0,92 (PhC-U373), 0,78 (DIC-HeLa) |

### Pixel Error (Pixelfehler)

- **Wofür**: die einfachste Prüfung — wie viele Pixel das falsche Label haben (Zelle oder Membran).
- **Wie lesen**: Anteil falscher Pixel, von 0 (alles richtig) bis 1 (alles falsch); kleiner ist besser. U-Nets 0,0611 heißt: etwa 6 % der Pixel sind falsch.
- **Achtung**: Jedes Pixel zählt gleich, daher ändert eine Unterbrechung von einem Pixel in einer dünnen Membran, die zwei Zellen verschmilzt, die Zahl kaum. Deshalb nutzt die EM-Challenge auch die nächsten zwei Metriken.

### Rand Error

- **Wofür**: prüft, ob das Bild in die richtigen **Objekte** (Zellen) zerlegt ist, nicht nur, ob Pixel stimmen.
- **Wie lesen**: Pixelpaare nehmen und fragen „gleiche Zelle oder verschiedene Zellen?“; der Rand Error ist der Anteil der Paare, bei denen die Antwort von der Referenz abweicht. Von 0 bis 1; kleiner ist besser. U-Net 0,0382 ≈ 4 % der Paare falsch beurteilt.
- **Achtung**: Eine kleine Lücke in einer Membran, die zwei Zellen verschmilzt, macht viele Paare falsch; diese Metrik bestraft also Verschmelzungen und Aufspaltungen, die der Pixel Error kaum sieht.

### Warping Error

- **Wofür**: zählt nur **topologische** Fehler — fälschlich verschmolzene, aufgespaltene Zellen oder Löcher — und verzeiht kleine Verschiebungen der Ränder.
- **Wie lesen**: Das Ergebnis darf sich zuerst leicht zur Referenz hin verbiegen, wo das die Topologie nicht ändert; die danach noch falschen Pixel sind der Warping Error. Kleiner ist besser; die Zahlen sind winzig (U-Net 0,000353, Mensch 0,000005), also nur untereinander vergleichen, nicht mit dem Pixel Error.
- **Warum wichtig**: Tabelle 1 ist nach dieser Metrik sortiert, und auf ihr liegt U-Net auf Platz 1.

Die drei EM-Metriken berechnen die Veranstalter mit ihren geheimen Referenzlösungen; sie schneiden die vorhergesagte Membrankarte an 10 Schwellen und werten aus (S. 6).

### IOU (Intersection over Union)

- **Wofür**: wie gut die vorhergesagte Zellfläche mit der wahren Zellfläche überlappt.
- **Wie lesen**: Überlappung ÷ von beiden zusammen bedeckte Fläche; 1 = perfekte Übereinstimmung, 0 = keine Überlappung; größer ist besser. U-Net 0,92 auf PhC-U373 gegen 0,83 für den Zweitbesten; 0,78 auf DIC-HeLa gegen 0,46.
- **Achtung**: Es ist ein Mittelwert über den Datensatz, ohne Fehlerbalken; das „significantly better“ des Papers stützt sich auf keinen statistischen Test.

### Jede Metrik in einem Satz (zum Wiedergeben)

- **Pixel Error**: Anteil falscher Pixel — kleiner ist besser.
- **Rand Error**: Anteil der Pixelpaare in der falschen Gruppe „gleiche / verschiedene Zelle“ — kleiner ist besser; bestraft verschmolzene oder aufgespaltene Zellen.
- **Warping Error**: nur Fehler, die die Zellanordnung ändern (Verschmelzungen, Aufspaltungen, Löcher) — kleiner ist besser; U-Net liegt hier auf Platz 1.
- **IOU**: Überlappung ÷ Vereinigung von vorhergesagter und wahrer Fläche — größer ist besser, 1 ist perfekt.

Hinweis: Das Paper definiert Warping Error und Rand Error nicht selbst, sondern verweist auf die Auswertung der Challenge (Literatur [14]). Die einfachen Erklärungen oben folgen den üblichen Definitionen dieser Metriken, nicht dem Text des Papers.
