import os 
import sys
import pandas as pd 
import numpy as np 

from src.logger import logging
from src.exception import CustomException
from src.utils import get_columns,save_object
from dataclasses import dataclass
from scipy import sparse

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

@dataclass
class DataTransformationConfig:
    preprocessor_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig

    def get_preprocessor_obj(self,cat_columns):
        try:
            cat_pipeline = Pipeline(
                steps=[
                    ('encoder',OneHotEncoder(handle_unknown='ignore'))
                ]
            )

            preprocessor = ColumnTransformer([
                ('cat_pipeline',cat_pipeline,cat_columns)
            ],remainder='passthrough')

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_data_path,test_data_path):
        try:
            train_df = pd.read_csv(train_data_path)
            test_df = pd.read_csv(test_data_path)
            logging.info("Read train and test data completed.")

            logging.info("Obtaining preprocessing object.")
            target_column = 'totalFare'
            cat_columns = get_columns(train_df,target_column)

            preprocessor_obj = self.get_preprocessor_obj(cat_columns)

            input_feature_train_df = train_df.drop([target_column],axis='columns')  #X_train
            target_feature_train_df = train_df[target_column]                       #y_train

            input_feature_test_df = test_df.drop([target_column],axis='columns')    #X_test
            target_feature_test_df = test_df[target_column]                         #y_test

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            

            save_object(self.data_transformation_config.preprocessor_path,preprocessor_obj)


            return(input_feature_train_arr,input_feature_test_arr,target_feature_train_df,target_feature_test_df)




        except Exception as e:
            raise CustomException(e,sys)
        

