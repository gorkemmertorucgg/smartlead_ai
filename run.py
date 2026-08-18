import os
from app import create_app

# Ortam değişkenine göre uygulamayı üret
ortam = os.environ.get('FLASK_ENV', 'development')
app = create_app(ortam)

if __name__ == '__main__':
    # Sunucuyu yerel makinede başlat (Port 5000)
    app.run(host='0.0.0.0', port=5000, debug=True)