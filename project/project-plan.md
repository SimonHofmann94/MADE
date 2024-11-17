# Project Plan

## Title
<!-- Give your project a short title. -->
Zusammenhänge zwischen Gesundheitsausgaben und Lebenserwartung in Nord-, Zentral- und Südamerika

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
Gibt es eine Korrelation zwischen den Gesundheitsausgaben pro Kopf und der Lebenserwartung in verschiedenen Ländern Amerikas?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
Das Projekt untersucht den Zusammenhang zwischen Gesundheitsausgaben und Lebenserwartung in Ländern Nord-, Zentral- und Südamerikas. Ziel ist es, herauszufinden, ob höhere Pro-Kopf-Gesundheitsausgaben mit einer höheren Lebenserwartung korrelieren und wie dieser Zusammenhang durch Faktoren wie das Einkommensniveau der Länder beeinflusst wird. Datenquellen wie die Weltbank und die WHO liefern die notwendigen Informationen zu Gesundheitsausgaben und Lebenserwartung.

## Datasources
World Bank Open Data: Umfangreiche Daten zu Gesundheitsausgaben pro Kopf, Lebenserwartung und Einkommensindikatoren
WHO Global Health Observatory: Detaillierte Informationen zu globalen Health Daten

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: WHO Global Health Observatory
* Metadata URL: https://www.who.int/data/gho/data/indicators/indicator-details/GHO/domestic-general-government-health-expenditure-(gghe-d)-as-percentage-of-general-government-expenditure-(gge)
* Data URL: https://www.who.int/data/gho/data/indicators/indicator-details/GHO/domestic-general-government-health-expenditure-(gghe-d)-as-percentage-of-general-government-expenditure-(gge)
* List of all indicators: https://www.who.int/data/gho/data/indicators
* Data Type: CSV

### Datasource1: World Bank Open Data
* Metadata URL: https://data.worldbank.org/indicator/SP.DYN.AMRT.MA?locations=BZ-AR&name_desc=false&view=chart
* Data URL: https://data.worldbank.org/indicator/SP.DYN.AMRT.MA?locations=BZ-AR&name_desc=false&view=chart
* List of all indicators: https://datacatalog.worldbank.org/search?q=health%20care&start=0&sort=
* Data Type: multiple different formats


## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

WP1: Projektplanung und Datenbeschaffung

1.1: Definition der Projektziele und Hypothesen.

1.2: Identifikation und Auswahl der relevanten Datenquellen (World Bank, WHO).

1.3: Zugriff und Download der benötigten Daten zu Gesundheitsausgaben, Lebenserwartung und Einkommensindikatoren.

1.4: Dokumentation der Datenquellen und Lizenzen.


WP2: Datenaufbereitung

2.1: Bereinigung der Daten (Entfernung fehlender oder fehlerhafter Einträge).

2.2: Zusammenführung der Datensätze in einer einheitlichen Datenstruktur, um regionale und zeitliche Vergleiche zu ermöglichen.


WP3: Explorative Datenanalyse (EDA)

3.1: Erstellung erster deskriptiver Statistiken für Gesundheitsausgaben und Lebenserwartung.

3.2: Visualisierung der Variablen nach Regionen und Einkommensniveaus

3.3: Identifikation von Datenmustern und ersten Trends.


WP4: Korrelationsanalyse

4.1: Berechnung von Korrelationskoeffizienten zwischen Gesundheitsausgaben und Lebenserwartung.


WP5: Vergleichsanalyse nach Region und Einkommensniveau

5.1: Vergleich der Ergebnisse zwischen Nord-, Zentral- und Südamerika.

5.2: Erstellung eines Berichts über regionale und einkommensspezifische Unterschiede.


WP6: Visualisierung und Ergebnispräsentation

6.1: Erstellung umfassender Visualisierungen zur Darstellung der Analyseergebnisse (Korrelationsmatrix, regionale Trends, Zeitreihen).

6.2: Entwicklung einer klar strukturierten Präsentation der Ergebnisse.

6.3: Interpretation und Erläuterung der Implikationen der Ergebnisse für politische Maßnahmen.


WP7: Berichterstellung und Dokumentation

7.1: Erstellung eines schriftlichen Abschlussberichts mit einer detaillierten Darstellung der Methodik, Ergebnisse und Implikationen.

7.2: Dokumentation aller Arbeitsschritte und genutzten Datenquellen.

7.3: Auflistung von Projektlimitationen und Vorschlägen für zukünftige Untersuchungen.

