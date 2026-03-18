import streamlit as st
import requests
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Meteo Ceredoleso Pro", page_icon="🎯", layout="centered")

# --- 2. FUNZIONI E SANTI ---
def get_weather_icon(code):
    icons = {0: "☀️", 1: "☀️", 2: "⛅", 3: "☁️", 45: "🌫️", 51: "🌧️", 61: "🌧️", 95: "⚡"}
    return icons.get(code, "☁️")

def get_santo(data_obj):
    santi = {"03-15": "S. Zaccaria", "03-16": "S. Eriberto", "03-17": "S. Patrizio", "03-18": "S. Cirillo", "03-19": "S. Giuseppe", "03-20": "S. Claudia", "03-21": "S. Benedetto"}
    return santi.get(data_obj.strftime("%m-%d"), "S. del Giorno")

giorni_ita = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
mesi_ita = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- 3. CSS (TEMA BLACK + MIRINO) ---
st.markdown("""
<style>
.stApp { background-color:#000000 !important; }
.main-card { border:1px solid #333; border-radius:20px; padding:20px; margin-bottom:15px; text-align:center; background:#000000; }
.header-text { color:#00FFFF; font-weight:100; letter-spacing:7px; text-transform:uppercase; font-size:26px; text-align:center; margin:20px 0; }
.weather-icon { font-size:80px; margin:10px 0; display:inline-block; }

/* MIRINO TATTICO */
.radar-container { position: relative; width: 100%; height: 450px; border-radius: 15px; border: 1px solid #444; overflow: hidden; }
.sniper-crosshair {
    position: absolute; top: 50%; left: 50%; width: 44px; height: 44px;
    border: 1.5px solid #FF0000; border-radius: 50%; transform: translate(-50%, -50%);
    pointer-events: none; z-index: 10;
}
.sniper-crosshair::before { content: ''; position: absolute; top: 50%; left: -15px; width: 74px; height: 1px; background: #FF0000; transform: translateY(-50%); }
.sniper-crosshair::after { content: ''; position: absolute; left: 50%; top: -15px; width: 1px; height: 74px; background: #FF0000; transform: translateX(-50%); }
.sniper-dot { position: absolute; top: 50%; left: 50%; width: 4px; height: 4px; background: #FF0000; border-radius: 50%; transform: translate(-50%, -50%); }
iframe { width: 100%; height: 450px; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 4. DATA FETCHING (DINAMICO DA SORGENTE) ---
@st.cache_data(ttl=600)
def fetch_meteo():
    # Estraiamo temperatura attuale e massime dei prossimi giorni
    url = "https://api.open-meteo.com/v1/forecast?latitude=45.6117&longitude=10.9710&current_weather=true&daily=temperature_2m_max,weathercode&timezone=Europe%2FRome"
    return requests.get(url).json()

data = fetch_meteo()
if not data: st.stop()

now = datetime.now()
curr_temp = data['current_weather']['temperature']
curr_code = data['current_weather']['weathercode']

# --- 5. CARD PRINCIPALE (VALORE SORGENTE) ---
st.markdown('<div class="header-text">Ceredoleso PRO</div>', unsafe_allow_html=True)
st.markdown(f'''
<div class="main-card">
    <div style="font-weight:100; font-size:18px; color:white; letter-spacing:2px;">{giorni_ita[now.weekday()]} {now.day} {mesi_ita[now.month-1]}</div>
    <div style="color:#00FFFF; font-size:11px; margin-top:5px;">✨ {get_santo(now)}</div>
    <div class="weather-icon">{get_weather_icon(curr_code)}</div>
    <div style="font-size:65px; font-weight:bold; color:white; margin-top:-10px;">{curr_temp}°</div>
</div>
''', unsafe_allow_html=True)

# --- 6. RADAR CON MIRINO ---
st.markdown('<div style="color:#00FFFF; font-size:10px; text-align:center; letter-spacing:2px; margin-bottom:10px;">TARGET: CEREDO FALESIA</div>', unsafe_allow_html=True)
radar_url = "https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=10&level=surface&overlay=radar&product=radar&marker=true"
st.markdown(f'''
<div class="radar-container">
    <div class="sniper-crosshair"><div class="sniper-dot"></div></div>
    <iframe src="{radar_url}"></iframe>
</div>
''', unsafe_allow_html=True)

# --- 7. TENDENZA (VALORI SORGENTE DAILY) ---
st.write("")
cols = st.columns(3)
daily_temps = data['daily']['temperature_2m_max']
daily_codes = data['daily']['weathercode']

for i in range(1, 4):
    with cols[i-1]:
        d_f = now + timedelta(days=i)
        temp_val = daily_temps[i]
        code_val = daily_codes[i]
        st.markdown(f'''
        <div class="main-card" style="padding:15px; border-color:#222;">
            <div style="font-size:11px; color:white; font-weight:bold;">{giorni_ita[d_f.weekday()][:3].upper()} {d_f.day}</div>
            <div style="font-size:30px; margin:5px 0;">{get_weather_icon(code_val)}</div>
            <div style="font-size:22px; font-weight:bold; color:white; margin-top:10px;">{temp_val}°</div>
        </div>
        ''', unsafe_allow_html=True)

if st.button("🔄 REFRESH TARGET"):
    st.cache_data.clear()
    st.rerun()
