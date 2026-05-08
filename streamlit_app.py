import streamlit as st
import pickle
import pandas as pd

model = pickle.load(open("model.pkl", "rb"))

st.title("🏠 House Price Predictor")

area = st.number_input("Area", min_value=500, step=1)

bedrooms = st.number_input("Bedrooms", min_value=1, step=1)

bathrooms = st.number_input("Bathrooms", min_value=1, step=1)

stories = st.number_input("Stories", min_value=1, step=1)

parking = st.number_input("Parking", min_value=0, step=1)
mainroad = st.selectbox("Main Road", ["yes", "no"])
guestroom = st.selectbox("Guest Room", ["yes", "no"])
basement = st.selectbox("Basement", ["yes", "no"])
hotwaterheating = st.selectbox("Hot Water Heating", ["yes", "no"])
airconditioning = st.selectbox("Air Conditioning", ["yes", "no"])

prefarea = st.selectbox("Near City Center", ["yes", "no"])

furnishingstatus = st.selectbox(
    "Furnishing",
    ["furnished", "semi-furnished", "unfurnished"]
)

if st.button("Predict Price"):

    input_data = pd.DataFrame([{
        "area": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "stories": stories,
        "mainroad": mainroad,
        "guestroom": guestroom,
        "basement": basement,
        "hotwaterheating": hotwaterheating,
        "airconditioning": airconditioning,
        "parking": parking,
        "prefarea": prefarea,
        "furnishingstatus": furnishingstatus
    }])

    prediction = model.predict(input_data)

    st.success(f"Predicted Price: ₹ {int(prediction[0]):,}")