import os
import requests
from flask import current_app

class AIServiceError(Exception):
    """Yapay zekâ servisi hataları için özel istisna sınıfı."""
    pass

class AIService:
    def __init__(self):
        self.groq_chat_url = "https://api.groq.com/openai/v1/chat/completions"
        self.groq_models_url = "https://api.groq.com/openai/v1/models"
        self._cached_model = None

    def _sistem_talimati_al(self):
        return current_app.config.get(
            "BUSINESS_CONTEXT",
            "Sen yardımsever ve profesyonel bir yapay zekâ asistanısın. Türkçe konuş."
        )

    def _aktif_modeli_bul(self, api_key):
        """Groq API'den o an aktif ve çalışan modelleri çekip en uygununu seçer."""
        if self._cached_model:
            return self._cached_model

        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            res = requests.get(self.groq_models_url, headers=headers, timeout=10)
            if res.status_code == 200:
                modeller = [m['id'] for m in res.json().get('data', [])]
                # Öncelikli ve güncel sohbet modellerini tara
                for aday in ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'llama3-70b-8192', 'mixtral-8x7b-32768']:
                    if aday in modeller:
                        self._cached_model = aday
                        return aday
                # Listeden ilk aktif modeli al
                if modeller:
                    self._cached_model = modeller[0]
                    return modeller[0]
        except Exception:
            pass
        return "llama-3.3-70b-versatile"

    def _groq_cagir(self, mesaj, gecmis=None):
        api_key = current_app.config.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY", "")

        if not api_key:
            return "Sistem şu anda demo modunda çalışmaktadır. Lütfen .env dosyanızdaki GROQ_API_KEY anahtarını kontrol edin."

        messages = [{"role": "system", "content": self._sistem_talimati_al()}]

        if gecmis and isinstance(gecmis, list):
            for item in gecmis:
                if isinstance(item, dict) and "role" in item and "content" in item:
                    messages.append(item)

        messages.append({"role": "user", "content": mesaj})

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        secilen_model = self._aktif_modeli_bul(api_key)

        payload = {
            "model": secilen_model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024
        }

        try:
            response = requests.post(self.groq_chat_url, headers=headers, json=payload, timeout=20)
            response_data = response.json()

            if response.status_code != 200:
                error_msg = response_data.get("error", {}).get("message", response.text)
                raise AIServiceError(f"Groq API Hatası ({response.status_code}): {error_msg}")

            return response_data["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            raise AIServiceError(f"Yapay zekâ servisi bağlantı hatası: {str(e)}")

    def yanit_uret(self, mesaj, gecmis=None):
        return self._groq_cagir(mesaj, gecmis)

ai_service = AIService()
yapay_zeka_servisi = ai_service