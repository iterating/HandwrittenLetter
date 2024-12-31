from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from PIL import Image
import io
import base64

application = Flask(__name__)
CORS(application, resources={
    r"/*": {
        "origins": [
            "https://d1511mhtx39tb3.cloudfront.net",
            "http://localhost:5173"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

if __name__ == '__main__':
    application.run()
