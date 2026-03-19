import pickle

def save_model(model):

    pickle.dump(model, open("../models/nutrition_model.pkl", "wb"))

    print("Model saved ✅")