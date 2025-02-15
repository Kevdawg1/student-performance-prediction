import os, sys

from src.pipeline.train_pipeline import TrainPipeline
from src.exception.exception import MLException
from src.logging.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

if __name__ == "__main__":
    train_pipeline = TrainPipeline()
    train_pipeline.run_pipeline()