from flask import Flask, request, jsonify
from utils.transformer import Transformer
from utils.fhir_mock import MockFHIR
from utils.ollama_request import ollama_request

app = Flask(__name__)

# Initialize the Transformer model
transformer = Transformer()
ollama_requester = ollama_request()

@app.route("/fhirmock", methods=["POST"])
def fhir_mock_server():
    data = request.get_json()
    if not data or "resourceType" not in data or "entry" not in data:
        return jsonify({"error": "'Invalid JSON FHIR request'"}), 400

    fhir_mock = MockFHIR()
    return jsonify(fhir_mock.create_response(data))

@app.route("/transform", methods=["POST"])
def embed_text():
    data = request.get_json()
    if not data or "description" not in data:
        return jsonify({"error": "Missing 'description'"}), 400

    return jsonify(transformer.create_vector(data))

@app.route("/flatten", methods=["POST"])
def flatten_desc():
    data = request.get_json()
    if not data or "request" not in data:
        return jsonify({"error": "Missing 'request'"}), 400
    response = ollama_requester.get_response(data["request"])
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
