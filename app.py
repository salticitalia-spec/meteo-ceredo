import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Meteo Ceredoleso Pro", page_icon="🧗", layout="centered")

# --- 2. FUNZIONI E SANTI ---
def get_weather_icon(code, is_main=False):
    pioggia_codes = [51, 53, 55, 61, 63, 65, 80, 81, 82]
    icons = {0: "☀️", 1: "☀️", 2: "⛅", 3: "☁️", 45: "🌫️", 51: "🌧️", 61: "🌧️", 95: "⚡"}
    icon = icons.get(code, "☁️")
    
    # Classe CSS unica per tutte le icone per uniformare la grandezza
    if code in pioggia_codes:
        return f'<span class="weather-icon rain-ani" style="color:#FF0000;filter:drop-shadow(0 0 8px #FF0000);">🌧️</span>'
    if icon in ["🌧️", "☁️", "⛅"]:
        return f'<span class="weather-icon" style="color:#FFFFFF;">{icon}</span>'
    if icon == "☀️":
        return f'<span class="weather-icon sun-ani">{icon}</span>'
    return f'<span class="weather-icon">{icon}</span>'

def get_santo(data_obj):
    santi = {"03-15": "S. Zaccaria", "03-16": "S. Eriberto", "03-17": "S. Patrizio", "03-18": "S. Cirillo", "03-19": "S. Giuseppe", "03-20": "S. Claudia", "03-21": "S. Benedetto", "03-22": "S. Lea", "03-23": "S. Turibio"}
    return santi.get(data_obj.strftime("%m-%d"), "S. del Giorno")

giorni_ita = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
mesi_ita = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- 3. CSS (Icone uniformate a 70px) ---
style_css = "<style>"
style_css += ".stApp, [data-testid='stAppViewContainer'], [data-testid='stHeader'] { background-color:#000000 !important; }"
style_css += ".main-card { border:1px solid #333; border-radius:20px; padding:20px; margin-bottom:15px; text-align:center; background:#000000 !important; }"
style_css += ".header-text { color:#00FFFF !important; font-weight:100 !important; letter-spacing:7px; text-transform:uppercase; font-size:26px; text-align:center; margin:20px 0; }"
style_css += "@keyframes rotate { from { transform:rotate(0deg); } to { transform:rotate(360deg); } }"
style_css += "@keyframes pulse { 0% { opacity:1; transform:scale(1); } 50% { opacity:0.6; transform:scale(1.05); } 100% { opacity:1; transform:scale(1); } }"
style_css += ".weather-icon { display:inline-block; font-size:70px; margin:15px 0; }"
style_css += ".sun-ani { animation:rotate 12s linear infinite; }"
style_css += ".rain-ani { animation:pulse 1s ease-in-out infinite; }"
style_css += ".rain-info-box { border:1px solid #FF3311; border-radius:10px; padding:10px; margin:10px 0; font-weight:bold; font-size:15px; }"
style_css += "</style>"
st.markdown(style_css, unsafe_allow_html=True)

# --- 4. DATA FETCHING ---
@st.cache_data(ttl=600)
def fetch_meteo_data():
    lat, lon = 45.6117, 10.9710
    try:
        url_fc = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,precipitation&daily=temperature_2m_max,precipitation_sum,weathercode&timezone=Europe%2FRome"
        start_hi = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
        end_hi = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        url_hi = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_hi}&end_date={end_hi}&hourly=precipitation,windspeed_10m,shortwave_radiation&timezone=Europe%2FRome"
        return requests.get(url_fc).json(), requests.get(url_hi).json()
    except: return None, None

dfc, dhi = fetch_meteo_data()
if not dfc: st.stop()

# --- 5. LOGICA PRECIPITAZIONI ---
now = datetime.now()
h_times = dfc['hourly']['time']
h_prec = dfc['hourly']['precipitation']
msg_pioggia = "CIELO ASCIUTTO NELLE 24H"
colore_msg = "#00FF00"

if dfc['current_weather']['weathercode'] in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
    msg_pioggia = "⚠️ PIOVE ORA"
    colore_msg = "#FF0000"
else:
    for t, p in zip(h_times, h_prec):
        dt_t = datetime.fromisoformat(t)
        if dt_t > now and p > 0.1:
            ora = dt_t.strftime('%H:00')
            giorno = "OGGI" if dt_t.day == now.day else "DOMANI"
            msg_pioggia = f"🌧️ INIZIO: {giorno} {ora}"
            colore_msg = "#FF3311"
            break

# --- 6. INTERFACCIA PRINCIPALE ---
st.markdown('<div class="header-text">Ceredoleso PRO</div>', unsafe_allow_html=True)
curr = dfc['current_weather']
c_temp, c_hum = curr['temperature'], dfc['hourly']['relativehumidity_2m'][now.hour]

st.markdown(f'''
<div class="main-card">
    <div style="font-weight:100; font-size:20px; color:white; letter-spacing:3px; text-transform:uppercase;">
        {giorni_ita[now.weekday()]} {now.day} {mesi_ita[now.month-1]}
    </div>
    <div style="color:#00FFFF; font-size:11px; margin-top:5px;">✨ {get_santo(now)}</div>
    <div>{get_weather_icon(curr['weathercode'])}</div>
    <div class="rain-info-box" style="color:{colore_msg}; border-color:{colore_msg};">
        {msg_pioggia}
    </div>
    <div style="font-size:55px; font-weight:bold; color:white;">{c_temp}°</div>
    <div style="display:flex; justify-content:center; gap:25px; margin-top:15px; color:#00FF00; font-weight:bold; font-size:14px;">
        <span>💨 {curr['windspeed']} kph</span>
        <span style="color:#FFFF00;">💧 {c_hum}%</span>
    </div>
</div>
''', unsafe_allow_html=True)

# --- 7. MOSTRO BOVINO ---
if dhi and 'hourly' in dhi:
    carico = sum(dhi['hourly']['precipitation'][-168:]) 
    if carico < 5: m_t, m_c, m_d = "SECCO ☀️", "#00FFFF", "🟢 Ottimo ovunque"
    elif carico < 18: m_t, m_c, m_d = "UMIDO 💧", "#FFFF00", "🟡 Peci & Ostramandra umide"
    else: m_t, m_c, m_d = "BAGNATO ⚠️", "#FF3311", "🔴 Bosco saturo"
    
    st.markdown(f'''
    <div style="border:1px solid {m_c}; padding:15px; border-radius:15px; text-align:center; background:black; margin-bottom:20px;">
        <div style="font-size:9px; color:#666; letter-spacing:2px;">MOSTRO BOVINO INDEX</div>
        <div style="font-size:22px; color:{m_c}; font-weight:bold; margin:3px 0;">{m_t}</div>
        <div style="font-size:12px; color:#999;">{m_d}</div>
    </div>
    ''', unsafe_allow_html=True)

# --- 8. TENDENZA (Uniformata) ---
cols = st.columns(3)
for i in range(1, 4):
    with cols[i-1]:
        d_f = now + timedelta(days=i)
        st.markdown(f'''
        <div class="main-card" style="padding:15px; border-color:#222;">
            <div style="font-size:11px; color:white; font-weight:bold;">{giorni_ita[d_f.weekday()][:3].upper()} {d_f.day}</div>
            <div>{get_weather_icon(dfc['daily']['weathercode'][i])}</div>
            <div style="font-size:22px; font-weight:bold; color:white;">{dfc['daily']['temperature_2m_max'][i]}°</div>
        </div>
        ''', unsafe_allow_html=True)

if st.button("🔄 AGGIORNA"):
    st.cache_data.clear()
    st.rerun()
