import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config_dict
from app.database import init_db

def create_app(config_name=None):
    """
    Uygulama Fabrikası fonksiyonu.
    Tüm modülleri (CORS, DB, Rotalar) burada birleştirir.
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__, template_folder='templates')

    # 1. Konfigürasyonu yükle
    app_config = config_dict.get(config_name, config_dict['default'])
    app.config.from_object(app_config)

    # 2. CORS izinlerini tanımla
    CORS(app, origins=app.config.get('CORS_ORIGINS', '*'), methods=['GET', 'POST', 'OPTIONS'])

    # 3. Veritabanını başlat
    with app.app_context():
        init_db(app)

    # 4. Blueprint rotalarını sisteme kaydet
    from app.routes import pages_bp, api_bp
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # 5. Sunucu canlılık kontrol rotası
    @app.route('/health')
    def health():
        return jsonify({'durum': 'aktif', 'mesaj': 'SmartLead AI sunucusu calisiyor'}), 200

    return app