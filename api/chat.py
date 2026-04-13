from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

# Your long SYSTEM_PROMPT here (keep it exactly as you have)

def call_groq_api(user_message, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 600,
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
    
    with urllib.request.urlopen(req, timeout=30) as response:
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
                self._send_json(500, {"response": "⚠️ Configuration error. Please contact Mike: +91 93821 81126"})
                return

            reply = call_groq_api(user_message, api_key)
            self._send_json(200, {"response": reply})

        except Exception as e:
            self._send_json(500, {
                "response": f"⚠️ Error: {str(e)[:100]}... Please contact Mike directly on WhatsApp: +91 93821 81126"
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
