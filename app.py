import streamlit as st
import requests
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Ceredotlan Tlachieloni", page_icon="🎯", layout="centered")

@st.cache_data(ttl=600)
def fetch_meteo():
    lat, lon = 45.6117, 10.9710
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability&models=icon_seamless&timezone=Europe%2FRome&forecast_days=2"
    try:
        response = requests.get(url, timeout=5)
        return response.json()
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

# --- 2. STILE CSS (MONO-WEIGHT LASER) ---
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
        margin-bottom: 25px;
    }
    
    /* LOGO LASER: Spessori Identici 0.5px */
    .logo-laser {
        width: 160px; 
        height: 160px;
        margin-bottom: 8px;
    }

    .header-text { 
        font-family: 'Inter', sans-serif; 
        font-weight: 100 !important;
        font-size: 24px;
        letter-spacing: 1px; 
        text-transform: uppercase;
        margin: 0;
        text-align: center;
        background: linear-gradient(90deg, #8A2BE2 0%, #007BFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .radar-box { 
        position: relative; width: 100%; height: 400px; 
        border-radius: 4px; border: 1px solid #111; 
        overflow: hidden; margin-bottom: 30px; 
    }
    
    .clock-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 20px;
    }

    .digital-clock {
        color: #fff; font-family: 'Inter', sans-serif; 
        font-size: 34px; font-weight: 100;
    }

    .countdown-text {
        color: #8A2BE2; font-family: 'Inter', sans-serif; 
        font-size: 12px; letter-spacing: 4px; opacity: 0.6;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGICA TEMPORALE ---
now = datetime.now() + timedelta(hours=1)
day_lab, count_val = get_aztec_context(now)

# --- 4. INTERFACCIA ---

# Header con Spessori Costanti (0.5)
st.markdown(f"""
<div class="header-container">
    <svg class="logo-laser" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="laserGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#8A2BE2;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#007BFF;stop-opacity:1" />
            </linearGradient>
        </defs>
        
        <circle cx="50" cy="50" r="48" stroke="url(#laserGrad)" stroke-width="0.5" fill="none" />
        <circle cx="50" cy="50" r="40" stroke="url(#laserGrad)" stroke-width="0.5" fill="none" stroke-dasharray="2 2"/>
        <circle cx="50" cy="50" r="32" stroke="url(#laserGrad)" stroke-width="0.5" fill="none"/>
        
        <path d="M35 35 L45 45 M65 35 L55 45 M35 65 L45 55 M65 65 L55 55" stroke="url(#laserGrad)" stroke-width="0.5"/>
        
        <circle cx="50" cy="50" r="12" stroke="url(#laserGrad)" stroke-width="0.5" fill="none"/>
        <path d="M50 30 L50 70 M30 50 L70 50" stroke="url(#laserGrad)" stroke-width="0.5"/>
        <circle cx="50" cy="50" r="2.5" fill="url(#laserGrad)"/>
        
        <path d="M50 0 L50 100 M0 50 L100 50" stroke="url(#laserGrad)" stroke-width="0.5" opacity="0.4"/>
    </svg>
    <h1 class="header-text">Ceredotlan Tlachieloni</h1>
</div>
""", unsafe_allow_html=True)

# Radar
st.markdown(f'<div class="radar-box"><iframe src="https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&overlay=rain&product=iconEu&marker=true" width="100%" height="100%" frameborder="0"></iframe></div>', unsafe_allow_html=True)

# Sezione Orologio
st.markdown(f"""
<div class="clock-section">
    <div class="digital-clock">
        {now.strftime("%H:%M")}<span style="color:#007BFF; font-size:16px; opacity:0.6;">:{now.second:02d}</span>
    </div>
    <div style="color:#444; font-size:10px; letter-spacing:3px;">{day_lab.upper()}</div>
    <div class="countdown-text">{count_val} DAYS</div>
</div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
