"""
Flask Application for Elastic Beanstalk Deployment
"""

import pickle
from flask import Flask, render_template, request
import numpy as np
import pandas as pd

import os, sys
from src.components.input_data import InputData
from src.config.artifact_entities import InputDataArtifact
from src.pipeline.predict_pipeline import PredictPipeline
from src.exception.exception import MLException

application = Flask(__name__)

app = application

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST'])
def predict_math_score():
    
    ## Form unsubmitted
    if request.method == 'GET':
        return render_template('form.html', results=None)
    
    ## Form submitted
    else:
        try:
            reading_score = float(request.form.get('reading_score'))
            writing_score = float(request.form.get('writing_score'))
            lunch = request.form.get('lunch')
            test_preparation_course = request.form.get('test_preparation_course')
            gender = request.form.get('gender')
            race_ethnicity = request.form.get('ethnicity')
            parental_level_of_education = request.form.get('parental_level_of_education')
            
            input_data_artifact = InputDataArtifact(reading_score=reading_score,
                                                    writing_score=writing_score,
                                                    lunch=lunch,    
                                                    test_preparation_course=test_preparation_course,
                                                    gender=gender,
                                                    race_ethnicity=race_ethnicity,
                                                    parental_level_of_education=parental_level_of_education)
            input_data = InputData(input_data_artifact)
            input_data_df = input_data.get_data_as_dataframe()
            predict_pipeline = PredictPipeline()
            predictions = predict_pipeline.predict(input_data_df)
            score = predictions[0].round(2)
            return render_template('form.html',  results=score)
        except Exception as e:
            raise MLException(e, sys)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)