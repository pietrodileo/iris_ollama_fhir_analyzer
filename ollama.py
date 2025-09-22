#send a request to ollama

# curl http://localhost:11434/api/generate -d '
# {  
# "model": "gemma3:12b-it-qat",  
# "prompt": "Why is the blue sky blue?",  
# "stream": false
# }'  | jq .

import json
import requests

# calculate the time taken to get a response
import time

url = "http://localhost:11434/api/chat"
model = "gemma3:4b"
content = "Why is the blue sky blue?"
payload = {
    "model": model,
    "messages": [
        {
            "role": "user",
            "content": content
        }
    ]
}
start_time = time.time()
print(f"Sending request to {url} with model {model} and content: {content}")
response = requests.post(url, json=payload)
end_time = time.time()
response_time = end_time - start_time