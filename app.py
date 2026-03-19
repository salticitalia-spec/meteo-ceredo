import streamlit as st
import requests
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="Ceredotlan Tlachieloni", page_icon="🎯", layout="centered")

@st.cache_data(ttl=600)
def fetch_meteo():
    lat, lon = 45.6117, 10.9710
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability&models=icon_seamless&timezone=Europe%2FRome&forecast_days=2"
    try:
        return requests.get(url).json()
    except:
        return None

def get_aztec_context(current_time):
    symbols = ["Cipactli", "Ehecatl", "Calli", "Cuetzpalin", "Coatl", "Miquiztli", "Mazatl", "Tochtli", 
               "Atl", "Itzcuintli", "Ozomatli", "Malinalli", "Acatl", "Ocelotl", "Quauhtli", "Cozcaquauhtli", 
               "Olin", "Tecpatl", "Quiahuitl", "Xochitl"]
    months = ["Izcalli", "Atlcahualo", "Tlacaxipehualiztli", "Tozoztontli", "Huey Tozoztli", "Toxcatl", 
              "Etzalcualiztli", "Tecuilhuitontli", "Huey Tecuilhuitl", "Tlaxochimaco", "Xocotl Huetzi", 
              "Ochpaniztli", "Teotleco", "Tepeilhuitl", "Quecholli", "Panquetzaliztli", "Atemoztli", "Tititl"]
    years = ["Acatl", "Tecpatl", "Calli", "Tochtli"]

    ref_date = datetime(2024, 1, 1)
    delta_days = (current_time - ref_date).days
    num_sacro = (delta_days % 13) + 1
    simbolo_sacro = symbols[(delta_days + 12) % 20]
    month_idx = min(int(current_time.timetuple().tm_yday / 20), 17)
    year_num = ((current_time.year - 2024 + 11) % 13) + 1
    year_symbol = years[(current_time.year - 2024) % 4]
    countdown = (datetime(2027, 11, 15) - current_time).days
    return f"{num_sacro} {simbolo_sacro}", months[month_idx], f"{year_num} {year_symbol}", countdown

# --- 2. STILE CSS (ULTRA-THIN & MINIMAL CYAN) ---
st.markdown("""
<style>
    /* Importazione font a spessore minimo 100 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100&display=swap');

    .stApp { background-color:#000; color: #eee; }
    
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 50px;
        margin-bottom: 50px;
    }
    
    .logo-svg {
        width: 25px;
        height: 25px;
        margin-bottom: 25px;
        opacity: 0.9;
    }

    /* IL TITOLO RICHIESTO: Ultra sottile, ciano intenso, spaziatura ampia */
    .header-text { 
        color: #00FFFF; 
        font-size: 18px; 
        font-family: 'Inter', sans-serif; 
        font-weight: 100 !important; /* Forza lo spessore minimo */
        letter-spacing: 15px; 
        text-transform: uppercase;
        margin: 0;
        text-align: center;
        /* Ombra minima solo per dare profondità senza allargare il font */
        text-shadow: 0 0 1px #00FFFF;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    .radar-box { position: relative; width: 100%; height: 380px; border-radius: 2px; border: 1px solid #111; overflow: hidden; margin-bottom: 40px; }
    .crosshair { position: absolute; top: 50%; left: 50%; width: 20px; height: 20px; border: 0.5px solid rgba(255,0,0,0.3); border-radius: 50%; transform: translate(-50%, -50%); z-index: 10; pointer-events: none; }
    
    .aztec-wrapper {
        position: relative; width: 200px; height: 200px; margin: 30px auto; border-radius: 50%;
        background: url('https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Piedra_del_Sol.png/600px-Piedra_del_Sol.png') center/cover;
        filter: grayscale(1) brightness(0.1); display: flex; align-items: center; justify-content: center; border: 1px solid #080808;
    }
    
    .digital-clock {
        background: transparent; color: #fff;
        font-family: 'Inter', sans-serif; font-size: 26px; font-weight: 100; z-index: 5;
    }

    .rings-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; transform: rotate(-90deg); }
    .ring-circle { fill: none; stroke-linecap: round; transition: stroke-dashoffset 0.1s linear; }
    
    .aztec-info { text-align: center; margin-bottom: 25px; font-family: 'Inter', sans-serif; }
    .aztec-day { color: #333; font-size: 10px; font-weight: 100; letter-spacing: 6px; text-transform: uppercase; }
    
    .xiuh-box { text-align: center; margin: 20px auto; max-width: 200px; opacity: 0.5; }
    .xiuh-days { color: #100; font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 100; letter-spacing: 4px; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGICA TEMPORALE (+1 ORA) ---
now = datetime.now() + timedelta(hours=1)
s, m, h = now.second, now.minute, now.hour

# --- 4. UI ---
fc = fetch_meteo()
day_lab, month_lab, year_lab, count_val = get_aztec_context(now)

# Intestazione con Ciano Tagliente
st.markdown(f"""
<div class="header-container">
    <svg class="logo-svg" viewBox="0 0 100 100">
        <path d="M50 0 L50 100 M0 50 L100 50" stroke="#00FFFF" stroke-width="0.5" opacity="0.5"/>
        <circle cx="50" cy="50" r="5" fill="#00FFFF"/>
    </svg>
    <h1 class="header-text">Ceredotlan Tlachieloni</h1>
</div>
""", unsafe_allow_html=True)

# Radar
st.markdown(f'<div class="radar-box"><div class="crosshair"></div><iframe src="https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&overlay=rain&product=iconEu&marker=true" width="100%" height="100%" frameborder="0"></iframe></div>', unsafe_allow_html=True)

# Orologio e Calendario (Design Sottile)
off_h = 289.02 - (((h % 24) + m/60) * 289.02 / 24)
off_m = 251.32 - ((m + s/60) * 251.32 / 60)
off_s = 213.62 - (s * 213.62 / 60)

st.markdown(f"""
<div class="aztec-wrapper">
    <div class="digital-clock">{now.strftime("%H:%M")}<span style="color:#00FFFF; font-size:12px; opacity:0.3;">:{s:02d}</span></div>
    <svg class="rings-svg" viewBox="0 0 100 100">
        <circle class="ring-circle" cx="50" cy="50" r="46" stroke="#00FFFF" stroke-width="0.2" stroke-dasharray="289.02" stroke-dashoffset="{off_h}" opacity="0.1"/>
        <circle class="ring-circle" cx="50" cy="50" r="40" stroke="#00FFFF" stroke-width="0.2" stroke-dasharray="251.32" stroke-dashoffset="{off_m}" opacity="0.15"/>
        <circle class="ring-circle" cx="50" cy="50" r="34" stroke="#00FFFF" stroke-width="0.2" stroke-dasharray="213.62" stroke-dashoffset="{off_s}" opacity="0.3"/>
    </svg>
</div>

<div class="aztec-info">
    <div class="aztec-day">{day_lab}</div>
    <div style="color:#1a1a1a; font-size:8px; font-family:Inter; letter-spacing:3px; margin-top:5px;">{month_lab.upper()} | {year_lab.upper()}</div>
</div>

<div class="xiuh-box">
    <div class="xiuh-days">{count_val} DAYS</div>
</div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
