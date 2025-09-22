import requests
import json
import time

# Access environment variables
OLLAMA_API_URL="http://localhost:11434/api/generate"
model = "tinyllama:1.1b" #"gemma3:4b"

class ollama_request:
    def __init__(self):
        pass

    def get_response(self, content):
        # define payload
        payload = {
            "model": model,
            "prompt": content,
            "stream": False
        }

        # Send HTTP request to the ollama API
        response = requests.post(OLLAMA_API_URL, json=payload)

        # Check if response is ok
        if response.status_code == 200:
            try:
                # Parse the response JSON
                json_data = response.json()
                # Print the response content
                if "response" in json_data:
                    return json_data["response"]
            except json.JSONDecodeError as e:
                return f"Error decoding JSON: {e}. Response: {response.text}"
        else:
            return f"Error: {response.status_code} - {response.text}"
        
        
if __name__ == "__main__":
    ollama = ollama_request()
    test_prompt = "What is the capital of France?"
    start_time = time.time()
    print(ollama.get_response(test_prompt)) 
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")