import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Uygulamanın genel ayar sınıfı."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'varsayilan-anahtar')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'smartlead.db')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # Doğrudan Türkçe yanıt vermesi için net sistem talimatı
    BUSINESS_CONTEXT = os.environ.get(
        'BUSINESS_CONTEXT',
        """Sen SmartLead AI akıllı satış ve destek asistanısın. 
        KURAL: Asla düşünme sürecini, analizini veya İngilizce taslaklarını cevaba dahil etme.
        Kullanıcıya doğrudan, kibar ve profesyonel bir Türkçe ile yanıt ver. 
        Müşteriye bilgi verdikten sonra adını ve telefon numarasını form üzerinden bırakmaya yönlendir."""
    )

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}