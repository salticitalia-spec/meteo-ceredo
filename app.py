import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Ceredoleso Sniper: Tiempo Azteca", page_icon="🎯", layout="centered")

# --- 2. CSS CUSTOM (TEMA BLACK, SNIPER E PIETRA) ---
st.markdown("""
<style>
.stApp { background-color:#000000 !important; }
.header-text { color:#00FFFF; font-weight:100; letter-spacing:5px; text-transform:uppercase; font-size:24px; text-align:center; margin:20px 0; }
.radar-container { position: relative; width: 100%; height: 500px; border-radius: 15px; border: 2px solid #333; overflow: hidden; }
.sniper-crosshair { position: absolute; top: 50%; left: 50%; width: 60px; height: 60px; border: 2.5px solid #FF0000; border-radius: 50%; transform: translate(-50%, -50%); pointer-events: none; z-index: 100; }
.sniper-dot { position: absolute; top: 50%; left: 50%; width: 10px; height: 10px; background: #FF0000; border-radius: 50%; transform: translate(-50%, -50%); box-shadow: 0 0 25px #FF0000; }
iframe { width: 100%; height: 100%; border: none; }

/* LEGENDA TATTICA STORICO */
.legend-container { display: flex; justify-content: space-around; background: #111; padding: 10px; border-radius: 10px; border: 1px solid #222; margin-bottom: 5px; }
.legend-item { text-align: center; font-family: monospace; font-weight: bold; font-size: 11px; }

/* GRIGLIA STORICO 15GG */
.history-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 20px; }
.history-item { background: #111; border: 1px solid #333; border-radius: 8px; padding: 10px; text-align:center; }
.history-bar { height: 6px; border-radius: 3px; background: #111; margin-top: 4px; overflow: hidden; }

/* --- STILE OROLOGIO AZTECO FUNZIONALE --- */
.aztec-stone { 
    text-align: center; 
    margin-top: 50px; 
    padding: 30px;
    background: #0a0a0a;
    border-radius: 20px;
    border: 1px solid #222;
    filter: sepia(0.3) grayscale(0.1); /* Effetto pietra */
}
.aztec-svg { width: 250px; height: 250px; fill: #555; }
.aztec-label { color: #555; font-family: 'Courier New', monospace; font-size: 11px; letter-spacing: 5px; margin-top: 20px; text-transform: uppercase; }

/* Orologio Digitale Grandi Dimensioni */
.big-digital { font-size: 40px; font-weight: bold; color: white; margin-bottom: 15px; font-family: 'Courier New', monospace; }
.seconds-digit { font-size: 25px; color: #888; }

/* Cerchi di Progresso Tempo */
.time-rings { display: flex; justify-content: center; gap: 20px; margin-top: 20px; }
.progress-ring { width: 60px; height: 60px; position: relative; }
.progress-ring__svg { width: 100%; height: 100%; }
.progress-ring__circle { 
    fill: none; 
    stroke-width: 5; 
    stroke-dasharray: 188.5; /* Circonferenza per r=30 */
    stroke-linecap: round; 
    transform-origin: 50% 50%;
    transform: rotate(-90deg); 
}
.ring-label { font-size: 10px; color: #666; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }

</style>
""", unsafe_allow_html=True)

# --- 3. DATA FETCHING ---
@st.cache_data(ttl=600)
def fetch_data():
    lat, lon = 45.6117, 10.9710
    # Previsioni 12h
    url_fc = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability&models=icon_seamless&timezone=Europe%2FRome&forecast_days=1"
    # Storico 15gg
    today = datetime.now()
    end_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = (today - timedelta(days=15)).strftime('%Y-%m-%d')
    url_hist = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=precipitation_sum&timezone=Europe%2FRome"
    
    return requests.get(url_fc).json(), requests.get(url_hist).json()

fc_data, hi_data = fetch_data()

# --- 4. HEADER & RADAR ---
st.markdown('<div class="header-text">Ceredoleso Sniper System</div>', unsafe_allow_html=True)
st.markdown('<div style="color:#FF0000; font-size:11px; text-align:center; letter-spacing:2px; margin-bottom:10px; font-weight:bold;">TARGET: ICON-EU (SWISS MODEL) PROJECTION +12H</div>', unsafe_allow_html=True)

radar_url = "https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&level=surface&overlay=rain&product=iconEu&menu=&message=true&marker=true&calendar=12&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"
st.markdown(f'<div class="radar-container"><div class="sniper-crosshair"><div class="sniper-dot"></div></div><iframe src="{radar_url}"></iframe></div>', unsafe_allow_html=True)

# --- 5. TIMELINE 12H ---
if fc_data and 'hourly' in fc_data:
    st.write("")
    now_h = datetime.now().hour
    cols = st.columns(6)
    for i in range(12):
        idx = now_h + i
        if idx < len(fc_data['hourly']['time']):
            with cols[i % 6]:
                time_str = fc_data['hourly']['time'][idx][-5:]
                prob = fc_data['hourly']['precipitation_probability'][idx]
                temp = fc_data['hourly']['temperature_2m'][idx]
                st.markdown(f'<div style="background:#111; border:1px solid #333; border-radius:8px; padding:8px; text-align:center;"><div style="font-size:9px; color:#555;">{time_str}</div><div style="font-size:13px; color:white; font-weight:bold;">{temp}°</div><div style="font-size:10px; color:{"#FF3311" if prob > 30 else "#00FF00"};">{prob}%</div></div>', unsafe_allow_html=True)

# --- 6. STORICO 15GG GRIGLIA DETTAGLIATA ---
st.write("")
st.markdown('''<div class="legend-container"><div class="legend-item" style="color:#007FFF;">🟦 PIOGGIA (mm/giorno)</div></div>''', unsafe_allow_html=True)

if hi_data and 'daily' in hi_data:
    st.markdown('<div class="history-grid">', unsafe_allow_html=True)
    dates = hi_data['daily']['time']
    precip = hi_data['daily']['precipitation_sum']
    for i in range(15):
        d_obj = datetime.strptime(dates[i], "%Y-%m-%d")
        p = precip[i]
        color = "#FF3311" if p > 2 else "#FFFF00" if p > 0.1 else "#00FF00"
        fill_pct = min(p * 20, 100) # Scala per la barra
        st.markdown(f'''
        <div class="history-item">
            <div style="font-size:9px; color:#666;">{d_obj.strftime("%d/%m")}</div>
            <div style="font-size:14px; color:{color}; font-weight:bold;">{p}mm</div>
            <div class="history-bar"><div style="height:100%; width:{fill_pct}%; background:{color};"></div></div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. OROLOGIO AZTECO FUNZIONALE (PIEDRA DEL SOL) ---
# 
# Calcoliamo il tempo attuale
curr_time = datetime.now()
h, m, s = curr_time.hour, curr_time.minute, curr_time.second
time_str = curr_time.strftime("%H:%M")

# Calcoliamo i progressi per i cerchi (per r=30, circ=188.5)
offset_h = 188.5 - ((h % 24) * 188.5 / 24)
offset_m = 188.5 - (m * 188.5 / 60)
offset_s = 188.5 - (s * 188.5 / 60)

st.markdown(f"""
<div class="aztec-stone">
    <div class="big-digital">{time_str}<span class="seconds-digit">:{s:02d}</span></div>
    
    <div class="time-rings">
        <div class="progress-ring">
            <svg class="progress-ring__svg" viewBox="0 0 70 70">
                <circle class="progress-ring__circle" stroke="#333" cx="35" cy="35" r="30"/>
                <circle class="progress-ring__circle" stroke="#00FFFF" cx="35" cy="35" r="30" style="stroke-dashoffset: {offset_h};"/>
            </svg>
            <div class="ring-label">H</div>
        </div>
        <div class="progress-ring">
            <svg class="progress-ring__svg" viewBox="0 0 70 70">
                <circle class="progress-ring__circle" stroke="#333" cx="35" cy="35" r="30"/>
                <circle class="progress-ring__circle" stroke="#007FFF" cx="35" cy="35" r="30" style="stroke-dashoffset: {offset_m};"/>
            </svg>
            <div class="ring-label">M</div>
        </div>
        <div class="progress-ring">
            <svg class="progress-ring__svg" viewBox="0 0 70 70">
                <circle class="progress-ring__circle" stroke="#333" cx="35" cy="35" r="30"/>
                <circle class="progress-ring__circle" stroke="#FF3311" cx="35" cy="35" r="30" style="stroke-dashoffset: {offset_s};"/>
            </svg>
            <div class="ring-label">S</div>
        </div>
    </div>

    <svg class="aztec-svg" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="48" fill="none" stroke="#555" stroke-width="1"/>
        <circle cx="50" cy="50" r="40" fill="none" stroke="#444" stroke-width="0.5"/>
        <text x="50" y="55" font-family="Arial" font-size="12" text-anchor="middle" fill="#555" font-weight="bold">AZTEC</text>
        <circle cx="50" cy="50" r="10" fill="none" stroke="#555" stroke-width="1"/>
    </svg>
    <div class="aztec-label">Tiempo Eterno de Ceredo</div>
</div>
""", unsafe_allow_html=True)

# Meccanismo di Ricarica per rendere l'orologio funzionale (Sperimentale)
# Aggiungi un pulsante invisibile per forzare il refresh o un piccolo loop.
# NOTA: Ricaricare la pagina ogni secondo non è consigliato per Streamlit.
# L'app si aggiornerà ogni volta che un utente interagisce o ogni 10 minuti (ttl cache).
st.button("🔄 RE-SYNC & UPDATE CLOCK", key="clock_refresh")
if st.cache_data.clear(): # Pulisce la cache per forzare l'update dei dati meteo
    st.rerun()

time.sleep(1) # Un piccolo ritardo per l'utente, non ricarica l'app
st.rerun() # Ricarica l'app ogni secondo per l'orologio (PUÒ RALLENTARE L'APP)
