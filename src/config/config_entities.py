import os, sys

from dataclasses import dataclass
from src.constants.training_pipeline import ARTIFACT_DIR, TRAIN_FILE_NAME, TEST_FILE_NAME, RAW_FILE_NAME

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join(ARTIFACT_DIR, TRAIN_FILE_NAME)
    test_data_path: str = os.path.join(ARTIFACT_DIR, TEST_FILE_NAME)
    raw_data_path: str = os.path.join(ARTIFACT_DIR, RAW_FILE_NAME)