import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score

from preprocess import load_dataset, preprocess_data


# load dataset
X, y = load_dataset("../data/creditcard.csv")

# preprocess dataset
X_train, X_test, y_train, y_test, scaler = preprocess_data(X, y)


models = {

    "Logistic Regression":
        LogisticRegression(max_iter=1000),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        ),

    "Gradient Boosting":
        GradientBoostingClassifier()

}


results = []

for name, model in models.items():

    print(f"\nTraining {name}...")

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    y_prob = model.predict_proba(X_test)[:,1]

    auc = roc_auc_score(y_test, y_prob)

    report = classification_report(
        y_test,
        y_pred,
        output_dict=True
    )

    results.append({
        "model": name,
        "precision": report["1"]["precision"],
        "recall": report["1"]["recall"],
        "f1": report["1"]["f1-score"],
        "auc": auc
    })


results_df = pd.DataFrame(results)

print("\nModel Comparison:\n")

print(results_df)