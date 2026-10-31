[中文](../zh/03-core-claim.md) · [English](../en/03-core-claim.md) · [Deutsch](../de/03-core-claim.md)

# Kernaussage

**Das konkrete Problem**: In medizinischen Bildern muss **jedes einzelne Pixel** eine Klasse bekommen (Segmentierung), aber oft gibt es nur ein paar Dutzend annotierte Trainingsbilder. Tiefe Netze brauchten damals meist Tausende annotierter Bilder.

Die beste bisherige Methode (Ciresan et al., Sliding Window): einen kleinen Ausschnitt um ein Pixel herausschneiden und entscheiden, zu welcher Klasse dieses Pixel gehört. Das Paper nennt zwei Nachteile (Einleitung):
1. Langsam: Das Netz läuft für jeden Ausschnitt einzeln; benachbarte Ausschnitte überlappen stark, vieles wird doppelt berechnet.
2. Ein Zielkonflikt: Ein großer Ausschnitt sieht mehr Kontext, lokalisiert aber grob; ein kleiner lokalisiert genau, sieht aber wenig Kontext.

**Kernaussage**: Ein U-förmiges Netz (das Bild erst verkleinern, um das Ganze zu erfassen, dann wieder vergrößern, um zu lokalisieren, und die Details der verkleinernden Seite direkt hinüberreichen), kombiniert mit starker Datenaugmentierung (vor allem elastischen Verformungen), **lässt sich mit sehr wenigen annotierten Bildern trainieren und segmentiert genauer und schneller als die Sliding-Window-Methode**.

**Belege des Papers (Abstract)**:
- Neuronale Strukturen in der Elektronenmikroskopie (ISBI 2012): besser als die bisher beste Sliding-Window-Methode.
- Zellsegmentierung in der Lichtmikroskopie (ISBI Cell Tracking Challenge 2015): auf den zwei schwierigsten Datensätzen mit großem Abstand gewonnen.
- Geschwindigkeit: Ein 512×512-Bild dauert auf einer GPU weniger als eine Sekunde.
