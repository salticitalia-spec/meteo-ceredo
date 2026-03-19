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

# --- 2. STILE CSS (LASER VIOLET-BLUE & COMPACT) ---
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
    
    /* ICONA PIEDRA DEL SOL LASER */
    .logo-laser {
        width: 160px; 
        height: 160px;
        margin-bottom: 5px;
    }

    /* TITOLO: Ultra sottile, compatto, gradiente laser */
    .header-text { 
        font-family: 'Inter', sans-serif; 
        font-weight: 100 !important;
        font-size: 24px;
        letter-spacing: 1px; /* Compatto come richiesto */
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
        margin-top: 5px;
    }

    .digital-clock {
        color: #fff; font-family: 'Inter', sans-serif; 
        font-size: 30px; font-weight: 100;
    }

    .aztec-day-label {
        color: #444; font-family: 'Inter', sans-serif;
        font-size: 10px; letter-spacing: 3px; margin-top: 2px;
    }

    .countdown-text {
        color: #8A2BE2; font-family: 'Inter', sans-serif; 
        font-size: 12px; letter-spacing: 4px; opacity: 0.5;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGICA TEMPORALE ---
now = datetime.now() + timedelta(hours=1)
day_lab, count_val = get_aztec_context(now)

# --- 4. INTERFACCIA ---

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
        
        <circle cx="50" cy="50" r="48" stroke="url(#laserGrad)" stroke-width="0.3" fill="none" opacity="0.3"/>
        <circle cx="50" cy="50" r="42" stroke="url(#laserGrad)" stroke-width="0.5" fill="none" stroke-dasharray="1 3"/>
        <circle cx="50" cy="50" r="32" stroke="url(#laserGrad)" stroke-width="0.4" fill="none"/>
        
        <path d="M32 32 L42 42 M68 32 L58 42 M32 68 L42 58 M68 68 L58 58" stroke="url(#laserGrad)" stroke-width="0.8"/>
        <rect x="44" y="44" width="12" height="12" stroke="url(#laserGrad)" stroke-width="0.5" fill="none" transform="rotate(45 50 50)"/>
        
        <circle cx="50" cy="50" r="10" stroke="url(#laserGrad)" stroke-width="1.2" fill="none"/>
        <path d="M50 35 L50 65 M35 50 L
