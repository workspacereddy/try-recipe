from fastapi import FastAPI
from datasets import load_dataset
import pandas as pd

app = FastAPI()

# Load dataset at startup
dataset = load_dataset('AkashPS11/recipes_data_food.com', split='train')
df = pd.DataFrame(dataset)
wanted_columns = ['Name', 'RecipeIngredientParts', 'Description', 'Calories']
df = df[wanted_columns]

def search_recipe_by_title(Name, dataframe):
    result = dataframe[dataframe['Name'].str.lower() == Name.lower()]
    if not result.empty:
        return result.iloc[0].to_dict()
    return {"error": "Recipe not found"}

@app.get("/recipe/{Name}")
async def get_recipe(Name: str):
    result = search_recipe_by_title(Name, df)
    return result