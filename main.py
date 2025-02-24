from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI()

# Get the path to the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the CSV file
csv_file_path = os.path.join(BASE_DIR, "recipes.csv")  # Make sure your recipes.csv is in the same directory as main.py
df = pd.read_csv(csv_file_path)

# Columns you want to keep
wanted_columns = ['RecipeName', 'Ingredients', 'Cuisine', 'Instructions']
df = df[wanted_columns]

# def search_recipe_by_title(RecipeName, dataframe):
#     # Case-insensitive exact match
#     result = dataframe[dataframe['RecipeName'].str.lower() == RecipeName.lower()]
#     if not result.empty:
#         return result.iloc[0].to_dict()  # Return first match as a dictionary
#     return {"error": "Recipe not found"}

def search_recipe_by_title(RecipeName, dataframe):
    # Case-insensitive partial match
    result = dataframe[dataframe['RecipeName'].str.contains(RecipeName, case=False, na=False)]
    if not result.empty:
        # return result.iloc[0].to_dict()  # Return the first match as a dictionary
        return result.to_dict(orient='records')  # Return all matched results as a list of dictionaries
    return {"error": "Recipe not found"}

@app.get("/")
@app.head("/")
async def read_root():
    return {"message": "API is working!"}
    
# Endpoint to get recipe by title
@app.get("/recipe/{RecipeName}")
async def get_recipe(RecipeName: str):
    result = search_recipe_by_title(RecipeName, df)
    return result
