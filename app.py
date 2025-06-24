# app.py
from flask import Flask, request, jsonify
import joblib, numpy as np
import pandas as pd
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
model = joblib.load("model.pkl")
df = pd.read_csv('housing.csv', header=None, sep='\s+')

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    # X = np.array(data["features"]).reshape(1, -1)
    X = df.iloc[:, :-1]
    preds = model.predict(X)
    return jsonify({"prediction": preds.tolist()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)