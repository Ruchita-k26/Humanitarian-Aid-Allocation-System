from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)
# Load model
regression_model = joblib.load("models/random_forest_tuned_model.pkl")

# Load encoders
country_encoder = joblib.load("encoders/country_encoder.pkl")
admin1_encoder = joblib.load("encoders/admin1_encoder.pkl")
admin2_encoder = joblib.load("encoders/admin2_encoder.pkl")

# Load feature order
regression_features = joblib.load("features/regression_features.pkl")

@app.route("/")
def home():
    return render_template("index.html")

### REGRESSION MODEL

@app.route("/regression")
def regression():
    return render_template("regression.html")

@app.route("/predict_regression", methods=["POST"])
def predict_regression():

    country = request.form["country"]
    admin1 = request.form["admin1"]
    admin2 = request.form["admin2"]

    edu = float(request.form["EDU"])
    shl = float(request.form["SHL"])
    fsc = float(request.form["FSC"])
    nut = float(request.form["NUT"])
    hea = float(request.form["HEA"])
    pro = float(request.form["PRO"])
    wsh = float(request.form["WSH"])

    # Encode categorical variables
    country = country_encoder.transform([country])[0]
    admin1 = admin1_encoder.transform([admin1])[0]
    admin2 = admin2_encoder.transform([admin2])[0]

    # Create input dataframe
    input_df = pd.DataFrame([{
        "Country": country,
        "Admin 1": admin1,
        "Admin 2": admin2,
        "EDU": edu,
        "SHL": shl,
        "FSC": fsc,
        "NUT": nut,
        "HEA": hea,
        "PRO": pro,
        "WSH": wsh
    }])

    # Arrange columns exactly as during training
    input_df = input_df[regression_features]

    prediction = regression_model.predict(input_df)[0]

    return render_template(
    "regression.html",

    prediction=round(prediction, 2),

    country=request.form["country"],
    admin1=request.form["admin1"],
    admin2=request.form["admin2"],

    edu=edu,
    shl=shl,
    fsc=fsc,
    nut=nut,
    hea=hea,
    pro=pro,
    wsh=wsh
)


##========================CLASSIFICATION MODEL================================

classification_model = joblib.load("models/gradient_boosting_classifier.pkl")
classification_features = joblib.load("features/classification_features.pkl")


@app.route("/classification")
def classification():
    return render_template("classification.html")


@app.route("/predict_classification", methods=["POST"])
def predict_classification():

    country = request.form["country"]
    admin1 = request.form["admin1"]
    admin2 = request.form["admin2"]

    edu = float(request.form["EDU"])
    shl = float(request.form["SHL"])
    fsc = float(request.form["FSC"])
    nut = float(request.form["NUT"])
    hea = float(request.form["HEA"])
    pro = float(request.form["PRO"])
    wsh = float(request.form["WSH"])

    # Encode categorical variables
    country = country_encoder.transform([country])[0]
    admin1 = admin1_encoder.transform([admin1])[0]
    admin2 = admin2_encoder.transform([admin2])[0]

    # Create input dataframe
    input_df = pd.DataFrame([[
        country,
        admin1,
        admin2,
        edu,
        shl,
        fsc,
        nut,
        hea,
        pro,
        wsh
    ]], columns=classification_features)

    prediction = classification_model.predict(input_df)[0]

    return render_template(
    "classification.html",

    prediction=int(prediction),

    country=request.form["country"],
    admin1=request.form["admin1"],
    admin2=request.form["admin2"],

    edu=edu,
    shl=shl,
    fsc=fsc,
    nut=nut,
    hea=hea,
    pro=pro,
    wsh=wsh
)
# ================= CLUSTERING MODEL =================

cluster_model = joblib.load("models/kmeans_clustering.pkl")
cluster_scaler = joblib.load("models/cluster_scaler.pkl")
cluster_features = joblib.load("features/cluster_features.pkl")

@app.route("/clustering")
def clustering():
    return render_template("clustering.html")

@app.route("/predict_clustering", methods=["POST"])
def predict_clustering():

    edu = float(request.form["EDU"])
    shl = float(request.form["SHL"])
    fsc = float(request.form["FSC"])
    nut = float(request.form["NUT"])
    hea = float(request.form["HEA"])
    pro = float(request.form["PRO"])
    wsh = float(request.form["WSH"])

    input_df = pd.DataFrame([[
        edu,
        shl,
        fsc,
        nut,
        hea,
        pro,
        wsh
    ]], columns=cluster_features)

    input_scaled = cluster_scaler.transform(input_df)

    cluster = cluster_model.predict(input_scaled)[0]

    cluster_names = {
        0: "Lower Humanitarian Needs",
        1: "Moderate Humanitarian Needs",
        2: "High Humanitarian Needs"
    }

    return render_template(
    "clustering.html",

    cluster=int(cluster),
    cluster_name=cluster_names.get(int(cluster), "Unknown Cluster"),

    edu=edu,
    shl=shl,
    fsc=fsc,
    nut=nut,
    hea=hea,
    pro=pro,
    wsh=wsh
)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)