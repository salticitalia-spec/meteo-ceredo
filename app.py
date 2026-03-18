import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Ceredoleso Sniper 15D+12H", page_icon="🎯", layout="centered")

# --- 2. CSS CUSTOM ---
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
    url_fc = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability&models=icon_seamless&timezone=Europe%2FRome&forecast_days=1"
    today = datetime.now()
    end_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    start_date = (today - timedelta(days=15)).strftime('%Y-%m-%d')
    url_hist = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=precipitation_sum,wind_speed_10m_max,shortwave_radiation_sum&timezone=Europe%2FRome"
    
    r_fc = requests.get(url_fc).json()
    r_hi = requests.get(url_hist).json()
    return r_fc, r_hi

fc_data, hi_data = fetch_data()

# --- 4. INTERFACCIA ---
st.markdown('<div class="header-text">Ceredoleso Sniper System</div>', unsafe_allow_html=True)

# Radar
st.markdown('<div style="color:#FF0000; font-size:11px; text-align:center; letter-spacing:2px; margin-bottom:10px; font-weight:bold;">TARGET: ICON-EU (SWISS MODEL) PROJECTION +12H</div>', unsafe_allow_html=True)
radar_url = "https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&level=surface&overlay=rain&product=iconEu&menu=&message=true&marker=true&calendar=12&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"

st.markdown(f'''
<div class="radar-container">
    <div class="sniper-crosshair"><div class="sniper-dot"></div></div>
    <iframe src="{radar_url}"></iframe>
</div>
''', unsafe_allow_html=True)

# Timeline 12h
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
                color = "#FF3311" if prob > 30 else "#00FF00"
                st.markdown(f'''
                <div style="background:#111; border:1px solid #333; border-radius:10px; padding:8px; text-align:center; margin-bottom:10px;">
                    <div style="font-size:9px; color:#555;">{time_str}</div>
                    <div style="font-size:13px; color:white; font-weight:bold;">{temp}°</div>
                    <div style="font-size:10px; color:{color};">{prob}%</div>
                </div>
                ''', unsafe_allow_html=True)

# --- 5. GRAFICO STORICO CON REGOLA "NO SOLE SE PIOVE" ---
st.write("")
st.markdown('<div style="color:#00FFFF; font-size:10px; text-align:center; letter-spacing:2px; margin-bottom:10px;">DRYING ANALYSIS (LAST 15 DAYS)</div>', unsafe_allow_html=True)

if hi_data and 'daily' in hi_data:
    df_hist = pd.DataFrame({
        'Data': hi_data['daily']['time'],
        'Pioggia': hi_data['daily']['precipitation_sum'],
        'Vento': hi_data['daily']['wind_speed_10m_max'],
        'Sole': hi_data['daily']['shortwave_radiation_sum']
    })

    # APPLICAZIONE REGOLA: Se Pioggia > 0.2mm, il Sole viene azzerato per quel giorno
    df_hist.loc[df_hist['Pioggia'] > 0.2, 'Sole'] = 0

    fig = go.Figure()

    # Sole (Asse Destro)
    fig.add_trace(go.Scatter(x=df_hist['Data'], y=df_hist['Sole'], name="Sole", fill='tozeroy', line_color='#FFFF00', opacity=0.3, yaxis="y2"))
    
    # Vento (Asse Sinistro)
    fig.add_trace(go.Scatter(x=df_hist['Data'], y=df_hist['Vento'], name="Vento", line=dict(color='#FF3311', width=2)))
    
    # Pioggia (Asse Sinistro)
    fig.add_trace(go.Bar(x=df_hist['Data'], y=df_hist['Pioggia'], name="Pioggia", marker_color='#007FFF'))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", y=1.15, x=0.5, xanchor="center"),
        yaxis=dict(title="mm / kmh", showgrid=False),
        yaxis2=dict(title="Sole", overlaying="y", side="right", showgrid=False)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

if st.button("🔄 RE-SYNC TARGET"):
    st.cache_data.clear()
    st.rerun()
