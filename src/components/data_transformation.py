import os, sys
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception.exception import MLException
from src.logging.logger import logging

from src.config.artifact_entities import DataIngestionArtifact, DataTransformationArtifact
from src.config.config_entities import DataTransformationConfig
from src.constants.training_pipeline import TARGET_COLUMN, ARTIFACT_DIR, PREPROCESSING_OBJECT_FILE_NAME
from src.utils.utils import save_object

class DataTransformation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact):
        self.data_transformation_config = DataTransformationConfig()
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_config.preprocessor_object_file_path = os.path.join(ARTIFACT_DIR, PREPROCESSING_OBJECT_FILE_NAME)

    def get_data_transformer_object(self):
        """
        This function returns a preprocessor object.
        This preprocessor object will be used to transform the numerical and categorical columns.
        The numerical columns will be imputed using the median of the column and then scaled using StandardScaler.
        The categorical columns will be imputed using the most frequent value in the column and then scaled using StandardScaler(with_mean=False).
        The preprocessor object is then used to transform the data.
        """
        try:
            df = pd.read_csv(self.data_ingestion_artifact.raw_data_path)
            df = df.drop(columns=[TARGET_COLUMN], axis=1)
            numerical_columns = list(df.select_dtypes(exclude="object").columns) ## ["writing_score", "reading_score"]
            categorical_columns = list(df.select_dtypes(include="object").columns)
            logging.info(f'numerical_columns: {numerical_columns}')
            logging.info(f'categorical_columns: {categorical_columns}')
            # [
            #     "gender",
            #     "race_ethnicity",
            #     "parental_level_of_education",
            #     "lunch",
            #     "test_preparation_course",
            # ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False)),
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns),
                ]
            )

            return preprocessor

        except Exception as e:
            raise MLException(e, sys)
        
    def separate_input_and_outputs(self, data):
        """
        This method takes a pandas DataFrame as an argument and separates it into input
        features and output features.
        """
        try:
            input_features = data.drop(TARGET_COLUMN, axis=1)
            output_features = data[TARGET_COLUMN]
            return input_features, output_features
        except Exception as e:
            raise MLException(e, sys)
        
    def transform_data(self, preprocessor:ColumnTransformer, data, is_train_data:bool):
        
        X, y = self.separate_input_and_outputs(data)

        if is_train_data:
            X_arr = preprocessor.fit_transform(X)
        else:
            X_arr = preprocessor.transform(X)
        arr = np.c_[X_arr, np.array(y)]
        
        return arr
        
    
    def initiate_data_transformation(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_data_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_data_path)
            
            preprocessor = self.get_data_transformer_object()
            
            logging.info("Data transformation initiated")
            
            
            train_arr = self.transform_data(preprocessor=preprocessor, data=train_df, is_train_data=True)
            test_arr = self.transform_data(preprocessor=preprocessor, data=test_df, is_train_data=False)
            
            logging.info("Saving Preprocessor Object")
            
            save_object(
                file_path = self.data_transformation_config.preprocessor_object_file_path,
                obj = preprocessor
            )
            
            artifact = DataTransformationArtifact(
                train_arr=train_arr,
                test_arr=test_arr,
                preprocessor_object_file_path=self.data_transformation_config.preprocessor_object_file_path
            )
            
            return artifact
        except Exception as e:
            raise MLException(e, sys)