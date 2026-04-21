# ============================================================
# VELOVERLEIH STANDORTANALYSE ZÜRICH
# Person B – Scoring-Modell & Auswertung
# ============================================================
# Voraussetzungen (in GitHub Codespaces Terminal ausführen):
#   pip install geopandas pandas matplotlib folium shapely
#
# Dieser Code liest die aus QGIS exportierten GeoJSON-Dateien
# und berechnet ein gewichtetes Scoring pro Stadtkreis.
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ── SCHRITT 1: Scoring-Daten manuell erfassen ─────────────────────────────────
# Diese Werte basieren auf eurer QGIS-Analyse.
# Zählt pro Stadtkreis: wie viele Buffer-Überschneidungen gibt es?
# Passt die Zahlen an eure echten QGIS-Ergebnisse an!

data = {
    "Stadtkreis": [
        "Kreis 1 (Altstadt)",
        "Kreis 2 (Enge/Wollishofen)",
        "Kreis 3 (Wiedikon)",
        "Kreis 4 (Aussersihl)",
        "Kreis 5 (Industriequartier)",
        "Kreis 6 (Unterstrass)",
        "Kreis 7 (Fluntern)",
        "Kreis 8 (Riesbach)",
        "Kreis 9 (Albisrieden)",
        "Kreis 10 (Höngg/Wipkingen)",
        "Kreis 11 (Oerlikon)",
        "Kreis 12 (Schwamendingen)",
    ],
    # Punkte 0–10 pro Kriterium (anpassen nach QGIS-Ergebnissen!)
    "OeV_Anbindung":       [10, 6, 7, 9, 7, 9, 5, 7, 4, 6, 7, 4],  # 30% Gewicht
    "Veloinfrastruktur":   [8, 7, 7, 8, 6, 9, 6, 7, 5, 6, 6, 4],   # 25% Gewicht
    "Bevoelkerungsdichte": [7, 6, 8, 9, 7, 8, 4, 7, 6, 5, 7, 6],   # 20% Gewicht
    "Tourismus_Hotspots":  [10, 5, 3, 4, 3, 4, 7, 8, 2, 3, 3, 2],  # 15% Gewicht
    "Keine_Konkurrenz":    [6, 8, 9, 8, 9, 7, 10, 6, 10, 9, 8, 10], # 10% Gewicht
}

df = pd.DataFrame(data)

# ── SCHRITT 2: Gewichtetes Scoring berechnen ──────────────────────────────────
gewichte = {
    "OeV_Anbindung":       0.30,
    "Veloinfrastruktur":   0.25,
    "Bevoelkerungsdichte": 0.20,
    "Tourismus_Hotspots":  0.15,
    "Keine_Konkurrenz":    0.10,
}

df["Gesamtscore"] = sum(
    df[kriterium] * gewicht * 10  # *10 damit Score 0–100
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

# ── SCHRITT 3: Balkendiagramm ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 7))
colors = ["#1A4731" if i < 3 else "#A8D5B5" for i in range(len(df))]
bars = ax.barh(df["Stadtkreis"], df["Gesamtscore"], color=colors, edgecolor="white", height=0.65)

# Werte an Balkenenden
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

# ── SCHRITT 4: Radar/Spinne-Diagramm für Top-3 ───────────────────────────────
import numpy as np

kategorien = ["ÖV-\nAnbindung", "Velo-\ninfrastruktur", "Bevölkerungs-\ndichte",
              "Tourismus-\nHotspots", "Keine\nKonkurrenz"]
N = len(kategorien)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]  # Kreis schliessen

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
