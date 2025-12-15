# 🧠 İki Aşamalı Yapay Zeka Destekli Beyin Tümörü Teşhis Sistemi

**Problem:** Radyoloji alanında yüksek dikkat gerektiren ve zaman alan tıbbi görüntüleme analiz süreçlerini hızlandırmak ve insan hatasını minimize etmek.

**Çözüm:** Derin Öğrenme (Deep Learning) tabanlı, hem veriyi doğrulayan hem de tümörü tespit eden iki aşamalı güvenlikli bir karar destek sistemi.

---

## ⚙️ Proje Mimarisi: İki Aşamalı Güvenlik Boru Hattı

Sistem, hatalı veri girişini engelleyen yenilikçi bir yapıda çalışır.

1.  ### Aşama 1: Validator Model (Veri Doğrulayıcı)
    * **İşlev:** Yüklenen görüntünün gerçekten bir **Beyin MR'ı** olup olmadığını saniyeler içinde kontrol eder.
    * **Faydası:** Alakasız verilerin (rastgele fotoğraflar vb.) ana modele ulaşmasını engelleyerek hatalı veya anlamsız teşhis üretme riskini sıfırlar.

2.  ### Aşama 2: Detector Model (Tümör Teşhis Uzmanı)
    * **İşlev:** Doğrulamadan geçen MR görüntüsü üzerinde tümörlü (Tumor) ve tümörsüz (No Tumor) ayrımını yaparak olasılık değeri (Confidence Score) ile sonuç döndürür.

---

## 🛠️ Teknoloji Yığını ve Algoritmalar

* **Programlama Dili:** Python 3.x
* **Derin Öğrenme:** TensorFlow & Keras
* **Algoritma:** Evrişimli Sinir Ağları (**CNN - Convolutional Neural Networks**)
* **Web Çatısı:** Flask (Modeli bir web servisi olarak çalıştırmak için)
* **Veri İşleme:** NumPy, OpenCV
* **Arayüz:** HTML/CSS (Templates klasöründe bulunmaktadır)

## ✅ Model Performansı

| Model | Kullanılan Algoritma | Test Doğruluğu (Accuracy) | Kritik Metrik (F1-Score) |
| :--- | :--- | :--- | :--- |
| **Detector** | CNN | **% [ÖRN: 97.5%]** | **[ÖRN: 0.96]** |
| **Validator** | CNN | **% [ÖRN: 99.8%]** | **[ÖRN: 0.99]** |

## 🚀 Yerel Kurulum ve Başlatma

1.  **Gereksinimler:** Proje klasörüne girin ve gerekli kütüphaneleri kurun:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Uygulamayı Başlat:** Flask uygulamasını çalıştırın:
    ```bash
    python app.py
    ```
3.  Tarayıcınızda `http://127.0.0.1:5000` adresine gidin.

---

## ✨ Gelecek Vizyonu

* Segmentasyon: Tümörün sadece varlığını değil, MR görüntüsü üzerinde tam konumunu işaretleme.
* Mobil Uyumlu Arayüz Geliştirme.
## 🖼️ Uygulama Arayüzü ve İş Akışı Görselleştirme

Projeniz, Derin Öğrenme modellerini bir araya getiren, kullanıcı ve yönetici panellerine sahip, tam fonksiyonlu bir Flask web uygulaması olarak tasarlanmıştır.

---

### 1. Kullanıcı Giriş ve Ana Analiz Ekranı (Frontend Girişi)
Uygulama, güvenli bir kullanıcı tabanı oluşturmak için giriş/kayıt ekranları ile başlar. Ana Sayfa, kullanıcıya MR görüntüsünü yüklemesi için yalın ve anlaşılır bir arayüz sunar.

|                Giriş Ekranı                |              Ana Yükleme Ekranı               |
|:------------------------------------------:|:---------------------------------------------:|
| ![Kullanıcı Giriş/Kayıt Ekranı](giris.png) | ![MR Görüntüsü Yükleme Arayüzü](anasayfa.png) |

<br>

### 2. Analiz Sonucu (Risk Tespiti)
Kullanıcı MR görüntüsünü yükledikten ve model (Detector) çalıştığında, sonuçlar net bir risk skoru ve görsel çıktı ile sunulur. Bu ekran, teşhiste güven skorunun ve görsel teyidin önemini vurgular.

* **Risk Skoru:** Modelin güven oranı (%3.38 DÜŞÜK RİSK).
* **Görsel Teyit:** Orijinal görüntü ile yapay zeka tarafından işlenmiş ısı haritası (Risk Analizi) yan yana gösterilir.

![Model Analiz Sonucu ve Isı Haritası](analiz.png)

<br>

### 3. Yönetici Paneli ve Raporlama (Sistem Yönetimi ve Veri Kaydı)
Bu bölüm, projenin sadece bir prototip değil, aynı zamanda operasyonel bir sistem olduğunu gösterir. Yönetici paneli, sistemin genel durumu ve geçmiş tarama kayıtlarının takibi için hayati önem taşır.

* **Genel Durum:** Toplam kullanıcı, analiz sayısı ve sistem durumu anlık takip edilir.
* **Kayıt ve Raporlama:** Her tarama, hasta adı, tarih, risk sonucu, sayısal skor ve **PDF rapor** oluşturma seçeneğiyle birlikte kayıt altında tutulur. Bu, tıbbi arşivleme yeteneğini gösterir.

![Hastane Genel Durumu ve Raporlama Paneli](adminPaneli.png)