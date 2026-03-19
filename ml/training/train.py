import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


def load_dataset():

    df = pd.read_csv("../data/final_data.csv")

    df=df.drop(columns=["nutrition-score-fr_100g","target","nutriscore_grade"])

    X = df.drop(columns=["target_encoded", "product_name", "ingredients_text"])
    y = df["target_encoded"]

    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_models(X_train, y_train):

    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)

    xgb = XGBClassifier()
    xgb.fit(X_train, y_train)

    return rf, xgb



from evaluate import evaluate
from save_model import save_model

X_train, X_test, y_train, y_test = load_dataset()

rf, xgb = train_models(X_train, y_train)

print("Random Forest:")
evaluate(rf, X_test, y_test)

print("XGBoost:")
evaluate(xgb, X_test, y_test)

# choose best
best_model = xgb

save_model(best_model)