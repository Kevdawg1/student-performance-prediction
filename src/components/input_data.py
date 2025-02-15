import os, sys

from src.config.artifact_entities import InputDataArtifact
from src.exception.exception import MLException
from src.logging.logger import logging

import pandas as pd

class InputData:
    def __init__(self, input_data_config:InputDataArtifact):
        self.input_data_config = input_data_config
    
    def get_data_as_dataframe(self)->pd.DataFrame:
        try:
            input_data_dict = {
                "gender": [self.input_data_config.gender],
                "race_ethnicity": [self.input_data_config.race_ethnicity],
                "parental_level_of_education": [self.input_data_config.parental_level_of_education],
                "lunch": [self.input_data_config.lunch],
                "test_preparation_course": [self.input_data_config.test_preparation_course],
                "writing_score": [self.input_data_config.writing_score],
                "reading_score": [self.input_data_config.reading_score],
            }
            data = pd.DataFrame(input_data_dict)
            return data
        except Exception as e:
            raise MLException(e, sys)