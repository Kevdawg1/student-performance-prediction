import os, sys

import numpy as np
import pandas as pd
import dill

from src.exception.exception import MLException

def save_object(file_path:str, obj:object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as f:
            dill.dump(obj, f)
            
    except Exception as e: 
        raise MLException(e, sys)