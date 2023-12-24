import os
import sys
from src.exception import CustomException
from src.logger import logging
import pickle
import json
import pandas as pd
import numpy as np 

def get_columns(input_df,target_column):
    try:
        cat_columns= []
        num_columns= []
        for x in input_df.columns:
            if x == target_column:
                pass
            else:
                if input_df[x].dtype == 'O':
                    cat_columns.append(x)
                else:
                    num_columns.append(x) 

        return cat_columns
    
    except Exception as e:
        raise CustomException(e,sys)
    
def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open (file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)


    except Exception as e:
        raise CustomException(e,sys)
    
def get_schedule(trainNumber,schedule_df):
    try:
        x = schedule_df.index[schedule_df['trainNumber'] == trainNumber].tolist()  #this will give us the index of the given train in schedule_df
        y = schedule_df['stationList'].tolist()[x[0]]                # this will read the stationList(dictionary) column of the train
        parsed_data = json.loads(y.replace("'", "\""))               # loading it as a JSON object
        parsed_data_df = pd.DataFrame(parsed_data)                   # converting the json object to a dataframe
        parsed_data_df.drop(['routeNumber','stnSerialNumber','boardingDisabled'],axis='columns',inplace=True)

        return parsed_data_df

    except Exception as e:
        raise CustomException(e,sys)
    
def get_distance():
    try:
        pass
    except Exception as e:
        
    

