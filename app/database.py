import sqlite3
from flask import current_app

def get_db():
    """SQLite veritabanı bağlantısı açar ve satırlara isimle erişim sağlar."""
    db_path = current_app.config.get('DATABASE_URL', 'smartlead.db')
    baglanti = sqlite3.connect(db_path)
    baglanti.row_factory = sqlite3.Row
    return baglanti

def init_db(app):
    """leads tablosunu veritabanında oluşturur (yoksa)."""
    db_path = app.config.get('DATABASE_URL', 'smartlead.db')
    baglanti = sqlite3.connect(db_path)
    imlec = baglanti.cursor()
    
    imlec.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            telefon TEXT NOT NULL,
            mesaj TEXT,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    baglanti.commit()
    baglanti.close()

def lead_ekle(isim, telefon, mesaj=""):
    """
    Yeni bir müşteri adayını güvenli parametrelerle (?) veritabanına ekler.
    """
    baglanti = get_db()
    imlec = baglanti.cursor()
    
    imlec.execute(
        'INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)',
        (isim, telefon, mesaj)
    )
    
    baglanti.commit()
    yeni_id = imlec.lastrowid
    baglanti.close()
    return yeni_id

def tum_leadler():
    """Tüm kayıtları en yeniden eskiye doğru listeler."""
    baglanti = get_db()
    imlec = baglanti.cursor()
    
    imlec.execute('SELECT * FROM leads ORDER BY tarih DESC')
    satirlar = imlec.fetchall()
    baglanti.close()
    
    sonuc = []
    for satir in satirlar:
        sonuc.append({
            'id': satir['id'],
            'isim': satir['isim'],
            'telefon': satir['telefon'],
            'mesaj': satir['mesaj'],
            'tarih': satir['tarih']
        })
    return sonuc