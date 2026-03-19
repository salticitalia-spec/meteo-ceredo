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

def get_aztec_data(current_time):
    symbols = ["Cipactli", "Ehecatl", "Calli", "Cuetzpalin", "Coatl", "Miquiztli", "Mazatl", "Tochtli", 
               "Atl", "Itzcuintli", "Ozomatli", "Malinalli", "Acatl", "Ocelotl", "Quauhtli", "Cozcaquauhtli", 
               "Olin", "Tecpatl", "Quiahuitl", "Xochitl"]
    months = ["Izcalli", "Atlcahualo", "Tlacaxipehualiztli", "Tozoztontli", "Huey Tozoztli", "Toxcatl", 
              "Etzalcualiztli", "Tecuilhuitontli", "Huey Tecuilhuitl", "Tlaxochimaco", "Xocotl Huetzi", 
              "Ochpaniztli", "Teotleco", "Tepeilhuitl", "Quecholli", "Panquetzaliztli", "Atemoztli", "Tititl"]
    year_carriers = ["Tecpatl", "Calli", "Tochtli", "Acatl"]
    
    ref_date = datetime(2024, 1, 1)
    delta_days = (current_time - ref_date).days
    
    # Angoli per la rotazione grafica
    angle_day = ((delta_days + 12) % 20) * 18  # 360/20
    angle_trecena = (delta_days % 13) * (360/13)
    
    num_day = (delta_days % 13) + 1
    sym_day = symbols[(delta_days + 12) % 20]
    current_month = months[min((delta_days % 365) // 20, 17)]
    year_num = ((delta_days // 365) % 13) + 1
    year_sym = year_carriers[(delta_days // 365) % 4]
    
    countdown = (datetime(2027, 11, 15) - current_time).days
    
    return {
        "angles": [angle_day, angle_trecena],
        "label": f"{num_day} {sym_day} • {current_month} • {year_num} {year_sym}",
        "days": countdown,
        "current_sym": sym_day
    }

# --- 2. STILE CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100&display=swap');
    .stApp { background-color:#000; color: #eee; }
    .header-container { display: flex; flex-direction: column; align-items: center; margin-bottom: 25px; }
    .logo-laser { width: 140px; height: 140px; }
    .header-text { 
        font-family: 'Inter', sans-serif; font-weight: 100; font-size: 24px; letter-spacing: 2px; 
        text-transform: uppercase; background: linear-gradient(90deg, #8A2BE2 0%, #007BFF 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .radar-box { width: 100%; height: 380px; border: 1px solid #111; border-radius: 4px; overflow: hidden; margin-bottom: 30px; }
    .clock-wrapper { display: flex; flex-direction: column; align-items: center; position: relative; padding-top: 20px; }
    .aztec-svg { width: 320px; height: 320px; }
    .digital-center {
        position: absolute; top: 42%; left: 50%; transform: translate(-50%, -50%);
        text-align: center; font-family: 'Inter', sans-serif; width: 100%;
    }
    .time-h { color: #fff; font-size: 38px; font-weight: 100; }
    .time-m { color: #007BFF; font-size: 38px; font-weight: 100; }
    .time-s { color: #8A2BE2; font-size: 20px; font-weight: 100; margin-left: 5px; }
    .sub-label { color: #444; font-size: 11px; letter-spacing: 3px; margin-top: 140px; text-transform: uppercase; text-align: center; }
    .cd-reset { color: #8A2BE2; font-size: 11px; letter-spacing: 5px; opacity: 0.4; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGICA ---
now = datetime.now() + timedelta(hours=1)
az = get_aztec_data(now)

# --- 4. INTERFACCIA ---
# Logo Superiore
st.markdown(f"""
<div class="header-container">
    <svg class="logo-laser" viewBox="0 0 100 100">
        <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#8A2BE2" /><stop offset="100%" style="stop-color:#007BFF" /></linearGradient></defs>
        <circle cx="50" cy="50" r="48" stroke="url(#g)" stroke-width="0.5" fill="none" />
        <path d="M50 5 L50 95 M5 50 L95 50" stroke="url(#g)" stroke-width="0.2" opacity="0.5"/>
        <circle cx="50" cy="50" r="12" stroke="url(#g)" stroke-width="0.5" fill="none"/>
    </svg>
    <div class="header-text">Ceredotlan Tlachieloni</div>
</div>
""", unsafe_allow_html=True)

# Radar
st.markdown(f'<div class="radar-box"><iframe src="https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&overlay=rain&product=iconEu&marker=true" width="100%" height="100%" frameborder="0"></iframe></div>', unsafe_allow_html=True)

# Orologio Azteco di Ieri Sera
st.markdown(f"""
<div class="clock-wrapper">
    <svg class="aztec-svg" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="48" stroke="#111" stroke-width="0.5" fill="none" />
        <g transform="rotate({-az['angles'][0]} 50 50)">
            {" ".join([f'<text x="50" y="8" font-size="3" fill="#333" text-anchor="middle" transform="rotate({i*18} 50 50)">{s.upper()}</text>' for i, s in enumerate(["Cipactli", "Ehecatl", "Calli", "Cuetzpalin", "Coatl", "Miquiztli", "Mazatl", "Tochtli", "Atl", "Itzcuintli", "Ozomatli", "Malinalli", "Acatl", "Ocelotl", "Quauhtli", "Cozcaquauhtli", "Olin", "Tecpatl", "Quiahuitl", "Xochitl"])])}
            <path d="M50 2 L50 10" stroke="#8A2BE2" stroke-width="0.5" />
        </g>
        
        <circle cx="50" cy="50" r="38" stroke="#007BFF" stroke-width="0.3" fill="none" opacity="0.3" />
        <circle cx="50" cy="50" r="30" stroke="#8A2BE2" stroke-width="0.3" fill="none" opacity="0.2" />
        
        <line x1="50" y1="2" x2="50" y2="15" stroke="#fff" stroke-width="0.5" />
    </svg>
    
    <div class="digital-center">
        <span class="time-h">{now.strftime("%H")}</span><span style="color:#222">:</span><span class="time-m">{now.strftime("%M")}</span><span class="time-seconds" style="color:#8A2BE2; font-size:18px;">{now.strftime("%S")}</span>
    </div>
    
    <div class="sub-label">{az['label']}</div>
    <div class="cd-reset">{az['days']} DAYS TO RESET</div>
</div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
