from make_data import CARS, CAR_CITIES, HOUSE_CITIES

PROJECT = dict(name="Gaadi & Ghar", emoji="🏠", kind="Project 2 · Regression", port=5002,
    a="#ff8a3d", b="#2ec4b6", bg="#140e22", light="#fbf3ec",
    h1a="What is it really", h1b="worth in ₹ today?",
    sub="Two regression models for the Indian market: used-car resale value across popular Maruti, Hyundai, Tata, Mahindra models, and residential property prices in 12 major cities.",
    nav=[("car", "Car Price", "🚗"), ("house", "House Price", "🏠")])

def num(name, label, lo, hi, step, default, unit="", hint=""):
    return dict(name=name, label=label, type="number", min=lo, max=hi, step=step, default=default, unit=unit, hint=hint)
def sel(name, label, options, default, hint=""):
    return dict(name=name, label=label, type="select", options=options, default=default, hint=hint)

DISC = "Estimate from a model trained on simulated Indian market data. Real prices vary with condition, negotiation and locality."

SPECS = {
 "car": dict(title="Used Car Price", icon="🚗", task="reg", csv="car_prices_india.csv", target="price_lakh", what="resale value",
   tagline="Get a fair resale value for popular Indian cars based on age, kilometres, fuel, owner history and city.",
   sweep="year", sweep_title="price vs manufacturing year", emi=dict(dp=20, rate=9.5, years=5), disclaimer=DISC,
   fields=[sel("car_model", "Car model", list(CARS), "Swift"), num("year", "Manufacturing year", 2009, 2025, 1, 2019),
     num("km_driven", "Kilometres driven", 500, 300000, 500, 45000, "km"), sel("fuel", "Fuel type", ["Petrol", "Diesel", "CNG"], "Petrol"),
     sel("transmission", "Transmission", ["Manual", "Automatic"], "Manual"), sel("owner", "Ownership", ["First", "Second", "Third", "Fourth & above"], "First"),
     sel("city", "Registered city", CAR_CITIES, "Bengaluru")],
   sample={"car_model": "Creta", "year": 2021, "km_driven": 32000, "fuel": "Diesel", "transmission": "Automatic", "owner": "First", "city": "Mumbai"}),
 "house": dict(title="House Price", icon="🏠", task="reg", csv="house_prices_india.csv", target="price_lakh", what="market price",
   tagline="Estimate property prices across metro and tier-2 Indian cities from area, BHK, locality, age and metro access.",
   sweep="area_sqft", sweep_title="price vs built-up area", emi=dict(dp=20, rate=8.75, years=20), disclaimer=DISC,
   fields=[sel("city", "City", list(HOUSE_CITIES), "Bengaluru"), sel("locality_tier", "Locality", ["Prime", "Mid-range", "Suburban"], "Mid-range"),
     sel("property_type", "Property type", ["Apartment", "Builder Floor", "Independent House", "Villa"], "Apartment"),
     num("area_sqft", "Built-up area", 350, 6500, 25, 1200, "sq ft"), num("bhk", "Bedrooms (BHK)", 1, 5, 1, 2), num("bathrooms", "Bathrooms", 1, 6, 1, 2),
     num("property_age_yrs", "Property age", 0, 30, 1, 5, "yrs"), num("floor", "Floor", 0, 25, 1, 6),
     sel("furnishing", "Furnishing", ["Unfurnished", "Semi-furnished", "Furnished"], "Semi-furnished"), num("parking", "Car parking", 0, 3, 1, 1),
     num("metro_distance_km", "Distance to metro / rail", 0.2, 25, 0.1, 3, "km")],
   sample={"city": "Mumbai", "locality_tier": "Prime", "property_type": "Apartment", "area_sqft": 950, "bhk": 2, "bathrooms": 2, "property_age_yrs": 3, "floor": 14,
           "furnishing": "Furnished", "parking": 1, "metro_distance_km": 1.2}),
}
