from sklearn.metrics import accuracy_score, classification_report

def evaluate(model, X_test, y_test):

    preds = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))