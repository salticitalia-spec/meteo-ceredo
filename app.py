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
    
    angle_day = ((delta_days % 20) * 18)
    angle_month = (((delta_days % 365) // 20) * 20)
    angle_year = (((delta_days // 365) % 52) * 6.92)
    
    num_day = (delta_days % 13) + 1
    sym_day = symbols[(delta_days + 12) % 20]
    current_month = months[min((delta_days % 365) // 20, 17)]
    year_num = ((delta_days // 365) % 13) + 1
    year_sym = year_carriers[(delta_days // 365) % 4]
    
    countdown = (datetime(2027, 11, 15) - current_time).days
    
    return {
        "angles": [angle_day, angle_month, angle_year],
        "label": f"{num_day} {sym_day} • {current_month} • {year_num} {year_sym}",
        "days": countdown
    }

# --- 2. STILE CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100&display=swap');
    .stApp { background-color:#000; color: #eee; }
    .header-container { display: flex; flex-direction: column; align-items: center; margin-bottom: 25px; }
    .logo-laser { width: 140px; height: 140px; margin-bottom: 10px; }
    .header-text { 
        font-family: 'Inter', sans-serif; font-weight: 100; font-size: 24px; letter-spacing: 2px; 
        text-transform: uppercase; background: linear-gradient(90deg, #8A2BE2 0%, #007BFF 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .radar-box { width: 100%; height: 380px; border: 1px solid #111; border-radius: 4px; overflow: hidden; margin-bottom: 30px; }
    .analog-clock-container { display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; width: 100%; padding-bottom: 60px; }
    .aztec-rings { width: 300px; height: 300px; }
    .digital-overlay { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -150%); text-align: center; font-family: 'Inter', sans-serif; }
    .time-hours { color: #ffffff; font-size: 38px; font-weight: 100; }
    .time-minutes { color: #007BFF; font-size: 38px; font-weight: 100; }
    .time-seconds { color: #8A2BE2; font-size: 18px; font-weight: 100; margin-left: 4px; }
    .time-separator { color: #222; font-size: 30px; padding: 0 4px; }
    .aztec-text-sub { color: #444; font-size: 11px; letter-spacing: 3px; margin-top: 150px; text-transform: uppercase; text-align: center; }
    .cd-reset { color: #8A2BE2; font-size: 11px; letter-spacing: 5px; opacity: 0.4; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGICA ---
now = datetime.now() + timedelta(hours=1)
az_data = get_aztec_data(now)

# --- 4. INTERFACCIA ---
st.markdown(f"""
<div class="header-container">
    <svg class="logo-laser" viewBox="0 0 100 100">
        <defs>
            <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#8A2BE2" /><stop offset="100%" style="stop-color:#007BFF" />
            </linearGradient>
        </defs>
        <circle cx="50" cy="50" r="48" stroke="url(#g)" stroke-width="0.5" fill="none" />
        <circle cx="50" cy="50" r="40" stroke="url(#g)" stroke-width="0.5" fill="none" stroke-dasharray="2 2" opacity="0.5"/>
        <path d="M50 0 L50 100 M0 50 L100 50" stroke="url(#g)" stroke-width="0.5" opacity="0.3"/>
        <circle cx="50" cy="50" r="12" stroke="url(#g)" stroke-width="0.5" fill="none"/>
        <circle cx="50" cy="50" r="2.5" fill="url(#g)"/>
    </svg>
    <h1 class="header-text">Ceredotlan Tlachieloni</h1>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="radar-box"><iframe src="https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&overlay=rain&product=iconEu&marker=true" width="100%" height="100%" frameborder="0"></iframe></div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="analog-clock-container">
    <svg class="aztec-rings" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="46" stroke="#1a1a1a" stroke-width="0.5" fill="none" />
        <line x1="50" y1="2" x2="50" y2="10" stroke="#8A2BE2" stroke-width="0.5" transform="rotate({az_data['angles'][2]} 50 50)" />
        <circle cx="50" cy="50" r="36" stroke="#1a1a1a" stroke-width="0.5" fill="none" />
        <line x1="50" y1="12" x2="50" y2="20" stroke="#007BFF" stroke-width="0.5" transform="rotate({az_data['angles'][1]} 50 50)" />
        <circle cx="50" cy="50" r="26" stroke="#1a1a1a" stroke-width="0.5" fill="none" />
        <line x1="50" y1="22" x2="50" y2="30" stroke="#ffffff" stroke-width="0.5" transform="rotate({az_data['angles'][0]} 50 50)" />
        <path d="M50 45 L50 55 M45 50 L55 50" stroke="url(#g)" stroke-width="0.5" opacity="0.6" />
    </svg>
    <div class="digital-overlay">
        <span class="time-hours">{now.strftime("%H")}</span><span class="time-separator">:</span><span class="time-minutes">{now.strftime("%M")}</span><span class="time-seconds">{now.strftime("%S")}</span>
    </div>
    <div class="aztec-text-sub">{az_data['label']}</div>
    <div class="cd-reset">{az_data['days']} DAYS TO RESET</div>
</div>
""", unsafe_allow_html=True)

time.sleep(1)
st.rerun()
