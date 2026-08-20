from flask import Flask, jsonify
from flask_cors import CORS
from config import config_dict
from app.database import init_db

def create_app(config_name='default'):
    """Uygulama fabrikası (Application Factory)."""
    app = Flask(__name__, template_folder='../templates')
    
    # 1. Konfigürasyonu yükle
    app.config.from_object(config_dict.get(config_name, config_dict['default']))

    # 2. CORS aç (Wix bağlantısı için)
    CORS(app, origins="*", methods=["GET", "POST", "OPTIONS"])

    # 3. Veritabanını başlat
    with app.app_context():
        init_db(app)

    # 4. Blueprint'leri kaydet
    from app.routes import api_blueprint, sayfa_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(sayfa_blueprint)

    # 5. Canlılık kontrolü
    @app.route('/health')
    def health_check():
        return jsonify({'durum': 'aktif', 'servis': 'PETWAP AI API', 'versiyon': '1.0.0'}), 200

    return app