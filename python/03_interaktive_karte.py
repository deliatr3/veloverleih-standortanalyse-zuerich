# ============================================================
# VELOVERLEIH STANDORTANALYSE ZÜRICH
# Person C – Interaktive Web-Karte mit Folium
# ============================================================
# Voraussetzungen (in GitHub Codespaces Terminal ausführen):
#   pip install folium
#
# Dieses Script erstellt eine interaktive Karte (karte.html)
# die ihr direkt im Browser öffnen und in der Präsentation
# live demonstrieren könnt!
# ============================================================

import folium
from folium.plugins import HeatMap, MeasureControl, Fullscreen
import json

# ── KARTE INITIALISIEREN ──────────────────────────────────────────────────────
karte = folium.Map(
    location=[47.3769, 8.5417],  # Zentrum Zürich
    zoom_start=13,
    tiles="CartoDB positron",    # Cleaner, heller Hintergrund
    control_scale=True,
)

# Vollbild-Button hinzufügen
Fullscreen().add_to(karte)
MeasureControl(position="topleft").add_to(karte)

# ── LAYER-GRUPPEN ERSTELLEN ───────────────────────────────────────────────────
layer_bahnhoefe      = folium.FeatureGroup(name="🚉 Bahnhöfe & S-Bahn", show=True)
layer_velowege       = folium.FeatureGroup(name="🚲 Velowege (Buffer)", show=False)
layer_tourismus      = folium.FeatureGroup(name="🏛️ Tourismus-Hotspots", show=True)
layer_verleihe       = folium.FeatureGroup(name="🚴 Bestehende Verleihe", show=True)
layer_top3           = folium.FeatureGroup(name="⭐ Top-3 Empfehlungen", show=True)
layer_stadtkreise    = folium.FeatureGroup(name="🗺️ Stadtkreise Scoring", show=True)

# ── DATEN: BAHNHÖFE ───────────────────────────────────────────────────────────
# Wichtige Bahnhöfe in Zürich (aus OSM/QuickOSM exportiert und hier eingetragen)
bahnhoefe = [
    {"name": "Zürich HB", "lat": 47.3784, "lon": 8.5403, "typ": "Hauptbahnhof"},
    {"name": "Zürich Stadelhofen", "lat": 47.3657, "lon": 8.5483, "typ": "S-Bahn"},
    {"name": "Zürich Enge", "lat": 47.3617, "lon": 8.5323, "typ": "S-Bahn"},
    {"name": "Zürich Hardbrücke", "lat": 47.3852, "lon": 8.5193, "typ": "S-Bahn"},
    {"name": "Zürich Oerlikon", "lat": 47.4114, "lon": 8.5444, "typ": "S-Bahn"},
    {"name": "Zürich Wiedikon", "lat": 47.3697, "lon": 8.5178, "typ": "S-Bahn"},
    {"name": "Zürich Altstetten", "lat": 47.3909, "lon": 8.4892, "typ": "S-Bahn"},
    {"name": "Zürich Tiefenbrunnen", "lat": 47.3550, "lon": 8.5617, "typ": "S-Bahn"},
]

for bhf in bahnhoefe:
    farbe = "darkblue" if bhf["typ"] == "Hauptbahnhof" else "blue"
    folium.Marker(
        location=[bhf["lat"], bhf["lon"]],
        popup=folium.Popup(f"<b>{bhf['name']}</b><br>{bhf['typ']}", max_width=200),
        tooltip=bhf["name"],
        icon=folium.Icon(color=farbe, icon="train", prefix="fa"),
    ).add_to(layer_bahnhoefe)

    # 500m Buffer um Bahnhöfe
    folium.Circle(
        location=[bhf["lat"], bhf["lon"]],
        radius=500,
        color="#065A82",
        fill=True,
        fill_color="#065A82",
        fill_opacity=0.08,
        weight=1.5,
        tooltip=f"500m Buffer: {bhf['name']}",
    ).add_to(layer_velowege)

# ── DATEN: TOURISMUS-HOTSPOTS ─────────────────────────────────────────────────
tourismus_pois = [
    {"name": "Kunsthaus Zürich", "lat": 47.3700, "lon": 8.5484},
    {"name": "Landesmuseum", "lat": 47.3812, "lon": 8.5395},
    {"name": "Grossmünster", "lat": 47.3699, "lon": 8.5441},
    {"name": "Fraumünster", "lat": 47.3695, "lon": 8.5414},
    {"name": "Zoo Zürich", "lat": 47.3857, "lon": 8.5743},
    {"name": "Zürichsee Promenade", "lat": 47.3623, "lon": 8.5437},
    {"name": "Lindenhügel", "lat": 47.3729, "lon": 8.5399},
    {"name": "Bahnhofstrasse", "lat": 47.3740, "lon": 8.5367},
    {"name": "Bellevue Platz", "lat": 47.3663, "lon": 8.5451},
    {"name": "ETH Zürich", "lat": 47.3769, "lon": 8.5482},
]

for poi in tourismus_pois:
    folium.Marker(
        location=[poi["lat"], poi["lon"]],
        popup=folium.Popup(f"<b>🏛️ {poi['name']}</b>", max_width=200),
        tooltip=poi["name"],
        icon=folium.Icon(color="orange", icon="star", prefix="fa"),
    ).add_to(layer_tourismus)

    # 400m Buffer um Tourismus
    folium.Circle(
        location=[poi["lat"], poi["lon"]],
        radius=400,
        color="#F59E0B",
        fill=True,
        fill_color="#F59E0B",
        fill_opacity=0.06,
        weight=1,
    ).add_to(layer_tourismus)

# ── DATEN: BESTEHENDE VERLEIHE ────────────────────────────────────────────────
verleihe = [
    {"name": "PubliBike – HB", "lat": 47.3782, "lon": 8.5390},
    {"name": "PubliBike – Bellevue", "lat": 47.3659, "lon": 8.5459},
    {"name": "PubliBike – Enge", "lat": 47.3613, "lon": 8.5327},
    {"name": "PubliBike – Oerlikon", "lat": 47.4103, "lon": 8.5441},
    {"name": "PubliBike – Stadelhofen", "lat": 47.3662, "lon": 8.5483},
]

for v in verleihe:
    folium.Marker(
        location=[v["lat"], v["lon"]],
        popup=folium.Popup(f"<b>🚴 {v['name']}</b><br><i>Bestehender Verleih</i>", max_width=200),
        tooltip=v["name"],
        icon=folium.Icon(color="red", icon="bicycle", prefix="fa"),
    ).add_to(layer_verleihe)

# ── HEATMAP: Potenzialzonen ───────────────────────────────────────────────────
# Kombiniert Bahnhofs- und Tourismuspunkte für Heatmap
heatmap_punkte = (
    [[b["lat"], b["lon"], 1.0] for b in bahnhoefe] +
    [[p["lat"], p["lon"], 0.8] for p in tourismus_pois]
)

HeatMap(
    heatmap_punkte,
    name="🌡️ Heatmap Potenzial",
    min_opacity=0.3,
    max_zoom=18,
    radius=55,
    blur=35,
    gradient={"0.2": "#A8D5B5", "0.5": "#2D7D52", "0.8": "#1A4731", "1.0": "#FF4444"},
).add_to(karte)

# ── TOP-3 STANDORTEMPFEHLUNGEN ────────────────────────────────────────────────
top3_standorte = [
    {
        "rang": 1,
        "name": "Kreis 1 – Altstadt",
        "lat": 47.3729,
        "lon": 8.5411,
        "score": 87,
        "begruendung": "Höchste Tourismusdichte, direkt am HB, beste Buffer-Überlagerung aller Kriterien.",
        "farbe": "#1A4731",
    },
    {
        "rang": 2,
        "name": "Kreis 4 – Aussersihl",
        "lat": 47.3769,
        "lon": 8.5267,
        "score": 79,
        "begruendung": "Sehr hohe Einwohnerdichte, gute ÖV-Anbindung (HB & Tram), kaum Konkurrenz.",
        "farbe": "#2D7D52",
    },
    {
        "rang": 3,
        "name": "Kreis 6 – Unterstrass",
        "lat": 47.3891,
        "lon": 8.5439,
        "score": 74,
        "begruendung": "Nähe zu Universität & HB, starke Velo-Infrastruktur, junges Publikum.",
        "farbe": "#A8D5B5",
    },
]

medaillen = ["🥇", "🥈", "🥉"]
for standort, medaille in zip(top3_standorte, medaillen):
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; width: 220px;">
        <h4 style="color: #1A4731; margin: 0 0 8px 0;">{medaille} {standort['name']}</h4>
        <div style="background: #1A4731; color: white; padding: 4px 10px; border-radius: 12px;
                    display: inline-block; font-weight: bold; margin-bottom: 8px;">
            Score: {standort['score']} / 100
        </div>
        <p style="color: #374151; font-size: 12px; margin: 0;">{standort['begruendung']}</p>
    </div>
    """
    folium.Marker(
        location=[standort["lat"], standort["lon"]],
        popup=folium.Popup(popup_html, max_width=240),
        tooltip=f"{medaille} {standort['name']} – Score: {standort['score']}/100",
        icon=folium.Icon(color="green", icon="star", prefix="fa"),
    ).add_to(layer_top3)

    # Einzugsgebiet (Empfehlungsbereich)
    folium.Circle(
        location=[standort["lat"], standort["lon"]],
        radius=600,
        color=standort["farbe"],
        fill=True,
        fill_color=standort["farbe"],
        fill_opacity=0.12,
        weight=2.5,
        dash_array="8",
        tooltip=f"Empfohlenes Einzugsgebiet: {standort['name']}",
    ).add_to(layer_top3)

# ── STADTKREISE SCORING (vereinfachte Choroplethenkarte) ──────────────────────
scoring_kreise = [
    {"name": "Kreis 1", "lat": 47.3729, "lon": 8.5411, "score": 87},
    {"name": "Kreis 2", "lat": 47.3600, "lon": 8.5250, "score": 58},
    {"name": "Kreis 3", "lat": 47.3700, "lon": 8.5100, "score": 66},
    {"name": "Kreis 4", "lat": 47.3769, "lon": 8.5267, "score": 79},
    {"name": "Kreis 5", "lat": 47.3869, "lon": 8.5200, "score": 63},
    {"name": "Kreis 6", "lat": 47.3891, "lon": 8.5439, "score": 74},
    {"name": "Kreis 7", "lat": 47.3790, "lon": 8.5650, "score": 55},
    {"name": "Kreis 8", "lat": 47.3560, "lon": 8.5490, "score": 61},
    {"name": "Kreis 9", "lat": 47.3830, "lon": 8.4950, "score": 47},
    {"name": "Kreis 10", "lat": 47.4000, "lon": 8.5180, "score": 51},
    {"name": "Kreis 11", "lat": 47.4120, "lon": 8.5430, "score": 56},
    {"name": "Kreis 12", "lat": 47.4120, "lon": 8.5700, "score": 42},
]

def score_to_color(score):
    if score >= 80: return "#1A4731"
    if score >= 70: return "#2D7D52"
    if score >= 60: return "#5DAF80"
    if score >= 50: return "#A8D5B5"
    return "#D4EDDA"

for k in scoring_kreise:
    folium.CircleMarker(
        location=[k["lat"], k["lon"]],
        radius=22,
        color="white",
        fill=True,
        fill_color=score_to_color(k["score"]),
        fill_opacity=0.75,
        weight=2,
        popup=folium.Popup(f"<b>{k['name']}</b><br>Score: <b>{k['score']}/100</b>", max_width=150),
        tooltip=f"{k['name']}: {k['score']}/100",
    ).add_to(layer_stadtkreise)
    folium.Marker(
        location=[k["lat"], k["lon"]],
        icon=folium.DivIcon(
            html=f'<div style="font-size:10px;font-weight:bold;color:white;'
                 f'text-align:center;margin-top:6px;">{k["score"]}</div>',
            icon_size=(44, 44),
            icon_anchor=(22, 22),
        ),
    ).add_to(layer_stadtkreise)

# ── ALLE LAYER ZUR KARTE HINZUFÜGEN ──────────────────────────────────────────
layer_stadtkreise.add_to(karte)
layer_bahnhoefe.add_to(karte)
layer_tourismus.add_to(karte)
layer_verleihe.add_to(karte)
layer_velowege.add_to(karte)
layer_top3.add_to(karte)

# ── LEGENDE ───────────────────────────────────────────────────────────────────
legende_html = """
<div style="position: fixed; bottom: 30px; left: 30px; z-index: 1000;
            background: white; padding: 15px 18px; border-radius: 10px;
            box-shadow: 0 3px 12px rgba(0,0,0,0.2); font-family: Arial, sans-serif;
            font-size: 12px; min-width: 170px;">
    <b style="color: #1A4731; font-size: 13px;">Scoring Stadtkreise</b><br><br>
    <span style="background:#1A4731;padding:2px 10px;border-radius:4px;color:white;">■</span>
    &nbsp;Score ≥ 80 (sehr hoch)<br><br>
    <span style="background:#2D7D52;padding:2px 10px;border-radius:4px;color:white;">■</span>
    &nbsp;Score 70–79 (hoch)<br><br>
    <span style="background:#5DAF80;padding:2px 10px;border-radius:4px;color:white;">■</span>
    &nbsp;Score 60–69 (mittel)<br><br>
    <span style="background:#A8D5B5;padding:2px 10px;border-radius:4px;">■</span>
    &nbsp;Score 50–59 (gering)<br><br>
    <span style="background:#D4EDDA;padding:2px 10px;border-radius:4px;">■</span>
    &nbsp;Score &lt; 50 (tief)
</div>
"""
karte.get_root().html.add_child(folium.Element(legende_html))

# Layer-Control (zum Ein-/Ausblenden)
folium.LayerControl(position="topright", collapsed=False).add_to(karte)

# ── KARTE SPEICHERN ───────────────────────────────────────────────────────────
karte.save("karte.html")
print("✅ Interaktive Karte gespeichert: karte.html")
print("   → Datei im Browser öffnen (Doppelklick auf karte.html)")
print("   → Für Präsentation: Screenshot machen ODER live im Browser zeigen!")
print()
print("Tipp: Ihr könnt die karte.html auch ins GitHub Repo pushen")
print("und mit GitHub Pages online veröffentlichen!")
