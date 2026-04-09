#PUT ON THE SPLUNK SEARCH HEAD IN THE AI TOOLKIT FOR LOCATION REFERENCE

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Proxy is running"

OLLAMA_URL = "http://192.168.x.x:11434/api/generate"

@app.route("/v1/chat/completions", methods=["POST"])
def chat():
    data = request.json

    # Extract prompt from OpenAI-style request
    messages = data.get("messages", [])
    prompt = messages[-1]["content"] if messages else ""

    # Send to Ollama
    r = requests.post(OLLAMA_URL, json={
        "model": "phi3:latest",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 200,
            "temperature": 0.2
        }
    })

    result = r.json()

    # Convert to OpenAI-compatible response
    return jsonify({
        "choices": [
            {
                "message": {
                    "content": result.get("response", "")
                }
            }
        ]
    })

app.run(host="127.0.0.1", port=5000)
