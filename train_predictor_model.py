import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
import os

os.makedirs("models", exist_ok=True)

# Training data with 6 features matching _build_features
X = np.array([
    [-15, 50, 10, 0, 2, 0.85],   # BUY: good gap, low volatility, high competition, high confidence
    [-60, 280, 40, 2, 2, 0.60],  # WAIT: bad gap, high volatility, high competition
    [-30, 120, 15, 1, 1, 0.75],  # BUY: decent gap, medium volatility, medium competition
    [-70, 300, 50, 2, 2, 0.50],  # WAIT: very bad gap, high spread, high volatility
    [-8, 30, 8, 0, 1, 0.90],     # BUY: slight gap, stable, good confidence
    [10, 400, 2, 2, 0, 0.40],    # WAIT: overpriced, high volatility, low sellers
    [-20, 80, 12, 0, 2, 0.80],   # BUY: good gap, stable, high competition
    [5, 350, 3, 2, 0, 0.45]      # WAIT: overpriced, volatile, low supply
])

y = [1, 0, 1, 0, 1, 0, 1, 0]  # 1 = BUY, 0 = WAIT

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

joblib.dump(model, "models/logistic_predictor.joblib")

print("✅ Model trained and saved successfully")
print(f"Model accuracy on training data: {model.score(X, y):.2%}")