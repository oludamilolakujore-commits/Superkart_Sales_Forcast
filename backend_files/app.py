from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load the serialized pipeline (preprocessing + trained model) once at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "superkart_sales_model.joblib")
model = joblib.load(MODEL_PATH)

# The exact feature columns the pipeline expects, in the same form as X_train
FEATURE_COLUMNS = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_Type",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Store_Age",
]


@app.route("/", methods=["GET"])
def health_check():
    """Simple health check endpoint so the Space shows as live."""
    return jsonify({"status": "ok", "message": "SuperKart Sales Prediction API is running."})


@app.route("/predict", methods=["POST"])
def predict():
    """
    Expects a JSON body with the fields listed in FEATURE_COLUMNS, e.g.:
    {
        "Product_Weight": 12.5,
        "Product_Sugar_Content": "Low Sugar",
        "Product_Allocated_Area": 0.05,
        "Product_Type": "Snack Foods",
        "Product_MRP": 150.0,
        "Store_Size": "Medium",
        "Store_Location_City_Type": "Tier 2",
        "Store_Type": "Supermarket Type1",
        "Store_Age": 15
    }
    Returns the predicted Product_Store_Sales_Total.
    """
    try:
        payload = request.get_json(force=True)

        missing = [col for col in FEATURE_COLUMNS if col not in payload]
        if missing:
            return jsonify({"error": f"Missing required fields: {missing}"}), 400

        input_df = pd.DataFrame([{col: payload[col] for col in FEATURE_COLUMNS}])
        prediction = model.predict(input_df)[0]

        return jsonify({"predicted_sales": round(float(prediction), 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Hugging Face Docker Spaces expect the app to listen on port 7860
    app.run(host="0.0.0.0", port=7860)
