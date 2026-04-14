import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ===============================
# 1. NO-LEAK (0) SEED DATA
# ===============================
no_leak_data = [
    [1.56, -2.19, 0.228, 52.9, -1.94, 0],
    [1.56, 0.43, 0.427, 73, 1.71, 0],
    [0.21, 2.72, 0.417, 44.66, -0.82, 0],
    [2.12, 3.15, 0.338, 71.66, -0.73, 0],
    [1.83, 2.29, 0.323, 57.46, 0.23, 0],
    [1.39, 1.23, 0.252, 44.21, 1.96, 0],
    [2.92, -1.69, 0.497, 48.08, -1.44, 0],
    [4.56, -1.89, 0.285, 70.32, 1.51, 0],
    [2, 2.3, 0.61, 45.07, 0.79, 0],
    [5.14, 1.38, 0.503, 73.18, 0.81, 0],
    [5.92, 3.87, 0.051, 40.25, -0.56, 0],
    [0.46, -0.28, 0.279, 48.04, -0.83, 0],
    [1.71, 2.13, 0.24, 74.59, 1.24, 0],
    [0.65, 2.61, 0.145, 72.6, 1.47, 0],
    [3.05, 0.23, 0.672, 56.27, 1.19, 0],
    [1.22, -4.69, 0.368, 72.88, 1.56, 0],
    [4.95, 1.36, 0.632, 68.42, -0.65, 0],
    [0.34, -1.86, 0.634, 44.68, -0.5, 0],
    [2.59, 4.08, 0.09, 53.26, 0.31, 0],
    [5.2, 2.56, 0.187, 59.65, 0.17, 0],
    [1.85, -4.23, 0.591, 71.56, 0.36, 0],
    [5.98, 1.33, 0.645, 49.76, -1.49, 0],
    [0.88, 3.04, 0.691, 54.04, 1.08, 0],
    [1.96, -3.13, 0.387, 41.22, -1.14, 0],
    [3.25, 0.39, 0.138, 48.86, -1.66, 0]
]

columns = [
    "pressure_drop",
    "flow_change",
    "vibration",
    "acoustic_db",
    "temp_anomaly",
    "leak"
]

df_no_leak_seed = pd.DataFrame(no_leak_data, columns=columns)

# ===============================
# 2. EXTRACT MIN–MAX RANGES
# ===============================
ranges_no_leak = {
    col: (df_no_leak_seed[col].min(), df_no_leak_seed[col].max())
    for col in columns if col != "leak"
}

# ===============================
# 3. GENERATE 2000 NO-LEAK SAMPLES
# ===============================
np.random.seed(42)
samples = 2000

synthetic_no_leak = {
    "pressure_drop": np.random.uniform(*ranges_no_leak["pressure_drop"], samples),
    "flow_change": np.random.uniform(*ranges_no_leak["flow_change"], samples),
    "vibration": np.random.uniform(0, 1, samples),
    "acoustic_db": np.random.uniform(
        ranges_no_leak["acoustic_db"][0],
        ranges_no_leak["acoustic_db"][1],
        samples
    ),
    "temp_anomaly": np.random.uniform(*ranges_no_leak["temp_anomaly"], samples),
    "leak": np.zeros(samples, dtype=int)
}

df_no_leak_2000 = pd.DataFrame(synthetic_no_leak)

# ===============================
# 4. SAVE DATASET
# ===============================
df_no_leak_2000.to_csv(DATA_DIR / "no_leak_dataset_2000.csv", index=False)

print("NO-LEAK dataset created:", df_no_leak_2000.shape)
print(df_no_leak_2000.head())
