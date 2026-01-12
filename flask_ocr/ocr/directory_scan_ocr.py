from typing import List, Dict
from glob import glob
import pprint
import argparse
import json

import pytesseract

from image_q_and_a_ocr import image_q_and_a_ocr

def directory_scan_ocr(directory: List[str], questions: List[str], save_json: bool, name_output: str, verbose: bool) -> List[Dict]:
    """Extrais les champs voulus pour chaque image du répertoire
        Prends un path de répertoire d'image en argument, et une liste de noms de champs
    """
    results = []
    for file in directory:
        q_a = []
        for q in questions:
            q = q.strip()
            try:
                text = pytesseract.image_to_string(file, lang="eng")
            except Exception as e:
                print(f"Échec {file}: {e}")
                continue
            answer = image_q_and_a_ocr(text, q)
            q_a.append(answer)
        new_line = {"filename": file, "Q&A": q_a}
        results.append(new_line)
        if verbose:
            pprint.pp(new_line)
    if save_json:
        with open("./outputs/" + name_output, "w") as f:
            json.dump(results, f, indent=4)
    else:
        pprint.pp(results)
    return results

if __name__ == "__main__":
    directory = glob("./dataset/*")
    with open('./ocr/questions.txt', 'r') as f:
        questions = f.readlines()

    parser = argparse.ArgumentParser()
    parser.add_argument("--save_json", action="store_true")
    parser.add_argument("--name_output", type=str, default="results_ocr.json")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    results = directory_scan_ocr(directory, questions, save_json=args.save_json, name_output=args.name_output, verbose=args.verbose)
