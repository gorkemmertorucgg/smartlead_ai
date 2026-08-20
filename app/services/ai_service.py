import requests
from flask import current_app

class AIServiceError(Exception):
    """Yapay zekâ servisine özel hata sınıfı."""
    pass

class AIService:
    """Groq LLaMA 3.3 LLM servisiyle haberleşen katman."""

    def _sistem_talimati_al(self):
        return current_app.config.get('BUSINESS_CONTEXT', 'Sen PETWAP asistanısın.')

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
        payload = {
            "model": "llama-3.3-70b-versatile",
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
                raise AIServiceError(f"Groq API Hatası: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            raise AIServiceError(f"Yapay zekâ servisine bağlanılamadı: {str(e)}")

ai_service = AIService()