#!/usr/bin/env python3
"""
Sadece Grafik 7 (PCA) ve Grafik 8 (Heatmap) yeniden oluşturma scripti
Optimal k bulma işlemi YAPILMAZ - mevcut cluster verisi kullanılır
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")
plt.ioff()

print("=" * 80)
print("         Grafik 7 ve 8 Yeniden Oluşturma (k=330 mevcut)")
print("=" * 80)

# Kümelenmiş veriyi yükle
df_cluster = pd.read_csv("../data/clustered_data.csv")
print(f"\n✓ Kümelenmiş veri yüklendi: {len(df_cluster):,} kayıt")

# Sütunları seç
numeric_cols = ["price", "mileage_km", "vehicle_age", "power_hp"]
categorical_cols = ["transmission", "fuel_category", "country_code"]

# Encoding
le_trans = LabelEncoder()
le_fuel = LabelEncoder()
le_country = LabelEncoder()

df_cluster["transmission_enc"] = le_trans.fit_transform(df_cluster["transmission"])
df_cluster["fuel_enc"] = le_fuel.fit_transform(df_cluster["fuel_category"])
df_cluster["country_enc"] = le_country.fit_transform(df_cluster["country_code"])

# Features
features = numeric_cols + ["transmission_enc", "fuel_enc", "country_enc"]
X = df_cluster[features].values

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Mevcut cluster labels
cluster_labels = df_cluster["cluster"].values
best_k = len(np.unique(cluster_labels))

print(f"✓ Küme sayısı: {best_k}")
print(f"✓ Özellik sayısı: {len(features)}")

# KMeans modelini yeniden oluştur (sadece merkezler için)
final_kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
final_kmeans.fit(X_scaled)

# PCA
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)

print(
    f"\n✓ PCA varyans: PC1={pca.explained_variance_ratio_[0]:.2%}, PC2={pca.explained_variance_ratio_[1]:.2%}"
)

# =============================================================================
# GRAFİK 7: PCA ile Kümeler (Colorbar kullanımı)
# =============================================================================
print("\n[Grafik 7] PCA Görselleştirme oluşturuluyor...")

plt.figure(figsize=(14, 10))

# 330 küme için colorbar kullanımı (legend çok kalabalık olur)
scatter = plt.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=cluster_labels,
    cmap="Spectral",
    alpha=0.5,
    s=20,
    edgecolors="none",
)

centers_pca = pca.transform(final_kmeans.cluster_centers_)
plt.scatter(
    centers_pca[:, 0],
    centers_pca[:, 1],
    c="black",
    marker="X",
    s=200,
    edgecolors="white",
    linewidth=2,
    label=f"Küme Merkezleri (n={best_k})",
    zorder=10,
)

# Colorbar ekle (330 küme için legend yerine)
plt.colorbar(scatter, label="Küme ID", shrink=0.8)

plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%} varyans)", fontsize=12)
plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%} varyans)", fontsize=12)
plt.title(
    f"K-Means Kümeleme - Mikro-Segmentasyon (k={best_k})",
    fontsize=14,
    fontweight="bold",
)
plt.legend(loc="upper right", framealpha=0.95, fontsize=11)
plt.grid(alpha=0.3, linestyle="--")
plt.tight_layout()
plt.savefig("../report/figures/07_clusters_pca.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Grafik 7 kaydedildi: 07_clusters_pca.png")

# =============================================================================
# GRAFİK 8: Küme Merkezleri Heatmap (Örnekleme ile)
# =============================================================================
print("\n[Grafik 8] Küme Merkezleri Heatmap oluşturuluyor...")

plt.figure(figsize=(16, 10))
centers_df = pd.DataFrame(
    final_kmeans.cluster_centers_,
    columns=features,
    index=[f"K{i}" for i in range(best_k)],
)

# 330 küme çok fazla - sadece örnekleme yap
if best_k > 50:
    sample_indices = list(range(0, min(10, best_k)))  # İlk 10
    sample_indices += list(range(10, best_k, max(1, best_k // 30)))  # Her ~11. küme
    sample_indices += list(range(max(0, best_k - 10), best_k))  # Son 10
    sample_indices = sorted(set(sample_indices))[:40]  # Maksimum 40 küme göster
    centers_sample = centers_df.iloc[sample_indices]
    title_text = f"Küme Merkezleri Örneği (40/{best_k} küme gösteriliyor)"
else:
    centers_sample = centers_df
    title_text = "Küme Merkezleri (Standardize Değerler)"

sns.heatmap(
    centers_sample.T,
    annot=False,  # 330 küme için annotation kapalı
    cmap="RdYlGn",
    center=0,
    linewidths=0.5,
    cbar_kws={"shrink": 0.8, "label": "Standardize Değer"},
    vmin=-2,
    vmax=2,
)
plt.title(title_text, fontsize=14, fontweight="bold", pad=20)
plt.xlabel("Küme ID", fontsize=12)
plt.ylabel("Özellik", fontsize=12)
plt.xticks(rotation=90, fontsize=8)
plt.yticks(fontsize=11)
plt.tight_layout()
plt.savefig("../report/figures/08_cluster_centers.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Grafik 8 kaydedildi: 08_cluster_centers.png")

print("\n" + "=" * 80)
print("✅ Grafik 7 ve 8 başarıyla yeniden oluşturuldu!")
print("=" * 80)
