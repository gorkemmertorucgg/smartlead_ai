import re
import requests
from flask import current_app

class AIServiceError(Exception):
    """Yapay zekâ servisinde oluşabilecek hatalar için özel istisna sınıfı."""
    pass

class AIService:
    """Groq API üzerinden yapay zekâ modelini çalıştıran servis sınıfı."""
    
    def _sistem_talimati_al(self):
        """Ayarlardan yapay zekânın kimlik ve davranış metnini çeker."""
        return current_app.config.get(
            'BUSINESS_CONTEXT', 
            'Sen SmartLead AI akıllı satış ve destek asistanısın. Ziyaretçilere doğrudan, profesyonel ve kibar bir Türkçe ile yanıt ver. Bilgi verdikten sonra ad ve telefon numaralarını formdan bırakmalarını öner.'
        )

    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanıcı mesajını ve geçmişi alıp yapay zekâ yanıtı döndürür."""
        api_key = current_app.config.get('GROQ_API_KEY')
        
        if not api_key:
            return f"[Demo Modu] Mesajınız: '{mesaj}'. Lütfen .env dosyasına geçerli bir GROQ_API_KEY ekleyin."

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 1. Sistem talimatı
        messages = [{"role": "system", "content": self._sistem_talimati_al()}]

        # 2. Varsa geçmiş konuşmalar
        if gecmis and isinstance(gecmis, list):
            messages.extend(gecmis)

        # 3. Kullanıcı mesajı
        messages.append({"role": "user", "content": mesaj})

        payload = {
            "model": "qwen/qwen3.6-27b",
            "messages": messages,
            "temperature": 0.6,
            "max_tokens": 1500
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=25)
            if response.status_code == 200:
                veri = response.json()
                ham_yanit = veri['choices'][0]['message']['content']
                
                # Düşünme adımlarını (<think>...</think>) tamamen filtrele
                temiz_yanit = re.sub(r'<think>.*?</think>', '', ham_yanit, flags=re.DOTALL).strip()
                
                if '</think>' in ham_yanit and not temiz_yanit:
                    temiz_yanit = ham_yanit.split('</think>')[-1].strip()

                return temiz_yanit if temiz_yanit else ham_yanit.strip()
            else:
                raise AIServiceError(f"Groq Hatası ({response.status_code}): {response.text}")
        except Exception as e:
            raise AIServiceError(f"Yapay zekâ servisine bağlanılamadı: {str(e)}")

# Proje genelinde kullanılacak tekil servis nesnesi
ai_service = AIService()