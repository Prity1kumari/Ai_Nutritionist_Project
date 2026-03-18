import pandas as pd

def load_data(path):
    
    cols = [
        "product_name",
        "ingredients_text",
        "energy_100g",
        "fat_100g",
        "saturated-fat_100g",
        "carbohydrates_100g",
        "sugars_100g",
        "fiber_100g",
        "proteins_100g",
        "salt_100g",
        "nutrition-score-fr_100g"
    ]
    
    df = pd.read_csv(path, usecols=cols, low_memory=False)
    
    return df

print("Data loading function is ready.")    