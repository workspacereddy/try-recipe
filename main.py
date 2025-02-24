from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# CORS setup to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production (e.g., specific domain)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the path to the CSV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(BASE_DIR, "recipes.csv")

# Load the CSV file with error handling
try:
    df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    raise Exception("recipes.csv file not found in the directory!")

# Columns to keep
wanted_columns = ['RecipeName', 'Ingredients', 'Cuisine', 'Instructions']
df = df[wanted_columns]

def search_recipe_by_title(recipe_name: str, dataframe: pd.DataFrame):
    """Search for recipes by partial, case-insensitive match."""
    result = dataframe[dataframe['RecipeName'].str.contains(recipe_name, case=False, na=False)]
    if not result.empty:
        return result.to_dict(orient='records')  # Return all matches as a list
    return {"error": f"No recipes found matching '{recipe_name}'"}

@app.get("/")
async def read_root():
    return {"message": "API is working!"}

@app.get("/recipe/{recipe_name}")
async def get_recipe(recipe_name: str):
    result = search_recipe_by_title(recipe_name, df)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
