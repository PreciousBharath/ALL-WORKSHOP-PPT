"""Creates the datasets for Project 1 (classification)."""
import numpy as np, pandas as pd
from pathlib import Path

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
sig = lambda z: 1 / (1 + np.exp(-z))


def cancer_diagnosis(out):
    """REAL data: Wisconsin Diagnostic Breast Cancer (FNA cytology), bundled inside scikit-learn."""
    from sklearn.datasets import load_breast_cancer
    d = load_breast_cancer(as_frame=True).frame
    cols = {"mean radius": "radius_mean", "mean texture": "texture_mean", "mean perimeter": "perimeter_mean",
            "mean area": "area_mean", "mean smoothness": "smoothness_mean", "mean compactness": "compactness_mean",
            "mean concavity": "concavity_mean", "mean concave points": "concave_points_mean"}
    df = d[list(cols)].rename(columns=cols)
    df["malignant"] = 1 - d["target"]          # sklearn: 0 = malignant -> flip so 1 = malignant
    df.to_csv(out, index=False)


def cancer_risk_india(out, n=6000, seed=7):
    """Synthetic lifestyle screening data reflecting common Indian risk factors (tobacco chewing, bidi, pollution...)."""
    r = np.random.RandomState(seed)
    df = pd.DataFrame({
        "age": r.randint(18, 86, n),
        "gender": r.choice(["Male", "Female"], n),
        "tobacco_chewing": r.choice(["No", "Occasionally", "Daily"], n, p=[.62, .16, .22]),
        "smoking": r.choice(["Never", "Occasional", "Daily (cigarette/bidi)"], n, p=[.66, .12, .22]),
        "alcohol": r.choice(["No", "Occasional", "Regular"], n, p=[.7, .18, .12]),
        "bmi": np.clip(r.normal(24.5, 4.5, n), 15, 42).round(1),
        "family_history": r.choice(["No", "Yes"], n, p=[.88, .12]),
        "fried_processed_food": r.choice(["Low", "Medium", "High"], n, p=[.3, .45, .25]),
        "physical_activity": r.choice(["Low", "Moderate", "High"], n, p=[.4, .4, .2]),
        "area": r.choice(["Urban", "Rural"], n, p=[.55, .45]),
        "air_pollution": r.choice(["Low", "Moderate", "High"], n, p=[.3, .4, .3]),
    })
    m = lambda c, d: df[c].map(d)
    z = (-4.6 + 0.045 * (df.age - 30) + m("tobacco_chewing", {"No": 0, "Occasionally": .9, "Daily": 2.0})
         + m("smoking", {"Never": 0, "Occasional": .5, "Daily (cigarette/bidi)": 1.5})
         + m("alcohol", {"No": 0, "Occasional": .25, "Regular": .9}) + 0.06 * np.maximum(df.bmi - 25, 0)
         + 1.0 * (df.family_history == "Yes") + m("fried_processed_food", {"Low": 0, "Medium": .3, "High": .7})
         + m("physical_activity", {"Low": .4, "Moderate": 0, "High": -.35}) + .2 * (df.area == "Rural")
         + m("air_pollution", {"Low": 0, "Moderate": .3, "High": .65}) + r.normal(0, .4, n))
    df["high_risk"] = (z > np.quantile(z, .74)).astype(int)   # top ~26% by risk score
    df.to_csv(out, index=False)


def weather_india(out, n=9000, seed=11):
    """Synthetic 'will it rain tomorrow?' data for 12 Indian cities with realistic monsoon seasons."""
    r = np.random.RandomState(seed)
    # city: (base temp, base humidity, {month: monsoon intensity 0-1})
    C = {"Mumbai": (28, 70, {6: .8, 7: 1, 8: 1, 9: .8, 10: .3}), "Delhi": (25, 48, {7: .8, 8: .8, 9: .4, 1: .1}),
         "Chennai": (30, 68, {10: .8, 11: 1, 12: .8, 6: .1}), "Bengaluru": (24, 62, {5: .5, 6: .5, 7: .6, 8: .6, 9: .8, 10: .8}),
         "Kolkata": (27, 72, {6: .8, 7: 1, 8: 1, 9: .9, 10: .4}), "Hyderabad": (27, 55, {7: .6, 8: .7, 9: .8, 10: .4}),
         "Pune": (26, 55, {6: .7, 7: .9, 8: .8, 9: .7}), "Jaipur": (27, 42, {7: .6, 8: .7, 9: .3}),
         "Kochi": (28, 78, {5: .5, 6: 1, 7: 1, 8: .8, 9: .6, 10: .6}), "Guwahati": (25, 74, {5: .5, 6: .9, 7: 1, 8: .9, 9: .8}),
         "Lucknow": (26, 52, {7: .8, 8: .8, 9: .5}), "Ahmedabad": (28, 45, {7: .7, 8: .7, 9: .4})}
    rows = []
    for _ in range(n):
        city = r.choice(list(C)); bt, bh, mon = C[city]; mo = r.randint(1, 13); ms = mon.get(mo, 0)
        temp = bt + 7 * np.sin((mo - 4) / 12 * 2 * np.pi) - 4 * ms + r.normal(0, 2)
        hum = np.clip(bh + 28 * ms + r.normal(0, 9), 15, 100)
        cloud = np.clip(25 + 55 * ms + .3 * (hum - 60) + r.normal(0, 15), 0, 100)
        pres = 1010 - 6 * ms + r.normal(0, 3)
        wind = np.clip(r.gamma(3, 4) + 8 * ms, 0, 60)
        rain_today = max(0, r.exponential(2 + 12 * ms) * (r.rand() < .25 + .6 * ms) if True else 0)
        z = (-3.7 + 0.055 * (hum - 60) + 0.028 * (cloud - 50) - 0.12 * (pres - 1008) + 0.06 * min(rain_today, 30)
             + 2.4 * ms + 0.02 * (wind - 15) - 0.03 * (temp - 28) + r.normal(0, .5))
        rows.append([city, MONTHS[mo - 1], round(temp, 1), round(hum, 1), round(pres, 1), round(wind, 1), round(cloud, 1),
                     round(rain_today, 1), int(r.rand() < sig(z))])
    pd.DataFrame(rows, columns=["city", "month", "temp_c", "humidity", "pressure_hpa", "wind_kmph", "cloud_cover",
                                "rain_today_mm", "rain_tomorrow"]).to_csv(out, index=False)


def build_all(folder):
    folder = Path(folder); folder.mkdir(exist_ok=True)
    for name, fn in [("cancer_diagnosis_wisconsin.csv", cancer_diagnosis), ("cancer_risk_india.csv", cancer_risk_india),
                     ("weather_india.csv", weather_india)]:
        if not (folder / name).exists(): fn(folder / name)


if __name__ == "__main__":
    build_all(Path(__file__).parent / "data")
