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