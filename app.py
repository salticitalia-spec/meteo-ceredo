import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE E DATI ---
st.set_page_config(page_title="Ceredoleso Yollotl", page_icon="❤️", layout="centered")

@st.cache_data(ttl=600)
def fetch_meteo():
    lat, lon = 45.6117, 10.9710
    # Fetch di 2 giorni per coprire il passaggio della mezzanotte nella timeline
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability&models=icon_seamless&timezone=Europe%2FRome&forecast_days=2"
    try:
        r = requests.get(url)
        return r.json()
    except Exception:
        return None

def get_aztec_context():
    symbols = ["Cipactli", "Ehecatl", "Calli", "Cuetzpalin", "Coatl", "Miquiztli", "Mazatl", "Tochtli", 
               "Atl", "Itzcuintli", "Ozomatli", "Malinalli", "Acatl", "Ocelotl", "Quauhtli", "Cozcaquauhtli", 
               "Olin", "Tecpatl", "Quiahuitl", "Xochitl"]
    months = ["Izcalli", "Atlcahualo", "Tlacaxipehualiztli", "Tozoztontli", "Huey Tozoztli", "Toxcatl", 
              "Etzalcualiztli", "Tecuilhuitontli", "Huey Tecuilhuitl", "Tlaxochimaco", "Xocotl Huetzi", 
              "Ochpaniztli", "Teotleco", "Tepeilhuitl", "Quecholli", "Panquetzaliztli", "Atemoztli", "Tititl"]
    years = ["Acatl", "Tecpatl", "Calli", "Tochtli"]

    today = datetime.now()
    ref_date = datetime(2024, 1, 1)
    delta_days = (today - ref_date).days
    
    num_sacro = (delta_days % 13) + 1
    simbolo_sacro = symbols[(delta_days + 12) % 20]
    month_idx = min(int(today.timetuple().tm_yday / 20), 17)
    year_num = ((today.year - 2024 + 11) % 13) + 1
    year_symbol = years[(today.year - 2024) % 4]
    countdown = (datetime(2027, 11, 15) - today).days
    
    return f"{num_sacro} {simbolo_sacro}", months[month_idx], f"{year_num} {year_symbol}", countdown

# --- 2. STILE CSS (YOLLOTL EDITION) ---
st.markdown("""
<style>
    @keyframes heart-beat {
        0% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
        15% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; border-color: #FF0000; }
        30% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
        45% { transform: translate(-50%, -50%) scale(1.1); opacity: 0.9; }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
    }

    .stApp { background-color:#000; color: #eee; }
    .header-text { 
        color:#FF3311; 
        font-size:24px; 
        text-align:center; 
        letter-spacing:5px; 
        margin-bottom:5px; 
        font-family:monospace; 
        text-shadow: 0 0 15px #600;
    }
    .radar-box { position: relative; width: 100%; height: 350px; border-radius: 15px; border: 2px solid #333; overflow: hidden; margin-bottom: 20px; }
    .crosshair { 
        position: absolute; top: 50%; left: 50%; width: 45px; height: 45px; 
        border: 2px solid #FF3311; border-radius: 50%; 
        transform: translate(-50%, -50%); z-index: 10; pointer-events: none;
        animation: heart-beat 1.5s infinite ease-in-out;
    }
    .aztec-wrapper {
        position: relative; width: 260px; height: 260px; margin: 20px auto; border-radius: 50%;
        background: url('https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Piedra_del_Sol.png/600px-Piedra_del_Sol.png') center/cover;
        filter: sepia(0.4) brightness(0.6); display: flex; align-items: center; justify-content: center; border: 2px solid #222;
    }
    .digital-clock {
        background: rgba(0,0,0,0.85); padding: 5px 12px; border-radius: 8px; color: #fff;
        font-family: monospace; font-size: 24px; font-weight: bold; border: 1px solid #400; z-index: 5;
    }
    .rings-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; transform: rotate(-90deg); }
    .ring-circle { fill: none; stroke-linecap: round; transition: stroke-dashoffset 0.5s ease; }
    
    .aztec-info { text-align: center; margin-bottom: 20px; }
    .aztec-day { color: #A52; font-size: 16px; font-family: monospace; font-weight: bold; text-transform: uppercase;}
    
    .xiuh-box { 
        text-align: center; margin: 10px auto; padding: 15px; border: 1px solid #800; 
        background: rgba(50,0,0,0.2); border-radius: 10px; max-width: 280px;
        box-shadow: inset 0 0 10px #400;
    }
    .xiuh-days { color: #FF3311; font-family: monospace; font-size: 28px; font-weight: bold; text-shadow: 0 0 5px #F00; }
</style>
""", unsafe_allow_html=True)

# --- 3. UI LOGIC ---
fc = fetch_meteo()
day_lab, month_lab, year_lab, count_val = get_aztec_context()

# Titolo Yollotl
st.markdown('<div class="header-text">CEREDOLESO YOLLOTL</div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; margin-top:-10px; margin-bottom:15px;">
    <span style="color:#600; font-size:11px; letter-spacing:3px; font-weight:bold;">EL CORAZÓN DEL SACRIFICIO</span>
</div>
""", unsafe_allow_html=True)

# Radar con mirino pulsante
st.markdown(f'''
<div class="radar-box">
    <div class="crosshair"></div>
    <iframe src="https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=10&overlay=rain&product=iconEu&marker=true" 
    width="100%" height="100%" frameborder="0"></iframe>
</div>
''', unsafe_allow_html=True)

# Timeline 6h (Sicurezza anti-IndexError garantita dal fetch_days=2)
if fc and 'hourly' in fc:
    cols = st.columns(6)
    now_dt = datetime.now()
    h_now = now_dt.hour
    
    for i in range(6):
        idx = h_now + i
        with cols[i]:
            prob = fc['hourly']['precipitation_probability'][idx]
            t_str = fc['hourly']['time'][idx][-5:]
            # Colore dinamico: dal verde al rosso sangue
            color = '#FF3311' if prob > 30 else '#00FFCC'
            st.markdown(f"""
                <div style='text-align:center; font-family:monospace;'>
                    <span style='font-size:10px; color:#666;'>{t_str}</span><br>
                    <b style='color:{color}; font-size:14px;'>{prob}%</b>
                </div>
            """, unsafe_allow_html=True)

# Orologio e Calcoli Anelli
n = datetime.now()
s = n.second
# Calcolo gradi per dashoffset (SVG circles)
off_h = 289.02 - (((n.hour % 24) + n.minute/60) * 289.02 / 24)
off_m = 251.32 - ((n.minute + s/60) * 251.32 / 60)
off_s = 213.62 - (s * 213.62 / 60)

st.markdown(f"""
<div class="aztec-wrapper">
    <div class="digital-clock">{n.strftime("%H:%M")}<span style="color:#FF3311; font-size:16px;">:{s:02d}</span></div>
    <svg class="rings-svg" viewBox="0 0 100 100">
        <circle class="ring-circle" cx="50" cy="50" r="46" stroke="#00FFFF" stroke-width="1.5" stroke-dasharray="289.02" stroke-dashoffset="{off_h}" opacity="0.2"/>
        <circle class="ring-circle" cx="50" cy="50" r="40" stroke="#007FFF" stroke-width="2" stroke-dasharray="251.32" stroke-dashoffset="{off_m}" opacity="0.4"/>
        <circle class="ring-circle" cx="50" cy="50" r="34" stroke="#FF3311" stroke-width="2.5" stroke-dasharray="213.62" stroke-dashoffset="{off_s}" opacity="0.8"/>
    </svg>
</div>
<div style="text-align:center; color:#333; font-size:9px; letter-spacing:4px; font-weight:bold; margin-top:-10px; font-family:monospace;">TIEMPO ETERNO DE CEREDO</div>

<div class="aztec-info">
    <div class="aztec-day">{day_lab}</div>
    <div style="color:#555; font-size:10px; font-family:monospace;">METZTLI: {month_lab} | XIHUATL: {year_lab}</div>
</div>

<div class="xiuh-box">
    <div style="color:#844; font-size:10px; letter-spacing:2px; font-weight:bold;">OFFERTA DI YOLLOTL</div>
    <div class="xiuh-days">{count_val} GIORNI</div>
    <div style="color:#600; font-size:9px; font-family:monospace;">AL SACRIFICIO DEL FUOCO NUOVO</div>
</div>
""", unsafe_allow_html=True)

# Auto-refresh ogni secondo per l'orologio
time.sleep(1)
st.rerun()
