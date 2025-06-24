# train.py
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

# X, y = load_iris(return_X_y=True)
df = pd.read_csv('housing.csv', header=None, sep='\s+')

df = df.dropna()
X = df.iloc[:, :-1]
y = df.iloc[:, -1]
# model = RandomForestClassifier()
# model.fit(X, y)
model = LinearRegression()
model.fit(X, y)
joblib.dump(model, "model.pkl")