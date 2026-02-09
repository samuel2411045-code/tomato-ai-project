from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import streamlit as st
from PIL import Image

from disease_model import predict_leaf_disease
from fertilizer_logic import SoilCard, recommend_fertilizer
from weather import fetch_open_meteo_daily, get_location_from_ip
from yield_model import predict_yield
from ocr_utils import extract_soil_values


TOMATO_VARIETIES = [
    "Desi / Heirloom",
    "Vaishali",
    "Rupali",
    "Pusa Ruby",
    "Arka Vikas",
    "Cherry",
    "Beefsteak",
    "Roma",
]


def _season_one_hot(season: str) -> dict[str, float]:
    season = season.lower().strip()
    return {
        "season_kharif": 1.0 if season == "kharif" else 0.0,
        "season_rabi": 1.0 if season == "rabi" else 0.0,
        "season_summer": 1.0 if season == "summer" else 0.0,
    }


st.set_page_config(page_title="Tomato AI Guidance System", layout="wide")

# Custom Theme: Green + White
st.markdown("""
<style>
    .stApp {
        background-color: #ffffff;
        color: #1a4d2e;
    }
    .stButton>button {
        background-color: #4f7942;
        color: white;
        border-radius: 8px;
    }
    .stSelectbox, .stNumberInput, .stSlider {
        color: #1a4d2e;
    }
    h1, h2, h3 {
        color: #1a4d2e !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0fdf4;
        border-radius: 4px 4px 0px 0px;
        color: #1a4d2e;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4f7942 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌿 Tomato AI Guidance System")
st.caption("Leaf disease • Yield estimate • Fertilizer & bio-fertilizer recommendation")

tab1, tab2, tab3 = st.tabs(["🔍 Disease Detection", "🌾 Yield Prediction", "🧪 Fertilizer Recommendation"])


with tab1:
    st.subheader("Tomato Leaf Disease Prediction")
    col_l, col_r = st.columns([1, 1])

    with col_l:
        uploaded = st.file_uploader("Upload a tomato leaf image (JPG/PNG)", type=["jpg", "jpeg", "png"])
        model_choice = st.radio("Select Model Architecture", ["CNN", "ViT", "Compare Both"], index=0, horizontal=True)

    with col_r:
        st.info("Tip: For best results, use a close-up image of a single leaf with good lighting.")

    if uploaded is not None:
        img = Image.open(uploaded).convert("RGB")
        st.image(img, caption="Uploaded leaf", use_container_width=True)
        image_rgb = np.array(img)

        results = []
        if model_choice in ["CNN", "Compare Both"]:
            results.append(predict_leaf_disease(image_rgb=image_rgb, model_path="models/disease_model.h5", model_type="CNN"))
        if model_choice in ["ViT", "Compare Both"]:
            results.append(predict_leaf_disease(image_rgb=image_rgb, model_path="models/disease_vit_model.h5", model_type="ViT"))

        for res in results:
            with st.expander(f"**Results: {res.model_type} Model**", expanded=True):
                st.markdown(f"**Prediction:** {res.label}")
                st.progress(min(max(res.confidence, 0.0), 1.0))
                st.markdown(f"**Confidence:** {res.confidence:.2f}")
                st.markdown(f"**Suggested action:** {res.remedy}")
    else:
        st.warning("Upload an image to run disease prediction.")


with tab2:
    st.subheader("Yield Prediction (Season + Open‑Meteo Weather + Soil)")
    col_a, col_b, col_c = st.columns([1, 1, 1])

    with col_a:
        season = st.selectbox("Season", ["Kharif", "Rabi", "Summer"], index=0)
        variety = st.selectbox("Tomato variety", TOMATO_VARIETIES, index=0)
        st.caption("Variety is collected for UI completeness; add it as a feature when you train a model.")

    with col_b:
        st.markdown("**Location Detection**")
        if st.button("📍 Detect My Location"):
            loc = get_location_from_ip()
            if loc:
                st.session_state.lat = loc[0]
                st.session_state.lon = loc[1]
                st.success(f"Located: {loc[0]:.4f}, {loc[1]:.4f}")
            else:
                st.error("Could not detect location automatically.")

        latitude = st.number_input("Latitude", value=st.session_state.get("lat", 19.0760), format="%.6f")
        longitude = st.number_input("Longitude", value=st.session_state.get("lon", 72.8777), format="%.6f")
        days = st.slider("Weather window (days)", min_value=3, max_value=14, value=7)

    with col_c:
        n = st.number_input("Soil Nitrogen (N)", min_value=0.0, value=200.0, step=1.0)
        p = st.number_input("Soil Phosphorus (P)", min_value=0.0, value=15.0, step=1.0)
        k = st.number_input("Soil Potassium (K)", min_value=0.0, value=200.0, step=1.0)
        ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.8, step=0.1)
        oc = st.number_input("Organic Carbon (%)", min_value=0.0, value=0.7, step=0.1)

    run = st.button("Predict yield", type="primary")

    if run:
        end = date.today()
        start = end - timedelta(days=int(days))

        with st.spinner("Fetching weather from Open‑Meteo..."):
            try:
                w = fetch_open_meteo_daily(latitude=float(latitude), longitude=float(longitude), start=start, end=end)
            except Exception as e:
                st.error(f"Weather fetch failed: {e}")
                st.stop()

        st.success("Weather fetched.")
        st.write(
            {
                "temp_mean_c": w.tmean_c,
                "temp_min_c": w.tmin_c,
                "temp_max_c": w.tmax_c,
                "rainfall_mm": w.rainfall_mm,
            }
        )

        features = {
            "temp_mean_c": float(w.tmean_c),
            "rainfall_mm": float(w.rainfall_mm),
            "soil_n": float(n),
            "soil_p": float(p),
            "soil_k": float(k),
            "soil_ph": float(ph),
            "organic_carbon": float(oc),
        }
        features.update(_season_one_hot(season))

        pred = predict_yield(features=features, output="bucket")
        st.markdown(f"**Yield category:** {pred.label}")
        if pred.value is not None:
            st.caption(f"Underlying value: {pred.value:.2f} {pred.units or ''}".strip())
        if pred.note:
            st.info(pred.note)


with tab3:
    st.subheader("Fertilizer & Bio-fertilizer Recommendation")
    st.caption("Upload your Soil Health Card OR enter values directly.")

    soil_uploaded = st.file_uploader("Upload Soil Health Card (OCR)", type=["jpg", "jpeg", "png"])
    
    # Initialize values from OCR or Defaults
    ocr_data = None
    if soil_uploaded:
        with st.spinner("Extracting data from Soil Health Card..."):
            ocr_data = extract_soil_values(Image.open(soil_uploaded))
            st.success("Data extracted! Please verify values below.")

    col1, col2 = st.columns([1, 1])
    with col1:
        n_val = ocr_data.n if ocr_data else 200.0
        p_val = ocr_data.p if ocr_data else 15.0
        k_val = ocr_data.k if ocr_data else 200.0
        
        n = st.number_input("Nitrogen (N)", min_value=0.0, value=n_val, step=1.0, key="fert_n")
        p = st.number_input("Phosphorus (P)", min_value=0.0, value=p_val, step=1.0, key="fert_p")
        k = st.number_input("Potassium (K)", min_value=0.0, value=k_val, step=1.0, key="fert_k")
    with col2:
        ph_val = ocr_data.ph if ocr_data else 6.8
        oc_val = ocr_data.organic_carbon if ocr_data else 0.7
        
        ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=ph_val, step=0.1, key="fert_ph")
        oc = st.number_input("Organic Carbon (%)", min_value=0.0, value=oc_val, step=0.1, key="fert_oc")

    if st.button("Get recommendation", type="primary"):
        rec = recommend_fertilizer(SoilCard(n=float(n), p=float(p), k=float(k), ph=float(ph), organic_carbon=float(oc)))
        st.markdown(f"**Soil summary:** {rec.summary}")

        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            st.markdown("**Chemical fertilizers**")
            if rec.chemical:
                for x in rec.chemical:
                    st.write(f"- {x}")
            else:
                st.write("No chemical fertilizer suggestions based on current rules.")
        with c2:
            st.markdown("**Bio-fertilizers / microbes**")
            for x in rec.bio:
                st.write(f"- {x}")
        with c3:
            st.markdown("**Organic recommendations**")
            if rec.organic:
                for x in rec.organic:
                    st.write(f"- {x}")
            else:
                st.write("Maintain current organic matter inputs.")

        if rec.notes:
            st.markdown("**Notes**")
            for n_ in rec.notes:
                st.write(f"- {n_}")

