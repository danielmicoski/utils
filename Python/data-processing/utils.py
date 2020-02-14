import pandas as pd
import numpy as np
import os
import re
import zipfile
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.base import TransformerMixin
from impyute.imputation import cs
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import statsmodels.api as sm 
from sklearn.linear_model import LinearRegression
from mlxtend.feature_selection import SequentialFeatureSelector as SFS

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_zip_and_pick_variables(path_to_zip,zip_archive_name_with_extension,archive_name_with_extension):
    """
    A function to read csvs from zipped folders

    :param path_to_zip: the path where the archive is
    :param zip_archive_name_with_extension: name of the archive in the format archive.zip 
    :param str archive_name_with_extension: csv file name
    :return: a DataFrame
    :rtype: pandas.DataFrame
    """
    zf = zipfile.ZipFile(path_to_zip + zip_archive_name_with_extension)
    df = pd.read_csv(zf.open(archive_name_with_extension))
    df = df.drop([0],axis=0)
    chosen = pd.read_csv(zf.open('chosen_variables.csv'),sep=';')
    new = list(chosen['new'])
    chosen = list(chosen['old'])
    df=df[chosen]
    df.columns = new
    return df

def get_missing_pct(df):
    """
    A function to find mising percentual per column in a dataframe

    :param df: the input dataframe
    :return: a DataFrame with the two column: The input df column labels and the missing percentual
    :rtype: pandas.DataFrame
    """
    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum()/df.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    return missing_data

class DataImputer(TransformerMixin):
    """ 
    A class to impute missing values.

    Attributes
    ----------

    Methods
    -------
    fit(self, dataframe, y=None)
        fits the imputation method(s) to the selected columns

    transform(self, dataframe)
        inputs the missing with fitted method
    """
    def __init__(self,strategy=None,output_array=False):
        """
        Builder with the following available attributes:   

        :param strategy: str,the method to use to input among ['mean','median','most_frequent','knn','mice','em']
        :param output_array: bool,if True the output is array, else dataframe  

        """    
        self.strategy = strategy
        self.output_array = output_array
    def fit(self, dataframe):
        """
        Method to be fitted, default is the most frequent value for str and int columns and median for float columns
        
        Custom: use a dict to set columns and imputation method like:
        {'mean':[columnname1,columnname2],'knn':[columname3,columnname4],'most_frequent':[columname5,columname6]}
        
        All unrelated columns will be imputed using default method
        :param dataframe: The input dataframe
        """
        self.fill = pd.Series([dataframe[c].value_counts().index[0]\
        if dataframe[c].dtype in [np.dtype('O'),np.dtype('int8'),np.dtype('int32'),np.dtype('int64')]\
        else dataframe[c].median() for c in dataframe],index=dataframe.columns)
        
        if self.strategy is not None:
            
            if type(self.strategy) is not dict:
                raise ValueError("Dict is required. Try {'method':[columname,...,],'method':['columname'...]} instead")
                
            else:
                self.strategy_single_imp = {method:column for method, aux in self.strategy.items() for column in aux}
                
                for method, column in self.strategy_single_imp.items():
                    
                    if column not in dataframe.columns:
                        raise ValueError("Column {} is not in dataset".format(column))
                    if method not in ['most_frequent','mean','median','mice','knn']:
                        raise ValueError("Unavailable method")
                    
                    for c in dataframe:
                        
                        if (column == c and method == 'most_frequent'):
                            self.fill[c] = dataframe[c].value_counts().index[0]
                        elif (column == c and method == 'mean'):
                            self.fill[c] = dataframe[c].mean()
                        elif (column == c and method == 'median'):
                            self.fill[c] = dataframe[c].median()
                          
                for method,columns in self.strategy.items():
                    
                    if column not in dataframe.columns:
                        raise ValueError("Column {} is not in dataset".format(column))
                    if method not in ['most_frequent','mean','median','mice','knn']:
                        raise ValueError("Unavailable method")
                    
                    if method == 'knn':
                        
                        train_cols = list(dataframe.select_dtypes(include=['floating']))
                        train = pd.DataFrame(cs.fast_knn(dataframe[train_cols],k=5))
                        train.columns = train_cols
                        dataframe[train_cols] = train.values 
                                             
                    if method == 'mice':
                                             
                        train_cols = list(dataframe.select_dtypes(include=['floating']))
                        train = pd.DataFrame(cs.mice(dataframe[train_cols]))
                        train.columns = train_cols
                        dataframe[train_cols] = train.values   
           
        return self

    def transform(self, dataframe):
        """
        A function to fill missings with self.fill values

        :param dataframe: The input dataframe
        """
        if self.output_array:
            return dataframe.fillna(self.fill).values
        else:
            return dataframe.fillna(self.fill)

def clean_string(serie):
    """
    A function to remove special characters and numbers from a string, lowercasing them

    :param serie: pandas.Series, The Serie tha should be cleaned
    :return: str
    """
    return serie.apply(lambda x: re.sub('[^A-Za-z0-9 ]+', '', x).lower())