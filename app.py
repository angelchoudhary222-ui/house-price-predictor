from flask import Flask, render_template, request
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def home():
    return render_template("index.html", prediction_text=None)


@app.route('/predict', methods=['POST'])
def predict():

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

    prediction = model.predict(df)

    # ---------------- GRAPH ----------------
    os.makedirs("static", exist_ok=True)

    features = ["area", "bedrooms", "bathrooms", "stories", "parking"]

    values_norm = np.array([
        input_data["area"] / 10000,
        input_data["bedrooms"] / 10,
        input_data["bathrooms"] / 10,
        input_data["stories"] / 5,
        input_data["parking"] / 5
    ])

    plt.figure(figsize=(10, 5))

    # -------- LEFT GRAPH --------
    plt.subplot(1, 2, 1)
    bars1 = plt.bar(features, values_norm)
    plt.title("Input Features (Balanced Scale)")
    plt.xticks(rotation=30)
    plt.ylim(0, 1.1)

    for bar in bars1:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{height:.2f}',
            ha='center',
            va='bottom'
        )

    # -------- RIGHT GRAPH --------
    plt.subplot(1, 2, 2)

    importance = None

    try:
        importance = abs(model.named_steps['model'].coef_)
    except:
        try:
            importance = abs(model.coef_)
        except:
            try:
                importance = model.feature_importances_
            except:
                importance = None

    if importance is not None:
        importance = importance[:len(features)]
        importance = importance / (importance.max() + 1e-6)

        bars2 = plt.bar(features, importance)
        plt.title("Feature Impact (Relative)")
        plt.xticks(rotation=30)
        plt.ylim(0, 1.1)

        for bar in bars2:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{height:.2f}',
                ha='center',
                va='bottom'
            )
    else:
        plt.text(0.5, 0.5, "Importance not available", ha='center')

    plt.tight_layout()

    graph_path = os.path.join("static", "graph.png")
    plt.savefig(graph_path)
    plt.close()

    return render_template(
        "index.html",
        prediction_text=f"Predicted Price: ₹ {int(prediction[0]):,}",
        graph_url="graph.png"
    )


if __name__ == "__main__":
    app.run(debug=True)