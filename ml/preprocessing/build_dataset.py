from load_data import load_data
from clean_data import clean_data
from features_engineering import create_target


def build_dataset():

    df = load_data("dataset/raw/small_food_data.csv")

    df = clean_data(df)

    df, mapping = create_target(df)

    
    # take small dataset
   # df = df.sample(n=10000, random_state=42)

    df.to_csv("ml/data/final_data.csv", index=False)

    print("Dataset ready ✅")

if __name__ == "__main__":
     build_dataset()