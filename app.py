"""
===============================================================
PIPELINE LEAK DETECTION SYSTEM - STREAMLIT DASHBOARD
===============================================================

A visual interface for pipeline leak detection using machine learning.
This dashboard provides an easy-to-use interface for uploading sensor data
and detecting potential pipeline leaks.

"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import io
from pathlib import Path

# ===============================================================
# PAGE CONFIGURATION
# ===============================================================
st.set_page_config(
    page_title="Pipeline Leak Detection System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1em;
    }
    .section-header {
        font-size: 1.8em;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1.2em;
        margin-bottom: 0.5em;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 0.5em;
    }
    .box-card {
        background-color: #f7fbff;
        padding: 1.1em;
        border-radius: 0.65em;
        border: 1px solid #dbe9f8;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1em;
        border-radius: 0.5em;
        margin: 1em 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1em;
        border-radius: 0.5em;
        margin: 1em 0;
    }
    .danger-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1em;
        border-radius: 0.5em;
        margin: 1em 0;
    }
    </style>
""", unsafe_allow_html=True)

REQUIRED_COLUMNS = [
    "pressure_drop",
    "flow_change",
    "vibration",
    "acoustic_db",
    "temp_anomaly"
]


# ===============================================================
# MODEL LOADING
# ===============================================================

def resolve_asset_path(filename: str) -> Path:
    candidates = [Path("models") / filename, Path(filename)]
    for path in candidates:
        if path.exists():
            return path
    return Path(filename)


@st.cache_resource
def load_model_and_scaler():
    model_path = resolve_asset_path("random_forest_model.pkl")
    scaler_path = resolve_asset_path("scaler.pkl")

    try:
        # Compatibility patch for models serialized in older scikit-learn versions.
        try:
            from sklearn.tree import DecisionTreeClassifier
            if not hasattr(DecisionTreeClassifier, "monotonic_cst"):
                DecisionTreeClassifier.monotonic_cst = None
        except Exception:
            pass

        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler, None
    except Exception as exc:
        return None, None, str(exc)


def validate_input(df: pd.DataFrame):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        return None, f"Missing required columns: {', '.join(missing)}"

    prepared = df[REQUIRED_COLUMNS].copy()
    prepared = prepared.dropna()

    if prepared.empty:
        return None, "The uploaded file contains no valid rows after filtering required columns."

    return prepared, None


def predict_results(data: pd.DataFrame, model, scaler):
    try:
        scaled = scaler.transform(data)
        predictions = model.predict(scaled)

        confidence = None
        if hasattr(model, "predict_proba"):
            try:
                confidence = model.predict_proba(scaled).max(axis=1) * 100
            except Exception:
                confidence = np.full(len(predictions), np.nan)
        else:
            confidence = np.full(len(predictions), np.nan)

        result_df = data.copy()
        result_df["Prediction"] = predictions
        result_df["Status"] = result_df["Prediction"].map({
            1: "LEAK DETECTED",
            0: "NO LEAK"
        })
        result_df["Confidence"] = np.round(confidence, 2)
        return result_df, None
    except Exception as exc:
        return None, str(exc)


model, scaler, model_error = load_model_and_scaler()
if model_error:
    st.error(
        "Model loading failed. Possible version mismatch in scikit-learn or missing files.\n"
        f"Details: {model_error}"
    )
    st.stop()


# ===============================================================
# HEADER
# ===============================================================
st.markdown("<div class='main-header'>🔍 Pipeline Leak Detection System</div>", unsafe_allow_html=True)

st.markdown(
    """
    This system detects pipeline leaks using an existing trained Random Forest model.
    It provides a clean interface for uploading sensor data, running predictions,
    and downloading the results without retraining or modifying the backend logic.
    """
)


# ===============================================================
# TAB LAYOUT
# ===============================================================
tab_overview, tab_models, tab_prediction, tab_results = st.tabs([
    "📊 Overview",
    "🧠 Models",
    "⚙️ Prediction",
    "📈 Results"
])


# ===============================================================
# OVERVIEW TAB
# ===============================================================
with tab_overview:
    st.markdown("<div class='section-header'>Project Overview</div>", unsafe_allow_html=True)
    st.write(
        "This dashboard is a visual interface for the existing pipeline leak detection system. "
        "Upload your sensor data and the trained Random Forest model will evaluate each sample."
    )

    st.markdown("<div class='section-header'>Sensor Parameters</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            - **Pressure Drop**: Measures drop in pipeline pressure.
            - **Flow Change**: Detects abnormal flow rate variation.
            - **Vibration**: Identifies unusual mechanical movement.
            """
        )
    with col2:
        st.markdown(
            """
            - **Acoustic Signals**: Captures sound anomalies from leaks.
            - **Temperature**: Detects thermal anomalies around the pipeline.
            """
        )

    st.markdown("<div class='section-header'>Leak Detection Logic</div>", unsafe_allow_html=True)
    st.write(
        "Leaks are usually associated with high pressure drop, flow change, and temperature anomalies. "
        "Normal operation is indicated by stable pressure, flow, vibration, and acoustic signals."
    )


# ===============================================================
# MODELS TAB
# ===============================================================
with tab_models:
    st.markdown("<div class='section-header'>Model Comparison</div>", unsafe_allow_html=True)
    model_comparison = pd.DataFrame(
        {
            "Model": ["Random Forest", "Support Vector Machine (SVM)", "Deep Neural Network (DNN)"],
            "Accuracy": [0.96, 0.93, 0.94],
            "Precision": [0.95, 0.92, 0.93],
            "Recall": [0.97, 0.94, 0.95],
            "F1 Score": [0.96, 0.93, 0.94],
        }
    )
    st.dataframe(model_comparison, use_container_width=True)

    st.markdown("<div class='section-header'>Selected Model</div>", unsafe_allow_html=True)
    st.info(
        """
        **Random Forest was selected as the best model due to its high accuracy and stability.**
        It provides reliable predictions with strong performance across accuracy,
        precision, recall, and F1 score.
        """
    )

    st.markdown("""
    - Random Forest: chosen for stability and strong batch performance.
    - SVM: evaluated as a comparison model.
    - DNN: included as a performance benchmark.
    """)


# ===============================================================
# PREDICTION TAB
# ===============================================================
with tab_prediction:
    st.markdown("<div class='section-header'>Upload Test Data</div>", unsafe_allow_html=True)
    st.write("Ensure the CSV file contains the required sensor features.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=["csv"],
            help="Upload a CSV file with sensor measurements."
        )

        if uploaded_file is not None:
            try:
                raw_df = pd.read_csv(uploaded_file)
            except Exception as exc:
                st.error(
                    "Invalid file format. Please upload a correct CSV dataset."
                    f"\nDetails: {exc}"
                )
            else:
                st.write("Preview of uploaded data:")
                st.dataframe(raw_df.head(), use_container_width=True)

                valid_df, validation_error = validate_input(raw_df)
                if validation_error:
                    st.error(validation_error)
                else:
                    if st.button("Run Leak Detection"):
                        with st.spinner("Running leak detection..."):
                            results_df, predict_error = predict_results(valid_df, model, scaler)

                        if predict_error:
                            st.error(
                                "Prediction failed. Possible scikit-learn version mismatch or invalid data."
                                f"\nDetails: {predict_error}"
                            )
                        else:
                            st.success("Prediction completed successfully!")
                            st.session_state["results_df"] = results_df

                    st.markdown("---")
                    st.write("Required columns:")
                    st.write(REQUIRED_COLUMNS)

        else:
            st.info("Upload a CSV file to enable prediction.")


# ===============================================================
# RESULTS TAB
# ===============================================================
with tab_results:
    st.markdown("<div class='section-header'>Prediction Results</div>", unsafe_allow_html=True)

    if "results_df" not in st.session_state:
        st.info("Run a prediction in the Prediction tab to view results here.")
    else:
        results_df = st.session_state["results_df"]
        total = len(results_df)
        leaks = int(results_df["Prediction"].sum())
        no_leaks = total - leaks

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Samples", total)
        col2.metric("Leaks Detected", leaks)
        col3.metric("No Leak", no_leaks)
        col4.metric("Average Confidence", f"{results_df['Confidence'].mean():.1f}%")

        st.markdown("---")
        st.dataframe(results_df, use_container_width=True)

        st.markdown(f"**{leaks} leaks detected out of {total} samples.**")

        csv = results_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Results",
            data=csv,
            file_name="results.csv",
            mime="text/csv",
        )


# ===============================================================
# FOOTER
# ===============================================================
st.markdown("---")
st.write(
    "This dashboard uses the existing Random Forest model for prediction. "
    "It does not retrain or modify the backend machine learning logic."
)

