import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image, ImageDraw

# --- AYARLAR ---
# Modelleri uygulamanın başında bir kere yükleyelim (Performans için)
# Eğer modelleri bulamazsa hata vermesin, kullanıcıyı uyarsın diye try-except koyuyoruz.
try:
    print("⏳ Modeller yükleniyor, lütfen bekleyin...")
    VALIDATOR_MODEL = load_model('models/mr_validator_model.h5')
    RISK_MODEL = load_model('models/cancer_risk_model.h5')
    print("✅ Modeller başarıyla hafızaya alındı!")
except Exception as e:
    print(f"❌ Model Yükleme Hatası: {e}")
    print("Lütfen 'models' klasöründe .h5 dosyalarının olduğundan emin olun.")
    VALIDATOR_MODEL = None
    RISK_MODEL = None


def prepare_image(filepath, target_size):
    """Resmi yapay zekanın anlayacağı formata (array) çevirir."""
    img = load_img(filepath, target_size=target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Tekli batch haline getir
    img_array /= 255.0  # Normalize et (0-1 arası)
    return img_array


def analyze_image(filepath):
    """
    Bu fonksiyon artık GERÇEK modelleri kullanır.
    """

    # 0. Model Kontrolü
    if VALIDATOR_MODEL is None or RISK_MODEL is None:
        return {
            "success": False,
            "message": "AI Modelleri yüklenemedi. Lütfen server loglarını kontrol edin."
        }

    # 1. PIPELINE: MR Doğrulama (Validator Model)
    # Validator modelimiz 128x128 ile eğitilmişti (Colab koduna göre)
    input_val = prepare_image(filepath, (128, 128))
    is_mri_prob = VALIDATOR_MODEL.predict(input_val)[0][0]

    # Eşik değer: %50'nin altındaysa bu bir MR değildir.
    if is_mri_prob < 0.5:
        # MR Değilse hemen reddet
        return {
            "success": False,
            "message": f"❌ Yüklenen görüntü bir MR testi olarak algılanmadı.\n(Güven Skoru: %{is_mri_prob * 100:.1f})\nLütfen geçerli bir beyin MR görüntüsü yükleyin."
        }

    # 2. PIPELINE: Kanser Risk Analizi (Risk Model)
    # Risk modelimiz 224x224 ile eğitilmişti
    input_risk = prepare_image(filepath, (224, 224))
    risk_score_raw = RISK_MODEL.predict(input_risk)[0][0]

    # Skoru yüzdeliğe çevir (%0 - %100)
    risk_percent = round(risk_score_raw * 100, 2)

    # Etiketleme
    if risk_percent > 50:
        risk_label = "YÜKSEK RİSK (TÜMÖR ŞÜPHESİ)"
        color_code = "red"
        overlay_color = (255, 0, 0)  # Saf Kırmızı
    else:
        risk_label = "DÜŞÜK RİSK (TEMİZ)"
        color_code = "green"
        overlay_color = (0, 255, 0)  # Yeşil

    # 3. GÖRSEL İŞLEME (Heatmap Efekti)
    # Not: Segmentasyon modeli (U-Net) kullanmadığımız için tümörün "tam yerini" nokta atışı çizemeyiz.
    # Ancak Classification modeline dayanarak risk yüksekse görüntüyü kırmızı tonla kaplayarak uyarı verebiliriz.

    original_img = Image.open(filepath).convert("RGBA")

    # Yarı saydam bir katman oluştur
    overlay = Image.new('RGBA', original_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Risk ne kadar yüksekse, kırmızılık o kadar koyu olsun (Opaklık ayarı)
    # Maksimum opaklık 100 olsun (resim tamamen kapanmasın diye)
    opacity = int(risk_score_raw * 100)

    # Tüm resme hafif bir renk filtresi atıyoruz
    draw.rectangle(
        [(0, 0), original_img.size],
        fill=(overlay_color[0], overlay_color[1], overlay_color[2], opacity)
    )

    # Resimleri birleştir
    processed_img = Image.alpha_composite(original_img, overlay)

    # Kaydet
    filename = os.path.basename(filepath)
    result_path = os.path.join('static/results', 'processed_' + filename)
    processed_img.convert("RGB").save(result_path)

    return {
        "success": True,
        "is_mri": True,
        "risk_score": risk_percent,
        "risk_label": risk_label,
        "original_path": filepath,
        "processed_path": result_path,
        "color_code": color_code
    }