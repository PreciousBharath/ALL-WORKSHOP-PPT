# Gaadi & Ghar — Project 2 (Regression)
Used Car Price · House Price (prices in ₹ lakh) with EMI planner

    pip install -r requirements.txt
    python app.py          # open http://127.0.0.1:5002

Models train automatically on first run (saved in /models). Delete /models to retrain.
Datasets are in /data (synthetic, modelled on Indian market patterns):
- car_prices_india.csv
- house_prices_india.csv
To use real data (e.g. CarDekho / Housing.com from Kaggle), keep the same column names and replace the CSV, then delete /models.
