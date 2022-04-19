# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:43:40 2021

@author: rincy
"""
import numpy as np
import pickle
from flask import Flask,request, render_template
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "lLQFuEDZ1O_gCPmzh3A1CYvsn_mYdxQ-bT69AFmxKcBI"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask(__name__,template_folder="templates")
model = pickle.load(open('abalone.pkl', 'rb'))
@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')
@app.route('/home', methods=['GET'])
def about():
    return render_template('home.html')
@app.route('/pred',methods=['GET'])
def page():
    return render_template('upload.html')
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    print(features_value)
    
    features_name = ['Sex','Length','Diameter','Height','Whole weight','Shucked weight','Viscera weight','Shell weight']
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": [
        ['Sex', 'Length', 'Diameter', 'Height', 'Whole weight', 'Shucked weight', 'Viscera weight',
         'Shell weight']],
                                       "values": total}]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/e090f502-19a9-4440-af2e-60e5eeb94b1d/predictions?version=2022-04-19', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    pred = response_scoring.json()
    
    output = pred['predictions'][0]['values'][0][0] 

    print(output)
    return render_template('upload.html', prediction_text='The predicted age of abalone is {} years.'.format((output+1.5)))

    
if __name__ == '__main__':
      app.run(debug=False)