# SmartLead AI - Akıllı Müşteri Toplama ve Destek Asistanı

SmartLead AI, web sitelerine gelen ziyaretçilerle doğal dilde sohbet ederek sorularını yanıtlayan ve potansiyel müşterilerin iletişim bilgilerini (Lead) toplayıp SQLite veritabanına kaydeden yapay zekâ destekli bir full-stack web uygulamasıdır.

## 🚀 Mimari ve Teknolojiler

* **Backend Framework:** Python Flask (Modüler Application Factory yapısı)
* **Yapay Zekâ Motoru:** Groq Cloud API (`llama3-8b-8192` modeli)
* **Veritabanı:** SQLite & Parametreli Güvenli SQL Sorguları
* **Frontend:** Wix Platformu & Velo (JavaScript / `wix-fetch`)
* **Canlı Dağıtım (Deployment):** Render Cloud Platform & Gunicorn WSGI

## 🛠️ API Uç Noktaları (Endpoints)

| Metot | Uç Nokta | Açıklama |
| :--- | :--- | :--- |
| `GET` | `/health` | Servis sağlık ve durum kontrolü |
| `POST` | `/chat` | Groq LLM tabanlı sohbet yanıtı üretme |
| `POST` | `/leads` | Müşteri bilgilerini doğrulayıp veritabanına kaydetme |
| `GET` | `/dashboard` | Kayıtlı potansiyel müşterileri listeleme |

## 🌐 Canlı Bağlantılar

* **Canlı API Servisi:** `https://smartlead-ai-jaxv.onrender.com`
* **Health Check:** `https://smartlead-ai-jaxv.onrender.com/health`
* **Lead Dashboard:** `https://smartlead-ai-jaxv.onrender.com/dashboard`