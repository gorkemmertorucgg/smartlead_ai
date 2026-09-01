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
            """Sen PETWAP platformunun akıllı pati asistanısın.
Görevin: Hayvanseverlere kedi/köpek bakımı, mama/beslenme tavsiyeleri, acil ilk yardım, aşı takvimi ve sahiplendirme konularında rehberlik etmek.
Kişilik: Çok kibar, sevecen, profesyonel ve çözüm odaklı bir dille Türkçe konuş.
UZUNLUK KURALI: Tüm yanıtlarını kesinlikle en fazla 2-3 kısa cümle ve maksimum 40-50 kelime ile sınırla.
Yönlendirme: Soruyu kısaca yanıtladıktan sonra, saha desteği veya koordinasyon için alttaki formdan iletişim bırakabileceklerini tek cümleyle hatırlat."""
        )

    def _aktif_modeli_bul(self, api_key):
        """Hesabındaki aktif modelleri listeler ve sadece metin sohbet modelini seçer."""
        if self._cached_model:
            return self._cached_model

        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            res = requests.get(self.groq_models_url, headers=headers, timeout=10)
            if res.status_code == 200:
                modeller = [m['id'] for m in res.json().get('data', [])]
                print(f"\n[Groq] Hesabınızdaki Aktif Modeller: {modeller}\n")
                
                # Ses (whisper), güvenlik ve görüntü modellerini filtrele
                gecerli_modeller = [
                    m for m in modeller 
                    if not any(yasak in m.lower() for yasak in ['whisper', 'vision', 'guard', 'safeguard', 'embed'])
                ]
                
                if gecerli_modeller:
                    # Tercih edilen modeller varsa ilk onu seç
                    for oncelik in ['llama', 'mixtral', 'gemma', 'qwen']:
                        for m in gecerli_modeller:
                            if oncelik in m.lower():
                                self._cached_model = m
                                print(f"[Groq] Seçilen Model: {self._cached_model}")
                                return self._cached_model
                    
                    self._cached_model = gecerli_modeller[0]
                    print(f"[Groq] Seçilen Model: {self._cached_model}")
                    return self._cached_model
        except Exception as e:
            print(f"[Groq Model Arama Hatası]: {e}")
            
        return "llama-3.1-8b-instant"

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
            "temperature": 0.4,
            "max_tokens": 512
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