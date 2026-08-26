import os
import re
import requests
from flask import current_app

class AIServiceError(Exception):
    pass

class AIService:
    def __init__(self):
        self.aktif_model = None

    def _modeli_tespit_et(self, api_key):
        """Groq hesabınızda anlık çalışan ve izinli olan modeli otomatik seçer."""
        if self.aktif_model:
            return self.aktif_model

        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json"
        }

        try:
            res = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=5)
            if res.status_code == 200:
                modeller = [m['id'] for m in res.json().get('data', []) if 'id' in m]
                
                # Tercih edilen kararlı model havuzu
                tercihler = [
                    "llama-3.3-70b-versatile",
                    "llama-3.1-8b-instant",
                    "llama3-8b-8192",
                    "llama3-70b-8192",
                    "mixtral-8x7b-32768",
                    "gemma2-9b-it"
                ]
                
                for t in tercihler:
                    if t in modeller:
                        self.aktif_model = t
                        return t
                
                if modeller:
                    self.aktif_model = modeller[0]
                    return self.aktif_model
        except Exception:
            pass

        return "llama3-8b-8192"

    def yanit_uret(self, mesaj=None, gecmis=None, kullanici_mesaji=None, sohbet_gecmisi=None, **kwargs):
        aktif_mesaj = mesaj or kullanici_mesaji
        aktif_gecmis = gecmis or sohbet_gecmisi or []

        if not aktif_mesaj:
            return "Lütfen bir soru belirtin."

        api_key = current_app.config.get('GROQ_API_KEY')
        if not api_key:
            return "🐾 PETWAP Asistanı Demo Modunda: Lütfen Render Environment ayarlarında GROQ_API_KEY tanımlayınız."

        system_prompt = current_app.config.get('BUSINESS_CONTEXT')
        
        messages = [{"role": "system", "content": system_prompt}]
        if aktif_gecmis:
            messages.extend(aktif_gecmis)
        messages.append({"role": "user", "content": aktif_mesaj})

        secilen_model = self._modeli_tespit_et(api_key)
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": secilen_model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 150
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)

            # İlk model hata verirse genel llama3-8b-8192 ile son bir deneme yap
            if response.status_code != 200:
                payload["model"] = "llama3-8b-8192"
                response = requests.post(url, headers=headers, json=payload, timeout=15)

            if response.status_code != 200:
                raise AIServiceError(f"Groq API Hatası ({response.status_code}): {response.text}")

            data = response.json()
            ham_cevap = data["choices"][0]["message"]["content"]
            
            # <think>...</think> düşünce zincirini filtrele
            temiz_cevap = re.sub(r'<think>.*?</think>', '', ham_cevap, flags=re.DOTALL).strip()
            return temiz_cevap
            
        except requests.exceptions.RequestException as e:
            raise AIServiceError(f"Bağlantı hatası: {str(e)}")
        except Exception as e:
            raise AIServiceError(f"Yapay zekâ servisine ulaşılamadı: {str(e)}")

ai_service = AIService()