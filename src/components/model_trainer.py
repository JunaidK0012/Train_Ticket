import os 
import sys
import pandas as pd
import numpy as np 

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import save_object

from sklearn.ensemble import RandomForestRegressor

@dataclass
class ModelTrainerConfig:
    model_path = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,X_train,X_test,y_train,y_test):
        try:
            model = RandomForestRegressor()
            model.fit(X_train,y_train)

            scores = model.score(X_test,y_test)

            save_object(self.model_trainer_config.model_path,model)

            return scores
        except Exception as e:
            raise CustomException(e,sys)
