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
    ref_date = datetime(2024, 1, 1)
    delta_days = (current_time - ref_date).days
    num_sacro = (delta_days % 13) + 1
    simbolo_sacro = symbols[(delta_days + 12) % 20]
    countdown = (datetime(2027, 11, 15) - current_time).days
    return f"{num_sacro} {simbolo_sacro}", countdown

# --- 2. STILE CSS (LASER VIOLET-BLUE & COMPACT DESIGN) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100&display=swap');

    .stApp { background-color:#000; color: #eee; }
    
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    
    /* ICONA LASER PIEDRA DEL SOL: Grande e definita */
    .logo-laser {
        width: 180px; 
        height: 180px;
        margin-bottom: 5px;
        filter: drop-shadow(0 0 2px #007BFF);
    }

    /* TITOLO: Ultra sottile, compatto, gradiente laser */
    .header-text { 
        font-family: 'Inter', sans-serif; 
        font-weight: 100 !important;
        font-size: 26px;
        letter-spacing: 1px; 
        text-transform: uppercase;
        margin: 0;
        text-align: center;
        background: linear-gradient(90deg, #8A2BE2 0%, #007BFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        -webkit-font-smoothing: antialiased;
    }

    .radar-box { 
        position: relative; width: 100%; height: 400px; 
        border-radius: 4px; border: 1px solid #111; 
        overflow: hidden; margin-bottom: 20px; 
    }
    
    .clock-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 10px;
    }

    .digital-clock {
        color: #fff; font-family: 'Inter', sans-serif; 
        font-size: 32px; font-weight: 100;
    }

    .countdown-text {
        color: #8A2BE2; font-family: 'Inter', sans-serif; 
        font-size: 12px; letter-spacing: 4px; opacity: 0.6;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. UI GENERATION ---
now = datetime.now() + timedelta(hours=1)
day_lab, count_val = get_aztec_context(now)

# Header con Icona Piedra del Sol e Titolo Laser
st.markdown(f"""
<div class="header-container">
    <svg class="logo-laser" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="laserGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#8A2BE2;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#007BFF;stop-opacity:1" />
            </linearGradient>
        </defs>
        <circle cx="50" cy="50" r="48" stroke="url(#laserGrad)" stroke-width="0.5" fill="none" opacity="0.3"/>
        <circle cx="50" cy="50" r="38" stroke="url(#laserGrad)" stroke-width="0.8" fill="none" stroke-dasharray="1 2"/>
        
        <path d="M35 35 L45 45 M65 35 L55 45 M35 65 L45 55 M65 65 L55 55" stroke="url(#laserGrad)" stroke-width="0.5"/>
        
        <circle cx="50" cy="50" r="12" stroke="url(#laserGrad)" stroke-width="1" fill="none"/>
        <path d="M50 38 L50 62 M38 50 L62 50" stroke="url(#laserGrad)" stroke-width="1"/>
        <circle cx="50" cy="50" r="3" fill="url(#laserGrad)"/>
        
        <path d="M50 0 L50 10 M50 90 L50 100 M0 50 L10 50 M90 50 L100 50" stroke="url(#laserGrad)" stroke-width="0.8"/>
    </svg>
    <h1 class="header-text">Ceredotlan Tlachieloni</h1>
</div>
""", unsafe_allow_html=True)

# Radar
st.markdown(f'<div class="radar-box"><iframe src="https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&overlay=rain&product=iconEu&marker=true" width="100%" height="100%" frameborder="0"></iframe></div>', unsafe_allow_html=True)

# Orologio e Countdown
st.markdown(f"""
<div class="clock-section">
    <div class="digital-clock">{now.strftime("%H:%M")}<span style="color:#007BFF; font-size:14px; opacity:0.5;">:{now.second:02d}</span></div>
    <div style="color:#555; font-size:10px; letter-spacing:2px; margin-top:5px;">{day_lab.upper()}</div>
    <div class="countdown-text">{count_val} DAYS UNTIL RESET</div>
</div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
