import io
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Gemelo Digital - Planta Piloto JICA (UNMSM)",
    layout="wide",
    page_icon="⚒️"
)

# 👇 AQUÍ COLOCAS EL PASO 2 (LÍNEA 14) 👇
clave = st.sidebar.text_input("🔒 Clave de Acceso JICA", type="password")
if clave != "UNMSM2026":
    st.warning("Ingresa la clave de acceso en la barra lateral para usar el Gemelo Digital.")
    st.stop()
# 👆 FIN DEL PASO 2 👆

st.markdown("""
<style>
.block-container { padding-top: 1.1rem; padding-bottom: 1rem; }
div[data-testid="stMetricValue"] { font-size: 1.32rem; }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.block-container { padding-top: 1.1rem; padding-bottom: 1rem; }
div[data-testid="stMetricValue"] { font-size: 1.32rem; }
</style>
""", unsafe_allow_html=True)

st.title("⚒️ Gemelo Digital: Planta Piloto JICA — UNMSM")
st.caption("Simulador Web Interactivo de 24 Equipos y 34 Corrientes | Escuela Profesional de Ingeniería Metalúrgica — UNMSM")

# ==================== BARRA LATERAL: CONFIGURACIÓN Y PARÁMETROS ====================
st.sidebar.header("🎛️ Panel de Control JICA")

tema_plano = st.sidebar.radio(
    "Estilo del Diagrama de Flujo",
    ["Modo Plano CAD (Blanco UNMSM)", "Modo SCADA (Oscuro)"],
    index=0
)

esquema_mineral = st.sidebar.selectbox(
    "Esquema de Flotación Diferencial",
    ["Pb - Zn (Galena en C1 / Esfalerita en C2)", "Cu - Zn (Calcopirita en C1 / Esfalerita en C2)", "Cu - Pb (Calcopirita en C1 / Galena en C2)"]
)

if esquema_mineral.startswith("Pb - Zn"):
    m1_sym, m2_sym = "Pb", "Zn"
    d_m1_f, d_m1_c, d_m2_f, d_m2_c = 3.20, 58.0, 5.50, 52.0
elif esquema_mineral.startswith("Cu - Zn"):
    m1_sym, m2_sym = "Cu", "Zn"
    d_m1_f, d_m1_c, d_m2_f, d_m2_c = 1.85, 28.0, 4.80, 51.0
else:
    m1_sym, m2_sym = "Cu", "Pb"
    d_m1_f, d_m1_c, d_m2_f, d_m2_c = 1.60, 27.5, 3.40, 60.0

with st.sidebar.expander("1. Chancado y Molienda (Equipos 1-8)", expanded=True):
    F_kgh = st.slider("1. Alimento Fresco (kg/h)", 100.0, 800.0, 325.0, 25.0)
    f80_alim_mm = st.slider("F80 Alimento (mm)", 25.0, 127.0, 105.0, 5.0)
    set_mandibulas_mm = st.slider("Set Chanc. Mandíbulas [Eq. 1] (mm)", 12.0, 38.0, 26.0, 1.0)
    set_rodillos_mm = st.slider("Set Chanc. Rodillos [Eq. 2] (mm)", 3.0, 15.0, 6.5, 0.5)
    wi_bond = st.number_input("Work Index Bond Wi (kWh/t)", 8.0, 25.0, 13.8, 0.2)
    sol_molino = st.slider("% Sólidos Molino 2'x2' [Eq. 5]", 60.0, 78.0, 72.0, 1.0)
    cc_espiral_pct = st.slider("Carga Circulante Espiral [Eq. 6] (%)", 80.0, 300.0, 210.0, 10.0)
    p80_rebose_um = st.slider("P80 Rebose Clasificador [Corr. 10] (µm)", 74.0, 210.0, 149.0, 5.0)
    sol_rebose = st.slider("% Sólidos Rebose a Flotación [Corr. 12]", 22.0, 40.0, 30.0, 1.0)
    sg_mineral = st.number_input("Gravedad Específica Mineral (SG)", 2.5, 4.5, 2.95, 0.05)

with st.sidebar.expander(f"2. Flotación Circuito 1 - C1 ({m1_sym})", expanded=False):
    ley_f_m1 = st.number_input(f"Ley Cabeza {m1_sym} (%)", 0.2, 20.0, d_m1_f, 0.1)
    ley_c1_m1 = st.number_input(f"Ley Conc. Final C1 [Corr. 17] (% {m1_sym})", 15.0, 80.0, d_m1_c, 1.0)
    rec_global_c1 = st.slider(f"Recuperación Global {m1_sym} en C1 (%)", 50.0, 96.0, 86.0, 1.0)
    rec_ro1 = st.slider("Recuperación Rougher C1 [Eq. 11] (%)", 60.0, 95.0, 82.0, 1.0)
    rec_cl1 = st.slider("Recuperación Cleaner 1 [Eq. 12] (%)", 65.0, 98.0, 88.0, 1.0)
    rec_scv1 = st.slider("Recuperación Scavenger C1 [Eq. 13] (%)", 30.0, 85.0, 55.0, 1.0)
    dosis_col_c1 = st.number_input(f"Colector Z-11 Acond. 1-2 (g/t)", 5.0, 150.0, 35.0, 5.0)
    dosis_dep_c1 = st.number_input("Depresor ZnSO4 Acond. 1 (g/t)", 50.0, 800.0, 250.0, 25.0)

with st.sidebar.expander(f"3. Flotación Circuito 2 - C2 ({m2_sym})", expanded=False):
    ley_f_m2 = st.number_input(f"Ley Cabeza {m2_sym} (%)", 0.5, 25.0, d_m2_f, 0.1)
    ley_c2_m2 = st.number_input(f"Ley Conc. Final C2 [Corr. 29] (% {m2_sym})", 20.0, 70.0, d_m2_c, 1.0)
    rec_global_c2 = st.slider(f"Recuperación Global {m2_sym} en C2 (%)", 50.0, 96.0, 84.0, 1.0)
    rec_ro2 = st.slider("Recuperación Rougher C2 [Eq. 20] (%)", 60.0, 95.0, 80.0, 1.0)
    rec_cl2 = st.slider("Recuperación Cleaner 2 [Eq. 21] (%)", 65.0, 98.0, 86.0, 1.0)
    rec_scv2 = st.slider("Recuperación Scavenger C2 [Eq. 22] (%)", 30.0, 85.0, 50.0, 1.0)
    dosis_act_c2 = st.number_input("Activador CuSO4 Acond. 3 (g/t)", 50.0, 1000.0, 350.0, 25.0)
    dosis_col_c2 = st.number_input("Colector Z-6 Acond. 4 (g/t)", 5.0, 150.0, 45.0, 5.0)

# ==================== CÁLCULO DE LAS 34 CORRIENTES ====================
p80_mandibulas_mm = set_mandibulas_mm * 1.22
p80_rodillos_mm = set_rodillos_mm * 1.18
f80_molino_um = p80_rodillos_mm * 1000.0

cc_esp = cc_espiral_pct / 100.0
s9_arenas_kgh = F_kgh * cc_esp
s5_alim_molino_kgh = F_kgh + s9_arenas_kgh
s7_desc_molino_kgh = s5_alim_molino_kgh
s10_rebose_kgh = F_kgh

w9_arenas_lh = s9_arenas_kgh * (24.0 / 76.0)
w5_molino_lh = s5_alim_molino_kgh * ((100.0 - sol_molino) / sol_molino)
w6_agua_entrada_lh = max(0.0, w5_molino_lh - w9_arenas_lh)
w10_rebose_lh = s10_rebose_kgh * ((100.0 - sol_rebose) / sol_rebose)
w8_agua_salida_lh = max(0.0, (w10_rebose_lh + w9_arenas_lh) - w5_molino_lh)

w_bond_kwht = 10.0 * wi_bond * ((1.0 / np.sqrt(p80_rebose_um)) - (1.0 / np.sqrt(f80_molino_um)))
potencia_molino_kw = w_bond_kwht * (F_kgh / 1000.0)

# Circuito 1
fino_m1_alim = F_kgh * (ley_f_m1 / 100.0)
fino_m1_c1 = fino_m1_alim * (rec_global_c1 / 100.0)
s17_conc_c1_kgh = fino_m1_c1 / (ley_c1_m1 / 100.0)
s22_cola_scv1_kgh = max(10.0, F_kgh - s17_conc_c1_kgh)

r_cl1, r_ro1, r_scv1 = rec_cl1 / 100.0, rec_ro1 / 100.0, rec_scv1 / 100.0
s15_esp_ro1_kgh = s17_conc_c1_kgh / max(0.35, r_cl1 * 0.78)
s18_cola_cl1_kgh = max(1.0, s15_esp_ro1_kgh - s17_conc_c1_kgh)
s19_esp_scv1_kgh = s22_cola_scv1_kgh * (0.12 * r_scv1)
s21_medios_c1_kgh = s18_cola_cl1_kgh + s19_esp_scv1_kgh
s14_alim_ro1_kgh = F_kgh + s21_medios_c1_kgh
s16_cola_ro1_kgh = s14_alim_ro1_kgh - s15_esp_ro1_kgh

# Circuito 2
fino_m2_alim = F_kgh * (ley_f_m2 / 100.0)
fino_m2_c2 = fino_m2_alim * (rec_global_c2 / 100.0)
s29_conc_c2_kgh = fino_m2_c2 / (ley_c2_m2 / 100.0)
s34_relave_final_kgh = max(5.0, s22_cola_scv1_kgh - s29_conc_c2_kgh)

r_cl2, r_scv2 = rec_cl2 / 100.0, rec_scv2 / 100.0
s27_esp_ro2_kgh = s29_conc_c2_kgh / max(0.35, r_cl2 * 0.76)
s30_cola_cl2_kgh = max(1.0, s27_esp_ro2_kgh - s29_conc_c2_kgh)
s31_esp_scv2_kgh = s34_relave_final_kgh * (0.14 * r_scv2)
s33_medios_c2_kgh = s30_cola_cl2_kgh + s31_esp_scv2_kgh
s26_alim_ro2_kgh = s22_cola_scv1_kgh + s33_medios_c2_kgh
s28_cola_ro2_kgh = s26_alim_ro2_kgh - s27_esp_ro2_kgh

fino_m1_c2 = s29_conc_c2_kgh * 0.015
fino_m1_rel = max(0.0, fino_m1_alim - fino_m1_c1 - fino_m1_c2)
ley_rel_m1 = (fino_m1_rel / s34_relave_final_kgh) * 100.0

fino_m2_c1 = s17_conc_c1_kgh * 0.035
fino_m2_rel = max(0.0, fino_m2_alim - fino_m2_c2 - fino_m2_c1)
ley_rel_m2 = (fino_m2_rel / s34_relave_final_kgh) * 100.0

# ==================== KPIS EJECUTIVOS ====================
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Alimento [Corr. 1]", f"{F_kgh:.1f} kg/h", f"P80 Molino: {p80_rebose_um:.0f} µm")
k2.metric(f"Conc. C1 ({m1_sym}) [17]", f"{s17_conc_c1_kgh:.2f} kg/h", f"Ley {m1_sym}: {ley_c1_m1:.1f}% | Rec: {rec_global_c1:.1f}%")
k3.metric(f"Conc. C2 ({m2_sym}) [29]", f"{s29_conc_c2_kgh:.2f} kg/h", f"Ley {m2_sym}: {ley_c2_m2:.1f}% | Rec: {rec_global_c2:.1f}%")
k4.metric("Relave Final [Corr. 34]", f"{s34_relave_final_kgh:.2f} kg/h", f"{ley_rel_m1:.2f}% {m1_sym} | {ley_rel_m2:.2f}% {m2_sym}")
k5.metric("Medios Recirculados", f"C1: {s21_medios_c1_kgh:.1f} kg/h", f"C2: {s33_medios_c2_kgh:.1f} kg/h")

tab_pfd, tab_et1, tab_et23, tab_34 = st.tabs([
    "🗺️ Flowsheet Simbólico Oficial JICA (24 Equipos / 34 Corrientes)",
    "⚙️ Etapa 1: Conminución y Clasificador Helicoidal",
    f"🧪 Etapas 2 y 3: Flotación ({m1_sym} / {m2_sym}) y Reactivos",
    "📋 Tabla Maestra de las 34 Corrientes y Descargas Web"
])

with tab_pfd:
    es_claro = "Blanco" in tema_plano
    bg_svg = "#ffffff" if es_claro else "#0b0f17"
    fg_txt = "#111827" if es_claro else "#e5e7eb"
    eq_fill = "#e5e7eb" if es_claro else "#1e293b"
    eq_stroke = "#111827" if es_claro else "#94a3b8"
    line_main = "#111827" if es_claro else "#38bdf8"
    line_rec = "#dc2626" if es_claro else "#f87171"
    line_conc = "#15803d" if es_claro else "#4ade80"

    svg_only = f"""<svg viewBox="0 0 1250 760" width="100%" height="680" xmlns="http://www.w3.org/2000/svg" style="font-family: Arial, sans-serif; background:{bg_svg};">
      <defs>
        <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="{line_main}"/>
        </marker>
        <marker id="arr-rec" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="{line_rec}"/>
        </marker>
        <marker id="arr-conc" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="{line_conc}"/>
        </marker>
      </defs>

      <!-- COLUMNA IZQUIERDA: CHANCADO Y MOLIENDA (EQUIPOS 1 AL 8) -->
      <circle cx="85" cy="25" r="7" fill="none" stroke="{line_main}" stroke-width="2"/>
      <text x="100" y="29" fill="{fg_txt}" font-size="11" font-weight="bold">ALIMENTO ({F_kgh:.0f} kg/h)</text>
      <line x1="85" y1="32" x2="85" y2="62" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="72" y="50" fill="{line_main}" font-size="11" font-weight="bold">1</text>

      <!-- [1] Chancadora de Mandíbulas -->
      <polygon points="65,65 80,65 80,115 70,115" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <polygon points="108,65 95,65 86,115 96,115" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <circle cx="106" cy="100" r="8" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="70" y="92" fill="{fg_txt}" font-size="11" font-weight="bold">1</text>
      <text x="122" y="82" fill="{fg_txt}" font-size="11" font-weight="bold">CHANCADORA DE MANDÍBULAS</text>
      <text x="122" y="96" fill="{fg_txt}" font-size="10">Set: {set_mandibulas_mm:.0f} mm | P80: {p80_mandibulas_mm:.1f} mm</text>

      <line x1="85" y1="117" x2="85" y2="152" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="72" y="138" fill="{line_main}" font-size="11" font-weight="bold">2</text>

      <!-- [2] Chancadora de Rodillos -->
      <polygon points="73,152 97,152 91,168 79,168" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
      <circle cx="71" cy="180" r="14" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <circle cx="99" cy="180" r="14" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="81" y="164" fill="{fg_txt}" font-size="11" font-weight="bold">2</text>
      <text x="122" y="176" fill="{fg_txt}" font-size="11" font-weight="bold">CHANCADORA DE RODILLOS</text>
      <text x="122" y="190" fill="{fg_txt}" font-size="10">Luz: {set_rodillos_mm:.1f} mm | P80: {p80_rodillos_mm:.1f} mm</text>

      <line x1="85" y1="196" x2="85" y2="232" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="72" y="217" fill="{line_main}" font-size="11" font-weight="bold">3</text>

      <!-- [3] Tolva de Finos -->
      <polygon points="65,235 105,235 105,275 89,302 81,302 65,275" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="81" y="268" fill="{fg_txt}" font-size="12" font-weight="bold">3</text>
      <text x="115" y="262" fill="{fg_txt}" font-size="11" font-weight="bold">TOLVA DE FINOS</text>
      <text x="115" y="276" fill="{fg_txt}" font-size="10">{F_kgh:.0f} kg/h | F80: {f80_molino_um:.0f} µm</text>

      <!-- Corriente 4 y Nodo 4 -->
      <line x1="85" y1="302" x2="85" y2="348" stroke="{line_main}" stroke-width="2"/>
      <line x1="85" y1="348" x2="118" y2="348" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="72" y="330" fill="{line_main}" font-size="11" font-weight="bold">4</text>
      <circle cx="126" cy="348" r="8" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="123" y="334" fill="{fg_txt}" font-size="11" font-weight="bold">4</text>

      <!-- Agua Entrada (6) -->
      <circle cx="165" cy="298" r="6" fill="none" stroke="#0284c7" stroke-width="2"/>
      <text x="176" y="302" fill="#0284c7" font-size="10" font-weight="bold">AGUA ENTRADA [6] ({w6_agua_entrada_lh:.0f} L/h)</text>
      <line x1="160" y1="304" x2="132" y2="340" stroke="#0284c7" stroke-width="1.8" marker-end="url(#arr)"/>

      <line x1="134" y1="348" x2="178" y2="348" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="152" y="342" fill="{line_main}" font-size="11" font-weight="bold">5</text>

      <!-- [5] Molino de Bolas 2'x2' -->
      <polygon points="180,338 192,326 192,370 180,358" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <rect x="192" y="316" width="68" height="64" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <rect x="260" y="310" width="8" height="76" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <rect x="268" y="336" width="12" height="24" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="222" y="352" fill="{fg_txt}" font-size="13" font-weight="bold">5</text>
      <text x="160" y="400" fill="{fg_txt}" font-size="11" font-weight="bold">MOLINO DE BOLAS 2'x2'</text>
      <text x="160" y="414" fill="{fg_txt}" font-size="10">Carga: {s5_alim_molino_kgh:.0f} kg/h ({sol_molino:.0f}% Sól)</text>

      <!-- Corriente 7 -->
      <polyline points="280,348 294,348 294,505" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="281" y="435" fill="{line_main}" font-size="11" font-weight="bold">7</text>

      <!-- Agua Salida (8) totalmente despejada entre la línea 7 y la línea 12 -->
      <circle cx="336" cy="462" r="5.5" fill="none" stroke="#0284c7" stroke-width="2"/>
      <text x="303" y="438" fill="#0284c7" font-size="9" font-weight="bold">AGUA SALIDA [8]</text>
      <text x="312" y="450" fill="#0284c7" font-size="9">({w8_agua_salida_lh:.0f} L/h)</text>
      <line x1="333" y1="468" x2="312" y2="510" stroke="#0284c7" stroke-width="1.8" marker-end="url(#arr)"/>

      <!-- [6] Clasificador Helicoidal -->
      <polygon points="205,438 320,515 320,545 290,545 205,472" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <line x1="212" y1="455" x2="305" y2="528" stroke="{eq_stroke}" stroke-width="2" stroke-dasharray="6,4"/>
      <text x="262" y="505" fill="{fg_txt}" font-size="12" font-weight="bold">6</text>
      <text x="155" y="535" fill="{fg_txt}" font-size="11" font-weight="bold">CLASIFICADOR HELICOIDAL</text>
      <text x="155" y="549" fill="{fg_txt}" font-size="10">CC: {cc_espiral_pct:.0f}% | Arenas: {s9_arenas_kgh:.0f} kg/h</text>

      <!-- Corriente 9 -->
      <polyline points="205,455 126,455 126,358" fill="none" stroke="{line_rec}" stroke-width="2.2" stroke-dasharray="5,3" marker-end="url(#arr-rec)"/>
      <text x="112" y="415" fill="{line_rec}" font-size="11" font-weight="bold">9</text>

      <!-- Corriente 10 y [7] Sumidero 1 -->
      <polyline points="320,532 345,532 345,575" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="350" y="555" fill="{line_main}" font-size="11" font-weight="bold">10</text>
      <polygon points="327,578 363,578 363,615 345,638 327,615" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="341" y="608" fill="{fg_txt}" font-size="12" font-weight="bold">7</text>
      <text x="250" y="612" fill="{fg_txt}" font-size="11" font-weight="bold">SUMIDERO 1</text>

      <!-- Corriente 11 y [8] Bomba 1 -->
      <line x1="345" y1="638" x2="345" y2="675" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="350" y="660" fill="{line_main}" font-size="11" font-weight="bold">11</text>
      <circle cx="345" cy="690" r="13" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <polygon points="333,704 357,704 352,698 338,698" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="341" y="694" fill="{fg_txt}" font-size="11" font-weight="bold">8</text>
      <text x="275" y="695" fill="{fg_txt}" font-size="11" font-weight="bold">BOMBA 1</text>

      <!-- Corriente 12 -->
      <polyline points="358,690 388,690 388,35 452,35 452,58" fill="none" stroke="{line_main}" stroke-width="2.2" marker-end="url(#arr)"/>
      <text x="394" y="295" fill="{line_main}" font-size="11" font-weight="bold">12 ({s10_rebose_kgh:.0f} kg/h)</text>
      <text x="394" y="310" fill="{line_main}" font-size="10">P80: {p80_rebose_um:.0f} µm</text>

      <!-- BLOQUE SUPERIOR DERECHO: FLOTACIÓN CIRCUITO 1 (EQUIPOS 9 AL 17) -->
      <polygon points="440,62 480,62 480,102 460,124 440,102" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="456" y="92" fill="{fg_txt}" font-size="12" font-weight="bold">9</text>
      <text x="488" y="85" fill="{fg_txt}" font-size="11" font-weight="bold">ACONDICIONADOR 1</text>

      <polyline points="460,124 460,140 520,140 520,158" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="482" y="135" fill="{line_main}" font-size="11" font-weight="bold">13</text>
      <polygon points="500,162 540,162 540,202 520,224 500,202" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="513" y="192" fill="{fg_txt}" font-size="12" font-weight="bold">10</text>
      <text x="435" y="192" fill="{fg_txt}" font-size="11" font-weight="bold">ACOND. 2</text>

      <!-- Corriente 14 con etiqueta debajo de la línea para no tocar la celda 11 -->
      <polyline points="520,224 520,242 585,242" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="502" y="257" fill="{line_main}" font-size="10" font-weight="bold">14 ({s14_alim_ro1_kgh:.0f} kg/h)</text>

      <!-- [11] Banco Rougher C1 -->
      <rect x="588" y="210" width="200" height="52" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <line x1="638" y1="210" x2="638" y2="262" stroke="{eq_stroke}" stroke-width="1.5"/>
      <line x1="688" y1="210" x2="688" y2="262" stroke="{eq_stroke}" stroke-width="1.5"/>
      <line x1="738" y1="210" x2="738" y2="262" stroke="{eq_stroke}" stroke-width="1.5"/>
      <polyline points="588,225 765,232 788,215" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="605" y="245" fill="{fg_txt}" font-size="12" font-weight="bold">11</text>
      <text x="625" y="202" fill="{fg_txt}" font-size="11" font-weight="bold">BANC. CEL. RO. C1 (4 Celdas)</text>

      <!-- Corriente 15 y [12] Banco Cleaner 1 -->
      <polyline points="755,210 755,152 875,152" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="780" y="145" fill="{line_main}" font-size="11" font-weight="bold">15 ({s15_esp_ro1_kgh:.1f} kg/h)</text>
      <rect x="878" y="135" width="96" height="48" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <line x1="926" y1="135" x2="926" y2="183" stroke="{eq_stroke}" stroke-width="1.5"/>
      <polyline points="878,148 955,154 974,140" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="892" y="168" fill="{fg_txt}" font-size="12" font-weight="bold">12</text>
      <text x="878" y="200" fill="{fg_txt}" font-size="11" font-weight="bold">BAN. CEL. CL. 1</text>

      <!-- Corriente 17: Concentrado Final C1 -->
      <polyline points="945,135 945,82 775,82" fill="none" stroke="{line_conc}" stroke-width="2.5" marker-end="url(#arr-conc)"/>
      <circle cx="765" cy="82" r="7" fill="none" stroke="{line_conc}" stroke-width="2"/>
      <text x="845" y="75" fill="{line_conc}" font-size="11" font-weight="bold">17</text>
      <text x="675" y="104" fill="{line_conc}" font-size="12" font-weight="bold">CONCENTRADO FINAL C1 ({s17_conc_c1_kgh:.2f} kg/h | Ley {m1_sym}: {ley_c1_m1:.1f}%)</text>

      <!-- Corriente 16 y [13] Banco Scavenger C1 -->
      <polyline points="788,242 998,242 998,338 935,338" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="860" y="236" fill="{line_main}" font-size="11" font-weight="bold">16 ({s16_cola_ro1_kgh:.1f} kg/h)</text>
      <rect x="680" y="308" width="250" height="52" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <line x1="730" y1="308" x2="730" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
      <line x1="780" y1="308" x2="780" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
      <line x1="830" y1="308" x2="830" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
      <line x1="880" y1="308" x2="880" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
      <polyline points="930,322 705,328 680,312" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="905" y="344" fill="{fg_txt}" font-size="12" font-weight="bold">13</text>
      <text x="695" y="298" fill="{fg_txt}" font-size="11" font-weight="bold">BANCO DE CELDAS SCV. CIRCUITO 1 (5 Celdas)</text>

      <!-- Corrientes 18 y 19 hacia [14] Sumidero 2 y [15] Bomba 2 -->
      <polyline points="974,162 1062,162 1062,395" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
      <text x="1068" y="280" fill="{line_rec}" font-size="11" font-weight="bold">18</text>
      <polyline points="710,360 710,382 1042,382 1042,395" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
      <text x="850" y="377" fill="{line_rec}" font-size="11" font-weight="bold">19</text>

      <polygon points="1032,398 1072,398 1072,435 1052,456 1032,435" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="1044" y="428" fill="{fg_txt}" font-size="12" font-weight="bold">14</text>
      <text x="948" y="428" fill="{fg_txt}" font-size="11" font-weight="bold">SUMIDERO 2</text>

      <polyline points="1052,456 1052,482 1085,482" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
      <text x="1035" y="474" fill="{line_rec}" font-size="11" font-weight="bold">20</text>
      <circle cx="1102" cy="482" r="13" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <polygon points="1090,496 1114,496 1109,490 1095,490" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="1095" y="486" fill="{fg_txt}" font-size="11" font-weight="bold">15</text>
      <text x="1080" y="462" fill="{fg_txt}" font-size="11" font-weight="bold">BOM. 2</text>

      <!-- Corriente 21 -->
      <polyline points="1115,482 1175,482 1175,18 468,18 468,58" fill="none" stroke="{line_rec}" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#arr-rec)"/>
      <text x="795" y="14" fill="{line_rec}" font-size="11" font-weight="bold">21 (Medios C1: {s21_medios_c1_kgh:.1f} kg/h)</text>

      <!-- Corriente 22, [16] Sumidero 3, Corriente 23, [17] Bomba 3 y Corriente 24 -->
      <polyline points="680,342 622,342 622,368" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="642" y="336" fill="{line_main}" font-size="11" font-weight="bold">22</text>
      <polygon points="602,372 642,372 642,408 622,428 602,408" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="614" y="402" fill="{fg_txt}" font-size="12" font-weight="bold">16</text>
      <text x="518" y="398" fill="{fg_txt}" font-size="11" font-weight="bold">SUMIDERO 3</text>

      <polyline points="622,428 622,452 572,452" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="595" y="446" fill="{line_main}" font-size="11" font-weight="bold">23</text>
      <circle cx="555" cy="452" r="13" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <polygon points="543,466 567,466 562,460 548,460" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="547" y="456" fill="{fg_txt}" font-size="11" font-weight="bold">17</text>
      <text x="528" y="482" fill="{fg_txt}" font-size="11" font-weight="bold">BOMBA 3</text>

      <polyline points="542,452 452,452 452,508" fill="none" stroke="{line_main}" stroke-width="2.2" marker-end="url(#arr)"/>
      <text x="455" y="445" fill="{line_main}" font-size="11" font-weight="bold">24 ({s22_cola_scv1_kgh:.1f} kg/h)</text>

      <!-- BLOQUE INFERIOR DERECHO: FLOTACIÓN CIRCUITO 2 (EQUIPOS 18 AL 24) -->
      <polygon points="440,512 480,512 480,550 460,570 440,550" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="452" y="542" fill="{fg_txt}" font-size="12" font-weight="bold">18</text>
      <text x="486" y="538" fill="{fg_txt}" font-size="11" font-weight="bold">ACON. 3</text>

      <polyline points="460,570 460,582 520,582 520,596" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="485" y="578" fill="{line_main}" font-size="11" font-weight="bold">25</text>
      <polygon points="500,600 540,600 540,636 520,656 500,636" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="512" y="628" fill="{fg_txt}" font-size="12" font-weight="bold">19</text>
      <text x="442" y="628" fill="{fg_txt}" font-size="11" font-weight="bold">ACON. 4</text>

      <!-- Corriente 26 y [20] Banco Rougher C2 -->
      <polyline points="520,656 520,668 585,668" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="542" y="663" fill="{line_main}" font-size="11" font-weight="bold">26</text>
      <rect x="588" y="635" width="200" height="48" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <line x1="638" y1="635" x2="638" y2="683" stroke="{eq_stroke}" stroke-width="1.5"/>
      <line x1="688" y1="635" x2="688" y2="683" stroke="{eq_stroke}" stroke-width="1.5"/>
      <line x1="738" y1="635" x2="738" y2="683" stroke="{eq_stroke}" stroke-width="1.5"/>
      <polyline points="588,648 765,655 788,640" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="605" y="666" fill="{fg_txt}" font-size="12" font-weight="bold">20</text>
      <text x="625" y="627" fill="{fg_txt}" font-size="11" font-weight="bold">BANC. CEL. RO. C2 (4 Celdas)</text>

      <!-- Corriente 27 y [21] Banco Cleaner 2 -->
      <polyline points="755,635 755,585 875,585" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="780" y="578" fill="{line_main}" font-size="11" font-weight="bold">27 ({s27_esp_ro2_kgh:.1f} kg/h)</text>
      <rect x="878" y="568" width="96" height="46" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <line x1="926" y1="568" x2="926" y2="614" stroke="{eq_stroke}" stroke-width="1.5"/>
      <polyline points="878,580 955,586 974,572" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="892" y="598" fill="{fg_txt}" font-size="12" font-weight="bold">21</text>
      <text x="878" y="630" fill="{fg_txt}" font-size="11" font-weight="bold">BAN. CEL. CL. 2</text>

      <!-- Corriente 29: Concentrado Final C2 -->
      <polyline points="945,568 945,525 775,525" fill="none" stroke="{line_conc}" stroke-width="2.5" marker-end="url(#arr-conc)"/>
      <circle cx="765" cy="525" r="7" fill="none" stroke="{line_conc}" stroke-width="2"/>
      <text x="845" y="518" fill="{line_conc}" font-size="11" font-weight="bold">29</text>
      <text x="675" y="546" fill="{line_conc}" font-size="12" font-weight="bold">CONCENTRADO FINAL C2 ({s29_conc_c2_kgh:.2f} kg/h | Ley {m2_sym}: {ley_c2_m2:.1f}%)</text>

      <!-- Corriente 28 y [22] Banco Scavenger C2 -->
      <polyline points="788,662 998,662 998,718 935,718" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="885" y="656" fill="{line_main}" font-size="11" font-weight="bold">28</text>
      <rect x="680" y="696" width="250" height="46" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <line x1="730" y1="696" x2="730" y2="742" stroke="{eq_stroke}" stroke-width="1.5"/>
      <line x1="780" y1="696" x2="780" y2="742" stroke="{eq_stroke}" stroke-width="1.5"/>
      <line x1="830" y1="696" x2="830" y2="742" stroke="{eq_stroke}" stroke-width="1.5"/>
      <line x1="880" y1="696" x2="880" y2="742" stroke="{eq_stroke}" stroke-width="1.5"/>
      <polyline points="930,708 705,714 680,700" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="905" y="726" fill="{fg_txt}" font-size="12" font-weight="bold">22</text>
      <text x="710" y="691" fill="{fg_txt}" font-size="10" font-weight="bold">BANCO DE CELDAS SCV. C2 (5 Celdas)</text>

      <!-- Corrientes 30 y 31 hacia [23] Sumidero 4 y [24] Bomba 4 -->
      <polyline points="974,592 1062,592 1062,672" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
      <text x="1068" y="635" fill="{line_rec}" font-size="11" font-weight="bold">30</text>
      <polyline points="710,742 710,752 1042,752 1042,672" fill="none" stroke="{line_rec}" stroke-width="1.8"/>
      <text x="850" y="749" fill="{line_rec}" font-size="11" font-weight="bold">31</text>

      <polygon points="1032,675 1072,675 1072,705 1052,722 1032,705" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="1044" y="698" fill="{fg_txt}" font-size="11" font-weight="bold">23</text>
      <text x="952" y="698" fill="{fg_txt}" font-size="10" font-weight="bold">SUMIDERO 4</text>

      <polyline points="1052,722 1052,735 1100,735" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
      <text x="1072" y="730" fill="{line_rec}" font-size="10" font-weight="bold">32</text>
      <circle cx="1116" cy="735" r="12" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="1109" y="739" fill="{fg_txt}" font-size="10" font-weight="bold">24</text>
      <text x="1095" y="718" fill="{fg_txt}" font-size="10" font-weight="bold">BOM. 4</text>

      <!-- Corriente 33 -->
      <polyline points="1128,735 1155,735 1155,498 468,498 468,508" fill="none" stroke="{line_rec}" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#arr-rec)"/>
      <text x="795" y="493" fill="{line_rec}" font-size="11" font-weight="bold">33 (Medios C2: {s33_medios_c2_kgh:.1f} kg/h)</text>

      <!-- Corriente 34: Relave Final -->
      <polyline points="680,718 425,718" fill="none" stroke="{line_rec}" stroke-width="2.5" marker-end="url(#arr-rec)"/>
      <circle cx="415" cy="718" r="7" fill="none" stroke="{line_rec}" stroke-width="2"/>
      <text x="435" y="708" fill="{line_rec}" font-size="11.5" font-weight="bold">34 — RELAVE FINAL ({s34_relave_final_kgh:.1f} kg/h)</text>
      <text x="435" y="734" fill="{line_rec}" font-size="10.5" font-weight="bold">Leyes: {ley_rel_m1:.2f}% {m1_sym} | {ley_rel_m2:.2f}% {m2_sym}</text>

      <!-- Cajetín Técnico UNMSM -->
      <rect x="20" y="655" width="235" height="85" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.5"/>
      <text x="32" y="675" fill="{fg_txt}" font-size="11" font-weight="bold">DIAGRAMA DE FLUJO</text>
      <text x="32" y="692" fill="{fg_txt}" font-size="11" font-weight="bold">"PLANTA PILOTO JICA"</text>
      <text x="32" y="708" fill="{fg_txt}" font-size="10">INGENIERÍA METALÚRGICA - UNMSM</text>
      <text x="32" y="726" fill="{fg_txt}" font-size="9">GEMELO DIGITAL INTERACTIVO (24 EQ / 34 CORR)</text>
    </svg>"""

    svg_flowsheet = f'<div style="background:{bg_svg}; border:1px solid {eq_stroke}; border-radius:8px; padding:6px; overflow-x:auto;">{svg_only}</div>'
    components.html(svg_flowsheet, height=700, scrolling=False)

    st.download_button(
        label="📐 Descargar Plano Flowsheet JICA Vectorial (.SVG para Informes UNMSM)",
        data=svg_only.encode("utf-8"),
        file_name=f"Flowsheet_Planta_Piloto_JICA_{m1_sym}_{m2_sym}.svg",
        mime="image/svg+xml"
    )

with tab_et1:
    c_izq, c_der = st.columns([1.45, 1])
    with c_izq:
        st.subheader("📈 Curvas Granulométricas Rosin-Rammler (Etapa 1)")
        n_rr = 1.15
        d63_reb = p80_rebose_um / ((-np.log(0.20)) ** (1.0 / n_rr))
        d63_rod = f80_molino_um / ((-np.log(0.20)) ** (1.0 / 0.95))
        aberturas = np.geomspace(15, 25000, 250)
        pas_reb = 100.0 * (1.0 - np.exp(-((aberturas / d63_reb) ** n_rr)))
        pas_rod = 100.0 * (1.0 - np.exp(-((aberturas / d63_rod) ** 0.95)))

        fig_g = go.Figure()
        fig_g.add_trace(go.Scatter(
            x=aberturas, y=pas_rod, mode="lines",
            name=f"Corr. 3/4: Salida Rodillos (F80 = {f80_molino_um:.0f} µm)",
            line=dict(dash="dash", color="#ffa726", width=2.8)
        ))
        fig_g.add_trace(go.Scatter(
            x=aberturas, y=pas_reb, mode="lines",
            name=f"Corr. 10/12: Rebose Espiral (P80 = {p80_rebose_um:.0f} µm)",
            line=dict(color="#29b6f6", width=3.5)
        ))
        fig_g.add_trace(go.Scatter(
            x=[15, 25000], y=[80, 80], mode="lines",
            name=f"Línea P80 ({p80_rebose_um:.0f} µm)",
            line=dict(dash="dot", color="#ef5350", width=1.8)
        ))
        fig_g.add_trace(go.Scatter(
            x=[149, 149], y=[0, 100], mode="lines",
            name="Malla 100 (149 µm)",
            line=dict(dash="dot", color="#66bb6a", width=1.8)
        ))
        fig_g.add_trace(go.Scatter(
            x=[74, 74], y=[0, 100], mode="lines",
            name="Malla 200 (74 µm)",
            line=dict(dash="dot", color="#ab47bc", width=1.5)
        ))

        fig_g.update_layout(
            xaxis=dict(
                type="log",
                title="Abertura de Malla (µm) — Escala Logarítmica",
                range=[np.log10(15), np.log10(25000)],
                tickvals=[20, 37, 53, 74, 105, 149, 210, 500, 1000, 2500, 7500, 20000],
                ticktext=["20", "37", "53", "74 (M200)", "105", "149 (M100)", "210", "500", "1000", "2500", "7500", "20000"]
            ),
            yaxis=dict(title="% Pasante Acumulado F(x)", range=[0, 105]),
            template="plotly_dark",
            height=420,
            legend=dict(orientation="h", y=1.14)
        )
        st.plotly_chart(fig_g, width="stretch")

    with c_der:
        st.subheader("💧 Balance de Agua y Energía en Molienda")
        st.info(
            f"**Agua Entrada [Corr. 6]:** {w6_agua_entrada_lh:.1f} L/h  \n"
            f"**Agua Salida / Dilución [Corr. 8]:** {w8_agua_salida_lh:.1f} L/h  \n"
            f"**Agua en Rebose [Corr. 10/12]:** {w10_rebose_lh:.1f} L/h  \n"
            f"**Consumo Específico Bond:** {w_bond_kwht:.2f} kWh/t ({potencia_molino_kw:.2f} kW)"
        )
        mallas = [("Malla 65", 210), ("Malla 100", 149), ("Malla 140", 105), ("Malla 200", 74), ("Malla 270", 53), ("Malla 400", 37)]
        df_m = pd.DataFrame([{"Malla": m, "µm": u, "% Pasante Rebose [10]": round(100*(1-np.exp(-((u/d63_reb)**n_rr))), 1)} for m, u in mallas])
        st.dataframe(df_m, width="stretch", hide_index=True)

with tab_et23:
    st.subheader(f"⚖️ Balance Metalúrgico Global de 3 Productos ({m1_sym} - {m2_sym})")
    df_3prod = pd.DataFrame({
        "Producto / Corriente": [
            "Alimento Fresco [Corr. 1 / 12]",
            f"Concentrado Final C1 ({m1_sym}) [Corr. 17]",
            f"Concentrado Final C2 ({m2_sym}) [Corr. 29]",
            "Relave Final [Corr. 34]"
        ],
        "Peso Seco (kg/h)": [F_kgh, s17_conc_c1_kgh, s29_conc_c2_kgh, s34_relave_final_kgh],
        "% Peso": [100.0, (s17_conc_c1_kgh/F_kgh)*100, (s29_conc_c2_kgh/F_kgh)*100, (s34_relave_final_kgh/F_kgh)*100],
        f"Ley {m1_sym} (%)": [ley_f_m1, ley_c1_m1, (fino_m1_c2/s29_conc_c2_kgh)*100, ley_rel_m1],
        f"Dist. {m1_sym} (%)": [100.0, rec_global_c1, (fino_m1_c2/fino_m1_alim)*100, (fino_m1_rel/fino_m1_alim)*100],
        f"Ley {m2_sym} (%)": [ley_f_m2, (fino_m2_c1/s17_conc_c1_kgh)*100, ley_c2_m2, ley_rel_m2],
        f"Dist. {m2_sym} (%)": [100.0, (fino_m2_c1/fino_m2_alim)*100, rec_global_c2, (fino_m2_rel/fino_m2_alim)*100],
    })
    st.dataframe(df_3prod.round(2), width="stretch", hide_index=True)

    c_reac1, c_reac2 = st.columns(2)
    t_h = F_kgh / 1000.0
    with c_reac1:
        st.markdown(f"#### 🧪 Dosificación de Reactivos Circuito 1 ({m1_sym})")
        st.write(f"- **Depresor $\\text{{ZnSO}}_4$ (Acond. 1 [Eq. 9]):** {dosis_dep_c1:.0f} g/t $\\rightarrow$ **{(dosis_dep_c1*t_h)/60:.2f} g/min**")
        st.write(f"- **Colector Xantato Z-11 (Acond. 2 [Eq. 10]):** {dosis_col_c1:.0f} g/t $\\rightarrow$ **{(dosis_col_c1*t_h)/60:.2f} g/min**")
    with c_reac2:
        st.markdown(f"#### 🧪 Dosificación de Reactivos Circuito 2 ({m2_sym})")
        st.write(f"- **Activador $\\text{{CuSO}}_4$ (Acond. 3 [Eq. 18]):** {dosis_act_c2:.0f} g/t $\\rightarrow$ **{(dosis_act_c2*t_h)/60:.2f} g/min**")
        st.write(f"- **Colector Xantato Z-6 (Acond. 4 [Eq. 19]):** {dosis_col_c2:.0f} g/t $\\rightarrow$ **{(dosis_col_c2*t_h)/60:.2f} g/min**")

with tab_34:
    st.subheader("📋 Registro Oficial de las 34 Corrientes — Planta Piloto JICA")
    corrientes_data = [
        (1, "Alimento Fresco a Chanc. Mandíbulas [Eq. 1]", F_kgh, 100.0, 0.0),
        (2, "Descarga Chanc. Mandíbulas a Rodillos [Eq. 2]", F_kgh, 100.0, 0.0),
        (3, "Descarga Chanc. Rodillos a Tolva Finos [Eq. 3]", F_kgh, 100.0, 0.0),
        (4, "Descarga Tolva Finos a Nodo Mezcla [Eq. 4]", F_kgh, 100.0, 0.0),
        (5, "Alimentación Compuesta a Molino 2'x2' [Eq. 5]", s5_alim_molino_kgh, sol_molino, w5_molino_lh),
        (6, "Agua Entrada a Molienda [Nodo 4]", 0.0, 0.0, w6_agua_entrada_lh),
        (7, "Descarga Molino Bolas 2'x2' a Clasificador [Eq. 6]", s7_desc_molino_kgh, sol_molino, w5_molino_lh),
        (8, "Agua Salida (Dilución a Clasificador Helicoidal)", 0.0, 0.0, w8_agua_salida_lh),
        (9, "Arenas Clasificador Helicoidal (Carga Circulante)", s9_arenas_kgh, 76.0, w9_arenas_lh),
        (10, "Rebose Clasificador Helicoidal a Sumidero 1 [Eq. 7]", s10_rebose_kgh, sol_rebose, w10_rebose_lh),
        (11, "Descarga Sumidero 1 a Bomba 1 [Eq. 8]", s10_rebose_kgh, sol_rebose, w10_rebose_lh),
        (12, "Impulsión Bomba 1 a Acondicionador 1 [Eq. 9]", s10_rebose_kgh, sol_rebose, w10_rebose_lh),
        (13, "Paso Acondicionador 1 a Acondicionador 2 [Eq. 10]", s14_alim_ro1_kgh, 29.0, s14_alim_ro1_kgh*(71/29)),
        (14, "Descarga Acond. 2 a Banco Rougher C1 [Eq. 11]", s14_alim_ro1_kgh, 29.0, s14_alim_ro1_kgh*(71/29)),
        (15, "Espumas Rougher C1 a Banco Cleaner 1 [Eq. 12]", s15_esp_ro1_kgh, 22.0, s15_esp_ro1_kgh*(78/22)),
        (16, "Colas Rougher C1 a Banco Scavenger C1 [Eq. 13]", s16_cola_ro1_kgh, 30.0, s16_cola_ro1_kgh*(70/30)),
        (17, f"CONCENTRADO FINAL C1 ({m1_sym}) (Espumas Cleaner 1)", s17_conc_c1_kgh, 25.0, s17_conc_c1_kgh*(75/25)),
        (18, "Colas Cleaner 1 a Sumidero 2 [Eq. 14]", s18_cola_cl1_kgh, 18.0, s18_cola_cl1_kgh*(82/18)),
        (19, "Espumas Scavenger C1 a Sumidero 2 [Eq. 14]", s19_esp_scv1_kgh, 20.0, s19_esp_scv1_kgh*(80/20)),
        (20, "Descarga Sumidero 2 a Bomba 2 [Eq. 15]", s21_medios_c1_kgh, 19.0, s21_medios_c1_kgh*(81/19)),
        (21, "Recirculación Medios C1 (Bomba 2 a Acond. 1)", s21_medios_c1_kgh, 19.0, s21_medios_c1_kgh*(81/19)),
        (22, "Colas Scavenger C1 a Sumidero 3 [Eq. 16]", s22_cola_scv1_kgh, 28.0, s22_cola_scv1_kgh*(72/28)),
        (23, "Descarga Sumidero 3 a Bomba 3 [Eq. 17]", s22_cola_scv1_kgh, 28.0, s22_cola_scv1_kgh*(72/28)),
        (24, "Impulsión Bomba 3 a Acondicionador 3 [Eq. 18]", s22_cola_scv1_kgh, 28.0, s22_cola_scv1_kgh*(72/28)),
        (25, "Paso Acondicionador 3 a Acondicionador 4 [Eq. 19]", s26_alim_ro2_kgh, 27.0, s26_alim_ro2_kgh*(73/27)),
        (26, "Descarga Acond. 4 a Banco Rougher C2 [Eq. 20]", s26_alim_ro2_kgh, 27.0, s26_alim_ro2_kgh*(73/27)),
        (27, "Espumas Rougher C2 a Banco Cleaner 2 [Eq. 21]", s27_esp_ro2_kgh, 22.0, s27_esp_ro2_kgh*(78/22)),
        (28, "Colas Rougher C2 a Banco Scavenger C2 [Eq. 22]", s28_cola_ro2_kgh, 28.0, s28_cola_ro2_kgh*(72/28)),
        (29, f"CONCENTRADO FINAL C2 ({m2_sym}) (Espumas Cleaner 2)", s29_conc_c2_kgh, 25.0, s29_conc_c2_kgh*(75/25)),
        (30, "Colas Cleaner 2 a Sumidero 4 [Eq. 23]", s30_cola_cl2_kgh, 18.0, s30_cola_cl2_kgh*(82/18)),
        (31, "Espumas Scavenger C2 a Sumidero 4 [Eq. 23]", s31_esp_scv2_kgh, 20.0, s31_esp_scv2_kgh*(80/20)),
        (32, "Descarga Sumidero 4 a Bomba 4 [Eq. 24]", s33_medios_c2_kgh, 19.0, s33_medios_c2_kgh*(81/19)),
        (33, "Recirculación Medios C2 (Bomba 4 a Acond. 3)", s33_medios_c2_kgh, 19.0, s33_medios_c2_kgh*(81/19)),
        (34, "RELAVE FINAL (Colas Banco Scavenger C2)", s34_relave_final_kgh, 26.0, s34_relave_final_kgh*(74/26)),
    ]
    df_34 = pd.DataFrame(corrientes_data, columns=["N° Corriente", "Descripción en Plano JICA", "Sólidos (kg/h)", "% Sólidos", "Agua (L/h)"])
    df_34["Pulpa Total (L/h)"] = (df_34["Sólidos (kg/h)"] / sg_mineral) + df_34["Agua (L/h)"]
    st.dataframe(df_34.round(2), width="stretch", hide_index=True)

    # Generar Excel en memoria RAM para descarga desde cualquier navegador web o celular
    buffer_excel = io.BytesIO()
    with pd.ExcelWriter(buffer_excel, engine="xlsxwriter") as writer:
        df_3prod.round(2).to_excel(writer, sheet_name="Balance_Global_C1_C2", index=False)
        df_34.round(2).to_excel(writer, sheet_name="34_Corrientes_JICA", index=False)
    buffer_excel.seek(0)

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="🌐 Descargar Excel Completo en el Navegador (34 Corrientes + Balance)",
            data=buffer_excel,
            file_name=f"Reporte_Planta_Piloto_JICA_{m1_sym}_{m2_sym}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col_dl2:
        ruta_drive = Path(r"G:\Mi unidad\02_Trabajo_Metalurgia\01_Balances_y_Planta")
        if ruta_drive.exists():
            if st.button("💾 Guardar Copia Directa en mi Google Drive Local (G:)"):
                archivo_full = ruta_drive / f"Gemelo_Digital_JICA_34Corrientes_{m1_sym}_{m2_sym}.xlsx"
                with open(archivo_full, "wb") as f:
                    f.write(buffer_excel.getvalue())
                st.success(f"Guardado en Google Drive: {archivo_full}")

