#!/usr/bin/env python3
"""Korelasyon matrisini düzelt ve yeniden oluştur"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Veriyi yükle
df = pd.read_csv("../data/sampled_dataset_50percent.csv")
numeric_cols = ["price", "mileage_km", "vehicle_age", "power_hp"]
df_clean = df[numeric_cols].dropna()

print(f"Veri yüklendi: {len(df_clean):,} kayıt")
print("\nKorelasyon matrisi:")
corr_matrix = df_clean.corr()
print(corr_matrix)

# Grafik oluştur
plt.figure(figsize=(10, 8))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".3f",
    cmap="coolwarm",
    center=0,
    square=True,
    linewidths=1,
    cbar_kws={"shrink": 0.8},
    vmin=-1,
    vmax=1,
)
plt.title("Korelasyon Matrisi (Pearson)", fontsize=14, fontweight="bold", pad=20)
plt.tight_layout()
plt.savefig("../report/figures/03_correlation.png", dpi=300, bbox_inches="tight")
plt.close()

print("\n✅ Korelasyon matrisi düzeltildi: 03_correlation.png")
