# Pipeline Leak Detection

This repository contains a pipeline leak detection system built with Python, scikit-learn, and Streamlit.
The project has been reorganized to improve maintainability and reduce root-level clutter.

## Repository Structure

- `app.py` — Main Streamlit dashboard entrypoint
- `Train.py` — Training script for model development
- `Test.py` — Existing Random Forest test GUI script
- `requirements.txt` — Python dependencies

### Organized folders
- `data/` — All dataset and sample CSV/XLSX files
- `models/` — Serialized model and scaler artifacts
- `docs/` — Documentation and deployment guides

## Usage

### Run the Streamlit dashboard
```bash
streamlit run app.py
```

### Train or regenerate models
```bash
python Train.py
```

### Run the existing GUI test script
```bash
python Test.py
```

### Generate synthetic datasets
```bash
python dataset1.py
python dataset2.py
python detection_dataset.py
```

## Notes

- The dashboard loads models from `models/`.
- All CSV datasets are now stored in `data/`.
- Documentation moved to `docs/` for a cleaner root folder.
