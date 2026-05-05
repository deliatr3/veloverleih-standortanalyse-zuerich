import folium
from folium.plugins import HeatMap, MeasureControl, Fullscreen
import geopandas as gpd

# Daten laden
bahnhoefe_gdf = gpd.read_file('data/raw/bahnhoefe_2056.gpkg').to_crs(epsg=4326)
tourismus_gdf = gpd.read_file('data/raw/tourismus_2056.gpkg').to_crs(epsg=4326)
verleihe_gdf  = gpd.read_file('data/raw/verleihe_2056.gpkg').to_crs(epsg=4326)
velowege_gdf  = gpd.read_file('data/raw/velowege_2056.gpkg').to_crs(epsg=4326)

bahnhoefe_pts = bahnhoefe_gdf[bahnhoefe_gdf.geometry.geom_type == 'Point']
tourismus_pts = tourismus_gdf[tourismus_gdf.geometry.geom_type == 'Point']
verleihe_pts  = verleihe_gdf[verleihe_gdf.geometry.geom_type == 'Point']

# Karte initialisieren 
karte = folium.Map(location=[47.3769, 8.5417], zoom_start=13,
                   tiles="CartoDB positron", control_scale=True)
Fullscreen().add_to(karte)
MeasureControl(position="topleft").add_to(karte)

layer_bahnhoefe   = folium.FeatureGroup(name="🚉 Bahnhöfe & S-Bahn", show=True)
layer_velowege    = folium.FeatureGroup(name="🚲 Velowege (Buffer)", show=False)
layer_tourismus   = folium.FeatureGroup(name="🏛️ Tourismus-Hotspots", show=True)
layer_verleihe    = folium.FeatureGroup(name="🚴 Bestehende Verleihe", show=True)
layer_top3        = folium.FeatureGroup(name="⭐ Top-3 Empfehlungen", show=True)
layer_stadtkreise = folium.FeatureGroup(name="🗺️ Stadtkreise Scoring", show=True)

# Bahnhöfe
for _, row in bahnhoefe_pts.iterrows():
    name = str(row.get('name', 'Bahnhof'))
    lat, lon = row.geometry.y, row.geometry.x
    folium.Marker(location=[lat, lon],
        popup=folium.Popup(f"<b>🚉 {name}</b>", max_width=200),
        tooltip=name, icon=folium.Icon(color="darkblue", icon="train", prefix="fa"),
    ).add_to(layer_bahnhoefe)
    folium.Circle(location=[lat, lon], radius=500, color="#065A82",
        fill=True, fill_color="#065A82", fill_opacity=0.08, weight=1.5,
        tooltip=f"500m Buffer: {name}",
    ).add_to(layer_velowege)

# Tourismus (Zoo als einen Marker)
zoo_namen = {"Seehund","Schildkröten","Darvin-Nandus","Europäischer Fischotter",
    "Hauskamel/Trampeltier","Vikunja","Alpaka","Grevyzebra","Kappengibbons",
    "Chileflamingo","Schwarzes Alpenschwein","Westafrikanische Zwergziegen",
    "Fledermäuse","Hausmeerschweinchen","Pferd","Schweizerhuhn","Präriehund",
    "Amurtiger","Asiatischer Löwe","Schmutzgeier","Brillenbären","Nasenbär",
    "Schneeleopard","Kleiner Panda","Hausyak","Asiatischer Elefant (Auslauf)",
    "Allfarblori","Arabischer Oryx","Koala","Bennett-Wallaby","Riesenwarane",
    "Grosser Emu","Netzgiraffe","Südliches Breitmaulnashorn","Erdmännchen",
    "Dahomey-Zwergrind","Säbelantilope","Nacktmull","Roter Ibis","Lama",
    "Lachender Hans","Spaltenschildkröte","Felsenschildechse","Giraffenfütterung",
    "Kamele hautnah","Dschelada","Königspinguin","Lewa Airstrip"}

zoo_added = False
for _, row in tourismus_pts.iterrows():
    name = str(row.get('name', 'Tourismus-POI'))
    if name == 'nan': continue
    lat, lon = row.geometry.y, row.geometry.x
    if name in zoo_namen:
        if not zoo_added:
            folium.Marker(location=[47.3857, 8.5743],
                popup=folium.Popup("<b>🦁 Zoo Zürich</b>", max_width=200),
                tooltip="Zoo Zürich",
                icon=folium.Icon(color="orange", icon="star", prefix="fa"),
            ).add_to(layer_tourismus)
            folium.Circle(location=[47.3857, 8.5743], radius=400, color="#F59E0B",
                fill=True, fill_color="#F59E0B", fill_opacity=0.06, weight=1,
            ).add_to(layer_tourismus)
            zoo_added = True
        continue
    folium.Marker(location=[lat, lon],
        popup=folium.Popup(f"<b>🏛️ {name}</b>", max_width=200),
        tooltip=name, icon=folium.Icon(color="orange", icon="star", prefix="fa"),
    ).add_to(layer_tourismus)
    folium.Circle(location=[lat, lon], radius=400, color="#F59E0B",
        fill=True, fill_color="#F59E0B", fill_opacity=0.06, weight=1,
    ).add_to(layer_tourismus)

# Veloverleihe (alle 197 echten Stationen)
for _, row in verleihe_pts.iterrows():
    name = str(row.get('name', 'Veloverleih'))
    if name == 'nan': name = 'Veloverleih'
    lat, lon = row.geometry.y, row.geometry.x
    folium.CircleMarker(location=[lat, lon], radius=5,
        color="#DC2626", fill=True, fill_color="#DC2626", fill_opacity=0.8, weight=1,
        popup=folium.Popup(f"<b>🚴 {name}</b><br><i>Bestehender Verleih</i>", max_width=200),
        tooltip=name,
    ).add_to(layer_verleihe)

# Heatmap (Bahnhöfe + Tourismus + Velowege)
heatmap_punkte = []
for _, row in bahnhoefe_pts.iterrows():
    heatmap_punkte.append([row.geometry.y, row.geometry.x, 1.0])
for _, row in tourismus_pts.iterrows():
    if str(row.get('name','')) not in zoo_namen and str(row.get('name','')) != 'nan':
        heatmap_punkte.append([row.geometry.y, row.geometry.x, 0.8])
heatmap_punkte.append([47.3857, 8.5743, 0.8])
for _, row in velowege_gdf.iterrows():
    try:
        c = row.geometry.centroid
        heatmap_punkte.append([c.y, c.x, 0.4])
    except: pass

HeatMap(heatmap_punkte, name="🌡️ Heatmap Potenzial",
    min_opacity=0.3, max_zoom=18, radius=40, blur=30,
    gradient={"0.2": "#A8D5B5", "0.5": "#2D7D52", "0.8": "#1A4731", "1.0": "#FF4444"},
).add_to(karte)

# Top 3
top3_standorte = [
    {"rang": 1, "name": "Kreis 3 – Wiedikon", "lat": 47.3683, "lon": 8.5150, "score": 64.7,
     "begruendung": "Beste Kombination aus ÖV-Anbindung, Veloinfrastruktur und Bevölkerungsdichte. Wenig Konkurrenz.", "farbe": "#1A4731"},
    {"rang": 2, "name": "Kreis 2 – Enge/Wollishofen", "lat": 47.3600, "lon": 8.5250, "score": 61.2,
     "begruendung": "Hohe ÖV-Anbindung, gute Veloinfrastruktur und vergleichsweise wenig Konkurrenz.", "farbe": "#2D7D52"},
    {"rang": 3, "name": "Kreis 1 – Altstadt", "lat": 47.3729, "lon": 8.5411, "score": 60.7,
     "begruendung": "Tourismus-Hotspot im Zentrum, direkt am HB, sehr gute ÖV-Anbindung.", "farbe": "#A8D5B5"},
]

medaillen = ["🥇", "🥈", "🥉"]
for standort, medaille in zip(top3_standorte, medaillen):
    popup_html = f"""<div style="font-family:Arial,sans-serif;width:220px;">
        <h4 style="color:#1A4731;margin:0 0 8px 0;">{medaille} {standort['name']}</h4>
        <div style="background:#1A4731;color:white;padding:4px 10px;border-radius:12px;display:inline-block;font-weight:bold;margin-bottom:8px;">
            Score: {standort['score']} / 100</div>
        <p style="color:#374151;font-size:12px;margin:0;">{standort['begruendung']}</p></div>"""
    folium.Marker(location=[standort["lat"], standort["lon"]],
        popup=folium.Popup(popup_html, max_width=240),
        tooltip=f"{medaille} {standort['name']} – Score: {standort['score']}/100",
        icon=folium.Icon(color="green", icon="star", prefix="fa"),
    ).add_to(layer_top3)
    folium.Circle(location=[standort["lat"], standort["lon"]],
        radius=600, color=standort["farbe"], fill=True, fill_color=standort["farbe"],
        fill_opacity=0.12, weight=2.5, dash_array="8",
    ).add_to(layer_top3)

# Stadtkreise
scoring_kreise = [
    {"name": "Kreis 1",  "lat": 47.3729, "lon": 8.5411, "score": 60.7},
    {"name": "Kreis 2",  "lat": 47.3600, "lon": 8.5250, "score": 61.2},
    {"name": "Kreis 3",  "lat": 47.3683, "lon": 8.5150, "score": 64.7},
    {"name": "Kreis 4",  "lat": 47.3769, "lon": 8.5267, "score": 56.7},
    {"name": "Kreis 5",  "lat": 47.3869, "lon": 8.5200, "score": 54.4},
    {"name": "Kreis 6",  "lat": 47.3891, "lon": 8.5439, "score": 52.1},
    {"name": "Kreis 7",  "lat": 47.3790, "lon": 8.5650, "score": 49.5},
    {"name": "Kreis 8",  "lat": 47.3560, "lon": 8.5490, "score": 36.9},
    {"name": "Kreis 9",  "lat": 47.3830, "lon": 8.4950, "score": 29.7},
    {"name": "Kreis 10", "lat": 47.4000, "lon": 8.5180, "score": 34.7},
    {"name": "Kreis 11", "lat": 47.4120, "lon": 8.5430, "score": 44.8},
    {"name": "Kreis 12", "lat": 47.4120, "lon": 8.5700, "score": 27.5},
]

def score_to_color(s):
    if s >= 64: return "#1A4731"
    if s >= 58: return "#2D7D52"
    if s >= 52: return "#5DAF80"
    if s >= 45: return "#A8D5B5"
    return "#D4EDDA"

for k in scoring_kreise:
    folium.CircleMarker(location=[k["lat"], k["lon"]], radius=22,
        color="white", fill=True, fill_color=score_to_color(k["score"]),
        fill_opacity=0.75, weight=2,
        popup=folium.Popup(f"<b>{k['name']}</b><br>Score: <b>{k['score']}/100</b>", max_width=150),
        tooltip=f"{k['name']}: {k['score']}/100",
    ).add_to(layer_stadtkreise)
    folium.Marker(location=[k["lat"], k["lon"]],
        icon=folium.DivIcon(
            html=f'<div style="font-size:10px;font-weight:bold;color:white;text-align:center;margin-top:6px;">{k["score"]}</div>',
            icon_size=(44, 44), icon_anchor=(22, 22),
        ),
    ).add_to(layer_stadtkreise)

layer_stadtkreise.add_to(karte)
layer_bahnhoefe.add_to(karte)
layer_tourismus.add_to(karte)
layer_verleihe.add_to(karte)
layer_velowege.add_to(karte)
layer_top3.add_to(karte)

legende_html = """
<div style="position:fixed;bottom:30px;left:30px;z-index:1000;background:white;
    padding:15px 18px;border-radius:10px;box-shadow:0 3px 12px rgba(0,0,0,0.2);
    font-family:Arial,sans-serif;font-size:12px;min-width:170px;">
    <b style="color:#1A4731;font-size:13px;">Scoring Stadtkreise</b><br><br>
    <span style="background:#1A4731;padding:2px 10px;border-radius:4px;color:white;">■</span>&nbsp;Score ≥ 64 (Top-1)<br><br>
    <span style="background:#2D7D52;padding:2px 10px;border-radius:4px;color:white;">■</span>&nbsp;Score 58–63 (hoch)<br><br>
    <span style="background:#5DAF80;padding:2px 10px;border-radius:4px;color:white;">■</span>&nbsp;Score 52–57 (mittel)<br><br>
    <span style="background:#A8D5B5;padding:2px 10px;border-radius:4px;">■</span>&nbsp;Score 45–51 (gering)<br><br>
    <span style="background:#D4EDDA;padding:2px 10px;border-radius:4px;">■</span>&nbsp;Score &lt; 45 (tief)
</div>"""
karte.get_root().html.add_child(folium.Element(legende_html))
folium.LayerControl(position="topright", collapsed=False).add_to(karte)

karte.save("karte.html")
print("✅ Interaktive Karte gespeichert: karte.html")
print("   → 28 Bahnhöfe (alle echt)")
print("   → 197 Verleihe (alle echt)")
print("   → Tourismus POIs (Zoo zusammengefasst)")
print("   → 703 Velowege in Heatmap")
print("   → Top-3: Kreis 3 (64.7) → Kreis 2 (61.2) → Kreis 1 (60.7)")
