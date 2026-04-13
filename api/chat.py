from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

# ================================================================
# BAJAJ LIFE INSURANCE — DEEP KNOWLEDGE BASE
# ================================================================
SYSTEM_PROMPT = """You are "Mike's AI Assistant" — a highly intelligent, deeply knowledgeable Financial Advisor AI specializing in Bajaj Life Insurance products. You work for Mike Ronald Lakra (IC: ABLIC1003446377), an authorized Bajaj Life Sales Manager based in Kolkata.

## YOUR IDENTITY & PERSONALITY
- You are warm, professional, and speak in a mix of Hindi and English (Hinglish) naturally
- You are deeply knowledgeable about Indian insurance, finance, taxation, and economics
- You always recommend consulting Mike personally for exact quotes
- You clearly distinguish between GUARANTEED vs NON-GUARANTEED benefits
- Use emojis appropriately

## RESPONSE STYLE
- Keep responses concise but complete (max 200-250 words)
- Use real numbers from knowledge base
- End with CTA: "📲 Mike se direct baat karein: +91 93821 81126"
"""

def call_groq_api(user_message, api_key, history=None):
    """Call Groq API using urllib"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    if history and isinstance(history, list):
        messages.extend(history[-8:])  # last 8 messages for context
    
    messages.append({"role": "user", "content": user_message})
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "max_tokens": 700,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=35) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['choices'][0]['message']['content']


class handler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            user_message = data.get('message', '').strip()
            if not user_message:
                self._send_json(400, {"response": "Please enter your question."})
                return

            api_key = os.environ.get("GROQ_API_KEY", "")
            if not api_key:
                self._send_json(500, {"response": "⚠️ Configuration error. Contact Mike: +91 93821 81126"})
                return

            history = data.get('history')
            reply = call_groq_api(user_message, api_key, history)
            self._send_json(200, {"response": reply})

        except Exception as e:
            self._send_json(500, {
                "response": f"⚠️ Error: {str(e)[:150]}. Please contact Mike on WhatsApp: +91 93821 81126"
            })

    def _send_json(self, status, data):
        response_body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(response_body)

    def log_message(self, format, *args):
        pass  # Suppress logs
