import pandas as pd

# To get the features which are actually detecting fraud
def feature_imp(feature_importance,feature_names):
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": feature_importance
    })

    importance_df = importance_df.sort_values(
        by="importance",
        ascending=False
    )

    return importance_df.head(10)