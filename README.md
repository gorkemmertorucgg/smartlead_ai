# PETWAP - Akıllı Pati Asistanı & Lead Toplama Sistemi (SmartLead AI)

Bu proje, sokak hayvanlarının refahı, acil durum rehberliği ve saha gönüllü koordinasyonunu sağlamak amacıyla geliştirilmiş B2B/B2C yapay zekâ destekli müşteri adayı (lead) toplama sistemidir.

## 🚀 Kullanılan Teknolojiler & Mimari
- **Backend:** Python, Flask (Application Factory & Blueprint deseni)
- **Veritabanı:** SQLite (SQL Injection korumalı parametrik sorgular)
- **Yapay Zekâ:** Groq API (Llama 3.x LLM Servisi)
- **Frontend / Entegrasyon:** HTML5/CSS3 & Wix Velo (RESTful API Entegrasyonu)
- **Yayınlama:** Render (Web Service) & GitHub

## 📁 Mimari Yapı (Separation of Concerns)
- `config.py`: Ortam değişkenleri ve PETWAP sistem talimatı (Business Context).
- `app/database.py`: Yalnızca veritabanı CRUD işlemleri.
- `app/routes.py`: HTTP rotaları ve hata yakalama katmanı.
- `app/services/ai_service.py`: İzole yapay zekâ entegrasyonu.
- `run.py`: Uygulama giriş noktası.

## 💡 Repository Dil Dağılımı ve Frontend Notu!
Bu proje temelde Flask tabanlı bir **RESTful Backend & API** servisidir. GitHub istatistiklerinde görülen **HTML/CSS** oranı; sistemin Wix Velo entegrasyonu öncesinde yerel ortamda uçtan uca test edilebilmesi amacıyla hazırlanan karşılama sayfası (`index.html`) ve yönetim paneli (`dashboard.html`) şablonlarının satır yoğunluğundan kaynaklanmaktadır. İş mantığı, veritabanı CRUD operasyonları ve yapay zekâ entegrasyonu tamamen **Python** katmanında koşmaktadır.

## 🛠️ Yerel Kurulum Adımları

1. Depoyu klonlayın:
```bash
git clone [https://github.com/gorkemmertorucgg/smartlead_ai.git](https://github.com/gorkemmertorucgg/smartlead_ai.git)
cd smartlead_ai