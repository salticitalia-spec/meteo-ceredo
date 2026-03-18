import streamlit as st
import requests
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="Ceredoleso Sniper Radar", page_icon="🎯", layout="centered")

# --- 2. CSS (TEMA BLACK + MIRINO + RADAR ANIMATO) ---
st.markdown("""
<style>
.stApp { background-color:#000000 !important; }
.main-card { border:1px solid #333; border-radius:20px; padding:20px; margin-bottom:15px; text-align:center; background:#000000; }
.header-text { color:#00FFFF; font-weight:100; letter-spacing:7px; text-transform:uppercase; font-size:26px; text-align:center; margin:20px 0; }

/* MIRINO TATTICO */
.radar-container { position: relative; width: 100%; height: 500px; border-radius: 15px; border: 2px solid #444; overflow: hidden; }
.sniper-crosshair {
    position: absolute; top: 50%; left: 50%; width: 50px; height: 50px;
    border: 2px solid #FF0000; border-radius: 50%; transform: translate(-50%, -50%);
    pointer-events: none; z-index: 10;
}
.sniper-crosshair::before { content: ''; position: absolute; top: 50%; left: -20px; width: 90px; height: 1px; background: #FF0000; transform: translateY(-50%); }
.sniper-crosshair::after { content: ''; position: absolute; left: 50%; top: -20px; width: 1px; height: 90px; background: #FF0000; transform: translateX(-50%); }
.sniper-dot { position: absolute; top: 50%; left: 50%; width: 6px; height: 6px; background: #FF0000; border-radius: 50%; transform: translate(-50%, -50%); box-shadow: 0 0 10px #FF0000; }

iframe { width: 100%; height: 500px; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA FETCHING (OPEN-METEO PER INFO CARD) ---
@st.cache_data(ttl=600)
def get_current_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=45.6117&longitude=10.9710&current_weather=true&timezone=Europe%2FRome"
    return requests.get(url).json()

data = get_current_data()
temp = data['current_weather']['temperature']

# --- 4. HEADER ---
st.markdown('<div class="header-text">Ceredoleso PRO</div>', unsafe_allow_html=True)

# --- 5. RADAR PREDITTIVO A 6 ORE ---
st.markdown('<div style="color:#FF0000; font-size:12px; text-align:center; letter-spacing:3px; margin-bottom:10px; font-weight:bold;">PREDICTIVE RADAR SCAN (+6H)</div>', unsafe_allow_html=True)

# URL Windy configurato per Radar (overlay=radar) con proiezione futura abilitata
# Lat/Lon di Ceredo: 45.6117, 10.9710
radar_predittivo = "https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&level=surface&overlay=radar&product=radar&menu=&message=true&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"

st.markdown(f'''
<div class="radar-container">
    <div class="sniper-crosshair"><div class="sniper-dot"></div></div>
    <iframe src="{radar_predittivo}"></iframe>
</div>
''', unsafe_allow_html=True)

st.markdown('<div style="color:#666; font-size:10px; text-align:center; margin-top:5px;">Usa la barra temporale in basso nel radar per scorrere le prossime 6 ore.</div>', unsafe_allow_html=True)

# --- 6. INFO CARD ---
st.write("")
cols = st.columns([1, 2, 1])
with cols[1]:
    st.markdown(f'''
    <div class="main-card">
        <div style="font-size:14px; color:#00FFFF; letter-spacing:2px;">TEMP ATTUALE</div>
        <div style="font-size:50px; font-weight:bold; color:white;">{temp}°</div>
        <div style="font-size:10px; color:#444;">TARGET LOCKED: 45.61°N 10.97°E</div>
    </div>
    ''', unsafe_allow_html=True)

# --- 7. TENDENZA RAPIDA ---
st.write("")
t_cols = st.columns(3)
for i in range(1, 4):
    with t_cols[i-1]:
        d = datetime.now() + timedelta(days=i)
        st.markdown(f'''
        <div style="background:#0a0a0a; border:1px solid #222; border-radius:10px; padding:10px; text-align:center;">
            <div style="font-size:10px; color:#555;">{d.strftime("%d/%m")}</div>
            <div style="font-size:18px; color:white;">☀️</div>
        </div>
        ''', unsafe_allow_html=True)

if st.button("🔄 REFRESH SYSTEM"):
    st.cache_data.clear()
    st.rerun()
