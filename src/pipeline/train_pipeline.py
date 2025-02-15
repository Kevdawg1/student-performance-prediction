import os, sys

from src.exception.exception import MLException
from src.logging.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

class TrainPipeline:
    def __init__(self):
        pass

    def run_pipeline(self) -> float:
        try:
            data_ingestion = DataIngestion()
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            

            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact)
            r2_score = model_trainer.initiate_model_trainer()
            return r2_score
        except Exception as e:
            raise MLException(e, sys)

if __name__ == "__main__":
    data_ingestion = DataIngestion()
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    
    data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact)
    data_transformation_artifact = data_transformation.initiate_data_transformation()
    
    model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact)
    r2_score = model_trainer.initiate_model_trainer()
    print(r2_score)