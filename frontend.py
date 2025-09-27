# streamlit_app.py
import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8000/predict_obesity"

st.set_page_config(page_title="Prediksi Obesitas", layout="wide")

st.title("⚖️ Prediksi Tingkat Obesitas")

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Jenis Kelamin", ["Male", "Female"])
    age = st.number_input("Usia (Tahun)", min_value=1.0, value=25.0)
    height = st.number_input("Tinggi (Meter)", min_value=0.5, value=1.70)
    weight = st.number_input("Berat (Kilogram)", min_value=1.0, value=70.0)
    family_history = st.selectbox("Riwayat Obesitas dalam Keluarga", ["yes", "no"])
    smoke = st.selectbox("Merokok", ["yes", "no"])
    scc = st.selectbox("Memantau Kalori", ["yes", "no"])

with col2:
    favc = st.selectbox("Konsumsi Makanan Berkalori", ["yes", "no"])
    fcvc = st.slider("Konsumsi Sayuran", 1.0, 3.0, 2.0)
    ncp = st.slider("Jumlah Makan per Hari", 1.0, 4.0, 3.0)
    caec = st.selectbox("Makan di Antara Waktu", ["never", "Sometimes", "Frequently", "Always"])
    ch2o = st.slider("Asupan Air (1-3)", 1.0, 3.0, 2.0)
    faf = st.slider("Aktivitas Fisik (0-3)", 0.0, 3.0, 1.0)
    tue = st.slider("Penggunaan Teknologi (0-3)", 0.0, 3.0, 1.0)
    calc = st.selectbox("Konsumsi Alkohol", ["never", "Sometimes", "Frequently", "Always"])
    mtrans = st.selectbox("Moda Transportasi", ["Public_Transportation", "Walking", "Automobile", "Motorbike", "Bike"])

if st.button("Prediksi Tingkat Obesitas"):
    # Normalisasi input sebelum dikirim
    input_data = {
        "Gender": gender.lower().strip(),
        "Age": age,
        "Height": height,
        "Weight": weight,
        "family_history_with_overweight": family_history.lower().strip(),
        "FAVC": favc.lower().strip(),
        "FCVC": fcvc,
        "NCP": ncp,
        "CAEC": caec.lower().strip(),
        "SMOKE": smoke.lower().strip(),
        "CH2O": ch2o,
        "SCC": scc.lower().strip(),
        "FAF": faf,
        "TUE": tue,
        "CALC": calc.lower().strip(),
        "MTRANS": mtrans.lower().strip(),
    }

    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success("Prediksi berhasil!")
            st.subheader(f"Tingkat Obesitas: {result['prediction'].replace('_', ' ')}")
            st.json(result["input_data"])
        else:
            st.error(f"Error: {response.status_code}")
            st.json(response.json())
    except requests.exceptions.ConnectionError:
        st.error("Tidak dapat terhubung ke server FastAPI. Pastikan FastAPI berjalan.")
