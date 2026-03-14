import joblib
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from utils import *
from process import feature_imp

from preprocess import load_dataset, preprocess_data

x,y = load_dataset("../data/creditcard.csv")
x_train,x_test,y_train,y_test,scaler = preprocess_data(x,y)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

model.fit(x_train,y_train)
y_pred = model.predict(x_test) 

y_prob = model.predict_proba(x_test)[:,1]

joblib.dump(scaler, "../models/scaler.pkl")

feature_importance = model.feature_importances_
feature_names = x.columns

top_features = feature_imp(feature_importance,feature_names)
plot_feature_imp(top_features)


# to visualize data (NA)
## plot_roc_curve(y_test,y_prob)
## plot_pre_rec_curve(y_test,y_prob)
report(y_test,y_pred)








