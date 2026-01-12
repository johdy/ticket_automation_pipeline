# Image Q&A

Image Q&A est un projet d’extraction d’informations à partir de documents scannés.
Il combine deux approches :
- Une approche par Donut (modèle multimodal vision et langage) pour extraire des réponses sans OCR classique.
- Une approche OCR avec regex, plus robuste dans certains cas et plus traçables.

De plus,une interface Streamlit est développée dans le Validator, qui permet de comparer et rectifier cas par cas les résultats produits par les deux méthodes.

L’objectif est de tester et comparer ces stratégies d'extraction d'informations.

***

## Image Q&A donut

Cette approche s'appuie sur [Donut](https://huggingface.co/docs/transformers/model_doc/donut), un modèle associant vision et langage, capable de répondre à une question en fonction d'un document, sans OCR direct.

### Structure

- `donut/image_q_and_a_multimodal.py` : chargement du modèle Donut et processing de l'input et de l'output du modèle, en fonction d'une image et d'une question.
- `donut/question_directory.py` : applique une liste de questions à un dossier d’images et renvoie un JSON.

***

## Image Q&A ocr

L’approche OCR repose sur un moteur de reconnaissance optique des caractères (ici Tesseract) couplé à des regex et règles simples pour identifier les champs d’intérêt.

### Structure

- `ocr/image_q_and_a_ocr.py` : exécute l’OCR sur une image puis applique des règles d’extraction.
- `ocr/question_directory.py` : même logique que pour `donut/`.

***

## Usages

Pour l'approche donut comme ocr, les outputs peuvent être obtenus en lançant la commande suivante, en fonction des images du dossier `dataset/` et des questions des fichiers `questions.txt`

```bash
python [donut ou ocr]/question_directory.py [-h] [--save_json] [--name_output NAME_OUTPUT]
                             [--verbose]
```

Le validator peut être lancé comme suit :

```bash
streamlit run validator/app.py -- [--load_json] [outputs/file]
```

***
***

## POC

Nous testons les deux approches sur la database [FUNSD](https://guillaumejaume.github.io/FUNSD/) constituée de formulaires scannés de natures différentes. Nous voulons récupérer deux informations :
- Le champ "FROM"
- Le champ "TO".

### Pipeline

- Chaque image est passée soit à Donut, soit à l’approche OCR.
- Donut renvoie une text_sequence contenant la question et la réponse. OCR produit un texte brut et applique des regex pour identifier les champs d’intérêt.
- Les résultats sont convertis en JSON, document par document.
- Le Validator permet de visualiser et corriger les sorties pour les deux approches.

#### Résultats et limites

- Les champs FROM et TO sont correctement extraits dans la majorité des documents contenant ces champs.
- Donut : flexible mais peut halluciner si l’information est absente ou illisible.
- OCR + regex : robuste et traçable, mais dépend fortement de la qualité du scan et des règles définies. Problème s'il y a plusieurs fois "from" ou "to" dans le document, ou selon les mises en pages.

#### What's next

- Pour des documents standardisés, un recadrage de l'image sur la zone de l'information requise permettrait de diminuer le bruit, notamment pour l'approche Donut.
- Une combinaison des deux méthodes (Donut + OCR + regex) pourrait offrir une approche hybride plus performante.
- Possibilité de générer un rapport d’évaluation automatisé dans Validator pour suivre la qualité des extractions sur un dataset entier.

***
***

## Docker

Le validator peut être rapidement testé avec Docker comme suit :

```bash
docker build -t validator -f Dockerfile.app .
docker run -p 8501:8501 -v $(pwd)/outputs:/app/outputs validator
```


