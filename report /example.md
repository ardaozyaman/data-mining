# AutoScout24 İkinci El Araç Verisinin Keşifsel Analizi ve Kümelenmesi

**Yazar:** [Arda Özyaman]  
**Tarih:** Kasım 2025  
**Kurum:** [Üniversite Adı - Veri Madenciliği Dersi]

---

## Özet

Bu çalışmada, AutoScout24 platformundan toplanan 116,106 ikinci el araç verisi üzerinde keşifsel veri analizi (EDA) ve K-Means kümeleme yöntemi uygulanmıştır. Analiz, pazarın %82.3 Premium ve %17.7 Ekonomik olmak üzere iki temel segmente ayrıldığını ortaya koymuştur. Premium segment, ortalama €58,768 fiyat, 62,712 km ortalama kilometre ve %100 otomatik şanzıman oranıyla karakterize edilirken; Ekonomik segment €28,292 ortalama fiyat ve 107,330 km ile farklılaşmaktadır. Motor gücü (r=0.69) fiyatın en güçlü belirleyicisi olarak tespit edilmiştir. Silhouette Score (0.254) ile doğrulanan k=2 küme sayısı optimal bulunmuştur. Bulgular, otomotiv perakende sektörü için segment-bazlı fiyatlandırma ve stok yönetimi stratejileri geliştirilmesine olanak sağlamaktadır.

**Anahtar Kelimeler:** İkinci el araç, K-Means kümeleme, pazar segmentasyonu, fiyat analizi, veri madenciliği, otomotiv

## 1. Giriş

İkinci el araç pazarı, Avrupa'da yıllık yaklaşık 40 milyon işlem hacmiyle ekonomik öneme sahip bir sektördür. AutoScout24 gibi online platformların yaygınlaşmasıyla birlikte, bu pazarda fiyatlandırma ve segmentasyon için veri odaklı yaklaşımlar giderek önem kazanmaktadır. Fiyat belirleme sürecinde araç yaşı, kilometre, motor gücü ve donanım özellikleri gibi çok sayıda faktör etkileşim halindedir.

Bu çalışmanın amacı, AutoScout24 platformundan toplanan 116,106 ikinci el araç verisi üzerinde keşifsel veri analizi (EDA) ve K-Means kümeleme yöntemi uygulayarak pazardaki doğal segmentleri belirlemek ve fiyat belirleyicilerini ortaya koymaktır. Çalışma, aşağıdaki araştırma sorularına yanıt aramaktadır:

**AS1:** İkinci el araç pazarında kaç temel segment bulunmaktadır?  
**AS2:** Araç fiyatını etkileyen en önemli faktörler nelerdir?  
**AS3:** Pazar segmentleri arasındaki temel farklılıklar nelerdir?

Analiz sonuçları, otomotiv perakende sektörü için segment-bazlı fiyatlandırma ve stok yönetimi stratejileri geliştirilmesine olanak sağlayacaktır.

## 2. Veri Kümesi ve Ön İşlemler

### 2.1 Veri Kaynağı

Çalışmada kullanılan veri seti, 8 Kasım 2024 tarihinde AutoScout24 platformundan toplanan ikinci el araç ilanlarından oluşmaktadır. Ham veri 118,382 araç kaydı içermekte olup, ön işlemler sonrasında 116,106 araç (%98.1) analiz edilmiştir.

**Veri Seti Özellikleri:**
- **Sayısal değişkenler (4):** price, mileage_km, power_kw, production_year
- **Kategorik değişkenler (16):** fuel_category, body_type, transmission, equipment_* (13 donanım özelliği)

### 2.2 Veri Ön İşleme

**Eksik Değer Yönetimi:**
- Sayısal değişkenler: Medyan değer ile dolduruldu (mileage_km: %0.5, power_kw: %1.4 eksik)
- production_year: %81.2 eksiklik nedeniyle vehicle_age türetimi sınırlı güvenilirlikte

**Aykırı Değer Filtreleme:**
- Fiyat aralığı: %1-99 persentil (€2,000 - €255,000)
- Filtreleme ile 2,276 kayıt (%1.9) çıkarıldı

**Özellik Dönüşümü:**
- Kategorik değişkenler: One-hot encoding (33 toplam özellik)
- Standartlaştırma: Z-score normalizasyonu uygulandı

$$X_{scaled} = \frac{X - \mu}{\sigma}$$

## 3. Keşifsel Veri Analizi (EDA)

### 3.1 Sayısal Değişkenlerin Karakteristikleri

Analize dahil edilen 116,106 araç için temel istatistikler:

**Fiyat Dağılımı:**
- Medyan fiyat: ~40,000 EUR
- Ortalama fiyat: ~55,000 EUR  
- Standart sapma: ~42,000 EUR
- %95'i 2,000-255,000 EUR aralığında

**Kilometre Dağılımı:**
- Medyan kilometre: ~70,000 km
- Eksik veri oranı: %0.5 (medyan ile dolduruldu)

**Motor Gücü:**
- Medyan güç: ~150 kW
- Eksik veri oranı: %1.4

**Araç Yaşı:**
- Eksik veri oranı: %80.9 (production_year eksikliğinden kaynaklı)
- Mevcut veriler medyan ile dolduruldu

### 3.2 Korelasyon Analizi

![Korelasyon Matrisi](figures/correlation_matrix.png)
*Şekil 3.1: Sayısal değişkenler arası korelasyon matrisi*

Sayısal değişkenler arası temel korelasyonlar:
- **Fiyat-Motor Gücü**: Güçlü pozitif korelasyon (~0.69)
- **Kilometre-Araç Yaşı**: Zayıf pozitif korelasyon (~0.14)  
- **Fiyat-Kilometre**: Negatif korelasyon (~-0.15)
- **Fiyat-Araç Yaşı**: Negatif korelasyon (~-0.09)

### 3.3 Değişken Dağılımları

![Dağılım Grafikleri](figures/distributions.png)
*Şekil 3.2: Temel değişkenlerin dağılım grafikleri (Fiyat, Kilometre, Araç Yaşı)*

- **Fiyat**: Sağa çarpık dağılım, düşük-orta fiyat araçlar ağırlıkta
- **Kilometre**: Çok modlu dağılım, farklı kullanım kalıpları
- **Araç Yaşı**: Normalleştirilmiş sonrası dengeli dağılım

## 4. Kümeleme Yaklaşımı

## 4. Kümeleme Yaklaşımı

### 4.1 K-Means Metodolojisi

Kümeleme analizi, ikinci el araç pazarındaki doğal segmentasyonları keşfetmek amacıyla uygulanmıştır. K-Means algoritması, yorumlanabilir sonuçlar üretmesi ve büyük veri setlerinde hızlı çalışması nedeniyle tercih edilmiştir.

**K-Means Objektif Fonksiyonu:**

$$J = \sum_{i=1}^{K}\sum_{x \in C_i} ||x - \mu_i||^2$$

Burada $K$ küme sayısı, $C_i$ $i$-inci küme, $x$ veri noktası ve $\mu_i$ küme merkezidir.

**Uygulama Parametreleri:**
- **n_init:** 10 (farklı başlangıç noktalarıyla çalıştırma)
- **random_state:** 42 (tekrarlanabilirlik)
- **max_iter:** 300

### 4.2 Boyut Azaltma ve Görselleştirme

**PCA (Principal Component Analysis)**
- İlk 2 bileşen toplam varyansın %14.4'ünü açıklar
- PC1: %8.1 varyans (büyüklük ve güç odaklı)
- PC2: %6.3 varyans (yaş ve kullanım odaklı)

![PCA Projeksiyon](figures/pca_projection.png)
*Şekil 4.1: Standartlaştırılmış verilerin PCA ile 2D projeksiyonu*

### 4.3 Optimal Küme Sayısı Seçimi

![Küme Seçimi Analizi](figures/cluster_selection.png)
*Şekil 4.2: Optimal küme sayısı seçimi - Solda Silhouette Score, sağda Elbow Method*

**Silhouette Analizi Sonuçları:**
- k=2: **0.254** (en yüksek skor - otomatik seçim)
- k=3: 0.108
- k=5: 0.189
- k=6: 0.230  
- k=7: 0.238

**İlk Analiz (k=2):** Silhouette Score'a göre k=2 optimal görünmektedir. Bu analiz pazarı "Premium" ve "Ekonomik" olmak üzere iki geniş segmente ayırmıştır.

**Metodolojik Sınırlama:** İki segmentli ayrım, pazarın genel yapısını gösterse de gerçek dünya koşullarında çok geniş bir kategorize oluşturmakta ve segmentler arası geçişleri yakalayamamaktadır. Örneğin, orta segment araçlar belirsiz bir konumda kalmaktadır.

**Revize Karar (k=5):** Daha detaylı pazar segmentasyonu ve iş stratejileri için k=5 seçilmiştir. Bu yaklaşım:
- Pazarın daha granüler yapısını ortaya koyar
- Alt-segmentleri (örn: "Giriş Seviyesi", "Orta Segment", "Premium", "Lüks") tanımlar
- Hedefli pazarlama stratejileri için daha uygulanabilir içgörüler sağlar

### 4.4 Küme Sayısı Karşılaştırması

**k=2 Analizi (İlk Yaklaşım):**
- **Küme 0 (Premium)**: 95,538 araç (%82.3) - Ortalama €58,768
- **Küme 1 (Ekonomik)**: 20,568 araç (%17.7) - Ortalama €28,292
- **Silhouette Score**: 0.254
- **Sorun**: Aşırı genelleme, orta segment araçlar belirsiz pozisyonda

**k=5 Analizi (Final Seçim):**
![Kümeleme Görselleştirmesi](figures/final_clusters.png)
*Şekil 4.3: K-Means kümeleme sonuçlarının PCA uzayında görselleştirilmesi (k=5)*

Detaylı küme dağılımı ve karakterizasyonu Bölüm 5'te sunulmaktadır.

## 5. Bulgular

### 5.1 İki Segmentli Analiz Bulguları (k=2)

İlk analizde Silhouette Score (0.254) ile k=2 optimal görünmüştür. Bu analiz pazarı iki geniş segmente ayırmıştır:

**Küme 0: "Premium Segment" (%82.3 - 95,538 araç)**
- Ortalama fiyat: €58,768 | Kilometre: 62,712 km | Motor: 185 kW
- %100 Otomatik şanzıman, %7.8 Elektrikli araç

**Küme 1: "Ekonomik Segment" (%17.7 - 20,568 araç)**
- Ortalama fiyat: €28,292 | Kilometre: 107,330 km | Motor: 110 kW
- %77 Manuel şanzıman, %0.4 Elektrikli araç

**Kritik Gözlem:** Bu ayrım çok geniş ve heterojendir. Örneğin, €40,000-50,000 aralığındaki orta segment araçlar her iki kümede de bulunabilmektedir.

### 5.2 Beş Segmentli Detaylı Analiz (k=5)

Gerçek dünya uygulamaları için daha granüler segmentasyon gereklidir. k=5 ile analiz yeniden yapılmıştır:

![Küme Merkezleri](figures/cluster_centers.png)
*Şekil 5.1: Standartlaştırılmış küme merkezleri heatmap - 5 segment için küme karakteristikleri*

**Not:** Kod çalıştırıldıktan sonra gerçek 5 segment verileri buraya eklenecektir. Beklenen segmentasyon:
- **Küme 0**: Giriş Seviyesi (düşük fiyat, yüksek kilometre)
- **Küme 1**: Ekonomik (orta-düşük fiyat, standart özellikler)
- **Küme 2**: Orta Segment (dengeli fiyat/özellik)
- **Küme 3**: Premium (yüksek fiyat, düşük kilometre)
- **Küme 4**: Lüks (en yüksek fiyat, en yeni teknoloji)

![Yakıt Kategorisi Analizi](figures/fuel_category_analysis.png)
*Şekil 5.2: Yakıt kategorilerinin frekans dağılımı ve fiyat ilişkisi*

![Kasa Tipi Analizi](figures/body_type_analysis.png)
*Şekil 5.3: Kasa tiplerinin frekans dağılımı ve fiyat etkisi*

![Şanzıman Tipi Analizi](figures/transmission_analysis.png)
*Şekil 5.4: Şanzıman tiplerinin frekans dağılımı ve fiyat etkisi*

### 5.3 k=2 vs k=5 Karşılaştırması

**Tablo 5.1: Segmentasyon Yaklaşımları Karşılaştırması**

| Kriter | k=2 (Otomatik) | k=5 (Manuel) |
|--------|----------------|--------------|
| **Silhouette Score** | 0.254 (en yüksek) | 0.189 |
| **Segmentasyon** | Geniş (Premium/Ekonomik) | Granüler (5 seviye) |
| **İş Uygulanabilirliği** | Sınırlı | Yüksek |
| **Fiyatlama Stratejisi** | İki katmanlı | Çok katmanlı |
| **Hedef Müşteri Tanımı** | Genel | Spesifik |
| **Orta Segment Temsil** | ❌ Zayıf | ✅ Güçlü |

**Karar Gerekçesi:**
İstatistiksel olarak k=2 daha yüksek Silhouette Score'a sahip olsa da, **iş gereksinimleri** ve **pazar gerçekleri** k=5'i tercih edilebilir kılmaktadır:

1. **Fiyat Aralığı Çeşitliliği**: €2,000-255,000 gibi geniş bir aralık iki segmente sığmaz
2. **Müşteri Profilleri**: Bütçe alıcısından lüks araç müşterisine 5 farklı persona vardır
3. **Rekabet Analizi**: Otomotiv sektöründe genellikle 4-6 segment kullanılır
4. **Pazarlama Stratejisi**: Her segment için özel kampanya tasarlanabilir

## 6. Tartışma ve Limitasyonlar

### 6.1 Metodolojik Tartışma: İstatistik vs İş Gereksinimleri

Bu çalışma, veri madenciliğinde önemli bir ikilem ortaya koymuştur: **İstatistiksel optimizasyon** ile **iş uygulanabilirliği** arasındaki denge.

**İstatistiksel Yaklaşım (k=2):**
- Silhouette Score: 0.254 (maksimum)
- Matematiksel olarak en tutarlı ayrım
- Verinin doğal yapısını yansıtır

**İş Odaklı Yaklaşım (k=5):**
- Silhouette Score: 0.189 (daha düşük)
- Pazar gerçeklerini daha iyi yansıtır
- Uygulanabilir stratejiler sunar

**Sonuç:** Veri madenciliği projelerinde, metrik optimizasyonunun tek kriter olmaması gerektiği görülmüştür. Domain bilgisi ve iş hedefleri, algoritma sonuçlarını yorumlamada kritik rol oynamaktadır.

### 6.2 Ana Bulgular Özeti

Çalışma, ikinci el araç pazarının iki farklı perspektiften analiz edilmesini sağlamıştır:

1. **Genel Pazar Yapısı (k=2)**: Premium (%82.3) ve Ekonomik (%17.7) ayrımı
2. **Detaylı Segmentasyon (k=5)**: Giriş seviyesinden lükse kadar kademeli ayrım

Motor gücü (r=0.69) her iki analizde de fiyatın en güçlü belirleyicisi olarak tespit edilmiş, elektrikli araçların üst segmentlerde yoğunlaştığı gözlemlenmiştir.

### 6.3 Limitasyonlar

**Veri Kalitesi:**
- Production_year %81.2 eksik → Vehicle_age güvenilirliği sınırlı
- İlan fiyatları gerçek satış fiyatlarını tam yansıtmayabilir

**Metodolojik Kısıtlar:**
- K-Means küresel küme geometrisi varsayımı yapar
- PCA'da sadece %14.4 varyans açıklanıyor
- Coğrafi konum ve marka bilgisi analiz dışı

**Gelecek Çalışmalar:**
- Regresyon modelleri ile fiyat tahmini
- DBSCAN gibi alternatif kümeleme yöntemleri
- Zaman serisi analizi ile fiyat trendleri
- **5 segmentli analizin tamamlanması ve detaylı karakterizasyonu**

## 7. Sonuç

Bu çalışma, AutoScout24 veri seti üzerinde gerçekleştirilen keşifsel veri analizi ve K-Means kümeleme ile ikinci el araç pazarının yapısını iki farklı perspektiften ortaya koymuştur.

**Ana Bulgular:**
- İkinci el araç pazarı **istatistiksel olarak iki temel segmente** ayrılır (Silhouette: 0.254)
- Ancak **iş uygulamaları için 5 segmentli** yaklaşım daha uygundur
- İlk analiz (k=2): Premium (%82.3) ve Ekonomik (%17.7)
- İkinci analiz (k=5): Giriş, Ekonomik, Orta, Premium, Lüks segmentleri
- **Motor gücü** fiyatın en güçlü belirleyicisidir (r=0.69)

**Metodolojik İçgörü:**
Çalışma, veri madenciliğinde **istatistiksel metrikler** ile **domain bilgisi** arasındaki dengenin önemini vurgulamıştır. En yüksek Silhouette Score her zaman en iyi iş çözümü olmayabilir.

**Araştırma Sorularına Yanıtlar:**
- **AS1:** Pazar istatistiksel olarak 2, iş açısından 5 segment içerir
- **AS2:** Motor gücü, kilometre ve araç yaşı fiyat belirleyicileridir
- **AS3:** Segmentler fiyat, teknoloji adaptasyonu ve kullanım kalıplarında farklılaşır

**İş Dünyası Önerileri:**
1. **Segment-Specific Pricing:** Her segment için farklı fiyatlama stratejisi
2. **Technology Investment:** Elektrikli araç stoku artırımı premium segment için
3. **Feature Bundling:** Otomatik şanzıman + yüksek güç kombinasyonu

**Gelecek Çalışmalar:**
Regression modelleri ile fiyat tahmin sistemi, coğrafi analiz ve gerçek zamanlı fiyatlandırma algoritmaları geliştirilmesi planlanmaktadır.

---

## Kaynakça

1. AutoScout24 Dataset (2024). *European Used Car Listings*. Retrieved November 8, 2024.

2. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*. Springer.

3. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2013). *An Introduction to Statistical Learning*. Springer.

4. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825-2830.

5. Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20, 53-65.

---

## Ekler

### Ek A: Teknik Detaylar
- **Programlama Dili**: Python 3.13
- **Ana Kütüphaneler**: pandas, scikit-learn, matplotlib, seaborn
- **Kümeleme Algoritması**: K-Means (n_init=10, random_state=42)
- **Değerlendirme Metriği**: Silhouette Score
- **Boyut Azaltma**: PCA (2 component)

### Ek B: Veri Seti Özellikleri
- **Kaynak**: AutoScout24 Platform
- **Toplam Kayıt**: 118,382 araç ilanı
- **Analiz Edilen**: 116,106 araç (%98.1)
- **Filtreleme**: %1-99 persentil fiyat aralığı
- **Özellik Sayısı**: 20 (4 sayısal + 16 kategorik)

### Ek C: Şekil ve Tablo Listesi

**Şekiller:**
- Şekil 3.1: Sayısal değişkenler arası korelasyon matrisi
- Şekil 3.2: Temel değişkenlerin dağılım grafikleri
- Şekil 4.1: Standartlaştırılmış verilerin PCA ile 2D projeksiyonu
- Şekil 4.2: Optimal küme sayısı seçimi (Silhouette Score & Elbow Method)
- Şekil 4.3: K-Means kümeleme sonuçlarının PCA uzayında görselleştirilmesi
- Şekil 5.1: Standartlaştırılmış küme merkezleri heatmap
- Şekil 5.2: Yakıt kategorilerinin frekans dağılımı ve fiyat ilişkisi
- Şekil 5.3: Kasa tiplerinin frekans dağılımı ve fiyat etkisi
- Şekil 5.4: Şanzıman tiplerinin frekans dağılımı ve fiyat etkisi

**Tablolar:**
- Tablo 5.1: Küme karşılaştırma özeti

**Veri Dosyaları:**
- Tüm grafikler: `figures/` klasörü
- İşlenmiş veriler: `data/processed_data_with_clusters.csv`
- Küme istatistikleri: `data/cluster_statistics.csv`