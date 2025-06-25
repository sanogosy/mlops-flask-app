# train.py
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split

# X, y = load_iris(return_X_y=True)
# model = RandomForestClassifier()
# model.fit(X, y)
df = pd.read_csv('housing.csv', header=None, sep='\s+')

df = df.dropna()
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# model = LinearRegression()
# model.fit(X, y)
# joblib.dump(model, "model.pkl")

model = RandomForestClassifier(n_estimators=100)
X_train, y_train, X_test, y_test = train_test_split(X, y, test_size=0.2)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Metrics
acc = accuracy_score(y_test, y_pred)

joblib.dump(model, "model.pkl")

# Tracking
mlflow.set_tracking_uri("http://localhost:5001") 
mlflow.set_experiment("mlops-example")

with mlflow.start_run():
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model.pkl")