# Arogya & Mausam — Project 1 (Classification)
Cancer Risk Screening · Tumor Diagnosis · Rain Prediction (12 Indian cities)

    pip install -r requirements.txt
    python app.py          # open http://127.0.0.1:5001

Models train automatically on first run (saved in /models). Delete /models to retrain.
Datasets are in /data:
- cancer_diagnosis_wisconsin.csv — real Wisconsin breast-cancer data (from scikit-learn)
- cancer_risk_india.csv — synthetic lifestyle data (tobacco chewing, bidi, pollution, family history)
- weather_india.csv — synthetic monsoon-aware weather data
To use your own data (e.g. from Kaggle), keep the same column names and replace the CSV, then delete /models.
Educational use only — not medical advice.
