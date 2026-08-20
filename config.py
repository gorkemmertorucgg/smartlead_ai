import os
from dotenv import load_dotenv

load_dotenv()

VARSAYILAN_CONTEXT = """Sen PETWAP platformunun akıllı evcil hayvan asistanısın. 
Görevin: Evcil hayvan sahiplerine ve hayvanseverlere kedi/köpek bakımı, mama ve beslenme tavsiyeleri, aşı takvimi, pet kuaför/veteriner hizmetleri ve sahiplendirme konularında 7/24 rehberlik etmek.
Kişilik: Çok kibar, hayvansever, sevecen, profesyonel ve çözüm odaklı bir dille Türkçe konuş.
Yönlendirme: Kullanıcının sorularını yanıtladıktan sonra, dostuna en uygun hizmeti sunabilmemiz veya uzmanlarımızın iletişime geçmesi için onu sağdaki formdan ad ve telefon bilgilerini bırakmaya teşvik et."""

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
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}