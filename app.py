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

# --- 2. STILE CSS (LASER VIOLET-BLUE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100&display=swap');

    .stApp { background-color:#000; color: #eee; }
    
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 30px;
        margin-bottom: 30px;
    }
    
    /* Logo coordinato con gradiente laser */
    .logo-svg {
        width: 35px;
        height: 35px;
        margin-bottom: 15px;
    }

    /* TITOLO LASER: Sottilissimo, senza spaziatura larga, gradiente Viola/Blu */
    .header-text { 
        font-family: 'Inter', sans-serif; 
        font-weight: 100 !important;
        font-size: 22px;
        letter-spacing: 2px; /* Ridotto drasticamente per non essere "largo" */
        text-transform: uppercase;
        margin: 0;
        text-align: center;
        
        /* Gradiente Viola & Blu Elettrico */
        background: linear-gradient(90deg, #8A2BE2 0%, #007BFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        
        /* Effetto nitidezza laser */
        filter: drop-shadow(0 0 1px rgba(138, 43, 226, 0.8));
    }

    .radar-box { position: relative; width: 100%; height: 380px; border-radius: 2px; border: 1px solid #111; overflow: hidden; margin-bottom: 30px; }
    
    .aztec-wrapper {
        position: relative; width: 200px; height: 200px; margin: 20px auto; border-radius: 50%;
        background: url('https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Piedra_del_Sol.png/600px-Piedra_del_Sol.png') center/cover;
        filter: grayscale(1) brightness(0.08); display: flex; align-items: center; justify-content: center; border: 1px solid #080808;
    }
    
    .digital-clock {
        background: transparent; color: #fff;
        font-family: 'Inter', sans-serif; font-size: 24px; font-weight: 100; z-index: 5;
    }

    .rings-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; transform: rotate(-90deg); }
    .ring-circle { fill: none; stroke-linecap: round; }
    
    .xiuh-days { color: #007BFF; font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 100; opacity: 0.5; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGICA TEMPORALE ---
now = datetime.now() + timedelta(hours=1)
s, m, h = now.second, now.minute, now.hour

# --- 4. UI ---
day_lab, month_lab, year_lab, count_val = get_aztec_context(now)

# Header Laser
st.markdown(f"""
<div class="header-container">
    <svg class="logo-svg" viewBox="0 0 100 100">
        <defs>
            <linearGradient id="laserGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#8A2BE2;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#007BFF;stop-opacity:1" />
            </linearGradient>
        </defs>
        <circle cx="50" cy="50" r="45" stroke="url(#laserGrad)" stroke-width="1" fill="none" stroke-dasharray="2 4"/>
        <path d="M50 10 L50 90 M10 50 L90 50" stroke="url(#laserGrad)" stroke-width="1"/>
        <circle cx="50" cy="50" r="4" fill="url(#laserGrad)"/>
    </svg>
    <h1 class="header-text">Ceredotlan Tlachieloni</h1>
</div>
""", unsafe_allow_html=True)

# Radar
st.markdown(f'<div class="radar-box"><iframe src="https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&overlay=rain&product=iconEu&marker=true" width="100%" height="100%" frameborder="0"></iframe></div>', unsafe_allow_html=True)

# Orologio
off_h = 289.02 - (((h % 24) + m/60) * 289.02 / 24)
off_m = 251.32 - ((m + s/60) * 251.32 / 60)
off_s = 213.62 - (s * 213.62 / 60)

st.markdown(f"""
<div class="aztec-wrapper">
    <div class="digital-clock">{now.strftime("%H:%M")}<span style="color:#007BFF; font-size:12px; opacity:0.4;">:{s:02d}</span></div>
    <svg class="rings-svg" viewBox="0 0 100 100">
        <circle class="ring-circle" cx="50" cy="50" r="46" stroke="#8A2BE2" stroke-width="0.2" stroke-dasharray="289.02" stroke-dashoffset="{off_h}" opacity="0.2"/>
        <circle class="ring-circle" cx="50" cy="50" r="38" stroke="#007BFF" stroke-width="0.2" stroke-dasharray="238.76" stroke-dashoffset="{off_m}" opacity="0.3"/>
    </svg>
</div>
<div class="xiuh-days">{count_val} DAYS</div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
