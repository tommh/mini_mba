from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
from pprint import pprint
from tabulate import tabulate

import os

load_dotenv()  # Load variables from .env

# TODO: Add a new Ingredients model that can be used in the Recipe model with the following properties:
# - amount
# - unit
# - name


class Ingredient(BaseModel):
    """
    Represents a single ingredient with amount, unit, and name.
    """
    amount: float = Field(description="Quantity of the ingredient")
    unit: str = Field(description="Unit of measurement (e.g., cups, grams)")
    name: str = Field(description="Name of the ingredient")


class Recipe(BaseModel):
    """
    Use this model when working with complete cooking recipes.
    """
    title: str = Field(description="Name of the recipe")
    ingredients: List[Ingredient] = Field(
        description="List of ingredients needed for the recipe")
    instructions: List[str] = Field(
        description="Step-by-step instructions to prepare the recipe")


def get_recipe_from_text(recipe_text: str) -> Recipe:
    """
    Convert recipe text into a structured Recipe object using OpenAI.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Make the API call
    response = client.responses.parse(
        model="gpt-4o-mini-2024-07-18",
        input=[
            {"role": "user", "content": f"Convert this recipe into the specified format:\n\n{recipe_text}"}
        ],
        text_format=Recipe
    )

    return response.output_parsed


# Example usage
if __name__ == "__main__":
    # Read recipe text from file

    script_dir = os.path.dirname(os.path.abspath(__file__))
    recipe_path = os.path.join(
        script_dir, "recipe_ingredients", "mac_and_cheese_recipe.txt")
    with open(recipe_path, "r") as file:
        recipe_text = file.read()

    # Get structured recipe
    recipe = get_recipe_from_text(recipe_text)

    # Print results
    # pprint(recipe.ingredients[0])
    # pprint(recipe)  # to see the whole object

# Pretty print ingredients as table
ingredient_table = [[i.amount, i.unit, i.name] for i in recipe.ingredients]
print(tabulate(ingredient_table, headers=[
      "Amount", "Unit", "Ingredient"], tablefmt="grid"))
