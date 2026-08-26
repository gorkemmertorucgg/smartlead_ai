import os
import re
import requests
from flask import current_app

class AIServiceError(Exception):
    pass

class AIService:
    def yanit_uret(self, mesaj=None, gecmis=None, kullanici_mesaji=None, sohbet_gecmisi=None, **kwargs):
        aktif_mesaj = mesaj or kullanici_mesaji
        aktif_gecmis = gecmis or sohbet_gecmisi or []

        if not aktif_mesaj:
            return "Lütfen bir soru belirtin."

        api_key = current_app.config.get('GROQ_API_KEY')
        if not api_key:
            return "🐾 PETWAP Asistanı Demo Modunda: Lütfen Render veya .env dosyasında GROQ_API_KEY tanımlayınız."

        system_prompt = current_app.config.get('BUSINESS_CONTEXT')
        
        messages = [{"role": "system", "content": system_prompt}]
        if aktif_gecmis:
            messages.extend(aktif_gecmis)
        messages.append({"role": "user", "content": aktif_mesaj})

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": messages,
            "temperature": 0.3
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)

            if response.status_code != 200:
                hata_detayi = response.text
                raise AIServiceError(f"Groq API Hatası ({response.status_code}): {hata_detayi}")

            data = response.json()
            ham_cevap = data["choices"][0]["message"]["content"]
            
            # <think>...</think> düşünce sürecini temizle
            temiz_cevap = re.sub(r'<think>.*?</think>', '', ham_cevap, flags=re.DOTALL).strip()
            
            return temiz_cevap
            
        except requests.exceptions.RequestException as e:
            raise AIServiceError(f"Bağlantı hatası: {str(e)}")
        except Exception as e:
            raise AIServiceError(f"Yapay zekâ servisine ulaşılamadı: {str(e)}")

ai_service = AIService()