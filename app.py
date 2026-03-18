import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="Ceredoleso Sniper 12H", page_icon="🎯", layout="centered")

# --- 2. CSS (TEMA BLACK + SNIPER CROSSHAIR) ---
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
}

/* MIRINO SNIPER OVERLAY */
.sniper-crosshair {
    position: absolute; top: 50%; left: 50%; width: 50px; height: 50px;
    border: 2.5px solid #FF0000; border-radius: 50%; transform: translate(-50%, -50%);
    pointer-events: none; z-index: 100;
}
.sniper-crosshair::before { content: ''; position: absolute; top: 50%; left: -30px; width: 110px; height: 1px; background: #FF0000; transform: translateY(-50%); }
.sniper-crosshair::after { content: ''; position: absolute; left: 50%; top: -30px; width: 1px; height: 110px; background: #FF0000; transform: translateX(-50%); }
.sniper-dot { 
    position: absolute; top: 50%; left: 50%; width: 8px; height: 8px; 
    background: #FF0000; border-radius: 50%; transform: translate(-50%, -50%); 
    box-shadow: 0 0 20px #FF0000; 
}

/* TIMELINE 12H */
.forecast-box { background:#111; border:1px solid #222; border-radius:10px; padding:10px; text-align:center; }
iframe { width: 100%; height: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA FETCHING (PREDIZIONE 12H) ---
@st.cache_data(ttl=600)
def fetch_12h_forecast():
    lat, lon = 45.6117, 10.9710
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation,precipitation_probability&timezone=Europe%2FRome&forecast_days=1"
    return requests.get(url).json()

f_data = fetch_12h_forecast()

# --- 4. HEADER ---
st.markdown('<div class="header-text">Ceredoleso PRO</div>', unsafe_allow_html=True)

# --- 5. RADAR PREDITTIVO (LOOP ANIMATO) ---
st.markdown('<div style="color:#FF0000; font-size:12px; text-align:center; letter-spacing:3px; margin-bottom:10px; font-weight:bold;">LONG-RANGE RADAR SCAN (+12H PROJECTION)</div>', unsafe_allow_html=True)

# RainViewer configurato per la massima estensione predittiva disponibile
radar_url = "https://www.rainviewer.com/map.html?loc=45.6117,10.971,10&type=radar&o=1&precip=1&trans=1&color=6&v=1&p=forecast&oP=1&lm=1&th=1&sm=1&sn=1"

st.markdown(f'''
<div class="radar-container">
    <div class="sniper-crosshair"><div class="sniper-dot"></div></div>
    <iframe src="{radar_url}"></iframe>
</div>
''', unsafe_allow_html=True)

# --- 6. TIMELINE TATTICA 12 ORE ---
st.write("")
st.markdown('<div style="color:#00FFFF; font-size:10px; text-align:center; letter-spacing:2px; margin-bottom:10px;">DATA STREAM: NEXT 12 HOURS</div>', unsafe_allow_html=True)

if f_data and 'hourly' in f_data:
    h_times = f_data['hourly']['time']
    h_precip = f_data['hourly']['precipitation']
    h_prob = f_data['hourly']['precipitation_probability']
    h_temp = f_data['hourly']['temperature_2m']
    
    # Selezioniamo le prossime 12 ore dall'ora attuale
    now_idx = datetime.now().hour
    cols = st.columns(6) # 2 righe da 6 per coprire le 12h
    
    for i in range(12):
        idx = now_idx + i
        if idx < len(h_times):
            with st.container():
                # Distribuiamo su due righe
                col_idx = i if i < 6 else i - 6
                target_col = st.columns(6)[col_idx] if i < 6 else st.columns(6)[col_idx]
                
                # Logica colore pioggia
                p_val = h_precip[idx]
                prob_val = h_prob[idx]
                p_color = "#FF3311" if p_val > 0.2 else "#FFFF00" if p_val > 0 else "#00FF00"
                
                # Visualizzazione compatta (usiamo colonne Streamlit standard per semplicità di layout)
    
    # Layout a griglia 2x6 per le 12 ore
    for row in range(2):
        r_cols = st.columns(6)
        for col in range(6):
            hour_offset = (row * 6) + col
            idx = now_idx + hour_offset
            if idx < len(h_times):
                with r_cols[col]:
                    time_str = h_times[idx][-5:]
                    p_val = h_precip[idx]
                    t_val = h_temp[idx]
                    prob = h_prob[idx]
                    p_color = "#FF3311" if p_val > 0.1 else "#00FF00"
                    
                    st.markdown(f'''
                    <div class="forecast-box">
                        <div style="font-size:10px; color:#555;">{time_str}</div>
                        <div style="font-size:14px; font-weight:bold; color:white;">{t_val}°</div>
                        <div style="font-size:11px; color:{p_color}; font-weight:bold;">{prob}%</div>
                    </div>
                    ''', unsafe_allow_html=True)

# --- 7. FOOTER ---
if st.button("🔄 RE-SYNC TARGET"):
    st.cache_data.clear()
    st.rerun()
