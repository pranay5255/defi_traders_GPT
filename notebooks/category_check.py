
import pandas as pd
import numpy as np

df=pd.read_csv("../GPT4_setup/coingeckoCategories_scraper_out.csv")

def preprocess(df):
    df.rename({"Unnamed: 0": "category", '0':"token"},axis=1,inplace=True)
    df['token'].apply(lambda x: eval(x))
    df['token'].apply(lambda x: str(x).lower())
    return(df)

def category_check(token):
    df['token'].apply(lambda x: str(x).lower())
    df['contains']=df['token'].apply(lambda x: (True if token in x else False))
    list_of_cats=df[df['contains']==True]['category'].to_list()
    return(list_of_cats)