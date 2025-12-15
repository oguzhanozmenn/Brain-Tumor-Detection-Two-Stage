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