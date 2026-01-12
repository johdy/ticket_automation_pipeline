import json
import streamlit as st
from PIL import Image
import argparse


def launch_validator(data, title: str, corrected_filename: str):
    """Affichage d'une interface pour valider ou modifier les
    """
    st.title(title)

    for doc in data:
        #Afficher l'image du document
        image = Image.open(doc["filename"])
        st.image(image)

        #Nom du document
        st.subheader(doc["filename"])

        corrected = []
        #Boucle sur chaque Q&A
        for qa in doc["Q&A"]:
            for question, answer in qa.items():
                new_answer = st.text_input(f"{question}", value=answer)
                corrected.append({question: new_answer})

        #Bouton pour sauvegarder les corrections
        if st.button(f"Sauvegarder corrections pour {doc['filename']}"):
            doc["Q&A"] = corrected
            with open(corrected_filename, "w") as f:
                json.dump(data, f, indent=4)
            st.success(f"Résultats sauvegardés pour {doc['filename']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--load_json", default="outputs/results_donut.json")
    args = parser.parse_args()

    with open(args.load_json) as f:
        data = json.load(f)
    corrected_filename = args.load_json.split(".json")[:-1][0]
    print(corrected_filename)
    corrected_filename += "_corrected.json"
    print(corrected_filename)
    launch_validator(data, title="Image Q&A Validator", corrected_filename=corrected_filename)