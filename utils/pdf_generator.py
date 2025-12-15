import os
from fpdf import FPDF
from datetime import datetime


class PDFReport(FPDF):
    def header(self):
        # Logo veya Başlık
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'AKILLI MR ANALIZ ASISTANI', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        # Alt bilgi
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}', 0, 0, 'C')


def clean_text(text):
    """
    FPDF standart fontlari bazi Turkce karakterleri desteklemez.
    Bu fonksiyon karakterleri en yakin Latin harfine cevirir.
    """
    replacements = {
        'ğ': 'g', 'Ğ': 'G', 'ş': 's', 'Ş': 'S', 'ı': 'i', 'İ': 'I',
        'ç': 'c', 'Ç': 'C', 'ö': 'o', 'Ö': 'O', 'ü': 'u', 'Ü': 'U'
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    return text


def create_pdf(result, output_filename="report.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- 1. Başlık Bilgileri ---
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, clean_text(f"Rapor Tarihi: {datetime.now().strftime('%d-%m-%Y %H:%M')}"), ln=True)
    pdf.cell(0, 10, clean_text(f"Dosya Adi: {os.path.basename(result['original_path'])}"), ln=True)
    pdf.ln(10)

    # --- 2. Analiz Sonucu (Kutu İçinde) ---
    pdf.set_font("Arial", 'B', 16)

    # Riski Yazdır
    risk_text = clean_text(f"TESPIT EDILEN RISK: %{result['risk_score']}")
    pdf.cell(0, 10, risk_text, ln=True, align='C')

    # Durum (Yüksek/Düşük)
    status_text = clean_text(result['risk_label'])
    pdf.set_font("Arial", size=14)
    if result['risk_score'] > 50:
        pdf.set_text_color(255, 0, 0)  # Kırmızı
    else:
        pdf.set_text_color(0, 128, 0)  # Yeşil

    pdf.cell(0, 10, f"({status_text})", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)  # Siyaha dön
    pdf.ln(10)

    # --- 3. Görseller ---
    # Resimlerin sayfaya sığması için genişlik ayarı
    page_width = pdf.w - 20
    img_width = page_width / 2 - 5

    y_position = pdf.get_y()

    # Orijinal Resim
    pdf.image(result['original_path'], x=10, y=y_position, w=img_width)
    pdf.set_xy(10, y_position + img_width + 5)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(img_width, 10, clean_text("Orijinal Goruntu"), align='C')

    # İşlenmiş Resim
    pdf.image(result['processed_path'], x=10 + img_width + 10, y=y_position, w=img_width)
    pdf.set_xy(10 + img_width + 10, y_position + img_width + 5)
    pdf.cell(img_width, 10, clean_text("AI Risk Analizi"), align='C')

    pdf.ln(20)

    # --- 4. Yasal Uyarı ---
    pdf.set_y(-50)  # Sayfanın sonuna yaklaş
    pdf.set_font("Arial", size=8)
    pdf.multi_cell(0, 5, clean_text(
        "YASAL UYARI: Bu rapor Yapay Zeka (AI) tarafindan olusturulmustur. "
        "Kesinlikle tıbbi teshis yerine gecmez. Sonuclar sadece on bilgi amacli olup, "
        "kesin tani icin uzman bir doktora basvurulmalidir."
    ))

    # Dosyayı Kaydet
    report_path = os.path.join('static/reports', output_filename)
    pdf.output(report_path)

    return report_path