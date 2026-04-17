import pandas as pd
import glob

# get all CSV files
files = glob.glob("FOOD-DATA*.csv")

dfs = []

for file in files:
    df = pd.read_csv(file)
    dfs.append(df)

# merge all
merged_df = pd.concat(dfs, ignore_index=True)

# save
merged_df.to_csv("ingredients.csv", index=False)

print("Merged into ingredients.csv")