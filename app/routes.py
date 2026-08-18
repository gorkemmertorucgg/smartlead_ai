import re
from flask import Blueprint, render_template, request, jsonify
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

pages_bp = Blueprint('pages', __name__)
api_bp = Blueprint('api', __name__)

@pages_bp.route('/')
def index():
    return render_template('index.html')

@pages_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    veri = request.get_json() or {}
    mesaj = veri.get('mesaj')
    gecmis = veri.get('gecmis', [])

    if not mesaj:
        return jsonify({'basari': False, 'hata': 'Mesaj alanı boş bırakılamaz.'}), 400

    try:
        yanit = ai_service.yanit_uret(mesaj, gecmis)
        
        # 1. <think> etiketleri varsa temizle
        if '</think>' in yanit:
            yanit = yanit.split('</think>')[-1].strip()
            
        # 2. Düşünme adımları veya İngilizce taslak kaldıysa sadece son yanıtı al
        if '**Formulate Response' in yanit:
            yanit = re.split(r'\*\*Formulate Response[^\n]*\*\*:?', yanit)[-1]
            if '**Check Against' in yanit:
                yanit = yanit.split('**Check Against')[0]
        
        yanit = yanit.strip()
        return jsonify({'basari': True, 'cevap': yanit}), 200
    except AIServiceError as e:
        return jsonify({'basari': False, 'hata': str(e)}), 503
    except Exception as e:
        return jsonify({'basari': False, 'hata': 'Sunucu hatası oluştu.'}), 500

@api_bp.route('/leads', methods=['POST'])
def yeni_lead():
    veri = request.get_json() or {}
    isim = veri.get('isim')
    telefon = veri.get('telefon')
    mesaj = veri.get('mesaj', '')

    if not isim or not telefon:
        return jsonify({'basari': False, 'hata': 'İsim ve telefon alanları zorunludur.'}), 400

    try:
        yeni_id = lead_ekle(isim, telefon, mesaj)
        return jsonify({
            'basari': True,
            'mesaj': 'Kayıt başarıyla oluşturuldu.',
            'id': yeni_id
        }), 201
    except Exception as e:
        return jsonify({'basari': False, 'hata': 'Veritabanına kaydedilemedi.'}), 500

@api_bp.route('/leads', methods=['GET'])
def lead_listesi():
    try:
        kayitlar = tum_leadler()
        return jsonify({
            'basari': True,
            'toplam': len(kayitlar),
            'leadler': kayitlar
        }), 200
    except Exception as e:
        return jsonify({'basari': False, 'hata': 'Kayıtlar listelenemedi.'}), 500