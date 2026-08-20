import requests
from flask import current_app

class AIServiceError(Exception):
    """Yapay zekâ servisine özel hata sınıfı."""
    pass

class AIService:
    """Groq API ile dinamik model desteği sağlayan katman."""

    def _sistem_talimati_al(self):
        return current_app.config.get('BUSINESS_CONTEXT', 'Sen PETWAP asistanısın.')

    def _aktif_modelleri_getir(self, headers):
        """Hesabınızda şu an aktif olan modelleri Groq API'den sorgular."""
        aday_modeller = []
        try:
            res = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json().get('data', [])
                for item in data:
                    mid = item.get('id', '')
                    # Whisper, guard veya ses modellerini hariç tut, sohbet modellerini al
                    if not any(yasak in mid.lower() for yasak in ['whisper', 'guard', 'embed', 'tts', 'moderation']):
                        aday_modeller.append(mid)
        except Exception:
            pass

        # Güvenlik yedeği olarak bilinen temel modeller
        yedekler = ['gemma2-9b-it', 'llama-3.2-3b-preview', 'llama-3.2-1b-preview', 'llama-3.3-70b-versatile']
        for y in yedekler:
            if y not in aday_modeller:
                aday_modeller.append(y)

        return aday_modeller

    def yanit_uret(self, mesaj, gecmis=None):
        api_key = current_app.config.get('GROQ_API_KEY', '')
        
        if not api_key:
            return "PETWAP Demo Modu: Lütfen sunucunuza GROQ_API_KEY anahtarını tanımlayın."

        if gecmis is None:
            gecmis = []

        messages = [{"role": "system", "content": self._sistem_talimati_al()}]
        for g in gecmis:
            if isinstance(g, dict) and 'role' in g and 'content' in g:
                messages.append({"role": g['role'], "content": g['content']})
        messages.append({"role": "user", "content": mesaj})

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Aktif modelleri al ve çalışan ilk modelden cevabı dön
        modeller = self._aktif_modelleri_getir(headers)
        son_hata = None

        for model in modeller:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500
            }
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=15)
                if response.status_code == 200:
                    veri = response.json()
                    return veri['choices'][0]['message']['content'].strip()
                else:
                    son_hata = f"{model} ({response.status_code}): {response.text}"
            except Exception as e:
                son_hata = str(e)

        raise AIServiceError(f"Groq modellerine erişilemedi. Son hata: {son_hata}")

ai_service = AIService()