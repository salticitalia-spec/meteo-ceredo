import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Meteo Ceredoleso Pro", page_icon="🧗", layout="centered")

# --- 2. FUNZIONI E SANTI ---
def get_weather_icon(code):
    pioggia_codes = [51, 53, 55, 61, 63, 65, 80, 81, 82]
    icons = {0: "☀️", 1: "☀️", 2: "⛅", 3: "☁️", 45: "🌫️", 51: "🌧️", 61: "🌧️", 95: "⚡"}
    icon = icons.get(code, "☁️")
    
    if code in pioggia_codes:
        return f'<span class="rain-ani" style="color: #FF0000; filter: drop-shadow(0 0 8px #FF0000);">🌧️</span>'
    if icon in ["🌧️", "☁️", "⛅"]:
        return f'<span style="color: #FFFFFF;">{icon}</span>'
    if icon == "☀️":
        return f'<span class="sun-ani">{icon}</span>'
    return icon

def calcola_percepita(T, rh):
    if T < 21: return T
    return round(0.5 * (T + 61.0 + ((T - 68.0) * 1.2) + (rh * 0.094)), 1)

def get_santo(data_obj):
    santi = {"03-15": "S. Zaccaria", "03-16": "S. Eriberto", "03-17": "S. Patrizio", "03-18": "S. Cirillo", "03-19": "S. Giuseppe", "03-20": "S. Claudia", "03-21": "S. Benedetto", "03-22": "S. Lea", "03-23": "S. Turibio"}
    return santi.get(data_obj.strftime("%m-%d"), "S. del Giorno")

giorni_ita = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
mesi_ita = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- 3. CSS AGGIORNATO ---
style_css = "<style>"
style_css += ".stApp, [data-testid='stAppViewContainer'], [data-testid='stHeader'] { background-color: #000000 !important; }"
style_css += ".main-card { border: 1px solid #333; border-radius: 20px; padding: 25px; margin-bottom: 20px; text-align: center; background: #000000 !important; }"
style_css += ".header-text { color: #00FFFF !important; font-weight: 100 !important; letter-spacing: 7px; text-transform: uppercase; font-size: 26px; text-align: center; margin: 20px 0; }"
style_css += "@keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }"
style_css += "@keyframes pulse { 0% { opacity: 1; transform: scale(1); } 50% { opacity: 0.6; transform: scale(1.1); } 100% { opacity: 1; transform: scale(1); } }"
style_css += ".sun-ani { display: inline-block; animation: rotate 12s linear infinite; font-size: 65px; }"
style_css += ".rain-ani { display: inline-block; animation: pulse 1s ease-in-out infinite; font-size: 75px; }"
style_css += ".rain-info-box { background: rgba(255, 0, 0, 0.1); border: 1px solid #FF3311; border-radius: 10px; padding: 10px; margin: 15px 0; color: #FF3311; font-weight: bold; font-size: 16px; letter-spacing:
