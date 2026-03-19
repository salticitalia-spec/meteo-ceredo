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

# --- 2. STILE CSS (MINIMALISTA) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300&display=swap');

    .stApp { background-color:#000; color: #eee; }
    
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-top: 10px;
        margin-bottom: 25px;
    }
    
    .logo-svg {
        width: 35px;
        height: 35px;
        fill: #00FFFF;
        filter: drop-shadow(0 0 2px rgba(0, 255, 255, 0.5));
    }

    .header-text { 
        color: #00FFFF; 
        font-size: 20px; 
        font-family: 'Inter', sans-serif; 
        font-weight: 200; /* Carattere ultra-sottile */
        letter-spacing: 5px; 
        text-transform: uppercase;
        margin: 0;
        opacity: 0.9;
    }

    .radar-box { position: relative; width: 100%; height: 350px; border-radius: 12px; border: 1px solid #222; overflow: hidden; margin-bottom: 20px; }
    .crosshair { position: absolute; top: 50%; left: 50%; width: 30px; height: 30px; border: 1px solid #FF0000; border-radius: 50%; transform: translate(-50%, -50%); z-index: 10; pointer-events: none; opacity: 0.5; }
    
    .aztec-wrapper {
        position: relative; width: 240px; height: 240px; margin: 20px auto; border-radius: 50%;
        background: url('https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Piedra_del_Sol.png/600px-Piedra_del_Sol.png') center/cover;
        filter: grayscale(1) contrast(1.2) brightness(0.4); display: flex; align-items: center; justify-content: center; border: 1px solid #222;
    }
    
    .digital-clock {
        background: rgba(0,0,0,0.9); padding: 5px 12px; border-radius: 4px; color: #fff;
        font-family: 'Inter', sans-serif; font-size: 22px; font-weight: 200; border: 1px solid #333; z-index: 5;
    }

    .rings-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; transform: rotate(-90deg); }
    .ring-circle { fill: none; stroke-linecap: round; transition: stroke-dashoffset 0.1s linear; }
    
    .aztec-info { text-align: center; margin-bottom: 15px; font-family: 'Inter', sans-serif; }
    .aztec-day { color: #888; font-size: 14px; font-weight: 300; letter-spacing: 2px; text-transform: uppercase; }
    
    .xiuh-box { 
        text-align: center; margin: 10px auto; padding: 10px; border: 1px solid #300; 
        background: rgba(20,0,0,0.2); border-radius: 8px; max-width: 250px;
    }
    .xiuh-days { color: #C00; font-family: 'Inter', sans-serif; font-size: 20px; font-weight: 200; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGICA TEMPORALE (+1 ORA) ---
now = datetime.now() + timedelta(hours=1)
s, m, h = now.second, now.minute, now.hour

# --- 4. UI ---
fc = fetch_meteo()
day_lab, month_lab, year_lab, count_val = get_aztec_context(now)

# Intestazione con Logo Vettoriale (Glifo del Sole)
st.markdown(f"""
<div class="header-container">
    <svg class="logo-svg" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="10" />
        <path d="M50 20 L50 35 M50 65 L50 80 M20 50 L35 50 M65 50 L80 50 M28 28 L38 38 M62 62 L72 72 M28 72 L38 62 M62 28 L72 38" stroke="#00FFFF" stroke-width="4"/>
        <circle cx="50" cy="50" r="45" fill="none" stroke="#00FFFF" stroke-width="1" stroke-dasharray="4 4"/>
    </svg>
    <h1 class="header-text">Ceredotlan Tlachieloni</h1>
</div>
""", unsafe_allow_html=True)

# Radar
st.markdown(f'<div class="radar-box"><div class="crosshair"></div><iframe src="https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&overlay=rain&product=iconEu&marker=true" width="100%" height="100%" frameborder="0"></iframe></div>', unsafe_allow_html=True)

# Timeline 6h
if fc and 'hourly' in fc:
    cols = st.columns(6)
    for i in range(6):
        idx = h + i
        if idx < len(fc['hourly']['precipitation_probability']):
            with cols[i]:
                p = fc['hourly']['precipitation_probability'][idx]
                time_label = fc['hourly']['time'][idx][-5:]
                st.markdown(f"<div style='text-align:center; font-size:10px; font-family:Inter; color:#666;'>{time_label}<br><b style='color:{'#F31' if p > 30 else '#0F0'}'>{p}%</b></div>", unsafe_allow_html=True)

# Orologio
off_h = 289.02 - (((h % 24) + m/60) * 289.02 / 24)
off_m = 251.32 - ((m + s/60) * 251.32 / 60)
off_s = 213.62 - (s * 213.62 / 60)

st.markdown(f"""
<div class="aztec-wrapper">
    <div class="digital-clock">{now.strftime("%H:%M")}<span style="color:#00FFFF; font-size:14px; opacity:0.5;">:{s:02d}</span></div>
    <svg class="rings-svg" viewBox="0 0 100 100">
        <circle class="ring-circle" cx="50" cy="50" r="46" stroke="#00FFFF" stroke-width="1" stroke-dasharray="289.02" stroke-dashoffset="{off_h}" opacity="0.2"/>
        <circle class="ring-circle" cx="50" cy="50" r="40" stroke="#00FFFF" stroke-width="1" stroke-dasharray="251.32" stroke-dashoffset="{off_m}" opacity="0.4"/>
        <circle class="ring-circle" cx="50" cy="50" r="34" stroke="#00FFFF" stroke-width="1" stroke-dasharray="213.62" stroke-dashoffset="{off_s}" opacity="0.6"/>
    </svg>
</div>
<div style="text-align:center; color:#333; font-size:9px; letter-spacing:5px; font-family:Inter; margin-top:-10px;">CEREDOTLAN OBSERVATORY</div>

<div class="aztec-info">
    <div class="aztec-day">{day_lab}</div>
    <div style="color:#444; font-size:9px; font-family:Inter; letter-spacing:1px;">{month_lab.upper()} | {year_lab.upper()}</div>
</div>

<div class="xiuh-box">
    <div style="color:#522; font-size:9px; letter-spacing:2px; font-family:Inter;">XIUHMOLPILLI COUNTDOWN</div>
    <div class="xiuh-days">{count_val} DAYS</div>
</div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
