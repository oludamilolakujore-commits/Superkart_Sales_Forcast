import streamlit as st
import requests
import pandas as pd

# Deployed backend URL (from the
# backend deployment step)
BACKEND_URL = "https://special-guide-vpqvp775v57q3xjv6-7860.app.github.dev/"

st.set_page_config(page_title="SuperKart Sales Predictor", layout="centered")
st.title("SuperKart Sales Forecast")
st.write(
    "Predict the total sales revenue for a product at a given store, "
    "to support inventory and regional sales decisions."
)

st.header("Product & Store Details")

col1, col2 = st.columns(2)

with col1:
    product_weight = st.number_input("Product Weight", min_value=0.0, value=12.5, step=0.1)
    product_sugar_content = st.selectbox(
        "Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"]
    )
    product_allocated_area = st.number_input(
        "Product Allocated Area (fraction of total store display area)",
        min_value=0.0, max_value=1.0, value=0.05, step=0.01
    )
    product_type = st.selectbox(
        "Product Type",
        ["Frozen Foods", "Dairy", "Canned", "Baking Goods", "Health and Hygiene",
         "Snack Foods", "Meat", "Household", "Hard Drinks", "Fruits and Vegetables",
         "Breads", "Soft Drinks", "Breakfast", "Others", "Starchy Foods", "Seafood"]
    )
    product_mrp = st.number_input("Product MRP", min_value=0.0, value=150.0, step=1.0)

with col2:
    store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
    store_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
    store_type = st.selectbox(
        "Store Type",
        ["Food Mart", "Supermarket Type1", "Supermarket Type2", "Departmental Store"]
    )
    store_age = st.number_input("Store Age (years)", min_value=0, value=15, step=1)

if st.button("Predict Sales"):
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": product_allocated_area,
        "Product_Type": product_type,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_city_type,
        "Store_Type": store_type,
        "Store_Age": store_age,
    }

    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Total Sales: ${result['predicted_sales']:, .2f}")
        else:
            st.error(f"Prediction failed: {response.json().get('error', response.text)}")
    except Exception as e:
        st.error(f"Could not reach the prediction API: {e}")

st.divider()
st.header("Batch Prediction (Upload CSV)")
st.write(
    "Upload a CSV with columns: Product_Weight, Product_Sugar_Content, "
    "Product_Allocated_Area, Product_Type, Product_MRP, Store_Size, "
    "Store_Location_City_Type, Store_Type, Store_Age"
)

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    batch_df = pd.read_csv(uploaded_file)
    if st.button("Run Batch Predictions"):
        predictions = []
        for _, row in batch_df.iterrows():
            try:
                resp = requests.post(BACKEND_URL, json=row.to_dict(), timeout=30)
                predictions.append(resp.json().get("predicted_sales") if resp.status_code == 200 else None)
            except Exception:
                predictions.append(None)
        batch_df["Predicted_Sales"] = predictions
        st.dataframe(batch_df)
        st.download_button(
            "Download Results as CSV",
            batch_df.to_csv(index=False),
            "superkart_predictions.csv",
            "text/csv"
        )
