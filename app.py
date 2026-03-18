import streamlit as st
import requests
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="Ceredoleso Swiss-HD 12H", page_icon="🎯", layout="centered")

# --- 2. CSS (TEMA BLACK + SNIPER CROSSHAIR) ---
st.markdown("""
<style>
.stApp { background-color:#000000 !important; }
.header-text { color:#00FFFF; font-weight:100; letter-spacing:5px; text-transform:uppercase; font-size:24px; text-align:center; margin:20px 0; }

/* CONTAINER RADAR */
.radar-container { 
    position: relative; 
    width: 100%; 
    height: 600px; 
    border-radius: 15px; 
    border: 2px solid #333; 
    overflow: hidden; 
}

/* MIRINO SNIPER */
.sniper-crosshair {
    position: absolute; top: 50%; left: 50%; width: 60px; height: 60px;
    border: 2px solid #FF0000; border-radius: 50%; transform: translate(-50%, -50%);
    pointer-events: none; z-index: 100;
}
.sniper-crosshair::before { content: ''; position: absolute; top: 50%; left: -40px; width: 140px; height: 1.5px; background: #FF0000; transform: translateY(-50%); }
.sniper-crosshair::after { content: ''; position: absolute; left: 50%; top: -40px; width: 1.5px; height: 140px; background: #FF0000; transform: translateX(-50%); }
.sniper-dot { 
    position: absolute; top: 50%; left: 50%; width: 10px; height: 10px; 
    background: #FF0000; border-radius: 50%; transform: translate(-50%, -50%); 
    box-shadow: 0 0 25px #FF0000; 
}

iframe { width: 100%; height: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown('<div class="header-text">Ceredoleso Target: Swiss ICON-CH</div>', unsafe_allow_html=True)

# --- 4. RADAR PREDITTIVO 12H (FORZATO SU MODELLO SVIZZERO) ---
st.markdown('<div style="color:#FF0000; font-size:11px; text-align:center; letter-spacing:2px; margin-bottom:10px; font-weight:bold;">PREDICTIVE RADAR: NEXT 12 HOURS (SWISS MODEL)</div>', unsafe_allow_html=True)

# URL Windy ottimizzato:
# overlay=rain (per vedere la predizione 12h, il radar 'puro' non arriva a 12h nel futuro)
# model=iconEu (il modello di MeteoSwiss ICON adattato all'Europa)
radar_windy = "https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&level=surface&overlay=rain&product=iconEu&menu=&message=true&marker=true&calendar=12&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"

st.markdown(f'''
<div class="radar-container">
    <div class="sniper-crosshair"><div class="sniper-dot"></div></div>
    <iframe src="{radar_windy}"></iframe>
</div>
''', unsafe_allow_html=True)

# --- 5. TIMELINE TATTICA (Dati ICON-CH) ---
@st.cache_data(ttl=600)
def get_swiss_data():
    # Estraiamo i dati orari precisi del modello ICON-CH
    url = "https://api.open-meteo.com/v1/forecast?latitude=45.6117&longitude=10.9710&hourly=temperature_2m,precipitation_probability&models=icon_seamless&timezone=Europe%2FRome&forecast_days=1"
    return requests.get(url).json()

w_data = get_swiss_data()

if w_data and 'hourly' in w_data:
    st.write("")
    st.markdown('<div style="color:#00FFFF; font-size:10px; text-align:center; letter-spacing:2px; margin-bottom:10px;">HOURLY PRECISION SCAN (NEXT 12H)</div>', unsafe_allow_html=True)
    
    now_h = datetime.now().hour
    cols = st.columns(6)
    
    for i in range(12):
        idx = now_h + i
        if idx < len(w_data['hourly']['time']):
            with cols[i % 6]:
                time_str = w_data['hourly']['time'][idx][-5:]
                prob = w_data['hourly']['precipitation_probability'][idx]
                temp = w_data['hourly']['temperature_2m'][idx]
                p_color = "#FF3311" if prob > 30 else "#00FF00"
                
                st.markdown(f'''
                <div style="background:#111; border:1px solid #333; border-radius:10px; padding:8px; text-align:center; margin-bottom:10px;">
                    <div style="font-size:10px; color:#666;">{time_str}</div>
                    <div style="font-size:14px; color:white; font-weight:bold;">{temp}°</div>
                    <div style="font-size:11px; color:{p_color};">{prob}%</div>
                </div>
                ''', unsafe_allow_html=True)

# --- 6. FOOTER ---
if st.button("🔄 RE-SYNC TARGET"):
    st.cache_data.clear()
    st.rerun()
