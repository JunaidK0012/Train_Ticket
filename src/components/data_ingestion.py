import os
import sys
import pandas as pd 
import numpy as np 

from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass


from src.components.data_cleaning import DataCleaningConfig
from src.components.data_cleaning import DataCleaning

from src.components.data_transformation import DataTransformationConfig
from src.components.data_transformation import DataTransformation

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    raw_data_path = os.path.join('artifacts','raw_data_path.csv')
    raw_schedule_data_path = os.path.join('artifacts','raw_schedule.csv')

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion component.")
        try:
            df = pd.read_csv('notebook\\data\\price_data.csv')
            schedules = pd.read_csv('notebook\\data\\schedules.csv')

            logging.info("Read the dataset as DataFrame.")
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path),exist_ok=True)

            df.to_csv(self.data_ingestion_config.raw_data_path,index=False,header=True)
            schedules.to_csv(self.data_ingestion_config.raw_schedule_data_path,index=False,header=True)

            logging.info("Data ingestion completed.")

            return(
                self.data_ingestion_config.raw_data_path,
                self.data_ingestion_config.raw_schedule_data_path
            )


        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj = DataIngestion()
    raw_data_path,raw_schedule_data_path = obj.initiate_data_ingestion()

    data_cleaning = DataCleaning()
    train_data_path,test_data_path = data_cleaning.initiate_data_cleaning(raw_data_path,raw_schedule_data_path)

    data_transformation = DataTransformation()
    X_train,X_test,y_train,y_test = data_transformation.initiate_data_transformation(train_data_path,test_data_path)

    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_trainer(X_train,X_test,y_train,y_test))



