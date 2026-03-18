import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Ceredoleso Sniper 15D+12H", page_icon="🎯", layout="centered")

# --- 2. CSS CUSTOM (TEMA PIETRA E DARK) ---
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

/* OROLOGIO MAYA STILIZZATO */
.maya-stone { 
    text-align: center; 
    margin-top: 40px; 
    padding: 20px;
    opacity: 0.4; 
    filter: sepia(0.8) grayscale(0.2);
}
.maya-svg { width: 200px; height: 200px; fill: #888; }
.maya-label { color: #555; font-family: 'Courier New', monospace; font-size: 10px; letter-spacing: 5px; margin-top: 15px; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA FETCHING ---
@st.cache_data(ttl=600)
def fetch_data():
    lat, lon = 45.6117, 10.9710
    url_fc = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability&models=icon_seamless&timezone=Europe%2FRome&forecast_days=1"
    today = datetime.now()
    end_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = (today - timedelta(days=15)).strftime('%Y-%m-%d')
    url_hist = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=precipitation_sum,wind_speed_10m_max,shortwave_radiation_sum&timezone=Europe%2FRome"
    return requests.get(url_fc).json(), requests.get(url_hist).json()

fc_data, hi_data = fetch_data()

# --- 4. RADAR & TIMELINE ---
st.markdown('<div class="header-text">Ceredoleso Sniper</div>', unsafe_allow_html=True)
radar_url = "https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&level=surface&overlay=rain&product=iconEu&menu=&message=true&marker=true&calendar=12&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"
st.markdown(f'<div class="radar-container"><div class="sniper-crosshair"><div class="sniper-dot"></div></div><iframe src="{radar_url}"></iframe></div>', unsafe_allow_html=True)

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
                st.markdown(f'<div style="background:#111; border:1px solid #333; border-radius:8px; padding:5px; text-align:center;"><div style="font-size:9px; color:#555;">{time_str}</div><div style="font-size:12px; color:white; font-weight:bold;">{temp}°</div><div style="font-size:10px; color:{"#FF3311" if prob > 30 else "#00FF00"};">{prob}%</div></div>', unsafe_allow_html=True)

# --- 5. STORICO 15GG ---
st.write("")
st.markdown('''<div class="legend-container"><div class="legend-item" style="color:#007FFF;">🟦 PIOGGIA</div><div class="legend-item" style="color:#FF3311;">🟥 VENTO</div><div class="legend-item" style="color:#FFFF00;">🟨 SOLE</div></div>''', unsafe_allow_html=True)

if hi_data and 'daily' in hi_data:
    df_hist = pd.DataFrame({
        'Data': hi_data['daily']['time'],
        'Pioggia': hi_data['daily']['precipitation_sum'],
        'Vento': hi_data['daily']['wind_speed_10m_max'],
        'Sole': hi_data['daily']['shortwave_radiation_sum']
    })
    df_hist.loc[df_hist['Pioggia'] > 0.2, 'Sole'] = 0
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_hist['Data'], y=df_hist['Sole'], fill='tozeroy', line_color='#FFFF00', opacity=0.3, yaxis="y2"))
    fig.add_trace(go.Scatter(x=df_hist['Data'], y=df_hist['Vento'], line=dict(color='#FF3311', width=2)))
    fig.add_trace(go.Bar(x=df_hist['Data'], y=df_hist['Pioggia'], marker_color='#007FFF'))
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(l=0, r=0, t=5, b=0), showlegend=False, yaxis=dict(showgrid=False), yaxis2=dict(overlaying="y", side="right", showgrid=False), xaxis=dict(showgrid=False))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- 6. OROLOGIO MAYA FINALE (PIEDRA DEL SOL) ---
st.markdown("""
<div class="maya-stone">
    <svg class="maya-svg" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="48" fill="none" stroke="#555" stroke-width="1"/>
        <circle cx="50" cy="50" r="40" fill="none" stroke="#444" stroke-width="0.5"/>
        <path d="M50 5 L55 20 L45 20 Z M50 95 L55 80 L45 80 Z M5 50 L20 45 L20 55 Z M95 50 L80 45 L80 55 Z" fill="#555"/>
        <text x="50" y="54" font-family="Arial" font-size="12" text-anchor="middle" fill="#555" font-weight="bold">MAYAN</text>
        <circle cx="50" cy="50" r="10" fill="none" stroke="#555" stroke-width="1"/>
    </svg>
    <div class="maya-label">Tiempo Eterno de Ceredo</div>
</div>
""", unsafe_allow_html=True)

# 

if st.button("🔄 RE-SYNC"):
    st.cache_data.clear()
    st.rerun()
