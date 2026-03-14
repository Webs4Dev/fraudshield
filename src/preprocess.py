import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

def load_dataset(path):
    df = pd.read_csv(path)
    x = df.drop("Class",axis=1)
    y = df["Class"]

    return x,y

def preprocess_data(x,y):
    x_train,x_test,y_train,y_test = train_test_split(
        x,y,test_size=0.2,random_state=42,stratify=y
    )

    scaler = StandardScaler()

    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    smote = SMOTE(random_state=42)

    x_train_resampled,y_train_resampled = smote.fit_resample(x_train_scaled,y_train)
    return x_train_resampled, x_test_scaled, y_train_resampled, y_test, scaler


