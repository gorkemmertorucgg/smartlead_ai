import os
import re
import requests
from flask import current_app

class AIServiceError(Exception):
    pass

class AIService:
    def yanit_uret(self, kullanici_mesaji, sohbet_gecmisi=None):
        api_key = current_app.config.get('GROQ_API_KEY')
        if not api_key:
            return "🐾 PETWAP Asistanı Demo Modunda: Lütfen .env dosyasında GROQ_API_KEY tanımlayınız."

        system_prompt = current_app.config.get('BUSINESS_CONTEXT')
        
        messages = [{"role": "system", "content": system_prompt}]
        if sohbet_gecmisi:
            messages.extend(sohbet_gecmisi)
        messages.append({"role": "user", "content": kullanici_mesaji})

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": messages,
                    "temperature": 0.3
                },
                timeout=10
            )

            if response.status_code != 200:
                raise AIServiceError(f"Groq API Hatası: {response.status_code}")

            data = response.json()
            ham_cevap = data["choices"][0]["message"]["content"]
            
            # <think>...</think> arasındaki tüm düşünce bloklarını temizle
            temiz_cevap = re.sub(r'<think>.*?</think>', '', ham_cevap, flags=re.DOTALL).strip()
            
            return temiz_cevap
            
        except Exception as e:
            raise AIServiceError(f"Yapay zekâ servisine ulaşılamadı: {str(e)}")

ai_service = AIService()