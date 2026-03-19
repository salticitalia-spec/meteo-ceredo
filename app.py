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

def get_full_aztec_date(current_time):
    # Simboli Tonalpohualli (Giorno)
    symbols = ["Cipactli", "Ehecatl", "Calli", "Cuetzpalin", "Coatl", "Miquiztli", "Mazatl", "Tochtli", 
               "Atl", "Itzcuintli", "Ozomatli", "Malinalli", "Acatl", "Ocelotl", "Quauhtli", "Cozcaquauhtli", 
               "Olin", "Tecpatl", "Quiahuitl", "Xochitl"]
    
    # Mesi Xiuhpohualli (20 giorni ciascuno)
    months = ["Izcalli", "Atlcahualo", "Tlacaxipehualiztli", "Tozoztontli", "Huey Tozoztli", "Toxcatl", 
              "Etzalcualiztli", "Tecuilhuitontli", "Huey Tecuilhuitl", "Tlaxochimaco", "Xocotl Huetzi", 
              "Ochpaniztli", "Teotleco", "Tepeilhuitl", "Quecholli", "Panquetzaliztli", "Atemoztli", "Tititl"]
    
    # Anni (Ciclo di 52 anni)
    year_carriers = ["Tecpatl", "Calli", "Tochtli", "Acatl"]
    
    ref_date = datetime(2024, 1, 1) # Riferimento: 1 Tecpatl
    delta_days = (current_time - ref_date).days
    
    # Calcolo Giorno (Tonalpohualli)
    num_day = (delta_days % 13) + 1
    sym_day = symbols[(delta_days + 12) % 20]
    
    # Calcolo Mese (Xiuhpohualli - approssimativo per visualizzazione)
    month_idx = (delta_days % 365) // 20
    current_month = months[min(month_idx, 17)]
    
    # Calcolo Anno
    year_num = ((delta_days // 365) % 13) + 1
    year_sym = year_carriers[(delta_days // 365) % 4]
    
    countdown = (datetime(2027, 11, 15) - current_time).days
    
    full_date = f"{num_day} {sym_day} • {current_month} • {year_num} {year_sym}"
    return full_date, countdown

# --- 2. STILE CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100&display=swap');
    .stApp { background-color:#000; color: #eee; }
    .header-container { display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 10px; margin-bottom: 25px; }
    .logo-laser { width: 160px; height: 160px; margin-bottom: 10px; }
    .header-text { 
        font-family: 'Inter', sans-serif; font-weight: 100 !important; font-size: 24px; letter-spacing: 1px; 
        text-transform: uppercase; margin: 0; text-align: center;
        background: linear-gradient(90deg, #8A2BE2 0%, #007BFF 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .radar-box { position: relative; width: 100%; height: 400px; border-radius: 4px; border: 1px solid #111; overflow: hidden; margin-bottom: 30px; }
    .clock-section { display: flex; flex-direction: column; align-items: center; margin-top: 10px; padding-bottom: 40px; }
    .digital-clock { color: #fff; font-family: 'Inter', sans-serif; font-size: 38px; font-weight: 100; letter-spacing: 2px; }
    .aztec-full-date { color: #555; font-family: 'Inter', sans-serif; font-size: 11px; letter-spacing: 3px; margin-top: 8px; text-transform: uppercase; }
    .countdown-text { color: #8A2BE2; font-family: 'Inter', sans-serif; font-size: 13px; letter-spacing: 5px; opacity: 0.6; margin-top: 18px; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGICA TEMPORALE ---
now = datetime.now() + timedelta(hours=1)
full_aztec, count_val = get_full_aztec_date(now)

# --- 4. INTERFACCIA ---
# Logo Laser 0.5 e Titolo
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

# Orologio e Data Azteca Ripristinata
st.markdown(f"""
<div class="clock-section">
    <div class="digital-clock">
        {now.strftime("%H:%M")}<span style="color:#007BFF; font-size:18px; opacity:0.6;">:{now.second:02d}</span>
    </div>
    <div class="aztec-full-date">{full_aztec}</div>
    <div class="countdown-text">{count_val} DAYS UNTIL RESET</div>
</div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
