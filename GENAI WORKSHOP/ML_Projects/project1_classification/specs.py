PROJECT = dict(name="Arogya & Mausam", emoji="🩺", kind="Project 1 · Classification", port=5001,
    a="#4cc9f0", b="#ffb703", bg="#0a1024", light="#eef3fc",
    h1a="Health risk & rain,", h1b="predicted in seconds.",
    sub="Two classification models trained for Indian conditions: cancer screening from lifestyle or cytology data, and next-day rain for 12 Indian cities through the monsoon.",
    nav=[("cancer", "Cancer Risk", "🎗️"), ("tumor", "Tumor", "🔬"), ("weather", "Weather", "🌧️")])

def num(name, label, lo, hi, step, default, unit="", hint=""):
    return dict(name=name, label=label, type="number", min=lo, max=hi, step=step, default=default, unit=unit, hint=hint)
def sel(name, label, options, default, hint=""):
    return dict(name=name, label=label, type="select", options=options, default=default, hint=hint)

DISC = "Educational demo only — not medical advice. Consult a qualified doctor."
CITIES = ["Mumbai","Delhi","Chennai","Bengaluru","Kolkata","Hyderabad","Pune","Jaipur","Kochi","Guwahati","Lucknow","Ahmedabad"]
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

SPECS = {
 "cancer": dict(title="Cancer Screening", icon="🎗️", task="clf", csv="cancer_risk_india.csv", target="high_risk",
   tagline="Lifestyle-based risk screening built around tobacco chewing, bidi, pollution and family history common in India.",
   labels=["Lower risk", "Higher risk"], levels=["Low", "Moderate", "High", "Very high"], tone="risk", sweep="age", sweep_title="risk vs age",
   disclaimer=DISC + " This model uses synthetic data and is not a diagnosis.",
   fields=[num("age", "Age", 18, 85, 1, 45, "yrs"), sel("gender", "Gender", ["Male", "Female"], "Male"),
     sel("tobacco_chewing", "Tobacco chewing (gutka / khaini / paan masala)", ["No", "Occasionally", "Daily"], "No"),
     sel("smoking", "Smoking", ["Never", "Occasional", "Daily (cigarette/bidi)"], "Never"),
     sel("alcohol", "Alcohol", ["No", "Occasional", "Regular"], "No"), num("bmi", "BMI", 15, 42, 0.5, 24, "kg/m²"),
     sel("family_history", "Family history of cancer", ["No", "Yes"], "No"),
     sel("fried_processed_food", "Fried / processed food", ["Low", "Medium", "High"], "Medium"),
     sel("physical_activity", "Physical activity", ["Low", "Moderate", "High"], "Moderate"),
     sel("area", "Living area", ["Urban", "Rural"], "Urban"), sel("air_pollution", "Air pollution exposure", ["Low", "Moderate", "High"], "Moderate")],
   sample={"age": 58, "gender": "Male", "tobacco_chewing": "Daily", "smoking": "Daily (cigarette/bidi)", "alcohol": "Regular", "bmi": 29,
           "family_history": "Yes", "fried_processed_food": "High", "physical_activity": "Low", "area": "Rural", "air_pollution": "High"},
   tips={"0": ["Keep up regular exercise and a fibre-rich diet with fruits & vegetables.", "Do yearly check-ups; women 30+ should ask about Pap smear / breast screening.", "Avoid starting tobacco in any form."],
         "1": ["Please consult a doctor or oncologist for proper screening (oral exam, mammography, Pap smear, chest imaging as advised).", "Quitting tobacco/bidi lowers risk quickly — seek a cessation programme.", "Reduce alcohol and fried food; stay active and manage weight."]}),
 "tumor": dict(title="Tumor Diagnosis", icon="🔬", task="clf", csv="cancer_diagnosis_wisconsin.csv", target="malignant",
   tagline="Real Wisconsin breast-cytology data: predict benign vs malignant from measurements of cell nuclei (FNA test).",
   labels=["Benign", "Malignant"], levels=["Very unlikely", "Unlikely", "Likely", "Very likely"], tone="risk", sweep="radius_mean", sweep_title="malignancy vs cell radius",
   disclaimer=DISC + " A biopsy report by a pathologist is the only confirmation.",
   fields=[num("radius_mean", "Mean radius", 7, 28, 0.1, 13.4, "", "Average distance from centre to edge"), num("texture_mean", "Mean texture", 9.5, 40, 0.1, 18.8),
     num("perimeter_mean", "Mean perimeter", 43, 190, 0.5, 86), num("area_mean", "Mean area", 140, 2500, 5, 550),
     num("smoothness_mean", "Mean smoothness", 0.05, 0.17, 0.001, 0.096), num("compactness_mean", "Mean compactness", 0.02, 0.35, 0.001, 0.093),
     num("concavity_mean", "Mean concavity", 0, 0.43, 0.001, 0.062), num("concave_points_mean", "Mean concave points", 0, 0.21, 0.001, 0.034)],
   sample={"radius_mean": 20, "texture_mean": 22, "perimeter_mean": 132, "area_mean": 1300, "smoothness_mean": 0.1, "compactness_mean": 0.17, "concavity_mean": 0.2, "concave_points_mean": 0.11},
   tips={"0": ["Measurements resemble benign samples.", "Continue routine breast self-exam and clinical check-ups.", "Share results with your doctor for confirmation."],
         "1": ["Measurements resemble malignant samples — see an oncologist promptly.", "Ask for a biopsy / histopathology and imaging.", "Government cancer centres and Tata Memorial-network hospitals offer support schemes."]}),
 "weather": dict(title="Rain Prediction", icon="🌧️", task="clf", csv="weather_india.csv", target="rain_tomorrow",
   tagline="Will it rain tomorrow? Tuned for 12 Indian cities with Southwest and Northeast monsoon patterns.",
   labels=["No rain expected", "Rain expected"], levels=["Unlikely", "Possible", "Likely", "Very likely"], tone="rain", sweep="humidity", sweep_title="rain chance vs humidity",
   disclaimer="Model trained on simulated Indian climate data — check IMD (mausam.imd.gov.in) for official forecasts.",
   fields=[sel("city", "City", CITIES, "Chennai"), sel("month", "Month", MONTHS, "Oct"), num("temp_c", "Temperature", 10, 45, 0.5, 29, "°C"),
     num("humidity", "Humidity", 15, 100, 1, 70, "%"), num("pressure_hpa", "Pressure", 990, 1025, 0.5, 1008, "hPa"), num("wind_kmph", "Wind speed", 0, 60, 1, 14, "km/h"),
     num("cloud_cover", "Cloud cover", 0, 100, 1, 50, "%"), num("rain_today_mm", "Rain today", 0, 100, 0.5, 0, "mm")],
   sample={"city": "Mumbai", "month": "Jul", "temp_c": 26, "humidity": 90, "pressure_hpa": 1002, "wind_kmph": 25, "cloud_cover": 92, "rain_today_mm": 22},
   tips={"0": ["Skies look manageable — a light day ahead.", "Good day for outdoor plans and drying clothes."],
         "1": ["Carry an umbrella or raincoat ☔", "Expect waterlogging & slow traffic in low-lying areas.", "Postpone outdoor events if possible; keep phone power-banks charged."]}),
}
