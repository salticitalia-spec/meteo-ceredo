import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="Ceredoleso Sniper 15D+12H", page_icon="🎯", layout="centered")

# --- 2. CSS (TEMA BLACK + SNIPER CROSSHAIR) ---
st.markdown("""
<style>
.stApp { background-color:#000000 !important; }
.header-text { color:#00FFFF; font-weight:100; letter-spacing:5px; text-transform:uppercase; font-size:24px; text-align:center; margin:20px 0; }

/* CONTAINER RADAR */
.radar-container { 
    position: relative; 
    width: 100%; 
    height: 550px; 
    border-radius: 15px; 
    border: 2px solid #333; 
    overflow: hidden; 
}

/* MIRINO SNIPER */
.sniper-crosshair {
    position: absolute; top: 50%; left: 50%; width: 60px; height: 60px;
    border: 2.5px solid #FF0000; border-radius: 50%; transform: translate(-50%, -50%);
    pointer-events: none; z-index: 100;
}
.sniper-crosshair::before { content: ''; position: absolute; top: 50%; left: -40px; width: 140px; height: 1.5px; background: #FF0000; transform: translateY(-50%); }
.sniper-crosshair::after { content: ''; position: absolute; left: 50%; top: -40px; width: 1.5px; height: 140px; background: #FF0000; transform: translateX(-50%); }
.sniper-dot { 
    position: absolute; top: 50%; left: 50%; width: 10px; height: 10px; 
    background: #FF0000; border-radius: 50%; transform: translate(-50%, -50%); 
    box-shadow: 0 0 25px #FF0000; 
}

/* STORICO STYLE */
.history-box { background:#0a0a0a; border:1px solid #222; border-radius:8px; padding:8px; text-align:center; margin-bottom:10px; }
.history-bar { height: 6px; border-radius: 3px; background: #111; margin-top: 4px; overflow: hidden; }
.history-fill { height: 100%; }

iframe { width: 100%; height: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA FETCHING (LIVE, 12H SWISS & 15D HISTORY) ---
@st.cache_data(ttl=600)
def fetch_all_data():
    lat, lon = 45.6117, 10.9710
    # 1. Forecast ICON-CH (MeteoSwiss) 12h
    url_fc = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability&models=icon_seamless&timezone=Europe%2FRome&forecast_days=1"
    
    # 2. Archive 15 days (Precipitation Sum)
    end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
    url_hist = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=precipitation_sum&timezone=Europe%2FRome"
    
    return requests.get(url_fc).json(), requests.get(url_hist).json()

fc_data, hi_data = fetch_all_data()

# --- 4. HEADER ---
st.markdown('<div class="header-text">Ceredoleso Sniper System</div>', unsafe_allow_html=True)

# --- 5. RADAR PREDITTIVO 12H (MODELLO SVIZZERO) ---
st.markdown('<div style="color:#FF0000; font-size:11px; text-align:center; letter-spacing:2px; margin-bottom:10px; font-weight:bold;">PREDICTIVE RADAR: NEXT 12 HOURS (SWISS MODEL)</div>', unsafe_allow_html=True)

radar_url = "https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&level=surface&overlay=rain&product=iconEu&menu=&message=true&marker=true&calendar=12&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"

st.markdown(f'''
<div class="radar-container">
    <div class="sniper-crosshair"><div class="sniper-dot"></div></div>
    <iframe src="{radar_url}"></iframe>
</div>
''', unsafe_allow_html=True)

# --- 6. TIMELINE TATTICA 12H (Dati ICON-CH) ---
if fc_data and 'hourly' in fc_data:
    st.write("")
    st.markdown('<div style="color:#00FFFF; font-size:10px; text-align:center; letter-spacing:2px; margin-bottom:10px;">HOURLY SCAN: NEXT 12 HOURS</div>', unsafe_allow_html=True)
    now_h = datetime.now().hour
    t_cols = st.columns(6)
    for i in range(12):
        idx = now_h + i
        if idx < len(fc_data['hourly']['time']):
            with t_cols[i % 6]:
                time_str = fc_data['hourly']['time'][idx][-5:]
                prob = fc_data['hourly']['precipitation_probability'][idx]
                temp = fc_data['hourly']['temperature_2m'][idx]
                p_color = "#FF3311" if prob > 30 else "#00FF00"
                st.markdown(f'''
                <div style="background:#111; border:1px solid #333; border-radius:10px; padding:6px; text-align:center; margin-bottom:10px;">
                    <div style="font-size:9px; color:#555;">{time_str}</div>
                    <div style="font-size:13px; color:white; font-weight:bold;">{temp}°</div>
                    <div style="font-size:10px; color:{p_color};">{prob}%</div>
                </div>
                ''', unsafe_allow_html=True)

# --- 7. STORICO PRECIPITAZIONI 15 GIORNI ---
st.write("")
st.markdown('<div style="color:#00FFFF; font-size:10px; text-align:center; letter-spacing:2px; margin-bottom:10px;">HISTORICAL SCAN (LAST 15 DAYS)</div>', unsafe_allow_html=True)

if hi_data and 'daily' in hi_data:
    dates = hi_data['daily']['time']
    precip = hi_data['daily']['precipitation_sum']
    
    # Griglia 3 righe x 5 colonne per i 15 giorni
    for row in range(3):
        h_cols = st.columns(5)
        for col in range(5):
            idx = (row * 5) + col
            if idx < len(dates):
                with h_cols[col]:
                    d = datetime.strptime(dates[idx], "%Y-%m-%d")
                    p = precip[idx]
                    # Logica colore: Verde 0, Giallo <2, Rosso >2
                    color = "#FF3311" if p > 2 else "#FFFF00" if p > 0.1 else "#00FF00"
                    pct = min(p * 15, 100) # scalo per la barra visiva
                    
                    st.markdown(f'''
                    <div class="history-box">
                        <div style="font-size:9px; color:#666;">{d.day}/{d.month}</div>
                        <div style="font-size:13px; font-weight:bold; color:{color};">{p}mm</div>
                        <div class="history-bar"><div class="history-fill" style="width:{pct}%; background:{color};"></div></div>
                    </div>
                    ''', unsafe_allow_html=True)

# --- 8. FOOTER ---
if st.button("🔄 RE-SYNC TARGET"):
    st.cache_data.clear()
    st.rerun()
