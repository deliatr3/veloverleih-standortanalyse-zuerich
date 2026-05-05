# ============================================================
# VELOVERLEIH STANDORTANALYSE ZÜRICH
# ============================================================
# Voraussetzungen (in GitHub Codespaces Terminal ausführen):
#   pip install geopandas pandas matplotlib folium shapely
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Alle Werte basieren auf echten Daten:
# OeV_Anbindung:    gezählt aus bahnhoefe_2056.gpkg (railway=station)
# Tourismus:        gezählt aus tourismus_2056.gpkg (tourism=attraction)
# Keine_Konkurrenz: gezählt aus verleihe_2056.gpkg (amenity=bicycle_rental), invertiert
# Bevoelkerung:     aus statistik.stadt-zuerich.ch (P/ha), normalisiert
# Veloinfrastruktur: Experten-Einschätzung basierend auf Velowege-Layer

data = {
    "Stadtkreis": [
        "Kreis 1 (Altstadt)",
        "Kreis 2 (Enge/Wollishofen)",
        "Kreis 3 (Wiedikon)",
        "Kreis 4 (Aussersihl)",
        "Kreis 5 (Industriequartier)",
        "Kreis 6 (Unterstrass)",
        "Kreis 7 (Fluntern/Zoo)",
        "Kreis 8 (Riesbach)",
        "Kreis 9 (Albisrieden)",
        "Kreis 10 (Höngg/Wipkingen)",
        "Kreis 11 (Oerlikon)",
        "Kreis 12 (Schwamendingen)",
    ],

    # Aus bahnhoefe_2056.gpkg gezählt & normalisiert (30% Gewicht)
    # Rohdaten: [5, 5, 5, 2, 3, 2, 2, 1, 1, 1, 3, 1]
    "OeV_Anbindung": [10.0, 10.0, 10.0, 3.2, 5.5, 3.2, 3.2, 1.0, 1.0, 1.0, 5.5, 1.0],

    # Einschätzung basierend auf Velowege-Layer aus QGIS (25% Gewicht)
    "Veloinfrastruktur": [8.0, 7.0, 7.0, 8.0, 6.0, 9.0, 6.0, 7.0, 5.0, 6.0, 6.0, 4.0],

    # Aus statistik.stadt-zuerich.ch, normalisiert auf 0-10 (20% Gewicht)
    # Rohdaten (P/ha): [31.9, 34.7, 59.7, 101.1, 79.9, 71.7, 26.7, 37.3, 50.7, 45.9, 60.3, 35.0]
    "Bevoelkerungsdichte": [1.6, 2.0, 5.0, 10.0, 7.4, 6.4, 1.0, 2.3, 3.9, 3.3, 5.1, 2.0],

    # Aus tourismus_2056.gpkg gezählt & normalisiert (15% Gewicht)
    # Rohdaten: [4, 1, 0, 1, 0, 0, 49, 1, 0, 1, 2, 1]
    # Hinweis: Kreis 7 hat Zoo Zürich → sehr viele POIs
    "Tourismus_Hotspots": [1.7, 1.2, 1.0, 1.2, 1.0, 1.0, 10.0, 1.2, 1.0, 1.2, 1.4, 1.2],

    # Aus verleihe_2056.gpkg gezählt, invertiert & normalisiert (10% Gewicht)
    # Rohdaten: [20, 13, 18, 19, 16, 18, 13, 8, 20, 12, 29, 11]
    # Weniger Verleihe = höherer Score (mehr Marktpotenzial)
    "Keine_Konkurrenz": [4.9, 7.9, 5.7, 5.3, 6.6, 5.7, 7.9, 10.0, 4.9, 8.3, 1.0, 8.7],
}

df = pd.DataFrame(data)

gewichte = {
    "OeV_Anbindung":       0.30,
    "Veloinfrastruktur":   0.25,
    "Bevoelkerungsdichte": 0.20,
    "Tourismus_Hotspots":  0.15,
    "Keine_Konkurrenz":    0.10,
}

df["Gesamtscore"] = sum(
    df[kriterium] * gewicht * 10
    for kriterium, gewicht in gewichte.items()
)

df = df.sort_values("Gesamtscore", ascending=False).reset_index(drop=True)
df["Rang"] = df.index + 1

print("=" * 55)
print("SCORING-ERGEBNIS: Veloverleih Standortanalyse Zürich")
print("=" * 55)
print(df[["Rang", "Stadtkreis", "Gesamtscore"]].to_string(index=False))
print("\nTop-3 Empfehlungen:")
for _, row in df.head(3).iterrows():
    print(f"  #{int(row['Rang'])}: {row['Stadtkreis']} – Score: {row['Gesamtscore']:.1f}/100")

# Balkendiagramm
fig, ax = plt.subplots(figsize=(11, 7))
colors = ["#1A4731" if i < 3 else "#A8D5B5" for i in range(len(df))]
bars = ax.barh(df["Stadtkreis"], df["Gesamtscore"], color=colors, edgecolor="white", height=0.65)

for bar, val in zip(bars, df["Gesamtscore"]):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}", va="center", ha="left", fontsize=10, color="#1E2A22", fontweight="bold")

ax.set_xlabel("Gesamtscore (max. 100)", fontsize=12, color="#6B7280")
ax.set_title("Scoring-Ergebnis: Optimaler Veloverleih-Standort in Zürich",
             fontsize=14, fontweight="bold", color="#1A4731", pad=15)
ax.set_xlim(0, 105)
ax.invert_yaxis()
ax.set_facecolor("#F4F9F6")
fig.patch.set_facecolor("white")
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="y", labelsize=10)
ax.xaxis.grid(True, color="#E5EDE8", linewidth=0.7)

legend_patches = [
    mpatches.Patch(color="#1A4731", label="Top-3 Standorte"),
    mpatches.Patch(color="#A8D5B5", label="Weitere Stadtkreise"),
]
ax.legend(handles=legend_patches, loc="lower right", fontsize=10)

plt.tight_layout()
plt.savefig("scoring_balkendiagramm.png", dpi=150, bbox_inches="tight")
print("\n✅ Diagramm gespeichert: scoring_balkendiagramm.png")
plt.show()

# Radar-Diagramm für Top-3
kategorien = ["ÖV-\nAnbindung", "Velo-\ninfrastruktur", "Bevölkerungs-\ndichte",
              "Tourismus-\nHotspots", "Keine\nKonkurrenz"]
N = len(kategorien)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(1, 1, figsize=(8, 8), subplot_kw=dict(polar=True))
ax.set_facecolor("#F4F9F6")
fig.patch.set_facecolor("white")

farben = ["#1A4731", "#2D7D52", "#A8D5B5"]
for i, (_, row) in enumerate(df.head(3).iterrows()):
    werte = [row["OeV_Anbindung"], row["Veloinfrastruktur"], row["Bevoelkerungsdichte"],
             row["Tourismus_Hotspots"], row["Keine_Konkurrenz"]]
    werte += werte[:1]
    ax.plot(angles, werte, "o-", linewidth=2, color=farben[i], label=row["Stadtkreis"])
    ax.fill(angles, werte, alpha=0.15, color=farben[i])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(kategorien, size=11)
ax.set_ylim(0, 10)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(["2", "4", "6", "8", "10"], color="#6B7280", size=9)
ax.grid(color="#E5EDE8", linewidth=0.8)
ax.set_title("Kriterienvergleich Top-3 Standorte", size=14, fontweight="bold",
             color="#1A4731", pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=10)

plt.tight_layout()
plt.savefig("scoring_radar.png", dpi=150, bbox_inches="tight")
print("✅ Radar-Diagramm gespeichert: scoring_radar.png")
plt.show()

print("\n✅ Fertig! Beide Grafiken für die Präsentation bereit.")
print("   → scoring_balkendiagramm.png")
print("   → scoring_radar.png")
