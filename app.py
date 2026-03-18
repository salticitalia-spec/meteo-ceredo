import streamlit as st
import requests
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE ---
st.set_page_config(page_title="Ceredoleso Swiss-HD 12H", page_icon="🎯", layout="centered")

# --- 2. CSS (TEMA BLACK + SNIPER CROSSHAIR) ---
st.markdown("""
<style>
.stApp { background-color:#000000 !important; }
.header-text { color:#FFD700; font-weight:100; letter-spacing:5px; text-transform:uppercase; font-size:24px; text-align:center; margin:20px 0; }

/* CONTAINER RADAR */
.radar-container { 
    position: relative; 
    width: 100%; 
    height: 550px; 
    border-radius: 15px; 
    border: 2px solid #333; 
    overflow: hidden; 
}

/* MIRINO SNIPER METEOSWISS */
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

iframe { width: 100%; height: 100%; border: none; filter: grayscale(20%) contrast(110%); }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA FETCHING (DATI ICON-CH VIA OPEN-METEO) ---
@st.cache_data(ttl=600)
def get_swiss_model_data():
    # Usiamo esplicitamente i dati del modello MeteoSwiss (ICON-CH)
    url = "https://api.open-meteo.com/v1/forecast?latitude=45.6117&longitude=10.9710&current_weather=true&hourly=precipitation,precipitation_probability&models=icon_seamless&timezone=Europe%2FRome"
    return requests.get(url).json()

data = get_swiss_model_data()

# --- 4. HEADER ---
st.markdown('<div class="header-text">Ceredoleso Target: Swiss-HD Model</div>', unsafe_allow_html=True)

# --- 5. RADAR PREDITTIVO 12H (MODELLO SVIZZERO) ---
st.markdown('<div style="color:#FF0000; font-size:11px; text-align:center; letter-spacing:2px; margin-bottom:10px; font-weight:bold;">SORGENTE: METEOSWISS ICON-CH (12H PROJECTION)</div>', unsafe_allow_html=True)

# URL configurato su Meteologix che usa il modello Swiss HD (ICON-CH) 
# Centrato su Ceredo/Verona per vedere le celle in arrivo da Nord/Ovest
radar_swiss = "https://meteologix.com/it/model-charts/swisshd-nowcast/verona/precipitation-1h.html"

st.markdown(f'''
<div class="radar-container">
    <div class="sniper-crosshair"><div class="sniper-dot"></div></div>
    <iframe src="{radar_swiss}"></iframe>
</div>
''', unsafe_allow_html=True)

# --- 6. TIMELINE TATTICA 12H (Dati Modello) ---
st.write("")
if data and 'hourly' in data:
    st.markdown('<div style="color:#FFD700; font-size:10px; text-align:center; letter-spacing:2px; margin-bottom:10px;">PRECIPITATION STREAM (NEXT 12H)</div>', unsafe_allow_html=True)
    
    now_h = datetime.now().hour
    cols = st.columns(6)
    
    # Visualizziamo 12 ore in due file da 6
    for i in range(12):
        idx = now_h + i
        with cols[i % 6]:
            time_str = data['hourly']['time'][idx][-5:]
            prob = data['hourly']['precipitation_probability'][idx]
            p_val = data['hourly']['precipitation'][idx]
            
            # Colore basato sulla probabilità
            color = "#FF3311" if prob > 40 else "#FFFF00" if prob > 15 else "#00FF00"
            
            st.markdown(f'''
            <div style="background:#111; border:1px solid #222; border-radius:8px; padding:5px; text-align:center; margin-bottom:5px;">
                <div style="font-size:10px; color:#666;">{time_str}</div>
                <div style="font-size:14px; color:white; font-weight:bold;">{p_val}mm</div>
                <div style="font-size:11px; color:{color};">{prob}%</div>
            </div>
            ''', unsafe_allow_html=True)

# --- 7. FOOTER ---
if st.button("🔄 RE-SYNC TARGET"):
    st.cache_data.clear()
    st.rerun()
