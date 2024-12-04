from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Define API endpoints
@app.route("/practice", methods=["POST"])
def generate_dataset():
    text = request.json["text"]
    subprocess.run(["python", "handwrite.py", text])
    return jsonify({"message": "Handwriting practice saved"})

@app.route("/render", methods=["POST"])
def render_handwriting():
    input_file = request.json["input_file"]
    subprocess.run(["python", "handwriteRender.py", input_file])
    image_url = os.environ.get("APP_URL", "") + "/output.html"
    return jsonify({"image_url": image_url})

if __name__ == "__main__":
    app.run(debug=True)