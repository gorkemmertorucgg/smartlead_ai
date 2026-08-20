import sqlite3
import os
from flask import current_app

def get_db():
    """Veritabanı bağlantısı açar ve satırlara sütun adıyla erişim sağlar."""
    db_path = current_app.config.get('DATABASE_URL', 'smartlead.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app=None):
    """'leads' tablosunu oluşturur (yoksa)."""
    db_path = app.config.get('DATABASE_URL', 'smartlead.db') if app else 'smartlead.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            telefon TEXT NOT NULL,
            mesaj TEXT,
            tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def lead_ekle(isim, telefon, mesaj=''):
    """Yeni bir müşteri adayı (lead) kaydeder. SQL Injection korumalıdır."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)',
        (isim, telefon, mesaj)
    )
    conn.commit()
    yeni_id = cursor.lastrowid
    conn.close()
    return yeni_id

def tum_leadler():
    """Tüm kayıtları en yeniden eskiye doğru liste olarak döndürür."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, isim, telefon, mesaj, tarih FROM leads ORDER BY tarih DESC')
    satirlar = cursor.fetchall()
    conn.close()
    
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