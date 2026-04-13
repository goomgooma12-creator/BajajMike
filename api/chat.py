def call_groq_api(user_message, api_key, history=None):
    """Call Groq API using urllib"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add history if provided (for better conversation memory)
    if history and isinstance(history, list):
        messages.extend(history[-8:])  # last 8 messages max
    
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
