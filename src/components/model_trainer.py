import os, sys

from src.exception.exception import MLException
from src.logging.logger import logging

# from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from sklearn.metrics import r2_score

from src.config.artifact_entities import DataTransformationArtifact
from src.config.config_entities import ModelTrainerConfig
from src.utils.utils import evaluate_models, save_object

class ModelTrainer:
    def __init__(self, data_transformation_artifact:DataTransformationArtifact):
        self.model_trainer_config = ModelTrainerConfig()
        self.data_transformation_artifact = data_transformation_artifact
        
    def initiate_model_trainer(self):
        try:
            logging.info("Model trainer initiated")
            logging.info("Splitting Training and Test Data")
            train_arr = self.data_transformation_artifact.train_arr
            test_arr = self.data_transformation_artifact.test_arr
            X_train = train_arr[:,:-1]
            y_train = train_arr[:,-1]
            X_test = test_arr[:,:-1]
            y_test = test_arr[:,-1]
            
            models = {
                "Linear Regression": LinearRegression(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest": RandomForestRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor(),
                "XGBRegressor": XGBRegressor(),
                # "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "KNN": KNeighborsRegressor(),
            }
            
            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error'],
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05],
                    'subsample':[0.6,0.7,0.9],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "XGBRegressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "KNN":{
                    'n_neighbors':[5,7,9,11],
                    'weights':['uniform', 'distance'],
                    'algorithm':['ball_tree', 'kd_tree', 'brute'],
                }
                }
            
            
            model_report = evaluate_models(models=models, params=params, X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
            
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]
            
            if best_model_score < 0.6:
                raise MLException("No best model and params found.")
            logging.info(f"Best model found: {best_model_name}")
            
            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )
            logging.info(f"{best_model_name} saved to {self.model_trainer_config.trained_model_file_path}")
            
            pred = best_model.predict(X_test)
            
            _r2_score = r2_score(y_pred=pred, y_true=y_test)
            
            return _r2_score
            
        except Exception as e:
            raise MLException(e, sys)