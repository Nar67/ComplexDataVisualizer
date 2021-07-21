import pandas as pd

def check_all_categorical(df):
    for col in df.columns:
        if df[col].dtype.name not in ['object']:
            return False
    return True


# trying to predict if a numerical column is a category
# likely_cat = {}
# for var in df.columns:
#     likely_cat[var] = 1.*df[var].nunique()/df[var].count() < 0.05 #or some other threshold