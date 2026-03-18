import streamlit as st
import requests
from datetime import datetime, timedelta

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Meteo Ceredoleso Pro", page_icon="🎯", layout="centered")

# --- 2. FUNZIONI E SANTI ---
def get_weather_icon(code):
    pioggia_codes = [51, 53, 55, 61, 63, 65, 80, 81, 82]
    icons = {0: "☀️", 1: "☀️", 2: "⛅", 3: "☁️", 45: "🌫️", 51: "🌧️", 61: "🌧️", 95: "⚡"}
    icon = icons.get(code, "☁️")
    if code in pioggia_codes:
        return f'<span class="weather-icon rain-ani" style="color:#FF0000;filter:drop-shadow(0 0 8px #FF0000);">🌧️</span>'
    if icon in ["🌧️", "☁️", "⛅"]:
        return f'<span class="weather-icon" style="color:#FFFFFF;">{icon}</span>'
    if icon == "☀️":
        return f'<span class="weather-icon sun-ani">{icon}</span>'
    return f'<span class="weather-icon">{icon}</span>'

def get_santo(data_obj):
    santi = {"03-15": "S. Zaccaria", "03-16": "S. Eriberto", "03-17": "S. Patrizio", "03-18": "S. Cirillo", "03-19": "S. Giuseppe", "03-20": "S. Claudia", "03-21": "S. Benedetto", "03-22": "S. Lea", "03-23": "S. Turibio"}
    return santi.get(data_obj.strftime("%m-%d"), "S. del Giorno")

giorni_ita = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
mesi_ita = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

# --- 3. CSS (STILE PRO + MIRINO) ---
style_css = """
<style>
.stApp, [data-testid='stAppViewContainer'], [data-testid='stHeader'] { background-color:#000000 !important; }
.main-card { border:1px solid #333; border-radius:20px; padding:20px; margin-bottom:15px; text-align:center; background:#000000 !important; }
.header-text { color:#00FFFF !important; font-weight:100 !important; letter-spacing:7px; text-transform:uppercase; font-size:26px; text-align:center; margin:20px 0; }
@keyframes rotate { from { transform:rotate(0deg); } to { transform:rotate(360deg); } }
@keyframes pulse { 0% { opacity:1; transform:scale(1); } 50% { opacity:0.6; transform:scale(1.05); } 100% { opacity:1; transform:scale(1); } }
.weather-icon { display:inline-block; font-size:80px; margin:10px 0; }
.sun-ani { animation:rotate 12s linear infinite; }
.rain-ani { animation:pulse 1s ease-in-out infinite; }
.rain-time-display { font-weight:bold; font-size:24px; margin-bottom:15px; }

/* CSS MIRINO PRECISIONE */
.radar-container { position: relative; width: 100%; height: 450px; overflow: hidden; border-radius: 15px; border: 1px solid #444; }
.sniper-crosshair {
    position: absolute;
    top: 50%; left: 50%;
    width: 40px; height: 40px;
    border: 2px solid #FF0000;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: 10;
}
.sniper-crosshair::before { content: ''; position: absolute; top: 50%; left: -10px; width: 60px; height: 1px; background: #FF0000; transform: translateY(-50%); }
.sniper-crosshair::after { content: ''; position: absolute; left: 50%; top: -10px; width: 1px; height: 60px; background: #FF0000; transform: translateX(-50%); }
.sniper-dot { position: absolute; top: 50%; left: 50%; width: 4px; height: 4px; background: #FF0000; border-radius: 50%; transform: translate(-50%, -50%); }

iframe { width: 100%; height: 450px; border: none; }
</style>
"""
st.markdown(style_css, unsafe_allow_html=True)

# --- 4. DATA FETCHING ---
@st.cache_data(ttl=600)
def fetch_meteo_data():
    lat, lon = 45.6117, 10.9710
    try:
        url_fc = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,precipitation&daily=temperature_2m_max,precipitation_sum,weathercode&timezone=Europe%2FRome"
        start_hi = (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d')
        end_hi = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        url_hi = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_hi}&end_date={end_hi}&hourly=precipitation,windspeed_10m,shortwave_radiation&timezone=Europe%2FRome"
        return requests.get(url_fc).json(), requests.get(url_hi).json()
    except: return None, None

dfc, dhi = fetch_meteo_data()
if not dfc: st.stop()

# --- 5. LOGICA PRECIPITAZIONI ---
now = datetime.now()
h_times = dfc['hourly']['time']
h_prec = dfc['hourly']['precipitation']

def check_rain_for_day(target_date):
    for t, p in zip(h_times, h_prec):
        dt_t = datetime.fromisoformat(t)
        if dt_t.date() == target_date.date() and dt_t >= now and p > 0.1:
            return f"Ore {dt_t.strftime('%H:00')}"
    return "Asciutto"

msg_oggi = check_rain_for_day(now)
colore_oggi = "#00FF00" if "Asciutto" in msg_oggi else "#FF3311"
if dfc['current_weather']['weathercode'] in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
    msg_oggi = "PIOVE ORA"
    colore_oggi = "#FF0000"

# --- 6. INTERFACCIA PRINCIPALE ---
st.markdown('<div class="header-text">Ceredoleso PRO</div>', unsafe_allow_html=True)
curr = dfc['current_weather']

st.markdown(f'''
<div class="main-card">
    <div style="font-weight:100; font-size:20px; color:white; letter-spacing:3px; text-transform:uppercase;">
        {giorni_ita[now.weekday()]} {now.day} {mesi_ita[now.month-1]}
    </div>
    <div style="color:#00FFFF; font-size:11px; margin-top:5px;">✨ {get_santo(now)}</div>
    <div>{get_weather_icon(curr['weathercode'])}</div>
    <div class="rain-time-display" style="color:{colore_oggi};">
        {msg_oggi if msg_oggi != "Asciutto" else ""}
    </div>
    <div style="font-size:65px; font-weight:bold; color:white; margin-top:-10px;">{curr['temperature']}°</div>
</div>
''', unsafe_allow_html=True)

# --- 7. RADAR METEO CON MIRINO ---
st.markdown('<div style="color:#00FFFF; font-size:10px; text-align:center; letter-spacing:2px; margin-bottom:10px;">TARGET: CEREDO FALESIA</div>', unsafe_allow_html=True)

radar_windy = "https://embed.windy.com/embed2.html?lat=45.6117&lon=10.9710&zoom=9&level=surface&overlay=radar&product=radar&menu=&message=false&marker=&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"

st.markdown(f'''
<div class="radar-container">
    <div class="sniper-crosshair"><div class="sniper-dot"></div></div>
    <iframe src="{radar_windy}"></iframe>
</div>
''', unsafe_allow_html=True)

# --- 8. MOSTRO BOVINO ---
st.write("")
if dhi and 'hourly' in dhi:
    carico = sum(dhi['hourly']['precipitation'][-168:]) 
    if carico < 5: m_t, m_c, m_d = "SECCO ☀️", "#00FFFF", "🟢 Ottimo ovunque"
    elif carico < 18: m_t, m_c, m_d = "UMIDO 💧", "#FFFF00", "🟡 Peci & Ostramandra umide"
    else: m_t, m_c, m_d = "BAGNATO ⚠️", "#FF3311", "🔴 Bosco saturo"
    
    st.markdown(f'''
    <div style="border:1px solid {m_c}; padding:15px; border-radius:15px; text-align:center; background:black; margin-bottom:20px;">
        <div style="font-size:9px; color:#666; letter-spacing:2px;">MOSTRO BOVINO INDEX</div>
        <div style="font-size:20px; color:{m_c}; font-weight:bold; margin:3px 0;">{m_t}</div>
        <div style="font-size:11px; color:#999;">{m_d}</div>
    </div>
    ''', unsafe_allow_html=True)

# --- 9. TENDENZA 3 GIORNI ---
cols = st.columns(3)
for i in range(1, 4):
    with cols[i-1]:
        d_f = now + timedelta(days=i)
        rain_time = check_rain_for_day(d_f)
        rain_color = "#FF3311" if rain_time != "Asciutto" else "#00FF00"
        
        st.markdown(f'''
        <div class="main-card" style="padding:15px; border-color:#222;">
            <div style="font-size:11px; color:white; font-weight:bold;">{giorni_ita[d_f.weekday()][:3].upper()} {d_f.day}</div>
            <div>{get_weather_icon(dfc['daily']['weathercode'][i])}</div>
            <div style="font-size:13px; font-weight:bold; color:{rain_color}; margin:5px 0;">
                {rain_time if rain_time != "Asciutto" else ""}
            </div>
            <div style="font-size:22px; font-weight:bold; color:white;">{dfc['daily']['temperature_2m_max'][i]}°</div>
        </div>
        ''', unsafe_allow_html=True)

if st.button("🔄 AGGIORNA"):
    st.cache_data.clear()
    st.rerun()
