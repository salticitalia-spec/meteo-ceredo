import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import time
import math
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="Ceredoleso Sniper", page_icon="🎯", layout="centered")

@st.cache_data(ttl=600)
def fetch_data():
    lat, lon = 45.6117, 10.9710
    base_fc = "https://api.open-meteo.com/v1/forecast"
    base_hi = "https://archive-api.open-meteo.com/v1/archive"
    
    # Forecast 24h
    r_fc = requests.get(f"{base_fc}?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability&models=icon_seamless&timezone=Europe%2FRome&forecast_days=1").json()
    
    # Storico 15gg
    end = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
    r_hi = requests.get(f"{base_hi}?latitude={lat}&longitude={lon}&start_date={start}&end_date={end}&daily=precipitation_sum,wind_speed_10m_max,shortwave_radiation_sum&timezone=Europe%2FRome").json()
    
    return r_fc, r_hi

# --- 2. STILE CSS ---
st.markdown("""
<style>
    .stApp { background-color:#000; }
    .header-text { color:#00FFFF; font-size:24px; text-align:center; letter-spacing:5px; margin:20px 0; font-family:monospace; }
    .radar-container { position: relative; width: 100%; height: 400px; border-radius: 15px; border: 2px solid #333; overflow: hidden; }
    .sniper-crosshair { position: absolute; top: 50%; left: 50%; width: 60px; height: 60px; border: 2.5px solid #FF0000; border-radius: 50%; transform: translate(-50%, -50%); z-index: 100; pointer-events: none; }
    .sniper-dot { position: absolute; top: 50%; left: 50%; width: 8px; height: 8px; background: #FF0000; border-radius: 50%; transform: translate(-50%, -50%); box-shadow: 0 0 15px #FF0000; }
    
    .aztec-wrapper {
        position: relative; width: 320px; height: 320px; margin: 30px auto; border-radius: 50%;
        background: url('https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Piedra_del_Sol.png/600px-Piedra_del_Sol.png') center/cover;
        border: 4px solid #222; box-shadow: inset 0 0 80px #000; display: flex; align-items: center; justify-content: center;
        filter: sepia(0.5) brightness(0.7) contrast(1.2);
    }
    .digital-clock {
        background: rgba(0,0,0,0.8); padding: 10px 20px; border-radius: 12px; color: #fff;
        font-family: monospace; font-size: 30px; font-weight: bold; border: 1px solid #333; text-shadow: 0 0 10px #00FFFF;
    }
    .rings-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; transform: rotate(-90deg); }
    .ring-circle { fill: none; stroke-linecap: round; transition: stroke-dashoffset 0.5s ease; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGICA DATI ---
fc, hi = fetch_data()

st.markdown('<div class="header-text">Ceredoleso Sniper</div>', unsafe_allow_html=True)

# Radar
radar = "https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&overlay=rain&product=iconEu&marker=true"
st.markdown(f'<div class="radar-container"><div class="sniper-crosshair"><div class="sniper-dot"></div></div><iframe src="{radar}" width="100%" height="100%" frameborder="0"></iframe></div>', unsafe_allow_html=True)

# Timeline 12h
if fc and 'hourly' in fc:
    cols = st.columns(6)
    h_now = datetime.now().hour
    for i in range(12):
        idx = h_now + i
        if idx < len(fc['hourly']['time']):
            with cols[i % 6]:
                p = fc['hourly']['precipitation_probability'][idx]
                st.markdown(f"""<div style="text-align:center; font-size:10px; color:#aaa;">{fc['hourly']['time'][idx][-5:]}<br>
                <b style="color:white">{fc['hourly']['temperature_2m'][idx]}°</b><br>
                <span style="color:{'#F31' if p > 30 else '#0F0'}">{p}%</span></div>""", unsafe_allow_html=True)

# Storico
if hi and 'daily' in hi:
    df = pd.DataFrame({'D': hi['daily']['time'], 'P': hi['daily']['precipitation_sum'], 'V': hi['daily']['wind_speed_10m_max'], 'S': hi['daily']['shortwave_radiation_sum']})
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['D'], y=df['P'], marker_color='#007FFF', name="Pioggia"))
    fig.add_trace(go.Scatter(x=df['D'], y=df['V'], line=dict(color='#FF3311'), name="Vento"))
    fig.update_layout(template="plotly_dark", height=200, margin=dict(l=0,r=0,t=0,b=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- 4. OROLOGIO AZTECO ---
n = datetime.now()
sec = n.second
# Circonferenze: R46=289.02, R40=251.32, R34=213.62
off_h = 289.02 - (((n.hour % 24) + n.minute/60) * 289.02 / 24)
off_m = 251.32 - ((n.minute + sec/60) * 251.32 / 60)
off_s = 213.62 - (sec * 213.62 / 60)

# Costruzione HTML pulita
clock = f"""
<div class="aztec-wrapper">
    <div class="digital-clock">{n.strftime("%H:%M")}<span style="color:#F31; font-size:18px;">:{sec:02d}</span></div>
    <svg class="rings-svg" viewBox="0 0 100 100">
        <circle class="ring-circle" cx="50" cy="50" r="46" stroke="#00FFFF" stroke-width="2.5" stroke-dasharray="289.02" stroke-dashoffset="{off_h}" opacity="0.4"/>
        <circle class="ring-circle" cx="50" cy="50" r="40" stroke="#007FFF" stroke-width="2.5" stroke-dasharray="251.32" stroke-dashoffset="{off_m}" opacity="0.6"/>
        <circle class="ring-circle" cx="50" cy="50" r="34" stroke="#FF3311" stroke-width="2.5" stroke-dasharray="213.62" stroke-dashoffset="{off_s}" opacity="0.8"/>
    </svg>
</div>
<div style="text-align:center; color:#444; font-size:10px; font-family:monospace; letter-spacing:5px;">TIEMPO DE CEREDO</div>
"""
st.markdown(clock, unsafe_allow_html=True)

time.sleep(1)
st.rerun()
