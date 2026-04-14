import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# -------------------------------
# 1. Original seed data
# -------------------------------
data = [
    [3.75, -1.11, 0.807, 57.05, 1.76, 1],
    [9.51, -2.29, 0.896, 45.67, 1.82, 1],
    [7.32, 3.29, 0.318, 86.23, 1.66, 1],
    [5.99, -1.43, 0.11, 83.87, -0.52, 1],
    [0.58, -3.59, 0.818, 80.86, -0.29, 1],
    [8.66, 3.02, 0.861, 67.76, 1.87, 1],
    [6.01, -4.25, 0.007, 66.48, 1.85, 1],
    [7.08, 4.87, 0.511, 52.09, 1.41, 1],
    [9.7, -3.01, 0.222, 84.86, -0.46, 1],
    [8.32, -4.94, 0.12, 85.02, 1.4, 1],
    [1.82, 2.07, 0.943, 56.95, -1.32, 1],
    [3.04, 2.71, 0.519, 76.3, 1.74, 1],
    [5.25, -4.26, 0.703, 84.86, 0.78, 1],
    [4.32, -1.42, 0.364, 84.35, 0.28, 1],
    [2.91, -3.84, 0.972, 78.99, -1.61, 1],
    [6.12, 3.63, 0.962, 72.1, 0.46, 1],
    [3.66, -4.36, 0.301, 84.93, 0.07, 1],
    [7.85, -1.75, 0.037, 40.46, 0.96, 1],
    [6.08, -3.8, 0.908, 67.44, 1.24, 1],
    [9.49, 0.61, 0.489, 51.21, 1.65, 1],
    [9.66, 2.71, 0.986, 75.61, 0.05, 1],
    [8.08, -0.06, 0.242, 51.86, 0.01, 1],
    [0.98, -0.72, 0.762, 77.32, 0.6, 1],
    [6.84, -4.75, 0.238, 72.48, 0.81, 1],
    [4.4, -3.92, 0.728, 82.46, 1.18, 1],
    [9.09, 0.09, 0.536, 58.39, -1.62, 1],
    [6.63, -2.51, 0.835, 52.2, -1.86, 1],
    [3.12, -0.9, 0.321, 88.65, -0.14, 1],
    [5.47, -2.71, 0.041, 84.6, -0.85, 1],
    [9.7, -2.1, 0.678, 79.74, -1.88, 1],
    [7.75, -3.39, 0.017, 65.13, -1.85, 1],
    [9.39, 4.3, 0.512, 68.85, 1.29, 1],
    [8.95, 3.08, 0.226, 64.63, -0.56, 1],
    [9.22, 3.71, 0.174, 76.12, 0.09, 1],
    [0.45, 3.93, 0.937, 72.27, 0.49, 1]
]

columns = [
    "pressure_drop",
    "flow_change",
    "vibration",
    "acoustic_db",
    "temp_anomaly",
    "leak"
]

df_seed = pd.DataFrame(data, columns=columns)

# -------------------------------
# 2. Get min–max ranges
# -------------------------------
ranges = {
    col: (df_seed[col].min(), df_seed[col].max())
    for col in columns if col != "leak"
}

# -------------------------------
# 3. Generate 2000 random leak samples
# -------------------------------
np.random.seed(42)
samples = 2000

synthetic_data = {
    "pressure_drop": np.random.uniform(*ranges["pressure_drop"], samples),
    "flow_change": np.random.uniform(*ranges["flow_change"], samples),
    "vibration": np.random.uniform(0, 1, samples),
    "acoustic_db": np.random.uniform(
        ranges["acoustic_db"][0], ranges["acoustic_db"][1], samples
    ),
    "temp_anomaly": np.random.uniform(*ranges["temp_anomaly"], samples),
    "leak": np.ones(samples, dtype=int)
}

df_2000 = pd.DataFrame(synthetic_data)

# -------------------------------
# 4. Save dataset
# -------------------------------
df_2000.to_csv(DATA_DIR / "leak_dataset_2000.csv", index=False)

print("Dataset created:", df_2000.shape)
print(df_2000.head())
