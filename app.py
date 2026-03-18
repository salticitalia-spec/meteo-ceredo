import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Ceredoleso Sniper", page_icon="🎯", layout="centered")

@st.cache_data(ttl=600)
def fetch_all_data():
    lat, lon = 45.6117, 10.9710
    url_fc = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability&models=icon_seamless&timezone=Europe%2FRome&forecast_days=1"
    end = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
    url_hi = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start}&end_date={end}&daily=precipitation_sum,wind_speed_10m_max,shortwave_radiation_sum&timezone=Europe%2FRome"
    return requests.get(url_fc).json(), requests.get(hi_url := url_hi).json()

def get_aztec_date():
    # 20 Simboli dei Giorni
    symbols = ["Cipactli", "Ehecatl", "Calli", "Cuetzpalin", "Coatl", "Miquiztli", "Mazatl", "Tochtli", 
               "Atl", "Itzcuintli", "Ozomatli", "Malinalli", "Acatl", "Ocelotl", "Quauhtli", "Cozcaquauhtli", 
               "Olin", "Tecpatl", "Quiahuitl", "Xochitl"]
    
    # 18 Mesi del Calendario Solare (Xiuhpohualli)
    months = ["Izcalli", "Atlcahualo", "Tlacaxipehualiztli", "Tozoztontli", "Huey Tozoztli", "Toxcatl", 
              "Etzalcualiztli", "Tecuilhuitontli", "Huey Tecuilhuitl", "Tlaxochimaco", "Xocotl Huetzi", 
              "Ochpaniztli", "Teotleco", "Tepeilhuitl", "Quecholli", "Panquetzaliztli", "Atemoztli", "Tititl"]

    ref_date = datetime(2024, 1, 1)
    today = datetime.now()
    delta_days = (today - ref_date).days
    
    # Calcolo Giorno Sacro (Tonalpohualli)
    num_sacro = (delta_days % 13) + 1
    simbolo_sacro = symbols[(delta_days + 12) % 20]
    
    # Calcolo Mese Solare (Xiuhpohualli - approssimativo su ciclo 365)
    day_of_year = today.timetuple().tm_yday
    month_idx = min(int(day_of_year / 20), 17)
    current_month = months[month_idx]
    
    return f"{num_sacro} {simbolo_sacro}", current_month

# --- 2. STILE CSS ---
st.markdown("""
<style>
    .stApp { background-color:#000; }
    .header-text { color:#00FFFF; font-size:22px; text-align:center; letter-spacing:5px; margin:10px 0; font-family:monospace; }
    .radar-box { position: relative; width: 100%; height: 380px; border-radius: 15px; border: 2px solid #333; overflow: hidden; margin-bottom: 20px; }
    .crosshair { position: absolute; top: 50%; left: 50%; width: 50px; height: 50px; border: 2px solid #FF0000; border-radius: 50%; transform: translate(-50%, -50%); z-index: 10; pointer-events: none; }
    .dot { position: absolute; top: 50%; left: 50%; width: 6px; height: 6px; background: #FF0000; border-radius: 50%; transform: translate(-50%, -50%); box-shadow: 0 0 10px #FF0000; }
    
    .aztec-wrapper {
        position: relative; width: 280px; height: 280px; margin: 20px auto 10px auto; border-radius: 50%;
        background: url('https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Piedra_del_Sol.png/600px-Piedra_del_Sol.png') center/cover;
        filter: sepia(0.4) brightness(0.8); display: flex; align-items: center; justify-content: center; border: 3px solid #222;
    }
    .digital-clock {
        background: rgba(0,0,0,0.8); padding: 8px 15px; border-radius: 10px; color: #fff;
        font-family: monospace; font-size: 26px; font-weight: bold; border: 1px solid #444; text-shadow: 0 0 8px #00FFFF; z-index: 5;
    }
    .rings-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; transform: rotate(-90deg); }
    .ring-circle { fill: none; stroke-linecap: round; transition: stroke-dashoffset 0.5s ease; }
    
    .footer-label { text-align: center; color: #555; font-size: 11px; font-family: monospace; letter-spacing: 6px; font-weight: bold; margin-top: -5px; }
    .aztec-info-box { text-align: center; margin-top: 10px; margin-bottom: 40px; }
    .aztec-day { color: #840; font-size: 14px; font-family: 'Courier New', monospace; font-weight: bold; text-transform: uppercase; }
    .aztec-month { color: #555; font-size: 10px; font-family: monospace; letter-spacing: 2px; }
</style>
""", unsafe_allow_html=True)

# --- 3. DATI E UI ---
fc, hi = fetch_all_data()
st.markdown('<div class="header-text">Ceredoleso Sniper</div>', unsafe_allow_html=True)

# Radar
radar_src = "https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&overlay=rain&product=iconEu&marker=true"
st.markdown(f'<div class="radar-box"><div class="crosshair"><div class="dot"></div></div><iframe src="{radar_src}" width="100%" height="100%" frameborder="0"></iframe></div>', unsafe_allow_html=True)

# Timeline 12h
if fc and 'hourly' in fc:
    cols = st.columns(6)
    h_start = datetime.now().hour
    for i in range(12):
        idx = h_start + i
        if idx < len(fc['hourly']['time']):
            with cols[i % 6]:
                p = fc['hourly']['precipitation_probability'][idx]
                st.markdown(f"""<div style="text-align:center; font-size:9px; color:#888;">{fc['hourly']['time'][idx][-5:]}<br>
                <b style="color:white">{fc['hourly']['temperature_2m'][idx]}°</b><br>
                <span style="color:{'#F31' if p > 30 else '#0F0'}">{p}%</span></div>""", unsafe_allow_html=True)

# Grafico Storico
if hi and 'daily' in hi:
    df = pd.DataFrame({'D': hi['daily']['time'], 'P': hi['daily']['precipitation_sum'], 'V': hi['daily']['wind_speed_10m_max']})
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['D'], y=df['P'], marker_color='#007FFF'))
    fig.add_trace(go.Scatter(x=df['D'], y=df['V'], line=dict(color='#FF3311', width=2)))
    fig.update_layout(template="plotly_dark", height=180, margin=dict(l=0,r=0,t=10,b=0), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Orologio e Calendario Azteco
n = datetime.now()
s = n.second
c_h, c_m, c_s = 289.02, 251.32, 213.62
off_h = c_h - (((n.hour % 24) + n.minute/60) * c_h / 24)
off_m = c_m - ((n.minute + s/60) * c_m / 60)
off_s = c_s - (s * c_s / 60)

day_label, month_label = get_aztec_date()

st.markdown(f"""
<div class="aztec-wrapper">
    <div class="digital-clock">{n.strftime("%H:%M")}<span style="color:#F31; font-size:16px;">:{s:02d}</span></div>
    <svg class="rings-svg" viewBox="0 0 100 100">
        <circle class="ring-circle" cx="50" cy="50" r="46" stroke="#00FFFF" stroke-width="2.5" stroke-dasharray="289.02" stroke-dashoffset="{off_h}" opacity="0.4"/>
        <circle class="ring-circle" cx="50" cy="50" r="40" stroke="#007FFF" stroke-width="2.5" stroke-dasharray="251.32" stroke-dashoffset="{off_m}" opacity="0.6"/>
        <circle class="ring-circle" cx="50" cy="50" r="34" stroke="#FF3311" stroke-width="2.5" stroke-dasharray="213.62" stroke-dashoffset="{off_s}" opacity="0.8"/>
    </svg>
</div>
<div class="footer-label">TIEMPO ETERNO DE CEREDO</div>
<div class="aztec-info-box">
    <div class="aztec-day">{day_label}</div>
    <div class="aztec-month">MES DE {month_label}</div>
</div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
