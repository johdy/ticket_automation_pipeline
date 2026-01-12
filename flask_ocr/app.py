from flask import Flask, request, jsonify
import sys
from threading import Thread
import time
import requests
from ocr_process import ocr_process

app = Flask(__name__)

def launch_ocr(data):
    try:
        print("début du traitement",  file=sys.stderr)
        #ocr_process()
        #time.sleep(300)  # simulation d’un job de 10 min
        result = {"status": "done", "message": "OCR terminé", "data": {"foo": "bar"}}
        webhook_url = "http://n8n:5678/webhook/2387791c-f097-43fd-9c60-315a006f43dc"
        response = requests.post(webhook_url, json=result)
        print("fin du traitement", response,  file=sys.stderr)

    except Exception as e:
        print("Erreur dans process_async:", e,  file=sys.stderr)

@app.route("/ocr", methods=["POST"])
def ocr_endpoint():
    data = request.get_json()
    Thread(target=launch_ocr, args=(data,)).start()
    return jsonify({"status": "processing"}), 202


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")