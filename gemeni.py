import subprocess
import json

def ollama_api(prompt, model):
    try:
        output = subprocess.check_output([
            "curl", "-s", "-X", "POST", "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyCc01pIA69-ng3RJeGzl4Mu9UPDCdHIChE", 
            "-H", "Content-Type: application/json", 
            "-d", json.dumps({
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            })
        ])

        # Parse the output as JSON
        response_data = json.loads(output)

        # Extract the text response from the candidates
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


