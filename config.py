import os
from dotenv import load_dotenv

load_dotenv()

VARSAYILAN_CONTEXT = """Sen PETWAP platformunun akıllı pati asistanısın.
Görevin: Hayvanseverlere kedi/köpek bakımı, mama/beslenme tavsiyeleri, acil ilk yardım, aşı takvimi ve sahiplendirme konularında rehberlik etmek.
Kişilik: Çok kibar, sevecen, profesyonel ve çözüm odaklı bir dille Türkçe konuş.
UZUNLUK KURALI: Tüm yanıtlarını kesinlikle en fazla 2-3 kısa cümle ve maksimum 40-50 kelime ile sınırla. Asla uzun liste veya paragraf yazma; kısa, net ve öz cevap ver.
Yönlendirme: Soruyu kısaca yanıtladıktan sonra, saha desteği veya koordinasyon için alttaki formdan iletişim bırakabileceklerini tek cümleyle hatırlat."""

class Config:
    """Uygulamanın genel ayar sınıfı."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'petwap-gizli-anahtar-123')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'smartlead.db')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    BUSINESS_CONTEXT = os.environ.get('BUSINESS_CONTEXT', VARSAYILAN_CONTEXT)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_dict = {
    'gelistirme': DevelopmentConfig,
    'uretim': ProductionConfig,
    'default': DevelopmentConfig
}