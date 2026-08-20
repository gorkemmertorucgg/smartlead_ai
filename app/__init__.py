import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config_dict
from app.database import init_db

def create_app(config_name='default'):
    """Uygulama fabrikası (Application Factory)."""
    # Templates klasörünün tam yolunu dinamik olarak belirle
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    app = Flask(__name__, template_folder=template_dir)
    
    # 1. Konfigürasyonu yükle
    app.config.from_object(config_dict.get(config_name, config_dict['default']))

    # 2. CORS aç
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

# Gunicorn (app:app) başlatıcı nesnesi
env_mode = os.environ.get('FLASK_ENV', 'production')
app = create_app(env_mode)