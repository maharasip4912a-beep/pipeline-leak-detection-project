# ============================================================
# LEAK DETECTION – RF vs DNN vs SVC vs KNN
# ============================================================

import pandas as pd
import numpy as np
import time
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, ConfusionMatrixDisplay
)

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
#from sklearn.neighbors import KNeighborsClassifier

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------
df = pd.read_csv(DATA_DIR / "leak_detection_dataset_1000.csv")

X = df.drop("leak", axis=1)
y = df["leak"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ------------------------------------------------------------
# 2. FEATURE SCALING
# ------------------------------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
joblib.dump(scaler, MODELS_DIR / "scaler.pkl")

# ------------------------------------------------------------
# 3. MODEL DEFINITIONS
# ------------------------------------------------------------
models = {
    "Random Forest": RandomForestClassifier(
        n_estimators=10, max_depth=5, random_state=42
    ),
    "SVM": SVC(kernel="poly", degree=3, C=10, gamma="scale"),
  
}

results = {}

# ------------------------------------------------------------
# 4. TRAIN & EVALUATE CLASSICAL MODELS
# ------------------------------------------------------------
for name, model in models.items():
    start = time.time()
    model.fit(X_train_scaled, y_train)
    train_time = time.time() - start

    y_pred = model.predict(X_test_scaled)

    results[name] = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1": f1_score(y_test, y_pred),
        "Train_Time": train_time
    }

    joblib.dump(model, MODELS_DIR / f"{name.lower().replace(' ', '_')}_model.pkl")

    cm = confusion_matrix(y_test, y_pred)
    ConfusionMatrixDisplay(cm).plot()
    plt.title(f"{name} Confusion Matrix")
    plt.show()

# ------------------------------------------------------------
# 5. DNN MODEL
# ------------------------------------------------------------
start = time.time()

dnn = Sequential([
    Dense(64, activation="relu", input_shape=(X_train_scaled.shape[1],)),
    Dropout(0.5),
    Dense(32, activation="relu"),
    Dropout(0.5),
    Dense(1, activation="sigmoid")
])

dnn.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

early_stop = EarlyStopping(
    monitor="val_loss", patience=4, restore_best_weights=True
)

history = dnn.fit(
    X_train_scaled, y_train,
    validation_split=0.2,
    epochs=15,
    batch_size=42,
    callbacks=[early_stop],
    verbose=1
)

dnn_time = time.time() - start

y_pred_dnn = (dnn.predict(X_test_scaled) > 0.5).astype(int)

results["DNN"] = {
    "Accuracy": accuracy_score(y_test, y_pred_dnn),
    "Precision": precision_score(y_test, y_pred_dnn),
    "Recall": recall_score(y_test, y_pred_dnn),
    "F1": f1_score(y_test, y_pred_dnn),
    "Train_Time": dnn_time
}

dnn.save(MODELS_DIR / "dnn_leak_model.h5")

cm_dnn = confusion_matrix(y_test, y_pred_dnn)
ConfusionMatrixDisplay(cm_dnn).plot()
plt.title("DNN Confusion Matrix")
plt.show()

# ------------------------------------------------------------
# 6. DNN ACCURACY & LOSS PLOTS
# ------------------------------------------------------------
plt.plot(history.history["accuracy"], label="Train Accuracy")
plt.plot(history.history["val_accuracy"], label="Val Accuracy")
plt.title("DNN Accuracy")
plt.legend()
plt.show()

plt.plot(history.history["loss"], label="Train Loss")
plt.plot(history.history["val_loss"], label="Val Loss")
plt.title("DNN Loss")
plt.legend()
plt.show()

# ------------------------------------------------------------
# 7. PERFORMANCE COMPARISON
# ------------------------------------------------------------
perf_df = pd.DataFrame(results).T
print("\n=== MODEL PERFORMANCE COMPARISON ===")
print(perf_df)

# ------------------------------------------------------------
# 8. BEST MODEL SELECTION
# ------------------------------------------------------------
best_model = perf_df["F1"].idxmax()

print("\n=== BEST MODEL SELECTED ===")
print(f"Best Algorithm : {best_model}")
print(f"F1-score      : {perf_df.loc[best_model, 'F1']:.4f}")

# ------------------------------------------------------------
# 9. BAR CHART COMPARISON
# ------------------------------------------------------------
perf_df[["Accuracy", "Precision", "Recall", "F1"]].plot(kind="bar")
plt.title("Algorithm Performance Comparison")
plt.ylabel("Score")
plt.xticks(rotation=0)
plt.grid(True)
plt.show()


# ------------------------------------------------------------
# 10. ACCURACY & LOSS PLOTS FOR ALL MODELS
# ------------------------------------------------------------

model_names = []
train_accuracies = []
test_accuracies = []
train_losses = []
test_losses = []

# ---------- Classical Models ----------
for name, model in models.items():
    model_names.append(name)

    # Train accuracy
    y_train_pred = model.predict(X_train_scaled)
    train_acc = accuracy_score(y_train, y_train_pred)

    # Test accuracy (already computed)
    test_acc = results[name]["Accuracy"]

    train_accuracies.append(train_acc)
    test_accuracies.append(test_acc)

    # Loss proxy = 1 - accuracy
    train_losses.append(1 - train_acc)
    test_losses.append(1 - test_acc)

# ---------- DNN ----------
model_names.append("DNN")

train_acc_dnn = history.history["accuracy"][-1]
test_acc_dnn = results["DNN"]["Accuracy"]

train_accuracies.append(train_acc_dnn)
test_accuracies.append(test_acc_dnn)

train_losses.append(history.history["loss"][-1])
test_losses.append(results["DNN"]["Accuracy"] * 0 + (1 - test_acc_dnn))

# ------------------------------------------------------------
# 11. ACCURACY COMPARISON PLOT
# ------------------------------------------------------------
x = np.arange(len(model_names))
width = 0.35

plt.figure(figsize=(8, 5))
plt.bar(x - width/2, train_accuracies, width, label="Train Accuracy")
plt.bar(x + width/2, test_accuracies, width, label="Test Accuracy")
plt.xticks(x, model_names)
plt.ylabel("Accuracy")
plt.title("Train vs Test Accuracy (All Models)")
plt.legend()
plt.grid(True)
plt.show()

# ------------------------------------------------------------
# 12. LOSS COMPARISON PLOT
# ------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.bar(x - width/2, train_losses, width, label="Train Loss")
plt.bar(x + width/2, test_losses, width, label="Test Loss")
plt.xticks(x, model_names)
plt.ylabel("Loss")
plt.title("Train vs Test Loss (All Models)")
plt.legend()
plt.grid(True)
plt.show()
