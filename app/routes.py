from flask import Blueprint, request, jsonify, render_template
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

api_blueprint = Blueprint('api', __name__)
sayfa_blueprint = Blueprint('sayfalar', __name__)

# --- SAYFA ROTALARI ---
@sayfa_blueprint.route('/')
def ana_sayfa():
    return render_template('index.html')

@sayfa_blueprint.route('/dashboard')
def dashboard():
    leadler = tum_leadler()
    return render_template('dashboard.html', leadler=leadler)

# --- RESTFUL API ROTALARI ---
@api_blueprint.route('/sohbet', methods=['POST'])
def sohbet():
    veri = request.get_json() or {}
    mesaj = veri.get('mesaj', '').strip()
    gecmis = veri.get('gecmis', [])

    if not mesaj:
        return jsonify({'basari': False, 'hata': 'Mesaj boş olamaz.'}), 400

    try:
        cevap = ai_service.yanit_uret(mesaj=mesaj, gecmis=gecmis)
        return jsonify({'basari': True, 'cevap': cevap}), 200
    except AIServiceError as e:
        return jsonify({'basari': False, 'hata': str(e)}), 503
    except Exception as e:
        return jsonify({'basari': False, 'hata': f'Sunucu hatası: {str(e)}'}), 500

@api_blueprint.route('/leads', methods=['POST'])
def yeni_lead():
    veri = request.get_json() or {}
    isim = veri.get('isim', '').strip()
    telefon = veri.get('telefon', '').strip()
    mesaj = veri.get('mesaj', 'PETWAP Kaydı').strip()

    if not isim or not telefon:
        return jsonify({'basari': False, 'hata': 'İsim ve telefon zorunludur.'}), 400

    try:
        yeni_id = lead_ekle(isim=isim, telefon=telefon, mesaj=mesaj)
        return jsonify({'basari': True, 'mesaj': 'Kayıt başarılı!', 'id': yeni_id}), 201
    except Exception as e:
        return jsonify({'basari': False, 'hata': f'Veritabanı hatası: {str(e)}'}), 500

@api_blueprint.route('/leads', methods=['GET'])
def listele_leads():
    try:
        kayitlar = tum_leadler()
        return jsonify({'basari': True, 'toplam': len(kayitlar), 'leadler': kayitlar}), 200
    except Exception as e:
        return jsonify({'basari': False, 'hata': str(e)}), 500