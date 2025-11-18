# AutoScout24 Veri Madenciliği Vize Projesi

## 📊 Proje Özeti

AutoScout24 platformundan elde edilen **56,806 ikinci el araç** verisi üzerinde kapsamlı veri madenciliği analizi.

**Yazar:** Arda Özyaman  
**Tarih:** 17 Kasım 2025

### 🔗 Veri Seti
[AutoScout24 Car Listings Dataset - Kaggle](https://www.kaggle.com/datasets/clkmuhammed/autoscout24-car-listings-dataset/data)

---

## 🎯 Amaç

1. İkinci el araç fiyatlarını etkileyen faktörleri belirlemek
2. Araçlar arasındaki doğal segmentleri (kümeleri) keşfetmek
3. Pazar dinamiklerini anlamak için istatistiksel yöntemler kullanmak

---

## 📁 Dosya Yapısı

```
homework/
├── data/
│   ├── autoscout24_dataset_20251108.csv   # Orijinal veri seti
│   ├── sampled_dataset_50percent.csv      # Ana veri seti (%50 örnek)
│   ├── clustered_data.csv                 # Kümelenmiş veri (k=330)
│   └── cluster_statistics.csv             # Küme istatistikleri
│
├── src/
│   └── analysis_vize.py                   # Ana analiz kodu ✅
│
├── report/
│   ├── vize_raporu.md                     # VİZE MAKALESİ (12 sayfa) ✅
│   ├── vize_raporu.pdf                    # PDF RAPOR ✅
│   └── figures/                            # Grafikler (6 adet)
│       ├── 01_distributions.png
│       ├── 03_correlation.png
│       ├── 04_scatter_matrix.png
│       ├── 05_categorical_dist.png
│       ├── 06_optimal_k.png
│       └── 07_clusters_pca.png
│
└── README.md                               # Bu dosya
```

---

## 🚀 Nasıl Çalıştırılır?

### Gereksinimler

Python 3.13+ ve şu kütüphaneler:
- numpy (2.3.4)
- pandas (2.3.3)
- scikit-learn (1.7.2)
- scipy (1.16.3)
- matplotlib (3.10.7)
- seaborn (0.13.2)

### Kurulum

```bash
# Sanal ortamı aktifleştir
source .venv/bin/activate  # macOS/Linux
# veya
.venv\Scripts\activate  # Windows

# Gerekli paketler:
# numpy, pandas, scikit-learn, scipy, matplotlib, seaborn
```

### Analizi Çalıştır

```bash
cd src/

# Virtual environment kullan
../.venv/bin/python analysis_vize.py
```

### Çıktılar

Kod çalıştığında şunlar oluşur:
- 6 adet grafik (`report/figures/`)
- Kümelenmiş veri (`data/clustered_data.csv`)
- Küme istatistikleri (`data/cluster_statistics.csv`)
- Detaylı console çıktısı

---

## 📊 Veri Seti

| Özellik | Açıklama | Tip |
|---------|----------|-----|
| `price` | Araç fiyatı (EUR) | Sayısal |
| `mileage_km` | Kilometre | Sayısal |
| `vehicle_age` | Araç yaşı (yıl) | Sayısal |
| `power_hp` | Motor gücü (hp) | Sayısal |
| `transmission` | Vites tipi | Kategorik |
| `fuel_category` | Yakıt türü | Kategorik |
| `country_code` | Ülke kodu | Kategorik |

**Toplam:** 56,806 kayıt (orijinal veri setinin %50 örneği)

---

## 🔬 Uygulanan Veri Madenciliği Teknikleri

### 1. Tanımlayıcı İstatistikler
- Mean, Median, Mode
- Min, Max, Range
- Standard Deviation, Variance
- Quartiles (Q1, Q2, Q3), IQR
- Skewness (Çarpıklık), Kurtosis (Basıklık)
- Coefficient of Variation (CV)

### 2. Hipotez Testleri
- **Shapiro-Wilk Normallik Testi**
  - H₀: Veri normal dağılıma sahiptir
  - Sonuç: Tüm değişkenler normal değil (p < 0.001)

- **ANOVA (Analysis of Variance)**
  - Kategorik → Sayısal ilişki
  - Transmission → Price: F=1,847 (p<0.001)
  - Fuel Category → Price: F=2,135 (p<0.001)
  - Country → Price: F=892 (p<0.001)

- **Chi-Square Bağımsızlık Testi**
  - Kategorik ↔ Kategorik ilişki
  - Transmission ↔ Fuel: χ²=14,238 (p<0.001)
  - Sonuç: Bağımlı (ilişki var)

### 3. Korelasyon Analizi (Pearson)
| Değişken Çifti | Korelasyon (r) | Yorum |
|----------------|----------------|-------|
| Price ↔ Power_hp | +0.726*** | Güçlü Pozitif |
| Price ↔ Mileage_km | -0.509*** | Orta Negatif |
| Mileage_km ↔ Vehicle_age | +0.556*** | Orta Pozitif |
| Price ↔ Vehicle_age | -0.310*** | Zayıf-Orta Negatif |

***: p < 0.001 (İstatistiksel olarak anlamlı)

### 4. Aykırı Değer Analizi (IQR Yöntemi)
- Price: %15.04 aykırı değer
- Mileage_km: %7.42 aykırı değer
- Vehicle_age: %6.85 aykırı değer
- Power_hp: %9.02 aykırı değer

### 5. Kümeleme Analizi (K-Means)
- **Optimal K:** 330 (Silhouette Score ile belirlendi)
- **Silhouette Score:** 0.2640
- **K Aralığı:** 10-400 (10'ar adımla test edildi)
- **Mikro-Segmentasyon Stratejisi:** Yüksek granülarite tercih edildi
- **PCA Görselleştirme:** 2D projeksiyonu
  - PC1 + PC2 varyans: 53.76%

---

## 📈 Ana Bulgular

### İstatistiksel Özellikler

| Özellik | Ortalama | Medyan | Std | Çarpıklık | CV (%) |
|---------|----------|---------|-----|-----------|--------|
| Price | 44,573 EUR | 32,990 EUR | 42,821 | 2.52 | 96.07% |
| Mileage | 94,173 km | 80,000 km | 67,814 | 1.38 | 72.00% |
| Age | 6.12 yıl | 5 yıl | 5.06 | 1.25 | 82.68% |
| Power | 212 hp | 190 hp | 124 | 1.45 | 58.49% |

### En Güçlü Fiyat Belirleyicileri

1. **Motor Gücü (r=0.726)** ⭐ En güçlü
2. **Kilometre (r=-0.509)** ⭐ Negatif etki
3. **Araç Yaşı (r=-0.310)** ⭐ Negatif etki

### Küme Segmentleri (Örnekler)

#### Segment 1: Ultra Lüks Spor Araçlar (Küme 326)
- 122 araç (%0.21)
- Ortalama fiyat: **235,029 EUR**
- Motor gücü: **569 hp**
- Kilometre: 9,247 km (çok düşük)
- %100 Otomatik, %92.6 Benzin

#### Segment 2: Ekonomik Kompakt Araçlar (Küme 30)
- 169 araç (%0.30)
- Ortalama fiyat: **4,313 EUR**
- Motor gücü: 120 hp
- Kilometre: 172,242 km (yüksek)
- 16.3 yaşında

#### Segment 3: Elektrikli Yüksek Performans (Küme 317)
- 68 araç (%0.12)
- Ortalama fiyat: **75,046 EUR**
- Motor gücü: **524 hp**
- %98.5 Elektrik, %100 Otomatik

---

## 📊 Grafikler

| # | Dosya | Açıklama |
|---|-------|----------|
| 1 | `01_distributions.png` | Histogram + KDE dağılımları |
| 2 | `03_correlation.png` | Korelasyon ısı haritası |
| 3 | `04_scatter_matrix.png` | Scatter plot matrisi |
| 4 | `05_categorical_dist.png` | Kategorik frekans dağılımları |
| 5 | `06_optimal_k.png` | Elbow + Silhouette eğrileri |
| 6 | `07_clusters_pca.png` | PCA 2D kümeleme görselleştirmesi |

---

## ✅ Metodolojik Güçlü Yönler

1. **Kapsamlı İstatistiksel Analiz:**
   - 12 farklı istatistiksel ölçüm (mean, median, mode, std, var, Q1, Q3, IQR, skew, kurtosis, CV, range)
   - Normallik testleri (Shapiro-Wilk)
   - Aykırı değer tespiti (IQR)

2. **Hipotez Testleri:**
   - ANOVA (3 test)
   - Chi-Square (1 test)
   - Pearson korelasyon testleri (6 test)
   - Tüm testler p-değerleri ile raporlanmış

3. **Makine Öğrenmesi:**
   - K-Means clustering (k=10-400 arası sistematik arama)
   - Silhouette Score ile objektif değerlendirme
   - PCA ile boyut indirgeme ve görselleştirme

4. **Kod Kalitesi:**
   - Temiz, okunabilir console çıktıları
   - Tüm adımlar açıklanmış
   - 6 yüksek kaliteli grafik (300 DPI)
   - Tekrarlanabilir (random_state=42)

---

## 📝 Rapor

**Dosya:** `report/vize_raporu.md` ve `report/vize_raporu.pdf`

**İçerik:**
1. Giriş (Problem tanımı, motivasyon)
2. Veri Kümesi Tanıtımı
3. Kullanılan Yöntemler (detaylı açıklamalar)
4. Deneysel Çalışma ve Sonuçlar
5. Tartışma (metodolojik değerlendirme, mikro-segmentasyon stratejisi)
6. Sonuç
7. Kaynaklar

**Sayfa Sayısı:** 12 sayfa  
**Format:** Markdown + PDF (10pt, 2cm margin)  
**Grafikler:** 6 adet yüksek çözünürlüklü görsel

---

## 🎓 Akademik Katkı

1. Çoklu veri madenciliği tekniklerinin **entegre kullanımı**
2. Büyük ölçekli **gerçek veri seti** üzerinde uygulama
3. **Metodolojik zenginlik:** Tanımlayıcı istatistikler + Hipotez testleri + Kümeleme
4. **330 farklı araç segmenti** keşfedilmesi
5. Otomotiv endüstrisine **pratik değer**

---

## 🔮 Gelecek Çalışmalar

1. **Model İyileştirmeleri:**
   - Hierarchical clustering
   - DBSCAN (density-based)
   - Ensemble clustering

2. **Feature Engineering:**
   - Türetilmiş özellikler (price/age ratio)
   - One-hot encoding
   - Zaman serisi özellikleri

3. **Tahmin Modelleri:**
   - Regresyon ile fiyat tahmini
   - Sınıflandırma modelleri
   - Deep learning yaklaşımları

4. **Daha Fazla Veri:**
   - Tam veri seti (%100)
   - Marka ve model bilgileri
   - Zaman serisi analizi

---

## 👨‍💻 Geliştirici Notları

### Performans Optimizasyonu
- %50 örnekleme ile işlem süresi: ~5-10 dakika
- Tam veri seti (~113K kayıt) ile: ~15-30 dakika (tahmini)
- RAM kullanımı: ~2-3 GB

### Önemli Notlar
1. **analysis_vize.py** kullanın
2. Virtual environment gerekli (`.venv/bin/python`)
3. Grafikler otomatik kaydedilir (`report/figures/`)
4. Console çıktıları detaylı ve okunabilir
5. K=330 kümeleme stratejisi: Mikro-segmentasyon yaklaşımı

---

## 📞 İletişim

**Proje:** AutoScout24 Veri Madenciliği Vize Analizi  
**Yazar:** Arda Özyaman  
**Ders:** BM 518 Veri Madenciliği ve Uygulamaları  
**Tarih:** 17 Kasım 2025

---

## 📄 Veri Kaynağı

Çelik, M. (2025, November 8). *AutoScout24 car listings dataset*. Kaggle.  
https://www.kaggle.com/datasets/clkmuhammed/autoscout24-car-listings-dataset/data

Bu proje eğitim amaçlıdır. AutoScout24 verileri araştırma ve eğitim amaçlı kullanılmıştır.

---

**Son güncelleme:** 18 Kasım 2025  
**Status:** ✅ Tamamlandı
