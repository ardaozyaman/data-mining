# ============================================================================
# AutoScout24 Veri Madenciliği Vize Projesi
# ============================================================================
# Özellikler: price, mileage_km, vehicle_age, power_hp,
#             transmission, fuel_category, country_code
# ============================================================================

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from scipy import stats
from scipy.stats import chi2_contingency, f_oneway, skew, kurtosis
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime
import os

warnings.filterwarnings("ignore")
plt.ioff()
plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")

# Klasör oluştur
os.makedirs("../report/figures", exist_ok=True)

print("=" * 80)
print("          AutoScout24 İkinci El Araç Veri Madenciliği Projesi")
print("                          VİZE ÇALIŞMASI")
print("=" * 80)

# ============================================================================
# 1. VERİ YÜKLEME
# ============================================================================
print("\n[ADIM 1] VERİ YÜKLEME")
print("-" * 80)

df = pd.read_csv("../data/sampled_dataset_50percent.csv")
print(f"✓ Örneklenmiş veri seti yüklendi: {len(df):,} kayıt")
print(f"✓ Toplam özellik sayısı: {df.shape[1]}")

# Sütunları seç
required_columns = [
    "price",
    "mileage_km",
    "vehicle_age",
    "power_hp",
    "transmission",
    "fuel_category",
    "country_code",
]

df_selected = df[required_columns].copy()
print(f"✓ Analiz için seçilen özellikler: {len(required_columns)} adet")

# ============================================================================
# 2. VERİ TEMİZLEME
# ============================================================================
print("\n[ADIM 2] VERİ TEMİZLEME")
print("-" * 80)

initial_count = len(df_selected)
df_selected = df_selected.dropna()
print(
    f"✓ Eksik değerler temizlendi: {initial_count - len(df_selected):,} kayıt kaldırıldı"
)
print(f"✓ Temiz veri seti: {len(df_selected):,} kayıt")

# Sayısal ve kategorik sütunları ayır
numeric_cols = ["price", "mileage_km", "vehicle_age", "power_hp"]
categorical_cols = ["transmission", "fuel_category", "country_code"]

# ============================================================================
# 3. KEŞİFSEL VERİ ANALİZİ (EDA) - VERİ MADENCİLİĞİ TEKNİKLERİ
# ============================================================================
print("\n[ADIM 3] KEŞİFSEL VERİ ANALİZİ VE VERİ MADENCİLİĞİ TEKNİKLERİ")
print("=" * 80)

# -----------------------------------------------------------------------------
# 3.1 TANIMLAYICI İSTATİSTİKLER (Mean, Median, Mode, Min, Max, Std, Var, vb.)
# -----------------------------------------------------------------------------
print("\n3.1 TANIMLAYICI İSTATİSTİKLER")
print("-" * 80)

print("\n📊 Temel İstatistikler (5-Sayı Özeti + Ortalama + Std):")
print(df_selected[numeric_cols].describe().round(2))

print("\n📊 Detaylı İstatistiksel Ölçümler:")
print("=" * 80)
for col in numeric_cols:
    data = df_selected[col]
    print(f"\n{col.upper().replace('_', ' ')}:")
    print(f"  {'Mean (Ortalama)':<25}: {data.mean():>15,.2f}")
    print(f"  {'Median (Medyan)':<25}: {data.median():>15,.2f}")
    try:
        mode_val = data.mode()[0] if len(data.mode()) > 0 else "N/A"
        print(f"  {'Mode (Mod)':<25}: {mode_val:>15}")
    except:
        print(f"  {'Mode (Mod)':<25}: {'N/A':>15}")
    print(f"  {'Minimum':<25}: {data.min():>15,.2f}")
    print(f"  {'Maximum':<25}: {data.max():>15,.2f}")
    print(f"  {'Range (Aralık)':<25}: {data.max() - data.min():>15,.2f}")
    print(f"  {'Std Dev (Std Sapma)':<25}: {data.std():>15,.2f}")
    print(f"  {'Variance (Varyans)':<25}: {data.var():>15,.2f}")
    print(f"  {'Q1 (1. Çeyrek)':<25}: {data.quantile(0.25):>15,.2f}")
    print(f"  {'Q2 (2. Çeyrek/Median)':<25}: {data.quantile(0.50):>15,.2f}")
    print(f"  {'Q3 (3. Çeyrek)':<25}: {data.quantile(0.75):>15,.2f}")
    print(
        f"  {'IQR (Çeyrekler Arası)':<25}: {data.quantile(0.75) - data.quantile(0.25):>15,.2f}"
    )
    print(f"  {'Skewness (Çarpıklık)':<25}: {skew(data):>15,.4f}")
    print(f"  {'Kurtosis (Basıklık)':<25}: {kurtosis(data):>15,.4f}")
    cv = (data.std() / data.mean()) * 100
    print(f"  {'CV (Varyasyon Katsayısı)':<25}: {cv:>14,.2f}%")

# -----------------------------------------------------------------------------
# 3.2 NORMALLİK TESTLERİ (Shapiro-Wilk)
# -----------------------------------------------------------------------------
print("\n\n3.2 NORMALLİK TESTLERİ (Shapiro-Wilk)")
print("-" * 80)
print("Hipotez:")
print("  H0: Veri normal dağılıma sahiptir")
print("  H1: Veri normal dağılıma sahip değildir")
print("  Anlamlılık: α = 0.05\n")

for col in numeric_cols:
    sample = df_selected[col].sample(min(5000, len(df_selected)), random_state=42)
    stat, p_value = stats.shapiro(sample)
    result = "❌ Normal DEĞİL (H0 red)" if p_value < 0.05 else "✅ Normal (H0 kabul)"
    print(f"  {col:<15s}: p = {p_value:.6f}  →  {result}")

# -----------------------------------------------------------------------------
# 3.3 AYKIRIDEĞER ANALİZİ (IQR Yöntemi)
# -----------------------------------------------------------------------------
print("\n\n3.3 AYKIRI DEĞER ANALİZİ (IQR Yöntemi)")
print("-" * 80)
print("Kural: Aykırı değer = Değer < Q1 - 1.5×IQR veya Değer > Q3 + 1.5×IQR\n")

for col in numeric_cols:
    Q1 = df_selected[col].quantile(0.25)
    Q3 = df_selected[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df_selected[(df_selected[col] < lower) | (df_selected[col] > upper)]
    count = len(outliers)
    pct = (count / len(df_selected)) * 100

    print(f"  {col}:")
    print(f"    Normal Aralık: [{lower:,.2f}, {upper:,.2f}]")
    print(f"    Aykırı Değer : {count:,} kayıt ({pct:.2f}%)\n")

# -----------------------------------------------------------------------------
# 3.4 KORELASYON ANALİZİ (Pearson) ve İSTATİSTİKSEL ANLAMLILIK
# -----------------------------------------------------------------------------
print("\n3.4 KORELASYON ANALİZİ (Pearson)")
print("-" * 80)
print("Korelasyon Yorumlama:")
print("  |r| > 0.7  : Güçlü ilişki")
print("  0.4< |r| <0.7 : Orta ilişki")
print("  |r| < 0.4  : Zayıf ilişki\n")

corr_matrix = df_selected[numeric_cols].corr()
print("Korelasyon Matrisi:")
print(corr_matrix.round(3))

print("\n🔍 Güçlü/Orta Korelasyonlar (|r| > 0.3):")
for i in range(len(numeric_cols)):
    for j in range(i + 1, len(numeric_cols)):
        r_val = corr_matrix.iloc[i, j]
        if abs(r_val) > 0.3:
            col1, col2 = numeric_cols[i], numeric_cols[j]
            r, p = stats.pearsonr(df_selected[col1], df_selected[col2])
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*"
            direction = "Pozitif" if r > 0 else "Negatif"
            strength = "Güçlü" if abs(r) > 0.7 else "Orta" if abs(r) > 0.4 else "Zayıf"
            print(f"  {col1:15s} ↔ {col2:15s}: r={r:>6.3f} {sig}")
            print(f"    → {strength} {direction} İlişki (p<0.001)")

# -----------------------------------------------------------------------------
# 3.5 KATEGORİK DEĞİŞKEN ANALİZİ
# -----------------------------------------------------------------------------
print("\n\n3.5 KATEGORİK DEĞİŞKEN FREKANS ANALİZİ")
print("-" * 80)

for col in categorical_cols:
    vc = df_selected[col].value_counts()
    total = len(df_selected)
    print(f"\n{col.upper().replace('_', ' ')}:")
    print(f"  Toplam kategori: {len(vc)}")
    print(f"  En yaygın 10:")
    for i, (cat, count) in enumerate(vc.head(10).items(), 1):
        pct = (count / total) * 100
        print(f"    {i:2d}. {str(cat)[:20]:20s}: {count:>7,} ({pct:>5.2f}%)")

# -----------------------------------------------------------------------------
# 3.6 ANOVA TESTİ (Kategorik → Sayısal İlişki)
# -----------------------------------------------------------------------------
print("\n\n3.6 ANOVA TESTİ (Kategorik Değişken → Fiyat İlişkisi)")
print("-" * 80)
print("Hipotez:")
print("  H0: Grup ortalamaları arasında fark yoktur")
print("  H1: En az bir grup ortalaması farklıdır")
print("  Anlamlılık: α = 0.05\n")

# Transmission → Price
groups_trans = [
    df_selected[df_selected["transmission"] == cat]["price"].values
    for cat in df_selected["transmission"].unique()
]
f_stat, p_val = f_oneway(*groups_trans)
result = "✅ Anlamlı fark VAR" if p_val < 0.05 else "❌ Anlamlı fark YOK"
print(f"  Transmission → Price:")
print(f"    F = {f_stat:.2f}, p = {p_val:.6f}")
print(f"    Sonuç: {result}\n")

# Fuel → Price
groups_fuel = [
    df_selected[df_selected["fuel_category"] == cat]["price"].values
    for cat in df_selected["fuel_category"].unique()
]
f_stat, p_val = f_oneway(*groups_fuel)
result = "✅ Anlamlı fark VAR" if p_val < 0.05 else "❌ Anlamlı fark YOK"
print(f"  Fuel Category → Price:")
print(f"    F = {f_stat:.2f}, p = {p_val:.6f}")
print(f"    Sonuç: {result}\n")

# Country → Price
top_countries = df_selected["country_code"].value_counts().head(10).index
groups_country = [
    df_selected[df_selected["country_code"] == cat]["price"].values
    for cat in top_countries
]
f_stat, p_val = f_oneway(*groups_country)
result = "✅ Anlamlı fark VAR" if p_val < 0.05 else "❌ Anlamlı fark YOK"
print(f"  Country Code (Top 10) → Price:")
print(f"    F = {f_stat:.2f}, p = {p_val:.6f}")
print(f"    Sonuç: {result}\n")

# -----------------------------------------------------------------------------
# 3.7 CHI-SQUARE TESTİ (Kategorik ↔ Kategorik Bağımsızlık)
# -----------------------------------------------------------------------------
print("\n3.7 CHI-SQUARE BAĞIMSIZLIK TESTİ (Kategorik ↔ Kategorik)")
print("-" * 80)
print("Hipotez:")
print("  H0: İki değişken bağımsızdır")
print("  H1: İki değişken arasında ilişki vardır")
print("  Anlamlılık: α = 0.05\n")

contingency = pd.crosstab(df_selected["transmission"], df_selected["fuel_category"])
chi2, p_val, dof, expected = chi2_contingency(contingency)
result = "✅ İlişki VAR (bağımlı)" if p_val < 0.05 else "❌ İlişki YOK (bağımsız)"
print(f"  Transmission ↔ Fuel Category:")
print(f"    χ² = {chi2:.2f}, p = {p_val:.6f}, df = {dof}")
print(f"    Sonuç: {result}\n")

# -----------------------------------------------------------------------------
# 3.8 GÖRSELLEŞTİRMELER
# -----------------------------------------------------------------------------
print("\n3.8 GÖRSELLEŞTİRMELER OLUŞTURULUYOR...")
print("-" * 80)

# Grafik 1: Dağılımlar (Histogram + KDE)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Sayısal Değişkenlerin Dağılımları", fontsize=16, fontweight="bold")

for idx, col in enumerate(numeric_cols):
    ax = axes[idx // 2, idx % 2]
    ax.hist(
        df_selected[col],
        bins=50,
        color="skyblue",
        edgecolor="black",
        alpha=0.7,
        density=True,
    )

    # KDE ekle
    df_selected[col].plot(
        kind="kde", ax=ax, color="red", linewidth=2, secondary_y=False
    )

    median_val = df_selected[col].median()
    mean_val = df_selected[col].mean()
    ax.axvline(
        median_val,
        color="green",
        linestyle="--",
        linewidth=2,
        label=f"Median: {median_val:,.0f}",
    )
    ax.axvline(
        mean_val,
        color="orange",
        linestyle="--",
        linewidth=2,
        label=f"Mean: {mean_val:,.0f}",
    )

    ax.set_xlabel(col.replace("_", " ").title(), fontsize=11)
    ax.set_ylabel("Yoğunluk", fontsize=11)
    ax.set_title(
        f'{col.replace("_", " ").title()} Dağılımı', fontsize=12, fontweight="bold"
    )
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("../report/figures/01_distributions.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Grafik 1: Dağılımlar (01_distributions.png)")

# Grafik 2: Box Plots - Aykırı Değer Görselleştirme
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Box Plot - Aykırı Değer Analizi", fontsize=16, fontweight="bold")

for idx, col in enumerate(numeric_cols):
    ax = axes[idx // 2, idx % 2]
    bp = ax.boxplot(
        [df_selected[col]], labels=[col], patch_artist=True, showfliers=True
    )
    bp["boxes"][0].set_facecolor("lightcoral")
    bp["boxes"][0].set_alpha(0.7)

    Q1 = df_selected[col].quantile(0.25)
    Q3 = df_selected[col].quantile(0.75)
    median = df_selected[col].median()

    info_text = f"Q1: {Q1:,.0f}\nMedian: {median:,.0f}\nQ3: {Q3:,.0f}"
    ax.text(
        0.02,
        0.98,
        info_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.7),
    )

    ax.set_ylabel("Değer", fontsize=11)
    ax.set_title(f'{col.replace("_", " ").title()}', fontsize=12, fontweight="bold")
    ax.grid(alpha=0.3, axis="y")

plt.tight_layout()
plt.savefig("../report/figures/02_boxplots.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Grafik 2: Box Plots (02_boxplots.png)")

# Grafik 3: Korelasyon Matrisi
plt.figure(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".3f",
    cmap="coolwarm",
    center=0,
    square=True,
    linewidths=1,
    cbar_kws={"shrink": 0.8},
    mask=mask,
)
plt.title("Korelasyon Matrisi (Pearson)", fontsize=14, fontweight="bold", pad=20)
plt.tight_layout()
plt.savefig("../report/figures/03_correlation.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Grafik 3: Korelasyon Matrisi (03_correlation.png)")

# Grafik 4: Scatter Matrix
from pandas.plotting import scatter_matrix

fig = plt.figure(figsize=(14, 14))
scatter_matrix(df_selected[numeric_cols], alpha=0.3, figsize=(14, 14), diagonal="kde")
plt.suptitle("Scatter Plot Matrisi", fontsize=16, fontweight="bold", y=0.995)
plt.tight_layout()
plt.savefig("../report/figures/04_scatter_matrix.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Grafik 4: Scatter Matrix (04_scatter_matrix.png)")

# Grafik 5: Kategorik Dağılımlar
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Kategorik Değişken Dağılımları", fontsize=16, fontweight="bold")

for idx, col in enumerate(categorical_cols):
    vc = df_selected[col].value_counts().head(10)
    axes[idx].bar(
        range(len(vc)), vc.values, color=sns.color_palette("Set2")[idx], alpha=0.8
    )
    axes[idx].set_xticks(range(len(vc)))
    axes[idx].set_xticklabels(vc.index, rotation=45, ha="right")
    axes[idx].set_ylabel("Frekans", fontsize=11)
    axes[idx].set_title(
        f'{col.replace("_", " ").title()} (Top 10)', fontsize=12, fontweight="bold"
    )
    axes[idx].grid(alpha=0.3, axis="y")

    for i, v in enumerate(vc.values):
        axes[idx].text(i, v, f"{v:,}", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.savefig("../report/figures/05_categorical_dist.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Grafik 5: Kategorik Dağılımlar (05_categorical_dist.png)")

# ============================================================================
# 4. KÜMELEME ANALİZİ (K-MEANS)
# ============================================================================
print("\n\n[ADIM 4] KÜMELEME ANALİZİ (K-MEANS)")
print("=" * 80)

# 4.1 Veri Hazırlama
print("\n4.1 Kümeleme için Veri Hazırlama")
print("-" * 80)

# Label Encoding
le_trans = LabelEncoder()
le_fuel = LabelEncoder()
le_country = LabelEncoder()

df_cluster = df_selected.copy()
df_cluster["transmission_enc"] = le_trans.fit_transform(df_selected["transmission"])
df_cluster["fuel_enc"] = le_fuel.fit_transform(df_selected["fuel_category"])
df_cluster["country_enc"] = le_country.fit_transform(df_selected["country_code"])

features = [
    "price",
    "mileage_km",
    "vehicle_age",
    "power_hp",
    "transmission_enc",
    "fuel_enc",
    "country_enc",
]

X = df_cluster[features].values
print(f"✓ Özellik matrisi: {X.shape}")
print(f"  Özellikler: {', '.join(features)}")

# Standardizasyon
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(f"✓ Standardizasyon tamamlandı (mean=0, std=1)")

# 4.2 Optimal K Bulma (k=10-400)
print("\n4.2 Optimal Küme Sayısı Bulma (k=10-400, 10'ar adımla)")
print("-" * 80)

k_range = list(range(10, 410, 10))
inertias = []
silhouettes = []

print("K-Means iterasyonları:")
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=300)
    labels = kmeans.fit_predict(X_scaled)
    inertias.append(kmeans.inertia_)
    sil = silhouette_score(X_scaled, labels)
    silhouettes.append(sil)

    if k % 50 == 0 or k == k_range[0]:
        print(f"  k={k:3d}: Inertia={kmeans.inertia_:>12,.2f}, Silhouette={sil:>7.4f}")

# En iyi k
best_k = k_range[np.argmax(silhouettes)]
best_sil = max(silhouettes)

print(f"\n✅ OPTIMAL K BULUNDU: k={best_k}")
print(f"   En yüksek Silhouette Score: {best_sil:.4f}")

# Silhouette eğrisi analizi
last_10_avg = np.mean(silhouettes[-10:])
print(f"\n📊 Silhouette Eğrisi Analizi:")
print(f"   En yüksek skor: {best_sil:.4f} (k={best_k})")
print(f"   Son 10 değer ort: {last_10_avg:.4f}")
if last_10_avg < best_sil * 0.95:
    print(f"   ✅ Eğri tamamlanmış - optimal k={best_k} güvenilir")
else:
    print(f"   ⚠️  Eğri tam tamamlanmamış - daha yüksek k test edilebilir")

# Grafik 6: Optimal K Seçimi
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle(
    f"Optimal Küme Sayısı Belirleme (k={best_k})", fontsize=16, fontweight="bold"
)

# Elbow
axes[0].plot(
    k_range, inertias, "o-", linewidth=2, markersize=6, color="blue", alpha=0.7
)
axes[0].set_xlabel("Küme Sayısı (k)", fontsize=12)
axes[0].set_ylabel("Inertia (WCSS)", fontsize=12)
axes[0].set_title("Elbow Method", fontsize=13, fontweight="bold")
axes[0].grid(alpha=0.3)

# Silhouette
axes[1].plot(
    k_range, silhouettes, "o-", linewidth=2, markersize=6, color="green", alpha=0.7
)
axes[1].axvline(
    best_k,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Optimal k={best_k} (score={best_sil:.4f})",
)
axes[1].axhline(best_sil, color="orange", linestyle=":", linewidth=1, alpha=0.5)
axes[1].set_xlabel("Küme Sayısı (k)", fontsize=12)
axes[1].set_ylabel("Silhouette Score", fontsize=12)
axes[1].set_title("Silhouette Score Eğrisi", fontsize=13, fontweight="bold")
axes[1].legend(fontsize=10)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("../report/figures/06_optimal_k.png", dpi=300, bbox_inches="tight")
plt.close()
print("\n  ✓ Grafik 6: Optimal K Analizi (06_optimal_k.png)")

# 4.3 Final K-Means Modeli
print(f"\n4.3 Final K-Means Modeli (k={best_k})")
print("-" * 80)

final_kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=20, max_iter=500)
cluster_labels = final_kmeans.fit_predict(X_scaled)
df_cluster["cluster"] = cluster_labels

final_sil = silhouette_score(X_scaled, cluster_labels)
print(f"✓ Kümeleme tamamlandı")
print(f"  Silhouette Score: {final_sil:.4f}")
print(f"  Inertia: {final_kmeans.inertia_:,.2f}")

print(f"\n📊 Küme Dağılımı:")
for i in range(best_k):
    count = np.sum(cluster_labels == i)
    pct = (count / len(cluster_labels)) * 100
    print(f"  Küme {i:2d}: {count:>6,} kayıt ({pct:>5.2f}%)")

# 4.4 Küme Profilleri
print(f"\n4.4 Küme Profilleri (Ortalama Değerler)")
print("-" * 80)

cluster_profiles = df_cluster.groupby("cluster")[numeric_cols].mean()
print(cluster_profiles.round(2))

print(f"\n📋 Kümelerin Kategorik Özellikleri:")
for i in range(best_k):
    cluster_data = df_cluster[df_cluster["cluster"] == i]
    trans_mode = (
        cluster_data["transmission"].mode()[0] if len(cluster_data) > 0 else "N/A"
    )
    fuel_mode = (
        cluster_data["fuel_category"].mode()[0] if len(cluster_data) > 0 else "N/A"
    )
    country_mode = (
        cluster_data["country_code"].mode()[0] if len(cluster_data) > 0 else "N/A"
    )

    print(f"\n  Küme {i:2d} ({len(cluster_data):,} kayıt):")
    print(f"    Vites : {trans_mode}")
    print(f"    Yakıt : {fuel_mode}")
    print(f"    Ülke  : {country_mode}")

# Grafik 7: PCA Görselleştirme
print(f"\n4.5 Kümelerin Görselleştirilmesi (PCA)")
print("-" * 80)

pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)

print(f"  PC1 varyans: {pca.explained_variance_ratio_[0]:.2%}")
print(f"  PC2 varyans: {pca.explained_variance_ratio_[1]:.2%}")
print(f"  Toplam     : {pca.explained_variance_ratio_.sum():.2%}")

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
print("  ✓ Grafik 7: PCA Görselleştirme (07_clusters_pca.png)")

# Grafik 8: Küme Merkezleri Heatmap (330 küme için sadece örnek kümeleri göster)
plt.figure(figsize=(16, 10))
centers_df = pd.DataFrame(
    final_kmeans.cluster_centers_,
    columns=features,
    index=[f"K{i}" for i in range(best_k)],
)

# 330 küme çok fazla - sadece her 10. kümeyi göster + ilk 5 ve son 5
if best_k > 50:
    sample_indices = list(range(0, min(10, best_k)))  # İlk 10
    sample_indices += list(range(10, best_k, max(1, best_k // 30)))  # Her 10-15. küme
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
print("  ✓ Grafik 8: Küme Merkezleri (08_cluster_centers.png)")

# Grafik 9: Kümelere Göre Özellik Karşılaştırması
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle("Kümelere Göre Özellik Karşılaştırmaları", fontsize=16, fontweight="bold")

# 330 küme için renk paleti
boxplot_colors = plt.cm.Spectral(np.linspace(0, 1, best_k))

for idx, col in enumerate(numeric_cols):
    ax = axes[idx // 2, idx % 2]
    data_to_plot = [
        df_cluster[df_cluster["cluster"] == i][col].values for i in range(best_k)
    ]
    bp = ax.boxplot(
        data_to_plot,
        labels=[f"K{i}" for i in range(best_k)],
        patch_artist=True,
        showfliers=False,
    )

    for patch, color in zip(bp["boxes"], boxplot_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_ylabel(col.replace("_", " ").title(), fontsize=11)
    ax.set_xlabel("Küme", fontsize=11)
    ax.set_title(
        f'{col.replace("_", " ").title()} Dağılımı', fontsize=12, fontweight="bold"
    )
    ax.grid(alpha=0.3, axis="y")
    # 330 küme için x-tick etiketlerini seyrekleştir
    if best_k > 50:
        ax.set_xticks(range(0, best_k, max(1, best_k // 10)))
        ax.set_xticklabels(
            [f"K{i}" for i in range(0, best_k, max(1, best_k // 10))],
            rotation=45,
            fontsize=8,
        )

plt.tight_layout()
plt.savefig("../report/figures/09_cluster_comparison.png", dpi=300, bbox_inches="tight")
plt.close()
print("  ✓ Grafik 9: Küme Karşılaştırmaları (09_cluster_comparison.png)")

# ============================================================================
# 5. KÜMELER ÜZERİNDE VERİ MADENCİLİĞİ TEKNİKLERİ
# ============================================================================
print("\n\n[ADIM 5] KÜMELER ÜZERİNDE VERİ MADENCİLİĞİ ANALİZİ")
print("=" * 80)

print("\n5.1 Her Küme İçin İstatistiksel Analiz")
print("-" * 80)

for cluster_id in range(best_k):
    cluster_data = df_cluster[df_cluster["cluster"] == cluster_id]
    print(f"\n{'=' * 80}")
    print(
        f"KÜME {cluster_id} ANALİZİ ({len(cluster_data):,} kayıt - %{len(cluster_data)/len(df_cluster)*100:.1f})"
    )
    print(f"{'=' * 80}")

    # Tanımlayıcı istatistikler
    print(f"\n📊 Sayısal Değişken İstatistikleri:")
    for col in numeric_cols:
        data = cluster_data[col]
        print(f"\n  {col.upper()}:")
        print(f"    Mean   : {data.mean():>12,.2f}")
        print(f"    Median : {data.median():>12,.2f}")
        print(f"    Std    : {data.std():>12,.2f}")
        print(f"    Min    : {data.min():>12,.2f}")
        print(f"    Max    : {data.max():>12,.2f}")

    # Kategorik özellikler
    print(f"\n📋 Kategorik Değişken Dağılımları:")
    for col in categorical_cols:
        top_3 = cluster_data[col].value_counts().head(3)
        print(f"\n  {col.upper()} (Top 3):")
        for cat, count in top_3.items():
            pct = (count / len(cluster_data)) * 100
            print(f"    {str(cat)[:20]:20s}: {count:>5,} ({pct:>5.1f}%)")

    # Küme içi korelasyon
    print(f"\n🔗 Küme İçi Korelasyonlar (|r| > 0.3):")
    cluster_corr = cluster_data[numeric_cols].corr()
    found_corr = False
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            r_val = cluster_corr.iloc[i, j]
            if abs(r_val) > 0.3:
                print(
                    f"    {numeric_cols[i]:15s} ↔ {numeric_cols[j]:15s}: r = {r_val:>6.3f}"
                )
                found_corr = True
    if not found_corr:
        print("    (Güçlü korelasyon bulunamadı)")

# Kümeler arası karşılaştırma (ANOVA)
print(f"\n\n5.2 Kümeler Arası ANOVA Testi")
print("-" * 80)
print("Hipotez: H0: Tüm kümelerin ortalamaları eşittir\n")

for col in numeric_cols:
    groups = [df_cluster[df_cluster["cluster"] == i][col].values for i in range(best_k)]
    f_stat, p_val = f_oneway(*groups)
    result = "✅ Kümeler FARKLI" if p_val < 0.05 else "❌ Kümeler benzer"
    print(f"  {col:15s}: F={f_stat:>8.2f}, p={p_val:.6f}  →  {result}")

# ============================================================================
# 6. SONUÇLARI KAYDETME
# ============================================================================
print("\n\n[ADIM 6] SONUÇLARI KAYDETME")
print("=" * 80)

# Kümelenmiş veri
df_cluster.to_csv("../data/clustered_data.csv", index=False)
print("✓ Kümelenmiş veri: ../data/clustered_data.csv")

# Küme istatistikleri
cluster_stats = df_cluster.groupby("cluster").agg(
    {
        "price": ["count", "mean", "median", "std", "min", "max"],
        "mileage_km": ["mean", "median", "std"],
        "vehicle_age": ["mean", "median", "std"],
        "power_hp": ["mean", "median", "std"],
    }
)
cluster_stats.to_csv("../data/cluster_statistics.csv")
print("✓ Küme istatistikleri: ../data/cluster_statistics.csv")

# Özet rapor
with open("../data/analysis_summary.txt", "w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write("AutoScout24 Veri Madenciliği Vize Projesi - Analiz Özeti\n")
    f.write("=" * 80 + "\n\n")

    f.write(f"VERİ SETİ BİLGİLERİ:\n")
    f.write(f"  Toplam Kayıt    : {len(df_cluster):,}\n")
    f.write(f"  Özellik Sayısı  : {len(features)}\n")
    f.write(f"  Sayısal Değişken: {len(numeric_cols)}\n")
    f.write(f"  Kategorik Değ.  : {len(categorical_cols)}\n\n")

    f.write(f"KÜMELEME SONUÇLARI:\n")
    f.write(f"  Optimal K       : {best_k}\n")
    f.write(f"  Silhouette Score: {final_sil:.4f}\n")
    f.write(f"  Inertia         : {final_kmeans.inertia_:,.2f}\n")
    f.write(f"  PCA Varyans     : {pca.explained_variance_ratio_.sum():.2%}\n\n")

    f.write(f"KÜME PROFİLLERİ (Ortalama Değerler):\n")
    f.write("=" * 80 + "\n")
    f.write(cluster_profiles.to_string())
    f.write("\n\n")

    f.write(f"KÜME DAĞILIMLARI:\n")
    for i in range(best_k):
        count = np.sum(cluster_labels == i)
        pct = (count / len(cluster_labels)) * 100
        f.write(f"  Küme {i:2d}: {count:>6,} kayıt ({pct:>5.2f}%)\n")

print("✓ Analiz özeti: ../data/analysis_summary.txt")

# ============================================================================
# FİNAL
# ============================================================================
print("\n" + "=" * 80)
print("                        ANALİZ TAMAMLANDI!")
print("=" * 80)
print(f"\n📊 VERİ SETİ:")
print(f"   Toplam kayıt: {len(df_cluster):,}")
print(f"   Özellik sayısı: {len(features)}")
print(f"\n🎯 KÜMELEME:")
print(f"   Optimal K: {best_k}")
print(f"   Silhouette Score: {final_sil:.4f}")
print(f"   K aralığı test: {k_range[0]}-{k_range[-1]}")
print(f"\n📁 ÇIKTILAR:")
print(f"   Grafikler: ../report/figures/ ({9} adet)")
print(f"   Veri: ../data/clustered_data.csv")
print(f"   İstatistikler: ../data/cluster_statistics.csv")
print(f"   Özet: ../data/analysis_summary.txt")
print("\n" + "=" * 80)
print("Sıradaki adım: Makale yazımı")
print("=" * 80 + "\n")
