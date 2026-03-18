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
    return requests.get(url_fc).json(), requests.get(url_hi).json()

def get_aztec_day():
    # I 20 simboli dei giorni aztechi (Tonalpohualli)
    symbols = ["Cipactli (Coccodrillo)", "Ehecatl (Vento)", "Calli (Casa)", "Cuetzpalin (Lucertola)", 
               "Coatl (Serpente)", "Miquiztli (Morte)", "Mazatl (Cervo)", "Tochtli (Coniglio)", 
               "Atl (Acqua)", "Itzcuintli (Cane)", "Ozomatli (Scimmia)", "Malinalli (Erba)", 
               "Acatl (Canna)", "Ocelotl (Giaguaro)", "Quauhtli (Aquila)", "Cozcaquauhtli (Avvoltoio)", 
               "Olin (Movimento)", "Tecpatl (Coltello)", "Quiahuitl (Pioggia)", "Xochitl (Fiore)"]
    
    # Data di riferimento (01-01-2024 era un giorno 'Canna')
    ref_date = datetime(2024, 1, 1)
    delta_days = (datetime.now() - ref_date).days
    
    # Calcolo dell'indice (ciclo di 20 giorni)
    symbol_idx = (delta_days + 12) % 20  # +12 è il correttivo basato sulla correlazione glifica
    # Calcolo del numero sacro (ciclo di 13 numeri)
    number_idx = (delta_days + 0) % 13 + 1
    
    return f"{number_idx} - {symbols[symbol_idx]}"

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
    .aztec-day-label { text-align: center; color: #840; font-size: 13px; font-family: 'Courier New', monospace; font-weight: bold; margin-bottom: 30px; margin-top: 5px; text-transform: uppercase; }
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

# Orologio e Segno del Giorno
n = datetime.now()
s = n.second
c_h, c_m, c_s = 289.02, 251.32, 213.62
off_h = c_h - (((n.hour % 24) + n.minute/60) * c_h / 24)
off_m = c_m - ((n.minute + s/60) * c_m / 60)
off_s = c_s - (s * c_s / 60)

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
<div class="aztec-day-label">{get_aztec_day()}</div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
