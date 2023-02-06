import pandas as pd

df = pd.read_csv('./data/initial_cleaned_data.csv', index_col=0)

print(df.columns)