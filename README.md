# 🚴 Veloverleih Standortanalyse Zürich

**Modul:** Einsatz von Geodaten im Marketing  
**Institution:** ZHAW – Zürcher Hochschule für Angewandte Wissenschaften  
**Abgabe:** 27. Mai 2026  
**Gruppe:** Delia Troncato, Gioia Finocchi, Samira Bingesser

---

## 📋 Projektbeschreibung

Dieses Projekt analysiert mit Hilfe von Geomarketing-Methoden, welche Stadtkreise Zürichs das höchste Potenzial für einen neuen Veloverleih-Standort bieten. Dabei werden öffentlich verfügbare Geodaten aus OpenStreetMap sowie amtliche Statistikdaten der Stadt Zürich kombiniert.

### Forschungsfrage
> **Welche Stadtteile Zürichs bieten das höchste Potenzial für einen neuen Veloverleih-Standort?**

### Hypothesen
1. Stadtteile mit hoher ÖV-Anbindung und hoher Tourismusdichte haben das grösste Potenzial
2. Gebiete mit gut ausgebautem Velowegnetz fördern die Nutzungsbereitschaft
3. Stadtteile mit hoher Einwohnerdichte und Nähe zu touristischen Sehenswürdigkeiten erzielen den höchsten kombinierten Score

---

## 🗂️ Projektstruktur

```
veloverleih-standortanalyse-zuerich/
│
├── data/
│   ├── raw/                          ← Rohdaten (OSM-Exporte, Statistikdaten)
│   │   ├── bahnhoefe_2056.gpkg       ← Bahnhöfe & S-Bahn (EPSG:2056)
│   │   ├── tourismus_2056.gpkg       ← Tourismus-POIs (EPSG:2056)
│   │   ├── verleihe_2056.gpkg        ← Bestehende Veloverleih-Stationen
│   │   ├── velowege_2056.gpkg        ← Velowegnetz Zürich
│   │   ├── stadtkreise.geojson       ← Stadtkreisgrenzen Zürich (1–12)
│   │   └── bevoelkerungsdichte.csv   ← Bevölkerungsdichte pro Stadtkreis
│   │
│   └── processed/                    ← Verarbeitete Geodaten aus QGIS
│       ├── puffer_bahnhoefe.gpkg     ← 500m Buffer um Bahnhöfe
│       ├── puffer_tourismus.gpkg     ← 400m Buffer um Tourismus-POIs
│       ├── puffer_velowege.gpkg      ← 300m Buffer um Velowege
│       ├── heatmap_bahnhoefe.tif     ← Heatmap Bahnhöfe (Kerndichteschätzung)
│       ├── heatmap_tourismus.tif     ← Heatmap Tourismus
│       ├── heatmap_velowege.tif      ← Heatmap Velowege
│       └── heatmap_merged.tif        ← Gewichtete kombinierte Heatmap
│
├── exports/
│   └── karten/
│       ├── heatmap.png               ← Exportierte Heatmap-Karte (QGIS)
│       └── puffer_analyse.png        ← Exportierte Buffer-Analyse (QGIS)
│
├── präsentation/
│   └── Veloverleih_Standortanalyse_Zuerich.pptx
│
├── python/
│   ├── 02_scoring_analyse.py         ← Gewichtetes Scoring-Modell + Diagramme
│   └── 03_interaktive_karte.py       ← Interaktive Web-Karte (Folium)
│
├── qgis/
│   └── veloverleih_zuerich.qgz       ← QGIS-Projektfile
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔧 Setup & Installation

### Voraussetzungen
- Python 3.10 oder höher
- QGIS 3.40 LTR (für die Geodatenanalyse)
- Git

### 1. Repository klonen
```bash
git clone https://github.com/deliatr3/veloverleih-standortanalyse-zuerich.git
cd veloverleih-standortanalyse-zuerich
```

### 2. Python-Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 3. Scoring-Analyse ausführen
```bash
python python/02_scoring_analyse.py
```
→ Generiert `scoring_balkendiagramm.png` und `scoring_radar.png`

### 4. Interaktive Karte erstellen
```bash
python python/03_interaktive_karte.py
```
→ Generiert `karte.html` — im Browser öffnen für die interaktive Karte

---

## 📦 Abhängigkeiten

| Paket | Verwendung |
|---|---|
| `geopandas` | Räumliche Datenverarbeitung |
| `pandas` | Datenanalyse und Tabellen |
| `matplotlib` | Diagramme (Balken- & Radardiagramm) |
| `folium` | Interaktive Web-Karte |
| `shapely` | Geometrieoperationen |
| `numpy` | Numerische Berechnungen |
| `jupyter` | Jupyter Notebook Unterstützung |

---

## 🗺️ Methodik

### Datenquellen

| Datensatz | Quelle | Format |
|---|---|---|
| Bahnhöfe, Velowege, Tourismus, Verleihe | OpenStreetMap via QuickOSM | GeoPackage (.gpkg) |
| Stadtkreisgrenzen Zürich | Overpass Turbo | GeoJSON |
| Bevölkerungsdichte | statistik.stadt-zuerich.ch | CSV |

### Analyseschritte

**1. Datenbeschaffung (QGIS + QuickOSM)**
- OSM-Daten via QuickOSM-Plugin direkt in QGIS geladen
- Alle Layer auf EPSG:2056 (Schweizer Landeskoordinaten) umprojiziert

**2. Buffer-Analysen (QGIS)**
- 500m Buffer um Bahnhöfe → ÖV-Einzugsgebiet
- 400m Buffer um Tourismus-POIs → Tourismus-Einzugsgebiet
- 300m Buffer um Velowege → Fahrradfreundliche Zone

**3. Heatmap / Kerndichteschätzung (QGIS)**
- Separate Heatmaps für Bahnhöfe, Tourismus und Velowege
- Gewichtete Kombination via Rasterrechner:
  ```
  (heatmap_bahnhoefe * 0.45) + (heatmap_tourismus * 0.30) + (heatmap_velowege * 0.25)
  ```

**4. Scoring-Modell (Python)**

Gewichtetes Scoring pro Stadtkreis basierend auf 5 Kriterien:

| Kriterium | Gewicht | Datenquelle |
|---|---|---|
| ÖV-Anbindung | 30% | Bahnhofzählungen aus OSM |
| Veloinfrastruktur | 25% | Velowege-Layer aus OSM |
| Bevölkerungsdichte | 20% | statistik.stadt-zuerich.ch |
| Tourismus-Hotspots | 15% | Tourismus-POIs aus OSM |
| Keine Konkurrenz | 10% | Verleihe-Layer aus OSM (invertiert) |

**5. Interaktive Web-Karte (Python / Folium)**
- Alle Layer interaktiv ein-/ausblendbar
- 28 echte Bahnhöfe, 197 echte Verleihe, alle Tourismus-POIs
- Top-3 Standorte mit Begründung als Popup

---

## 📊 Ergebnisse

### Top-3 Standortempfehlungen

| Rang | Stadtkreis | Score |
|---|---|---|
| 🥇 1 | Kreis 3 – Wiedikon | 64.7 / 100 |
| 🥈 2 | Kreis 2 – Enge/Wollishofen | 61.2 / 100 |
| 🥉 3 | Kreis 1 – Altstadt | 60.7 / 100 |

### Interpretation
- **Kreis 3** überzeugt durch die beste Kombination aus ÖV-Anbindung, Veloinfrastruktur und hoher Bevölkerungsdichte bei gleichzeitig wenig bestehender Konkurrenz
- **Kreis 1** ist touristisch am stärksten, verliert aber Punkte durch die hohe Verleih-Dichte
- Die visuelle Heatmap bestätigt das Stadtzentrum als heisseste Zone, das Scoring differenziert feiner nach Marktpotenzial

---

## 🛠️ Tools & Software

| Tool | Version | Verwendung |
|---|---|---|
| QGIS | 3.40 LTR | Buffer-Analyse, Heatmap, Kartenexport |
| QuickOSM Plugin | 2.x | OSM-Datenabfragen in QGIS |
| Python | 3.12 | Scoring-Modell, Visualisierung |
| GeoPandas | 1.x | Räumliche Datenverarbeitung |
| Folium | 0.x | Interaktive Web-Karte |
| Matplotlib | 3.x | Diagramme |
| GitHub Codespaces | - | Gemeinsame Entwicklungsumgebung |
| Google Earth Pro | - | Visuelle Verifikation Top-3 Standorte |

---

## 📚 Quellen

- OpenStreetMap Contributors (2024). *OpenStreetMap*. https://www.openstreetmap.org
- Stadt Zürich – Open Data Katalog (2024). https://data.stadt-zuerich.ch
- Statistik Stadt Zürich (2024). *Bevölkerungsdichte nach Stadtkreis*. https://statistik.stadt-zuerich.ch
- QGIS Development Team (2024). *QGIS Geographic Information System*, Version 3.40. https://qgis.org
- Cliquet, G. (2006). *Geomarketing: Methods and Strategies in Spatial Marketing*. ISTE.
- Folium Documentation (2024). https://python-visualization.github.io/folium/

---

## 👥 Gruppe

| Person | Aufgabe |
|---|---|
| Delia Troncato | QGIS-Analyse, Geodaten, Buffer, Heatmap |
| [Name Person B] | Python Scoring-Modell, Diagramme, Auswertung |
| [Name Person C] | Interaktive Web-Karte (Folium), Präsentation |
