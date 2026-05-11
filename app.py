from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

# ---------------------------
# REAL SOCIETY DATABASE
# ---------------------------
SOCIETY_DB = {

    "Delhi": [

        {
            "name": "DLF Capital Greens",
            "base_price": 18000000,
            "facilities": ["Gym", "Pool", "Metro Nearby"],
            "search": "Moti Nagar New Delhi"
        },

        {
            "name": "ATS One Hamlet",
            "base_price": 15000000,
            "facilities": ["Club House", "Security", "Park"],
            "search": "Sector 104 Noida"
        },

        {
            "name": "Godrej South Estate",
            "base_price": 12000000,
            "facilities": ["Green Area", "Gym", "Security"],
            "search": "Okhla Delhi"
        },

        {
            "name": "DLF New Town Heights",
            "base_price": 9500000,
            "facilities": ["Gym", "Club House"],
            "search": "Sector 90 Gurgaon"
        }
    ],

    "Jaipur": [

        {
            "name": "Mahima Panorama",
            "base_price": 9000000,
            "facilities": ["Garden", "Gym", "Security"],
            "search": "Jagatpura Jaipur"
        },

        {
            "name": "Ashiana Umang",
            "base_price": 7000000,
            "facilities": ["Club House", "Pool", "Park"],
            "search": "Tonk Road Jaipur"
        },

        {
            "name": "Manglam Aroma",
            "base_price": 6000000,
            "facilities": ["Parking", "Security", "Lift"],
            "search": "Mansarovar Jaipur"
        },

        {
            "name": "Okay Plus Emerald",
            "base_price": 5000000,
            "facilities": ["Gym", "Security"],
            "search": "Ajmer Road Jaipur"
        }
    ],

    "Alwar": [

        {
            "name": "Ashiana Town",
            "base_price": 3500000,
            "facilities": ["Gym", "Parking"],
            "address": "Sector 39, Bhiwadi, Rajasthan",
            "lat": "28.2105",
            "lon": "76.8606"
        },

        {
            "name": "Terra Heritage",
            "base_price": 5000000,
            "facilities": ["Club House", "Security", "Garden"],
            "address": "Neemrana, Rajasthan",
            "lat": "27.9882",
            "lon": "76.3844"
        },

        {
            "name": "Krish Vatika",
            "base_price": 4000000,
            "facilities": ["Park", "Security"],
            "address": "Alwar, Rajasthan",
            "lat": "27.5529",
            "lon": "76.6346"
        },

        {
            "name": "Trehan Delight Residence",
            "base_price": 4500000,
            "facilities": ["Garden", "Lift"],
            "address": "Bhiwadi, Rajasthan",
            "lat": "28.2100",
            "lon": "76.8600"
        }
    ]
}

# ---------------------------
# GET ADDRESS + MAP LINK
# ---------------------------
def get_address(search_query):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": search_query,
        "format": "json",
        "addressdetails": 1,
        "limit": 3
    }

    headers = {
        "User-Agent": "house-price-app"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=5
        )

        data = response.json()

        print("SEARCH:", search_query)
        print("DATA:", data)

        if data and len(data) > 0:
            place = max(
                data,
                key=lambda x: len(x.get("display_name", ""))
            )

            address = place.get(
                "display_name",
                "Address unavailable"
            )

            lat = place.get("lat")
            lon = place.get("lon")

            map_link = (
                f"https://www.openstreetmap.org/"
                f"?mlat={lat}&mlon={lon}"
                f"#map=16/{lat}/{lon}"
            )

            return {
                "address": address,
                "map_link": map_link
            }

        return {
            "address": "Location unavailable",
            "map_link": "#"
        }

    except Exception as e:

        print("ERROR:", e)

        return {
            "address": "Address unavailable",
            "map_link": "#"
        }


# ---------------------------
# GET SOCIETIES
# ---------------------------
# ---------------------------
# GET SOCIETIES
# ---------------------------
# ---------------------------
# GET SOCIETIES
# ---------------------------
def get_societies(city, predicted_price):

    societies = []

    city_societies = SOCIETY_DB.get(city, [])

    min_price = predicted_price * 0.45
    max_price = predicted_price * 1.80

    for s in city_societies:

        price = s["base_price"]

        if min_price <= price <= max_price:

            # ---------------------------
            # DELHI + JAIPUR
            # ---------------------------
            if "search" in s:

                location_data = get_address(s["search"])

            # ---------------------------
            # ALWAR
            # ---------------------------
            else:

                location_data = {
                    "address": s["address"],
                    "map_link":
                        f"https://www.openstreetmap.org/"
                        f"?mlat={s['lat']}&mlon={s['lon']}"
                        f"#map=16/{s['lat']}/{s['lon']}"
                }

            # ---------------------------
            # DIFFERENT SCHOOLS/HOSPITALS
            # ---------------------------

            society_name = s["name"]

            # DELHI
            if society_name == "DLF Capital Greens":

                schools = [
                    "Bal Bharati Public School",
                    "SD Public School",
                    "Cambridge Foundation School"
                ]

                hospitals = [
                    "BLK Max Hospital",
                    "Apollo Cradle",
                    "MGS Hospital"
                ]


            elif society_name == "ATS One Hamlet":

                schools = [
                    "Delhi Public School Noida",
                    "Pathways School",
                    "Lotus Valley School"
                ]

                hospitals = [
                    "Jaypee Hospital",
                    "Yatharth Hospital",
                    "Felix Hospital"
                ]


            elif society_name == "Godrej South Estate":

                schools = [
                    "Cambridge School",
                    "DAV Public School",
                    "St. George School"
                ]

                hospitals = [
                    "Holy Family Hospital",
                    "Fortis Escorts",
                    "Max Saket"
                ]


            elif society_name == "DLF New Town Heights":

                schools = [
                    "RPS International School",
                    "Delhi Public School Gurgaon",
                    "St. Xavier School"
                ]

                hospitals = [
                    "Medanta Hospital",
                    "Artemis Hospital",
                    "Park Hospital"
                ]


            # JAIPUR
            elif society_name == "Mahima Panorama":

                schools = [
                    "Jayshree Periwal School",
                    "Seedling Public School",
                    "Cambridge Court School"
                ]

                hospitals = [
                    "Fortis Jaipur",
                    "EHCC Hospital",
                    "Narayana Hospital"
                ]


            elif society_name == "Ashiana Umang":

                schools = [
                    "India International School",
                    "Ryan International School",
                    "Saint Soldier School"
                ]

                hospitals = [
                    "Manipal Hospital",
                    "Apex Hospital",
                    "CKS Hospital"
                ]


            elif society_name == "Manglam Aroma":

                schools = [
                    "Tagore Public School",
                    "Neerja Modi School",
                    "MPS School"
                ]

                hospitals = [
                    "SMS Hospital",
                    "Shalby Hospital",
                    "Bhandari Hospital"
                ]


            elif society_name == "Okay Plus Emerald":

                schools = [
                    "Delhi Public School Jaipur",
                    "Kids Paradise School",
                    "Sanskar School"
                ]

                hospitals = [
                    "Metro Hospital",
                    "Mahatma Gandhi Hospital",
                    "Jyoti Nursing Home"
                ]


            # ALWAR
            elif society_name == "Ashiana Town":

                schools = [
                    "RPS Public School",
                    "St. Xavier School",
                    "Modern Public School"
                ]

                hospitals = [
                    "Apex Hospital",
                    "Medicare Hospital",
                    "Om Hospital"
                ]


            elif society_name == "Terra Heritage":

                schools = [
                    "Neemrana Public School",
                    "Cambridge School",
                    "Prince Academy"
                ]

                hospitals = [
                    "Mittal Hospital",
                    "Soni Hospital",
                    "Life Care Hospital"
                ]


            elif society_name == "Krish Vatika":

                schools = [
                    "Happy Public School",
                    "Central Academy",
                    "Lords International"
                ]

                hospitals = [
                    "Vivekanand Hospital",
                    "Rajiv Gandhi Hospital",
                    "City Hospital"
                ]


            elif society_name == "Trehan Delight Residence":

                schools = [
                    "Bhiwadi Public School",
                    "Presidium School",
                    "Starex School"
                ]

                hospitals = [
                    "Kalyani Hospital",
                    "Astha Hospital",
                    "Genesis Hospital"
                ]

            else:

                schools = ["Nearby School"]

                hospitals = ["Nearby Hospital"]

            societies.append({

                "name": s["name"],
                "city": city,
                "avg_price": int(price),
                "facilities": s["facilities"],
                "address": location_data["address"],
                "map_link": location_data["map_link"],

                # Society image
                "image":
                    f"https://picsum.photos/400/250?random={s['name']}",

                # Nearby places
                "schools": schools,
                "hospitals": hospitals
            })

    # ---------------------------
    # FALLBACK
    # ---------------------------
    if len(societies) < 4:

        for s in city_societies:

            already_added = any(
                x["name"] == s["name"]
                for x in societies
            )

            if not already_added:

                if "search" in s:

                    location_data = get_address(s["search"])

                else:

                    location_data = {
                        "address": s["address"],
                        "map_link":
                            f"https://www.openstreetmap.org/"
                            f"?mlat={s['lat']}&mlon={s['lon']}"
                            f"#map=16/{s['lat']}/{s['lon']}"
                    }

                if city == "Delhi":

                    schools = [
                        "Delhi Public School",
                        "Modern School",
                        "Bal Bharati School"
                    ]

                    hospitals = [
                        "AIIMS Delhi",
                        "Max Hospital",
                        "Fortis Hospital"
                    ]

                elif city == "Jaipur":

                    schools = [
                        "Ryan International School",
                        "St. Xavier School",
                        "Delhi Public School Jaipur"
                    ]

                    hospitals = [
                        "EHCC Hospital",
                        "Fortis Jaipur",
                        "SMS Hospital"
                    ]

                else:

                    schools = [
                        "St. Xavier School Bhiwadi",
                        "Modern Public School",
                        "RPS Public School"
                    ]

                    hospitals = [
                        "Medicare Hospital",
                        "Apex Hospital",
                        "Mittal Hospital"
                    ]

                societies.append({

                    "name": s["name"],
                    "city": city,
                    "avg_price": int(s["base_price"]),
                    "facilities": s["facilities"],
                    "address": location_data["address"],
                    "map_link": location_data["map_link"],

                    "image":
                        f"https://picsum.photos/400/250?random={s['name']}",

                    "schools": schools,
                    "hospitals": hospitals
                })

            if len(societies) >= 4:
                break

    societies.sort(key=lambda x: x["avg_price"])

    return societies

# ---------------------------
# ROUTES
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

        # ---------------------------
        # BALANCE PREDICTION
        # ---------------------------
        if prediction > 30000000:
            prediction *= 0.45

        elif prediction > 20000000:
            prediction *= 0.60

        elif prediction > 12000000:
            prediction *= 0.75

        elif prediction < 1000000:
            prediction *= 1.5

        prediction = int(prediction)

        societies = get_societies(city, prediction)

        return render_template(
            "index.html",
            prediction_text=f"₹ {prediction:,}",
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