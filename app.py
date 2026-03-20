import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="Ceredoleso Yollotl", page_icon="❤️", layout="centered")

@st.cache_data(ttl=600)
def fetch_meteo():
    lat, lon = 45.6117, 10.9710
    # Previsioni a 2 giorni per evitare IndexError a mezzanotte
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=precipitation_probability&models=icon_seamless&timezone=Europe%2FRome&forecast_days=2"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json()
    except:
        return None

@st.cache_data(ttl=3600)
def fetch_historical():
    lat, lon = 45.6117, 10.9710
    # L'archivio arriva fino a ieri. Oggi non è ancora "storia".
    yesterday = datetime.now() - timedelta(days=1)
    start_date = (yesterday - timedelta(days=9)).strftime('%Y-%m-%d')
    end_date = yesterday.strftime('%Y-%m-%d')
    
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=precipitation_sum&timezone=Europe%2FRome"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json()
    except:
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

# --- 2. STILE CSS ---
st.markdown("""
<style>
    @keyframes heart-beat {
        0% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
        15% { transform: translate(-50%, -50%) scale(1.15); opacity: 1; border-color: #FF0000; }
        30% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
    }
    .stApp { background-color:#000; color: #eee; }
    .header-text { color:#FF3311; font-size:24px; text-align:center; letter-spacing:5px; font-family:monospace; text-shadow: 0 0 15px #600; }
    .radar-box { position: relative; width: 100%; height: 350px; border-radius: 15px; border: 2px solid #333; overflow: hidden; margin-bottom: 20px; }
    .crosshair { position: absolute; top: 50%; left: 50%; width: 45px; height: 45px; border: 2px solid #FF3311; border-radius: 50%; transform: translate(-50%, -50%); z-index: 10; animation: heart-beat 1.5s infinite ease-in-out; pointer-events: none; }
    .aztec-wrapper { position: relative; width: 220px; height: 220px; margin: 10px auto; border-radius: 50%; background: url('https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Piedra_del_Sol.png/600px-Piedra_del_Sol.png') center/cover; filter: sepia(0.6) brightness(0.4); display: flex; align-items: center; justify-content: center; border: 1px solid #400; }
    .digital-clock { background: rgba(0,0,0,0.8); padding: 5px 12px; border-radius: 8px; color: #fff; font-family: monospace; font-size: 20px; border: 1px solid #400; z-index: 5; }
    .rings-svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; transform: rotate(-90deg); }
    .xiuh-box { text-align: center; margin: 10px auto; padding: 12px; border: 1px solid #800; background: rgba(50,0,0,0.2); border-radius: 10px; max-width: 260px; }
</style>
""", unsafe_allow_html=True)

# --- 3. UI ---
fc = fetch_meteo()
hist = fetch_historical()
day_lab, month_lab, year_lab, count_val = get_aztec_context()

st.markdown('<div class="header-text">CEREDOLESO YOLLOTL</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; margin-bottom:15px;"><span style="color:#600; font-size:10px; letter-spacing:3px; font-weight:bold;">EL CORAZÓN DEL SACRIFICIO</span></div>', unsafe_allow_html=True)

# Radar principale
st.markdown(f'<div class="radar-box"><div class="crosshair"></div><iframe src="https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=10&overlay=rain&product=iconEu&marker=true" width="100%" height="100%" frameborder="0"></iframe></div>', unsafe_allow_html=True)

# Timeline 6h
if fc and 'hourly' in fc:
    cols = st.columns(6)
    h_now = datetime.now().hour
    for i in range(6):
        try:
            idx = h_now + i
            prob = fc['hourly']['precipitation_probability'][idx]
            t_str = fc['hourly']['time'][idx][-5:]
            color = '#FF3311' if prob > 30 else '#00FFCC'
            with cols[i]:
                st.markdown(f"<div style='text-align:center; font-size:10px; font-family:monospace;'>{t_str}<br><b style='color:{color}'>{prob}%</b></div>", unsafe_allow_html=True)
        except (IndexError, KeyError):
            continue

# Orologio e Cerchi SVG
n = datetime.now()
s = n.second
off_h = 289.02 - (((n.hour % 24) + n.minute/60) * 289.02 / 24)
off_m = 251.32 - ((n.minute + s/60) * 251.32 / 60)
off_s = 213.62 - (s * 213.62 / 60)

st.markdown(f"""
<div class="aztec-wrapper">
    <div class="digital-clock">{n.strftime("%H:%M")}<span style="color:#FF3311; font-size:14px;">:{s:02d}</span></div>
    <svg class="rings-svg" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="46" fill="none" stroke="#00FFFF" stroke-width="1" stroke-dasharray="289.02" stroke-dashoffset="{off_h}" opacity="0.1"/>
        <circle cx="50" cy="50" r="40" fill="none" stroke="#007FFF" stroke-width="1.5" stroke-dasharray="251.32" stroke-dashoffset="{off_m}" opacity="0.3"/>
        <circle cx="50" cy="50" r="34" fill="none" stroke="#FF3311" stroke-width="2" stroke-dasharray="213.62" stroke-dashoffset="{off_s}" opacity="0.8"/>
    </svg>
</div>
<div class="xiuh-box">
    <div style="color:#844; font-size:9px; letter-spacing:2px; font-weight:bold;">OFFERTA DI YOLLOTL</div>
    <div style="color:#FF3311; font-family:monospace; font-size:24px; font-weight:bold;">{count_val} GIORNI</div>
    <div style="color:#600; font-size:8px;">AL SACRIFICIO DEL FUOCO NUOVO</div>
</div>
""", unsafe_allow_html=True)

# --- STORICO 10 GIORNI (MEMORIA) ---
if hist and 'daily' in hist:
    st.markdown("<div style='color:#444; font-size:9px; letter-spacing:3px; text-align:center; margin-top:15px;'>MEMORIA DEL SANGUE (MM PIOGGIA)</div>", unsafe_allow_html=True)
    df_hist = pd.DataFrame({
        'Giorno': [d[-5:] for d in hist['daily']['time']],
        'Pioggia': hist['daily']['precipitation_sum']
    }).set_index('Giorno')
    
    if not df_hist.empty:
        st.bar_chart(df_hist, color='#800', height=180)

# Refresh
time.sleep(1)
st.rerun()
