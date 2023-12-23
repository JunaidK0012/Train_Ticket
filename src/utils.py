import os
import sys
from src.exception import CustomException
from src.logger import logging
import pickle

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
    