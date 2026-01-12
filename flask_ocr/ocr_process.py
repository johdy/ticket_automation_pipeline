from donut import image_q_and_a_donut as donut
from PIL import Image
import sys

def ocr_process(data):
    return
    print(data,  file=sys.stderr)
    processor, model = donut.load_donut()
    body = data.get("body", {})
    print("body", body,  file=sys.stderr)
    items = body.get("items", [])
    print("items", items,  file=sys.stderr)
    if not items:
        return data
    url = items[0]["Fichier"][0]["url"]
    row_id = items[0]["id"]
    path = url.replace("http://localhost", "/baserow/data")
    try:
        image = Image.open(path)
    except Exception as e:
        print(f"Échec {url}: {e}", file=sys.stderr)
        return jsonify({
            "path": path
        })


    questions = ["Date", "Venue", "Name of the show", "Name of artist"]
    print("questions", questions,  file=sys.stderr)

    output = {}
    for q in questions:
        output[q] = donut.image_q_and_a_donut(image, q, processor, model)
    print(output)
    return jsonify({"status": "ok", "result": output, "row_id": row_id})