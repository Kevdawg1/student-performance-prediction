import os, sys

from src.exception.exception import MLException
from src.constants.training_pipeline import ARTIFACT_DIR, MODEL_FILE_NAME, PREPROCESSING_OBJECT_FILE_NAME
from src.utils.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self, features):
        try:
            model = load_object(os.path.join(ARTIFACT_DIR, MODEL_FILE_NAME))
            preprocessor = load_object(os.path.join(ARTIFACT_DIR, PREPROCESSING_OBJECT_FILE_NAME))
            
            transformed_features = preprocessor.transform(features)
            
            prediction = model.predict(transformed_features)
            if prediction > 100: 
                prediction = 100
            return prediction
        except Exception as e:
            raise MLException(e, sys)