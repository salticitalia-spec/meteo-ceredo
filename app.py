import streamlit as st
import requests
from datetime import datetime

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="Ceredoleso Sniper Radar", page_icon="🎯", layout="centered")

# --- 2. CSS (TEMA BLACK + MIRINO SNIPER) ---
st.markdown("""
<style>
.stApp { background-color:#000000 !important; }
.header-text { color:#00FFFF; font-weight:100; letter-spacing:7px; text-transform:uppercase; font-size:26px; text-align:center; margin:20px 0; }

/* CONTAINER RADAR */
.radar-container { 
    position: relative; 
    width: 100%; 
    height: 500px; 
    border-radius: 15px; 
    border: 2px solid #444; 
    overflow: hidden; 
    background: #111;
}

/* MIRINO SNIPER OVERLAY */
.sniper-crosshair {
    position: absolute; top: 50%; left: 50%; width: 50px; height: 50px;
    border: 2px solid #FF0000; border-radius: 50%; transform: translate(-50%, -50%);
    pointer-events: none; z-index: 100;
}
.sniper-crosshair::before { content: ''; position: absolute; top: 50%; left: -25px; width: 100px; height: 1px; background: #FF0000; transform: translateY(-50%); }
.sniper-crosshair::after { content: ''; position: absolute; left: 50%; top: -25px; width: 1px; height: 100px; background: #FF0000; transform: translateX(-50%); }
.sniper-dot { 
    position: absolute; top: 50%; left: 50%; width: 6px; height: 6px; 
    background: #FF0000; border-radius: 50%; transform: translate(-50%, -50%); 
    box-shadow: 0 0 15px #FF0000; 
}

iframe { width: 100%; height: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown('<div class="header-text">Ceredoleso PRO</div>', unsafe_allow_html=True)

# --- 4. RADAR PREDITTIVO REAL-TIME (+6 ORE) ---
st.markdown('<div style="color:#FF0000; font-size:12px; text-align:center; letter-spacing:3px; margin-bottom:10px; font-weight:bold;">PREDICTIVE SCAN: MOVIMENTO CELLE +6H</div>', unsafe_allow_html=True)

# Utilizziamo RainViewer per la predizione automatica
# lat=45.61, lon=10.97 (Ceredo)
# m=1 (mostra radar), s=1 (loop animato), oper=1 (proiezione futura)
radar_url = "https://www.rainviewer.com/map.html?loc=45.6117,10.971,9&type=radar&o=1&precip=1&trans=1&color=6&v=1&p=forecast&oP=1&lm=1&th=1&sm=1&sn=1"

st.markdown(f'''
<div class="radar-container">
    <div class="sniper-crosshair">
        <div class="sniper-dot"></div>
    </div>
    <iframe src="{radar_url}" allowfullscreen></iframe>
</div>
''', unsafe_allow_html=True)

# --- 5. DATA FETCHING (OPEN-METEO) ---
@st.cache_data(ttl=600)
def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=45.6117&longitude=10.9710&current_weather=true&hourly=precipitation_probability&timezone=Europe%2FRome"
    return requests.get(url).json()

w_data = get_weather()
temp = w_data['current_weather']['temperature']
prob_rain = w_data['hourly']['precipitation_probability'][0] # probabilità ora attuale

# --- 6. INFO TATTICA ---
st.write("")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'''
    <div style="background:#0a0a0a; border:1px solid #222; border-radius:15px; padding:15px; text-align:center;">
        <div style="font-size:10px; color:#00FFFF;">TEMPERATURA</div>
        <div style="font-size:35px; font-weight:bold; color:white;">{temp}°</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    color_p = "#FF3311" if prob_rain > 30 else "#00FF00"
    st.markdown(f'''
    <div style="background:#0a0a0a; border:1px solid #222; border-radius:15px; padding:15px; text-align:center;">
        <div style="font-size:10px; color:#00FFFF;">PROB. PIOGGIA</div>
        <div style="font-size:35px; font-weight:bold; color:{color_p};">{prob_rain}%</div>
    </div>
    ''', unsafe_allow_html=True)

# --- 7. FOOTER ---
if st.button("🔄 RE-SYNC RADAR"):
    st.cache_data.clear()
    st.rerun()
