import os, sys
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_data_path: str
    test_data_path: str
    raw_data_path: str
    
@dataclass
class DataTransformationArtifact:
    preprocessor_object_file_path: str
    train_arr: list
    test_arr: list
    
@dataclass
class InputDataArtifact: 
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation_course: str
    writing_score: float
    reading_score: float