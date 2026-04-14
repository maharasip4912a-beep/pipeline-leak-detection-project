# ============================================================
# LEAK DETECTION – TESTING GUI (RANDOM FOREST)
# ============================================================

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "random_forest_model.pkl"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ------------------------------------------------------------
# MAIN WINDOW
# ------------------------------------------------------------
root = tk.Tk()
root.title("Leak Detection – Test Module")
root.geometry("850x500")
root.configure(bg="#f4f6f7")

# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------
title = tk.Label(
    root,
    text="LEAK DETECTION – RANDOM FOREST TESTING",
    font=("Arial", 16, "bold"),
    bg="#2c3e50",
    fg="white",
    pady=10
)
title.pack(fill=tk.X)

# ------------------------------------------------------------
# GLOBAL VARIABLES
# ------------------------------------------------------------
test_df = None
result_df = None

# ------------------------------------------------------------
# UPLOAD CSV FUNCTION
# ------------------------------------------------------------
def upload_csv():
    global test_df
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")]
    )
    if not file_path:
        return

    try:
        test_df = pd.read_csv(file_path)
        lbl_file.config(text=os.path.basename(file_path))
        messagebox.showinfo("Success", "Test CSV uploaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ------------------------------------------------------------
# PROCESS & PREDICT FUNCTION
# ------------------------------------------------------------
def process_data():
    global result_df

    if test_df is None:
        messagebox.showwarning("Warning", "Please upload a test CSV file!")
        return

    try:
        X_test = test_df.copy()
        X_scaled = scaler.transform(X_test)

        predictions = model.predict(X_scaled)

        result_df = test_df.copy()
        result_df["Prediction"] = predictions
        result_df["Status"] = result_df["Prediction"].map(
            {1: "LEAK DETECTED", 0: "NO LEAK"}
        )

        display_results(result_df)

        messagebox.showinfo("Completed", "Leak prediction completed!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ------------------------------------------------------------
# DISPLAY RESULTS IN TABLE
# ------------------------------------------------------------
def display_results(df):
    for row in tree.get_children():
        tree.delete(row)

    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

# ------------------------------------------------------------
# SAVE OUTPUT CSV
# ------------------------------------------------------------
def save_csv():
    if result_df is None:
        messagebox.showwarning("Warning", "No results to save!")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if file_path:
        result_df.to_csv(file_path, index=False)
        messagebox.showinfo("Saved", "Output CSV saved successfully!")

# ------------------------------------------------------------
# BUTTON FRAME
# ------------------------------------------------------------
btn_frame = tk.Frame(root, bg="#f4f6f7")
btn_frame.pack(pady=10)

tk.Button(
    btn_frame,
    text="Upload Test CSV",
    command=upload_csv,
    bg="#3498db",
    fg="white",
    width=18
).grid(row=0, column=0, padx=10)

tk.Button(
    btn_frame,
    text="Process & Predict",
    command=process_data,
    bg="#27ae60",
    fg="white",
    width=18
).grid(row=0, column=1, padx=10)

tk.Button(
    btn_frame,
    text="Save Output CSV",
    command=save_csv,
    bg="#8e44ad",
    fg="white",
    width=18
).grid(row=0, column=2, padx=10)

# ------------------------------------------------------------
# FILE LABEL
# ------------------------------------------------------------
lbl_file = tk.Label(
    root,
    text="No file selected",
    bg="#f4f6f7",
    fg="gray"
)
lbl_file.pack()

# ------------------------------------------------------------
# RESULT TABLE
# ------------------------------------------------------------
table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tree = ttk.Treeview(table_frame)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)

# ------------------------------------------------------------
# RUN APP
# ------------------------------------------------------------
root.mainloop()
