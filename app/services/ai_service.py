import os
import re
import requests
from flask import current_app

class AIServiceError(Exception):
    """Yapay zekâ servisi hataları için özel istisna sınıfı."""
    pass

class AIService:
    def __init__(self):
        self.groq_chat_url = "https://api.groq.com/openai/v1/chat/completions"

    def _sistem_talimati_al(self):
        return current_app.config.get(
            "BUSINESS_CONTEXT",
            """Sen PETWAP platformunun akıllı pati asistanısın.
Görevin: Hayvanseverlere kedi/köpek bakımı, mama/beslenme tavsiyeleri, acil ilk yardım, aşı takvimi ve sahiplendirme konularında rehberlik etmek.
Kişilik: Çok kibar, sevecen, profesyonel ve çözüm odaklı bir dille Türkçe konuş.
UZUNLUK KURALI: Tüm yanıtlarını kesinlikle en fazla 2-3 kısa cümle ve maksimum 40-50 kelime ile sınırla.
Yönlendirme: Soruyu kısaca yanıtladıktan sonra, saha desteği veya koordinasyon için alttaki formdan iletişim bırakabileceklerini tek cümleyle hatırlat."""
        )

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

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 512
        }

        try:
            response = requests.post(self.groq_chat_url, headers=headers, json=payload, timeout=20)
            response_data = response.json()

            if response.status_code != 200:
                error_msg = response_data.get("error", {}).get("message", response.text)
                raise AIServiceError(f"Groq API Hatası ({response.status_code}): {error_msg}")

            ham_yanit = response_data["choices"][0]["message"]["content"]
            
            # İç düşünme etiketlerini tamamen temizler
            temiz_yanit = re.sub(r'<think>.*?</think>', '', ham_yanit, flags=re.DOTALL).strip()
            return temiz_yanit if temiz_yanit else ham_yanit

        except requests.RequestException as e:
            raise AIServiceError(f"Yapay zekâ servisi bağlantı hatası: {str(e)}")

    def yanit_uret(self, mesaj, gecmis=None):
        return self._groq_cagir(mesaj, gecmis)

ai_service = AIService()
yapay_zeka_servisi = ai_service