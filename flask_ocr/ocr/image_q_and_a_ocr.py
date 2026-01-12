import re
import argparse
from typing import List
import pprint

def image_q_and_a_ocr(text: str, search: str):
    """Récupération de la liste de champ voulue dans une image
    """

    """(?i) : insensible à la casse
        \b{search}\b : recherche du mot exact
        \s* : peu importe le nombre d'espaces
        :? : qu'il y ait ':' ou non
        (.+) : capture jusqu'au bout de la ligne
    """
    pattern = rf"(?i)\b{search}\b\s*:?\s*(.+)"
    
    match = re.search(pattern, text)
    if match:
        return {search: match.group(1).strip()}
    
    return None



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", type=str)
    args = parser.parse_args()

    output = image_q_and_a_ocr(args.image_path, ["from", "to"])
    pprint.pp(output)