import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import time
import math
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Ceredoleso Sniper: Tiempo Azteca", page_icon="🎯", layout="centered")

# --- 2. DATA FETCHING ---
@st.cache_data(ttl=600)
def fetch_data():
    lat, lon = 45.6117, 10.9710
    url_fc = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability&models=icon_seamless&timezone=Europe%2FRome&forecast_days=1"
    today = datetime.now()
    end_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = (today - timedelta(days=15)).strftime('%Y-%m-%d')
    url_hist = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=precipitation_sum,wind_speed_10m_max,shortwave_radiation_sum&timezone=Europe%2FRome"
    
    r_fc = requests.get(url_fc).json()
    r_hi = requests.get(url_hist).json()
    return r_fc, r_hi

# --- 3. CSS CUSTOM ---
st.markdown("""
<style>
    .stApp { background-color:#000000 !important; }
    .header-text { color:#00FFFF; font-weight:100; letter-spacing:5px; text-transform:uppercase; font-size:24px; text-align:center; margin:20px 0; }
    .radar-container { position: relative; width: 100%; height: 500px; border-radius: 15px; border: 2px solid #333; overflow: hidden; }
    .sniper-crosshair { position: absolute; top: 50%; left: 50%; width: 60px; height: 60px; border: 2.5px solid #FF0000; border-radius: 50%; transform: translate(-50%, -50%); pointer-events: none; z-index: 100; }
    .sniper-dot { position: absolute; top: 50%; left: 50%; width: 10px; height: 10px; background: #FF0000; border-radius: 50%; transform: translate(-50%, -50%); box-shadow: 0 0 25px #FF0000; }
    iframe { width: 100%; height: 100%; border: none; }

    .legend-container { display: flex; justify-content: space-around; background: #111; padding: 10px; border-radius: 10px; border: 1px solid #222; margin-bottom: 5px; }
    .legend-item { text-align: center; font-family: monospace; font-weight: bold; font-size: 11px; }

    /* OROLOGIO AZTECO DINAMICO */
    .aztec-wrapper {
        position: relative;
        width: 320px;
        height: 320px;
        margin: 40px auto;
        border-radius: 50%;
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Piedra_del_Sol.png/600px-Piedra_del_Sol.png');
        background-size: cover;
        background-position: center;
        border: 4px solid #222;
        box-shadow: inset 0 0 80px #000, 0 0 40px #111;
        display: flex;
        align-items: center;
        justify-content: center;
        filter: sepia(0.5) brightness(0.7) contrast(1.2);
    }
    .digital-clock {
        background: rgba(0,0,0,0.85);
        padding: 10px 22px;
        border-radius: 12px;
        color: white;
        font-family: 'Courier New', monospace;
        font-size: 32px;
        font-weight: bold;
        z-index: 10;
        border: 1px solid #333;
        text-shadow: 0 0 15px #00FFFF;
    }
    .rings-svg {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        transform: rotate(-90deg);
        pointer-events: none;
    }
    .ring-circle {
        fill: none;
        stroke-linecap: round;
        transition: stroke-dashoffset 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
</style>
""", unsafe_allow_html=True)

# --- 4. DATA FETCHING ---
fc_data, hi_data = fetch_data()

# --- 5. HEADER & RADAR ---
st.markdown('<div class="header-text">Ceredoleso Sniper</div>', unsafe_allow_html=True)
radar_url = "https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&level=surface&overlay=rain&product=iconEu&menu=&message=true&marker=true&calendar=12&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"
st.markdown(f'<div class="radar-container"><div class="sniper-crosshair"><div class="sniper-dot"></div></div><iframe src="{radar_url}"></iframe></div>', unsafe_allow_html=True)

# --- 6. TIMELINE 12H ---
if fc_data and 'hourly' in fc_data:
    st.write("")
    now_h = datetime.now().hour
    cols = st.columns(6)
    for i in range(12):
        idx = now_h + i
        if idx < len(fc_data['hourly']['time']):
            with cols[i % 6]:
                t_str = fc_data['hourly']['time'][idx][-5:]
                p = fc_data['hourly']['precipitation_probability'][idx]
                temp = fc_data['hourly']['temperature_2m'][idx]
                c = "#FF3311" if p > 30 else "#00FF00"
                st.markdown(f'<div style="background:#111; border:1px solid #333; border-radius:8px; padding:8px; text-align:center;"><div style="font-size:9px; color:#555;">{t_str}</div><div style="font-size:13px; color:white; font-weight:bold;">{temp}°</div><div style="font-size:10px; color:{c};">{p}%</div></div>', unsafe_allow_html=True)

# --- 7. STORICO 15GG ---
st.write("")
st.markdown('<div class="legend-container"><div class="legend-item" style="color:#007FFF;">🟦 PIOGGIA</div><div class="legend-item" style="color:#FF3311;">🟥 VENTO</div><div class="legend-item" style="color:#FFFF00;">🟨 SOLE</div></div>', unsafe_allow_html=True)

if hi_data and 'daily' in hi_data:
    df = pd.DataFrame({
        'D': hi_data['daily']['time'],
        'P': hi_data['daily']['precipitation_sum'],
        'V': hi_data['daily']['wind_speed_10m_max'],
        'S': hi_data['daily']['shortwave_radiation_sum']
    })
    df.loc[df['P'] > 0.2, 'S'] = 0 
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['D'], y=df['S'], fill='tozeroy', line_color='#FFFF00', opacity=0.15, yaxis="y2"))
    fig.add_trace(go.Scatter(x=df['D'], y=df['V'], line=dict(color='#FF3311', width=2)))
    fig.add_trace(go.Bar(x=df['D'], y=df['P'], marker_color='#007FFF'))
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(l=0, r=0, t=5, b=0), showlegend=False, yaxis=dict(showgrid=False), yaxis2=dict(overlaying="y", side="right", showgrid=False), xaxis=dict(showgrid=False))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- 8. OROLOGIO AZTECO FUNZIONALE ---
now = datetime.now()
h, m, s = now.hour, now.minute, now.second

# Calcolo Circonferenze Precise: C = 2 * pi * r
circ_h = 2 * math.pi * 46  # 289.0265
circ_m = 2 * math.pi * 40  # 251.3274
circ_s = 2 * math.pi * 34  # 213.6283

# Calcolo Offset (Il cerchio si svuota al passare del tempo)
off_h = circ_h - ((h % 24 + m/60) * circ_h / 24)
off_m = circ_m - ((m + s/60) * circ_m / 60)
off_s = circ_s - (s * circ_s / 60)

st.markdown(f"""
<div class="aztec-wrapper">
    <div class="digital-clock">{now.strftime("%H:%M")}<span style="font-size:20px; color:#FF3311;">:{s:02d}</span></div>
    
    <svg class="rings-svg" viewBox="0 0 100 100">
        <circle class="ring-circle" cx="50" cy="50" r="46" stroke="#00FFFF" stroke-width="2.5" 
            stroke-dasharray="{circ_h}" stroke-dashoffset="{off_h}" opacity="0.5"/>
        
        <circle class="ring-circle" cx="50" cy="50" r="40" stroke="#007FFF" stroke-width="2.5" 
            stroke-dasharray="{circ_m}" stroke-dashoffset="{off_m}" opacity="0.6"/>
            
        <circle class="ring-circle" cx="50" cy="50" r="34" stroke="#FF3311" stroke-width="2.5" 
            stroke-dasharray="{circ_s}" stroke-dashoffset="{off_s}" opacity="0.8"/>
    </svg>
</div>
<div style="text-align:center; color:#555; letter-spacing:8px; font-size:10px; margin-top:-20px; font-family:monospace; font-weight:bold;">
    TIEMPO ETERNO DE CEREDO
</div>
""", unsafe_allow_html=True)

# Update automatico ogni secondo
time.sleep(1)
st.rerun()
