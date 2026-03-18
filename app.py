import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="Meteo Ceredoleso Pro", page_icon="🎯", layout="centered")

# --- 2. CSS (TEMA BLACK + MIRINO + TIMELINE) ---
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

/* STORICO STYLE */
.history-bar { height: 10px; border-radius: 5px; background: #222; margin-top: 5px; overflow: hidden; }
.history-fill { height: 100%; background: #00FFFF; }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA FETCHING (LIVE + STORICO 10gg) ---
@st.cache_data(ttl=3600)
def fetch_all_data():
    lat, lon = 45.6117, 10.9710
    # Dati attuali e forecast
    url_curr = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,weathercode&timezone=Europe%2FRome"
    
    # Dati Storici (precipitazioni ultimi 10 giorni)
    end_date = datetime.now().date() - timedelta(days=1)
    start_date = end_date - timedelta(days=10)
    url_hist = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=precipitation_sum&timezone=Europe%2FRome"
    
    return requests.get(url_curr).json(), requests.get(url_hist).json()

curr_data, hist_data = fetch_all_data()

# --- 4. HEADER E CORRENTE ---
now = datetime.now()
st.markdown('<div class="header-text">Ceredoleso PRO</div>', unsafe_allow_html=True)
st.markdown(f'''
<div class="main-card">
    <div style="font-size:16px; color:white; opacity:0.7;">LIVE TARGET DATA</div>
    <div style="font-size:80px; margin:10px 0;">☀️</div>
    <div style="font-size:65px; font-weight:bold; color:white; margin-top:-10px;">{curr_data['current_weather']['temperature']}°</div>
</div>
''', unsafe_allow_html=True)

# --- 5. RADAR CON MIRINO ---
st.markdown('<div style="color:#00FFFF; font-size:10px; text-align:center; letter-spacing:2px; margin-bottom:10px;">RADAR LIVE & TARGET LOCK</div>', unsafe_allow_html=True)
radar_url = "https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=10&level=surface&overlay=radar&product=radar&marker=true"
st.markdown(f'''
<div class="radar-container">
    <div class="sniper-crosshair"><div class="sniper-dot"></div></div>
    <iframe src="{radar_url}"></iframe>
</div>
''', unsafe_allow_html=True)

# --- 6. SEQUENZA STORICA (10 GIORNI) ---
st.write("")
st.markdown('<div style="color:#00FFFF; font-size:10px; text-align:center; letter-spacing:2px; margin-bottom:10px;">HISTORICAL SCAN (LAST 10 DAYS)</div>', unsafe_allow_html=True)

if hist_data and 'daily' in hist_data:
    dates = hist_data['daily']['time']
    precip = hist_data['daily']['precipitation_sum']
    
    # Creiamo una griglia per lo storico
    h_cols = st.columns(5)
    for i in range(10):
        with h_cols[i % 5]:
            d = datetime.strptime(dates[i], "%Y-%m-%d")
            p = precip[i]
            color = "#FF3311" if p > 2 else "#00FF00" if p == 0 else "#FFFF00"
            pct = min(p * 10, 100) # scalo per la barra visiva
            
            st.markdown(f'''
            <div style="background:#111; border-radius:10px; padding:10px; margin-bottom:10px; border:1px solid #222; text-align:center;">
                <div style="font-size:10px; color:#666;">{d.day}/{d.month}</div>
                <div style="font-size:14px; font-weight:bold; color:{color};">{p}mm</div>
                <div class="history-bar"><div class="history-fill" style="width:{pct}%; background:{color};"></div></div>
            </div>
            ''', unsafe_allow_html=True)

# --- 7. TENDENZA ---
st.write("")
t_cols = st.columns(3)
for i in range(1, 4):
    with t_cols[i-1]:
        d_f = now + timedelta(days=i)
        st.markdown(f'''
        <div class="main-card" style="padding:15px; border-color:#222;">
            <div style="font-size:11px; color:white;">{d_f.day}/{d_f.month}</div>
            <div style="font-size:30px; margin:5px 0;">☀️</div>
            <div style="font-size:22px; font-weight:bold; color:white;">{curr_data['daily']['temperature_2m_max'][i]}°</div>
        </div>
        ''', unsafe_allow_html=True)

if st.button("🔄 RE-SCAN TARGET"):
    st.cache_data.clear()
    st.rerun()
