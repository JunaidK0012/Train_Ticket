import os
import sys
import numpy as np 
import pandas as pd 

from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass

from sklearn.model_selection import train_test_split

@dataclass
class DataCleaningConfig:
    availability_path = os.path.join('artifacts','availability.csv')
    train_data_path = os.path.join('artifacts','train_data.csv')
    test_data_path = os.path.join('artifacts','test_data.csv')
    cleaned_schedule_path = os.path.join('artifacts','clean_schedule.csv')

class DataCleaning:
    def __init__(self):
        self.data_cleaning_config = DataCleaningConfig()

    def initiate_data_cleaning(self,raw_data_path,raw_schedule_data_path):
        logging.info("Entered the Data Cleaning method.")
        try:
            df = pd.read_csv(raw_data_path)
            schedules = pd.read_csv(raw_schedule_data_path)

            logging.info("Dropping unwanted columns.")
            df.drop(['fuelAmount','totalConcession', 'tatkalFare','reservationCharge','serviceTax',
                     'cateringCharge','timeStamp','dynamicFare','otherCharge','baseFare','duration']
                     ,axis='columns',inplace=True)
            schedules.drop(['timeStamp'],axis='columns',inplace=True)
            
            logging.info("Dropping Duplicate rows.")
            df.drop_duplicates(subset=['trainNumber', 'fromStnCode', 'toStnCode','classCode', 
                                       'distance'],ignore_index=True,keep='last',inplace=True)
            
            df['superfastCharge'] = df['superfastCharge'].apply(lambda x:0 if x==0 else 1)
            df = df.rename(columns={'superfastCharge':'SuperFast'})
            df = df[['trainNumber', 'fromStnCode', 'toStnCode','availability','classCode', 'distance','SuperFast', 'totalFare']]

            logging.info("Initiating Train Test split.")
            train_set,test_set = train_test_split(df,train_size=0.7,random_state=45) 

            logging.info("Saving the trained dataset with the availability column.")
            train_set.to_csv(self.data_cleaning_config.availability_path,index=False,header=True)

            train_set.drop(['availability'],axis='columns',inplace=True)
            test_set.drop(['availability'],axis='columns',inplace=True)

            logging.info("Saving train and test data.")
            train_set.to_csv(self.data_cleaning_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.data_cleaning_config.test_data_path,index=False,header=True)
            schedules.to_csv(self.data_cleaning_config.cleaned_schedule_path,index=False,header=True)

            logging.info("Data Cleaning and splitting completed.")

            return(
                self.data_cleaning_config.train_data_path,
                self.data_cleaning_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)
        