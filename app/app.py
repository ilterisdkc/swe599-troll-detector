from flask import Flask, render_template, url_for, request
import numpy as np
import pandas as pd
import re
from googleapiclient import discovery
import json

from pathlib import Path
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    TextClassificationPipeline
)

model_loc = "/Users/ilteriscivelek/Desktop/SWE Master/Semestr3 - Fall22/SWE 599/transformers_state_trolls_cch/troll_detect"

nlp_clf = TextClassificationPipeline(
    model=DistilBertForSequenceClassification.from_pretrained(model_loc),
    tokenizer=DistilBertTokenizerFast.from_pretrained(model_loc)
)

API_KEY = 'AIzaSyB8BRXqjeME1Udi1aLKkY8fZkiPE2PhOi4'

client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
)

analyze_request = {
    'comment': {'text': 'friendly greetings from python'},
    'requestedAttributes': {'TOXICITY': {}}
}

response = client.comments().analyze(body=analyze_request).execute()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('perspective_home.html')


def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\'t", " not", text)  # Change 't to 'not'
    text = re.sub(r'(@.*?)[\s]', ' ', text)  # Remove @name
    text = re.sub(r"$\d+\W+|\b\d+\b|\W+\d+$", " ", text)  # remove digits
    text = re.sub(r"[^\w\s\#]", "", text)  # remove special characters except hashtags
    text = text.strip(" ")
    text = re.sub(' +', ' ', text).strip()  # get rid of multiple spaces and replace with a single
    return text

"""
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        message = request.form['message']
        message = clean_text(message)
        data = [message]
        my_prediction = nlp_clf(data)[0]['label']
    return render_template('result.html', prediction=my_prediction)
"""



@app.route('/perspective-predict', methods=['POST'])
def perspective_predict():
    if request.method == 'POST':
        message = request.form['message']
        data_chuachinhon = [message]
        chuachinhon_prediction = nlp_clf(data_chuachinhon)[0]['label']
        if chuachinhon_prediction == 'LABEL_1':
            chuachinhon_result = 1
        else:
            chuachinhon_result = 0
        request_text = {
            'comment': {'text': message},
            'requestedAttributes': {'TOXICITY': {}, 'THREAT': {}, 'INSULT': {}, 'IDENTITY_ATTACK': {}, 'PROFANITY': {}}
        }
        response = client.comments().analyze(body=request_text).execute()
        result = json.dumps(response, indent=2)
        print(result)
        result_toxicity = response['attributeScores']['TOXICITY']['summaryScore']['value']
        result_thread = response['attributeScores']['THREAT']['summaryScore']['value']
        result_insult = response['attributeScores']['INSULT']['summaryScore']['value']
        result_identity_attack = response['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value']
        result_profanity = response['attributeScores']['PROFANITY']['summaryScore']['value']
        troll_probability = (result_toxicity + result_thread + result_insult + result_identity_attack + result_profanity) / 5

        combined = (troll_probability + chuachinhon_result) / 2
        combined_result = "TROLL" if combined > 0.6 else "NOT TROLL"
    return render_template('main_page.html',
                           message=message,
                           toxicity=result_toxicity,
                           threat=result_thread,
                           insult=result_insult,
                           identity_attack=result_identity_attack,
                           profanity=result_profanity,
                           troll=troll_probability,
                           chuachinhon_result=chuachinhon_result,
                           combined_result=combined_result)


if __name__ == '__main__':
    app.run(debug=True)
