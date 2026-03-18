import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="Ceredoleso Sniper 15D+12H", page_icon="🎯", layout="centered")

# --- 2. CSS (TEMA BLACK + SNIPER CROSSHAIR) ---
st.markdown("""
<style>
.stApp { background-color:#000000 !important; }
.header-text { color:#00FFFF; font-weight:100; letter-spacing:5px; text-transform:uppercase; font-size:24px; text-align:center; margin:20px 0; }
.radar-container { position: relative; width: 100%; height: 550px; border-radius: 15px; border: 2px solid #333; overflow: hidden; }
.sniper-crosshair { position: absolute; top: 50%; left: 50%; width: 60px; height: 60px; border: 2.5px solid #FF0000; border-radius: 50%; transform: translate(-50%, -50%); pointer-events: none; z-index: 100; }
.sniper-dot { position: absolute; top: 50%; left: 50%; width: 10px; height: 10px; background: #FF0000; border-radius: 50%; transform: translate(-50%, -50%); box-shadow: 0 0 25px #FF0000; }
iframe { width: 100%; height: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA FETCHING ---
@st.cache_data(ttl=600)
def fetch_data():
    lat, lon = 45.6117, 10.9710
    # Forecast 12h
    url_fc = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability&models=icon_seamless&timezone=Europe%2FRome&forecast_days=1"
    # Archive 15d (Pioggia, Vento, Irraggiamento)
    end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
    url_hist = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=precipitation_sum,wind_speed_10m_max,shortwave_radiation_sum&timezone=Europe%2FRome"
    
    return requests.get(url_fc).json(), requests.get(url_hist).json()

fc_data, hi_data = fetch_data()

# --- 4. HEADER ---
st.markdown('<div class="header-text">Ceredoleso Sniper System</div>', unsafe_allow_html=True)

# --- 5. RADAR PREDITTIVO ICON-EU ---
st.markdown('<div style="color:#FF0000; font-size:11px; text-align:center; letter-spacing:2px; margin-bottom:10px; font-weight:bold;">SORGENTE: RADAR PREDITTIVO ICON-EU (SWISS MODEL) +12H</div>', unsafe_allow_html=True)
radar_url = "https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&level=surface&overlay=rain&product=iconEu&menu=&message=true&marker=true&calendar=12&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"

st.markdown(f'''
<div class="radar-container">
    <div class="sniper-crosshair"><div class="sniper-dot"></div></div>
    <iframe src="{radar_url}"></iframe>
</div>
''', unsafe_allow_html=True)

# --- 6. TIMELINE 12H ---
if fc_data and 'hourly' in fc_data:
    st.write("")
    now_h = datetime.now().hour
    t_cols = st.columns(6)
    for i in range(12):
        idx = now_h + i
        if idx < len(fc_data['hourly']['time']):
            with t_cols[i % 6]:
                time_str = fc_data['hourly']['time'][idx][-5:]
                prob = fc_data['hourly']['precipitation_probability'][idx]
                temp = fc_data['hourly']['temperature_2m'][idx]
                st.markdown(f'''
                <div style="background:#111; border:1px solid #333; border-radius:10px; padding:6px; text-align:center; margin-bottom:10px;">
                    <div style="font-size:9px; color:#555;">{time_str}</div>
                    <div style="font-size:13px; color:white; font-weight:bold;">{temp}°</div>
                    <div style="font-size:10px; color:{"#FF3311" if prob > 30 else "#00FF00"};">{prob}%</div>
                </div>
                ''', unsafe_allow_html=True)

# --- 7. GRAFICO STORICO 15 GIORNI (MULTI-AXIS) ---
st.write("")
st.markdown('<div style="color:#00FFFF; font-size:10px; text-align:center; letter-spacing:2px; margin-bottom:10px;">HISTORICAL SCAN: DRYING FACTORS (LAST 15 DAYS)</div>', unsafe_allow_html=True)

if hi_data and 'daily' in hi_data:
    df = pd.DataFrame({
        'Data': hi_data['daily']['time'],
        'Pioggia': hi_data['daily']['precipitation_sum'],
        'Vento': hi_data['daily']['wind_speed_10m_max'],
        'Sole': hi_data['daily']['shortwave_radiation_sum']
    })

    fig = go.Figure()

    # Sole (Irraggiamento) - Area Gialla (Scalata su asse secondario)
    fig.add_trace(go.Scatter(x=df['Data'], y=df['Sole'], name="Sole (MJ/m²)", 
                             fill='tozeroy', line_color='#FFFF00', opacity=0.3, yaxis="y2"))

    # Vento - Linea Rossa
    fig.add_trace(go.Scatter(x=df['Data'], y=df['Vento'], name="Vento (km/h)", 
                             line=dict(color='#FF3311', width=2)))

    # Pioggia - Istogrammi Blu
    fig.add_trace(go.Bar(x=df['Data'], y=df['Pioggia'], name="Pioggia (mm)", 
                         marker_color='#007FFF', opacity=0.8))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title="Pioggia/Vento", titlefont=dict(color="#007FFF"), tickfont=dict(color="#007FFF")),
        yaxis2=dict(title="Sole", overlaying="y", side="right", showgrid=False, tickfont=dict(color="#FFFF00")),
        xaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

if st.button("🔄 RE-SYNC TARGET"):
    st.cache_data.clear()
    st.rerun()
