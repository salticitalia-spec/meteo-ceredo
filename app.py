import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Meteo Ceredoleso Pro", page_icon="🧗", layout="centered")

# --- 2. FUNZIONI E SANTI ---
def get_weather_icon(code):
    icons = {0: "☀️", 1: "☀️", 2: "⛅", 3: "☁️", 45: "🌫️", 51: "🌧️", 61: "🌧️", 95: "⚡"}
    icon = icons.get(code, "☁️")
    if icon == "☀️": return f'<span class="sun-ani">{icon}</span>'
    if icon == "🌧️": return f'<span class="rain-ani">{icon}</span>'
    return icon

def calcola_percepita(T, rh):
    if T < 21: return T
    return round(0.5 * (T + 61.0 + ((T - 68.0) * 1.2) + (rh * 0.094)), 1)

def get_santo(data_obj):
    santi = {
        "03-15": "S. Zaccaria", "03-16": "S. Eriberto", "03-17": "S. Patrizio", 
        "03-18": "S. Cirillo", "03-19": "S. Giuseppe", "03-20": "S. Claudia", 
        "03-21": "S. Benedetto", "03-22": "S. Lea", "03-23": "S. Turibio"
    }
    return santi.get(data_obj.strftime("%m-%d"), "S. del Giorno")

giorni_ita = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
mesi_ita = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- 3. CSS "TOTAL BLACK" & ANIMAZIONI (Versione Anti-Errore) ---
st.markdown("""
<style>
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000 !important;
    }
    .main-card {
        border: 1px solid #333;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        text-align: center;
        background: #000000 !important;
    }
    .header-text {
        color: #00FFFF !important; font-weight: 100 !important; letter-spacing: 7px;
        text-transform: uppercase; font-size: 26px; text-align: center; margin: 20px 0;
    }
    .status-alert {
        display: inline-block; padding: 8px 15px; border: 1px solid #FFD700;
        border-radius: 5px; color: #FFD700 !important; font-size: 10px;
        font-weight: bold; letter-spacing: 1px; margin-top: 15px; background: transparent !important;
    }
    @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    .sun-ani { display: inline-block; animation: rotate 12s linear infinite; }
    .rain-ani { display: inline-block; animation: pulse
