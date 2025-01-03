import subprocess
import json

api_key = "YOUR-API-KEY"

def ollama_api(prompt, model):
    try:
        output = subprocess.check_output([
            "curl", "-s", "-X", "POST", f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}", 
            "-H", "Content-Type: application/json", 
            "-d", json.dumps({
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            })
        ])

        
        response_data = json.loads(output)

        
        text_response = response_data['candidates'][0]['content']['parts'][0]['text']

        return text_response

    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
    except json.JSONDecodeError as e:
        return f"JSON Decode Error: {e}"

def process_data(raw_text):
    prompt = raw_text
    summary = ollama_api(prompt=prompt, model="gemini-1.5-flash")
    return summary.strip()


