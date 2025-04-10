import os, sys

import numpy as np
import pandas as pd
import dill

from sklearn.metrics import r2_score

from sklearn.model_selection import GridSearchCV
from src.exception.exception import MLException

def save_object(file_path:str, obj:object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as f:
            dill.dump(obj, f)
            
    except Exception as e: 
        raise MLException(e, sys)
    
def evaluate_models(models, params, X_train, y_train, X_test, y_test): 
    try:
        report = {}
        
        for i in range(len(list(models))):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]
            
            gs = GridSearchCV(model, param, cv=3)
            gs.fit(X_train, y_train)
            
            model.set_params(**gs.best_params_)
            
            model.fit(X_train, y_train)
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            report[list(models.keys())[i]] = test_model_score
        return report
    except Exception as e:
        raise MLException(e, sys)
    
def load_object(file_path:str):
    try:
        with open(file_path, 'rb') as f:
            return dill.load(f)
    except Exception as e:
        raise MLException(e, sys)