import subprocess
import json

def ollama_api(prompt, model):
    try:
        
        output = subprocess.check_output([
            "curl", "-s", "-X", "POST", "https://sacred-currently-quail.ngrok-free.app/api/generate", 
            "-d", json.dumps({
                "role": "system",
                "model": model,
                "prompt": prompt,
                "temprature": "1"
            })
        ])

        
        json_objects = output.strip().splitlines()

        responses = []
        
        for json_str in json_objects:
            try:
                json_data = json.loads(json_str)
                
                if 'response' in json_data:
                    responses.append(json_data['response'])
            except json.JSONDecodeError:
                continue  

        
        final_response = ''.join(responses)
        return final_response

    except subprocess.CalledProcessError as e:
        return f"Error: {e}"


def process_data(raw_text):
    
    prompt = raw_text
    
    
    summary = ollama_api(prompt=prompt, model="llama3")
    return summary.strip()  
