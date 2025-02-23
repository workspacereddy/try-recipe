from fastapi import FastAPI
from datasets import load_dataset
import pandas as pd

app = FastAPI()

# Load dataset at startup
dataset = load_dataset('AkashPS11/recipes_data_food.com', split='train')
df = pd.DataFrame(dataset)
wanted_columns = ['title', 'description', 'ingredients', 'calories']
df = df[wanted_columns]

def search_recipe_by_title(title, dataframe):
    # Case-insensitive exact match
    result = dataframe[dataframe['title'].str.lower() == title.lower()]
    if not result.empty:
        return result.iloc[0].to_dict()  # Return first match as a dictionary
    return {"error": "Recipe not found"}

# Endpoint to get recipe by title
@app.get("/recipe/{title}")
async def get_recipe(title: str):
    result = search_recipe_by_title(title, df)
    return result
