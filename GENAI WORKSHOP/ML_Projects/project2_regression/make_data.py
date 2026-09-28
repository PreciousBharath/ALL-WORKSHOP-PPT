"""Creates the datasets for Project 2 (regression). Prices are in Rs. LAKH (1 lakh = 1,00,000)."""
import numpy as np, pandas as pd
from pathlib import Path

# model: (brand, ex-showroom price in lakh, body)
CARS = {"Alto K10": ("Maruti Suzuki", 4.5), "Swift": ("Maruti Suzuki", 6.8), "Baleno": ("Maruti Suzuki", 7.6), "Brezza": ("Maruti Suzuki", 9.5),
        "Ertiga": ("Maruti Suzuki", 10.5), "i20": ("Hyundai", 8.5), "Venue": ("Hyundai", 9.8), "Verna": ("Hyundai", 11.5), "Creta": ("Hyundai", 14),
        "Punch": ("Tata", 7.5), "Nexon": ("Tata", 10.5), "Altroz": ("Tata", 8), "Harrier": ("Tata", 18), "Scorpio": ("Mahindra", 14.5),
        "Thar": ("Mahindra", 15.5), "XUV700": ("Mahindra", 19), "Bolero": ("Mahindra", 10), "City": ("Honda", 12.5), "Amaze": ("Honda", 8.2),
        "Glanza": ("Toyota", 8), "Innova Crysta": ("Toyota", 22), "Fortuner": ("Toyota", 40), "Seltos": ("Kia", 13.5), "Sonet": ("Kia", 9.8), "Kwid": ("Renault", 5)}
CAR_CITIES = ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Kochi"]
CITY_ADJ = dict(zip(CAR_CITIES, [1.0, 1.02, 1.03, 1.0, 1.0, 1.01, .96, .97, .95, .98]))

HOUSE_CITIES = {"Mumbai": 22000, "Delhi NCR": 11500, "Bengaluru": 8800, "Hyderabad": 7400, "Pune": 7800, "Chennai": 7300, "Kolkata": 6200,
                "Ahmedabad": 5200, "Kochi": 6300, "Jaipur": 4600, "Lucknow": 4400, "Coimbatore": 5000}   # avg Rs / sq ft


def car_prices(out, n=8000, seed=3):
    r = np.random.RandomState(seed)
    names = list(CARS); rows = []
    for _ in range(n):
        m = r.choice(names); brand, base = CARS[m]; yr = int(r.randint(2009, 2026)); age = 2025 - yr
        km = int(np.clip(r.normal(11000 * max(age, 1) + 3000, 5000 * max(age, .8) ** .6), 500, 300000))
        fuel = r.choice(["Petrol", "Diesel", "CNG"], p=[.55, .33, .12])
        if m in ("Alto K10", "Kwid", "Punch", "Amaze", "Baleno", "Glanza", "Swift") and fuel == "Diesel": fuel = "Petrol"
        if m in ("Fortuner", "Scorpio", "Bolero", "Innova Crysta", "Thar", "XUV700") and fuel == "CNG": fuel = "Diesel"
        trans = r.choice(["Manual", "Automatic"], p=[.72, .28]); owner = r.choice(["First", "Second", "Third", "Fourth & above"], p=[.62, .26, .09, .03])
        city = r.choice(CAR_CITIES)
        p = base * np.exp(-0.105 * age) * np.exp(-0.0000025 * km) * (1.07 if trans == "Automatic" else 1)
        p *= {"Petrol": 1, "Diesel": 1.07 if age < 9 else .93, "CNG": .96}[fuel] * {"First": 1, "Second": .92, "Third": .84, "Fourth & above": .76}[owner] * CITY_ADJ[city]
        p *= np.exp(r.normal(0, .05))
        rows.append([brand, m, yr, km, fuel, trans, owner, city, round(max(p, .35), 2)])
    pd.DataFrame(rows, columns=["brand", "car_model", "year", "km_driven", "fuel", "transmission", "owner", "city", "price_lakh"]).to_csv(out, index=False)


def house_prices(out, n=9000, seed=5):
    r = np.random.RandomState(seed); rows = []
    for _ in range(n):
        city = r.choice(list(HOUSE_CITIES)); bhk = int(r.choice([1, 2, 3, 4, 5], p=[.15, .38, .32, .12, .03]))
        ptype = r.choice(["Apartment", "Builder Floor", "Independent House", "Villa"], p=[.62, .16, .16, .06])
        area = int(np.clip(r.normal(330 + bhk * 380 - (bhk == 1) * 60, 90) * (1.25 if ptype in ("Villa", "Independent House") else 1), 350, 6500))
        bath = int(np.clip(bhk + r.choice([-1, 0, 0, 1]), 1, 6)); age = int(r.randint(0, 31)); floor = int(r.randint(0, 26))
        if ptype != "Apartment": floor = int(r.randint(0, 3))
        furn = r.choice(["Unfurnished", "Semi-furnished", "Furnished"], p=[.35, .45, .2]); park = int(r.choice([0, 1, 2, 3], p=[.2, .5, .25, .05]))
        metro = round(float(np.clip(r.exponential(4), .2, 25)), 1); tier = r.choice(["Prime", "Mid-range", "Suburban"], p=[.2, .45, .35])
        ppsf = HOUSE_CITIES[city] * {"Prime": 1.55, "Mid-range": 1, "Suburban": .68}[tier] * {"Apartment": 1, "Builder Floor": .97, "Independent House": 1.08, "Villa": 1.3}[ptype]
        ppsf *= (1 - .012 * age) * (1 + .004 * min(floor, 20)) * {"Unfurnished": 1, "Semi-furnished": 1.04, "Furnished": 1.1}[furn] * (1.06 - .012 * min(metro, 10))
        price = (area * ppsf + park * 4e5 + bath * 1e5) / 1e5 * np.exp(r.normal(0, .06))
        rows.append([city, tier, ptype, area, bhk, bath, age, floor, furn, park, metro, round(price, 2)])
    pd.DataFrame(rows, columns=["city", "locality_tier", "property_type", "area_sqft", "bhk", "bathrooms", "property_age_yrs", "floor",
                                "furnishing", "parking", "metro_distance_km", "price_lakh"]).to_csv(out, index=False)


def build_all(folder):
    folder = Path(folder); folder.mkdir(exist_ok=True)
    for name, fn in [("car_prices_india.csv", car_prices), ("house_prices_india.csv", house_prices)]:
        if not (folder / name).exists(): fn(folder / name)


if __name__ == "__main__":
    build_all(Path(__file__).parent / "data")
