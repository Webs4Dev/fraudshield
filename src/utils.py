import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import roc_curve,precision_recall_curve,auc
from sklearn.metrics import confusion_matrix,classification_report


# ROC CURVE
def plot_roc_curve(y_test,y_prob):
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    plt.figure()
    plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
    plt.plot([0,1],[0,1], linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve - Fraud Detection")
    plt.legend()
    plt.show()

# Precision Recall Curve 
def plot_pre_rec_curve(y_test,y_prob):
    precision, recall, _ = precision_recall_curve(y_test, y_prob)
    plt.figure()
    plt.plot(recall, precision)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall Curve")
    plt.show()

# to get precision,recall,F1 score values
def report(y_test,y_pred):
    print("Confusion Matrix")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report")
    print(classification_report(y_test, y_pred))

# to visualize how important each top feature is
def plot_feature_imp(top_features):
    plt.figure()
    plt.barh(
        top_features["feature"],
        top_features["importance"]
    )
    plt.xlabel("Importance")
    plt.title("Top 10 Fraud Detection Features")
    plt.gca().invert_yaxis()
    plt.show()
