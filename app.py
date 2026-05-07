from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

# ---------------------------
# City Boost System
# ---------------------------
def city_price_boost(city):
    if city == "Delhi":
        return 1.25
    elif city == "Jaipur":
        return 1.10
    elif city == "Alwar":
        return 0.90
    return 1.0


# ---------------------------
# REAL SOCIETY DATABASE
# ---------------------------
SOCIETY_DB = {

    "Delhi": [
        {"name": "DLF Capital Greens", "base_price": 18000000, "facilities": ["Gym", "Pool", "Metro Nearby"]},
        {"name": "ATS One Hamlet", "base_price": 15000000, "facilities": ["Club House", "Security", "Park"]},
        {"name": "Godrej South Estate", "base_price": 12000000, "facilities": ["Green Area", "Gym", "Security"]},
        {"name": "RWA Dwarka Homes", "base_price": 8500000, "facilities": ["Lift", "Security"]},
        {"name": "Metro View Apartments", "base_price": 7500000, "facilities": ["Parking", "Park"]},
        {"name": "Delhi Heights", "base_price": 9500000, "facilities": ["Gym", "Club House"]},
        {"name": "Sunshine Residency", "base_price": 6500000, "facilities": ["Security", "Garden"]}
    ],

    "Jaipur": [
        {"name": "Mahima Panorama", "base_price": 9000000, "facilities": ["Garden", "Gym", "Security"]},
        {"name": "Ashiana Umang", "base_price": 7000000, "facilities": ["Club House", "Pool", "Park"]},
        {"name": "Manglam Aroma", "base_price": 6000000, "facilities": ["Parking", "Security", "Lift"]},
        {"name": "Royal Greens Jaipur", "base_price": 5000000, "facilities": ["Gym", "Security"]},
        {"name": "Pink City Homes", "base_price": 4500000, "facilities": ["Garden", "Parking"]},
        {"name": "Jaipur Residency", "base_price": 8000000, "facilities": ["Pool", "Club House"]}
    ],

    "Alwar": [
        {"name": "Krish City Heights", "base_price": 4000000, "facilities": ["Park", "Security"]},
        {"name": "Trehan Hill View", "base_price": 3500000, "facilities": ["Gym", "Parking"]},
        {"name": "R Tech Capital Greens Alwar", "base_price": 5000000, "facilities": ["Club House", "Security", "Garden"]},
        {"name": "Alwar Residency", "base_price": 3000000, "facilities": ["Parking", "Security"]},
        {"name": "Hill View Homes", "base_price": 4500000, "facilities": ["Garden", "Lift"]},
        {"name": "Smart City Alwar", "base_price": 5500000, "facilities": ["Gym", "Park"]}
    ]
}

def get_societies(city, predicted_price):

    societies = []

    for s in SOCIETY_DB.get(city, []):

        price = s["base_price"]

        # wider matching
        if price >= predicted_price * 0.5 and price <= predicted_price * 1.8:

            societies.append({
                "name": s["name"],
                "city": city,
                "avg_price": int(price),
                "facilities": s["facilities"]
            })

    # if less than 3 societies found
    if len(societies) < 3:

        for s in SOCIETY_DB.get(city, []):

            exists = any(x["name"] == s["name"] for x in societies)

            if not exists:
                societies.append({
                    "name": s["name"],
                    "city": city,
                    "avg_price": int(s["base_price"]),
                    "facilities": s["facilities"]
                })

            if len(societies) >= 4:
                break

    societies.sort(key=lambda x: x["avg_price"])

    return societies


# ---------------------------
# Routes
# ---------------------------
@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    try:
        city = request.form["city"]

        input_data = {
            "area": float(request.form["area"]),
            "bedrooms": int(request.form["bedrooms"]),
            "bathrooms": int(request.form["bathrooms"]),
            "stories": int(request.form["stories"]),
            "mainroad": request.form["mainroad"],
            "guestroom": request.form["guestroom"],
            "basement": request.form["basement"],
            "hotwaterheating": request.form["hotwaterheating"],
            "airconditioning": request.form["airconditioning"],
            "parking": int(request.form["parking"]),
            "prefarea": request.form["prefarea"],
            "furnishingstatus": request.form["furnishingstatus"]
        }

        df = pd.DataFrame([input_data])
        prediction = model.predict(df)[0]

        # 🔥 FIX 3: clamp unrealistic values
        # Better prediction balancing
        if prediction > 30000000:
            prediction *= 0.45
        elif prediction > 20000000:
            prediction *= 0.60
        elif prediction < 1000000:
            prediction *= 1.5
        societies = get_societies(city, prediction)

        return render_template(
            "index.html",
            prediction_text=f"₹ {int(prediction):,}",
            societies=societies
        )

    except Exception as e:
        return render_template(
            "index.html",
            prediction_text=f"Error: {str(e)}",
            societies=None
        )


if __name__ == "__main__":
    app.run(debug=True)