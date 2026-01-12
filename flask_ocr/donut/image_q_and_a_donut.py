import pprint
import argparse
import logging
from typing import Dict

import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel

from PIL import Image

def get_device():
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    return device

def load_donut(verbose: bool = False):
    """Fetch du processor Donut et du model
    """
    
    if not verbose:
        logging.getLogger("transformers").setLevel(logging.ERROR)

    processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
    model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
    model = model.to(get_device())

    return processor, model

def image_q_and_a_donut(image, prompt: str, processor, model) -> Dict:
    """Récupération de l'information voulue dans le document
    """

    device = get_device()
    #Préparation des inputs du model via le processor (l'image et le prompt)
    pixel_values = processor(image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)
    task_prompt = f"<s_docvqa><s_question>{prompt}</s_question><s_answer>"

    tokenized_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
    tokenized_input_ids = tokenized_input_ids.to(device)

    #Feeding du model récupération de l'output
    output = model.generate(
        pixel_values,
        decoder_input_ids=tokenized_input_ids,
        max_length=256
    )

    #Préparation de l'outpur en token par le processor
    sequence = processor.batch_decode(output, skip_special_tokens=True)[0]

    #Parsing en json
    parsed = processor.token2json(sequence)
    return parsed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("doc_path", type=str)
    parser.add_argument("prompt", type=str)
    args = parser.parse_args()

    image = Image.open(args.doc_path).convert("RGB")
    processor, model = load_donut()
    output = image_q_and_a_donut(image, args.prompt, processor, model)
    pprint.pp(output)