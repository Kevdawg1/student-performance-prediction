import os, sys

from src.exception.exception import MLException
from src.logging.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation

if __name__ == "__main__":
    data_ingestion = DataIngestion()
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    
    data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact)
    data_transformation_artifact = data_transformation.initiate_data_transformation()