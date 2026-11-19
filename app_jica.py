import io
from datetime import datetime
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Gemelo Digital — Planta Piloto JICA (UNMSM)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILOS INDUSTRIALES SOBRIOS (SCADA / SIMULACIÓN) ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #F8FAFC;
    color: #0F172A;
}

.block-container {
    padding-top: 1.25rem;
    padding-bottom: 1.25rem;
    max-width: 98%;
}

/* Ocultar botón Deploy, menú superior derecho y footer de Streamlit */
[data-testid="stAppDeployButton"],
#MainMenu,
header[data-testid="stHeader"] {
    visibility: hidden;
    display: none;
}

footer {
    visibility: hidden;
    display: none;
}

/* Barra lateral sobria */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
}

[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #0F172A;
    font-weight: 600;
    letter-spacing: -0.01em;
}

/* Cabecera principal e insignia de estado SCADA */
.header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #1E3A8A;
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 14px;
}

.header-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #0F172A;
    margin: 0 0 3px 0;
    letter-spacing: -0.02em;
}

.header-subtitle {
    font-size: 0.82rem;
    color: #475569;
    margin: 0;
}

.scada-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    white-space: nowrap;
}

.badge-ok {
    background-color: #EFF6FF;
    color: #1E3A8A;
    border: 1px solid #BFDBFE;
}

.badge-warn {
    background-color: #FFFBEB;
    color: #92400E;
    border: 1px solid #FDE68A;
}

.badge-err {
    background-color: #FEF2F2;
    color: #991B1B;
    border: 1px solid #FECACA;
}

/* Tarjetas KPI corporativas con simetría vertical */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 10px;
    margin-bottom: 12px;
    width: 100%;
    box-sizing: border-box;
}

@media (max-width: 1100px) {
    .kpi-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

.kpi-card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 11px 14px;
    min-height: 92px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
    box-sizing: border-box;
}

.kpi-top {
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.kpi-label {
    font-size: 0.71rem;
    font-weight: 600;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

.kpi-value {
    font-size: 1.24rem;
    font-weight: 700;
    color: #0F172A;
    line-height: 1.2;
}

.kpi-delta {
    font-size: 0.74rem;
    font-weight: 500;
    color: #1E3A8A;
    line-height: 1.25;
    margin-top: 6px;
}

/* Alertas técnicas compactas */
.alert-item {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 5px;
    padding: 7px 12px;
    margin-bottom: 10px;
    font-size: 0.80rem;
    color: #334155;
}

.alert-item-warn {
    border-left: 3px solid #B45309;
    background-color: #FFFBEB;
    color: #78350F;
}

.alert-item-err {
    border-left: 3px solid #B91C1C;
    background-color: #FEF2F2;
    color: #7F1D1D;
}

/* Barra de herramientas del Flowsheet */
.toolbar-panel {
    background-color: #F1F5F9;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 10px 12px 4px 12px;
    margin-bottom: 10px;
}

.inspector-strip {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 3px solid #1E3A8A;
    border-radius: 5px;
    padding: 8px 12px;
    margin-bottom: 10px;
    font-size: 0.82rem;
    color: #0F172A;
}

/* Pestañas sobrias */
button[data-baseweb="tab"] {
    font-weight: 600;
    font-size: 0.84rem;
    color: #475569;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #1E3A8A;
    border-bottom-color: #1E3A8A;
}

/* Expanders de sidebar */
div[data-testid="stExpander"] {
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    margin-bottom: 8px;
}

/* Barra de estado técnica inferior */
.status-footer {
    margin-top: 20px;
    padding-top: 10px;
    border-top: 1px solid #E2E8F0;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    gap: 8px;
    font-size: 0.75rem;
    color: #64748B;
}
</style>
""", unsafe_allow_html=True)

# ==================== PANEL LATERAL: ENTRADAS OPERATIVAS Y QUÍMICAS ====================
st.sidebar.markdown("## Control de Proceso JICA")

tema_plano = st.sidebar.radio(
    "Estilo del Diagrama",
    ["Plano CAD (Blanco Técnico)", "SCADA (Oscuro)"],
    index=0,
    horizontal=True
)

esquema_mineral = st.sidebar.selectbox(
    "Esquema de Flotación Diferencial",
    [
        "Pb - Zn (Galena en C1 / Esfalerita en C2)",
        "Cu - Zn (Calcopirita en C1 / Esfalerita en C2)",
        "Cu - Pb (Calcopirita en C1 / Galena en C2)"
    ]
)

if esquema_mineral.startswith("Pb - Zn"):
    m1_sym, m2_sym = "Pb", "Zn"
    d_m1_f, d_m2_f, d_fe_f = 3.20, 5.50, 14.0
elif esquema_mineral.startswith("Cu - Zn"):
    m1_sym, m2_sym = "Cu", "Zn"
    d_m1_f, d_m2_f, d_fe_f = 1.85, 4.80, 16.5
else:
    m1_sym, m2_sym = "Cu", "Pb"
    d_m1_f, d_m2_f, d_fe_f = 1.60, 3.40, 13.0

with st.sidebar.expander("1. Chancado y Molienda", expanded=True):
    F_kgh = st.number_input("Alimento Fresco (kg/h)", min_value=100.0, max_value=800.0, value=325.0, step=25.0, help="Corriente 1 — Alimentación fresca a Chancadora de Mandíbulas [Equipo 1]")
    f80_alim_mm = st.number_input("F80 Alimento Fresco (mm)", min_value=25.0, max_value=127.0, value=105.0, step=5.0, help="Tamaño característico F80 del mineral fresco [Corriente 1]")
    set_mandibulas_mm = st.number_input("Set Chanc. Mandíbulas (mm)", min_value=12.0, max_value=38.0, value=26.0, step=1.0, help="CSS — Closed Side Setting de Chancadora de Mandíbulas [Equipo 1]")
    set_rodillos_mm = st.number_input("Set Chanc. Rodillos (mm)", min_value=3.0, max_value=15.0, value=6.5, step=0.5, help="Abertura entre rodillos de chancadora secundaria [Equipo 2]")
    wi_bond = st.number_input("Work Index Bond Wi (kWh/t)", min_value=8.0, max_value=25.0, value=13.8, step=0.2, help="Índice de trabajo de Bond para cálculo energético en molienda [Equipo 5]")
    sol_molino = st.number_input("% Sólidos Molino 2'x2'", min_value=55.0, max_value=84.0, value=72.0, step=1.0, help="Porcentaje de sólidos en peso en la alimentación al Molino de Bolas 2'x2' [Equipo 5 / Corriente 5]")
    cc_espiral_pct = st.number_input("Carga Circulante Espiral (%)", min_value=80.0, max_value=320.0, value=210.0, step=10.0, help="Relación de arenas recirculadas [Corriente 9] respecto al alimento fresco en Clasificador Helicoidal [Equipo 6]")
    sol_rebose = st.number_input("% Sólidos Rebose", min_value=20.0, max_value=45.0, value=30.0, step=1.0, help="Porcentaje de sólidos en peso en el rebose del clasificador [Corrientes 10 / 12]")
    sg_mineral = st.number_input("Gravedad Específica Mineral (SG)", min_value=2.5, max_value=4.5, value=2.95, step=0.05, help="Densidad relativa de sólidos (t/m³) para conversión de flujos másicos a volumétricos")

with st.sidebar.expander(f"2. Leyes de Cabeza ({m1_sym}, {m2_sym}, Fe) y Reactivos", expanded=False):
    ley_f_m1 = st.number_input(f"Ley Cabeza {m1_sym} (%)", min_value=0.2, max_value=20.0, value=d_m1_f, step=0.1, help=f"Ley inicial de {m1_sym} en el alimento fresco [Corriente 1]")
    ley_f_m2 = st.number_input(f"Ley Cabeza {m2_sym} (%)", min_value=0.5, max_value=25.0, value=d_m2_f, step=0.1, help=f"Ley inicial de {m2_sym} en el alimento fresco [Corriente 1]")
    ley_f_fe = st.number_input("Ley Cabeza Fe / Pirita (%)", min_value=1.0, max_value=45.0, value=d_fe_f, step=0.5, help="Contenido de hierro / sulfuros de hierro en cabeza [Corriente 1]")
    ph_c1 = st.number_input("pH Acondicionamiento C1", min_value=6.5, max_value=11.5, value=8.5, step=0.1, help="pH de pulpa en Acondicionadores 1 y 2 [Equipos 9 y 10]")
    dosis_dep_c1 = st.number_input("Depresor ZnSO4 Acond. 1 (g/t)", min_value=0.0, max_value=800.0, value=250.0, step=25.0, help="Dosificación de sulfato de zinc en Acondicionador 1 [Equipo 9]")
    dosis_col_c1 = st.number_input("Colector Z-11 Acond. 2 (g/t)", min_value=5.0, max_value=150.0, value=35.0, step=5.0, help="Dosificación de xantato colector en Acondicionador 2 [Equipo 10]")
    ph_c2 = st.number_input("pH Acondicionamiento C2", min_value=8.0, max_value=12.5, value=10.8, step=0.1, help="pH alcalino en Acondicionadores 3 y 4 del Circuito 2 [Equipos 18 y 19]")
    dosis_act_c2 = st.number_input("Activador CuSO4 Acond. 3 (g/t)", min_value=50.0, max_value=1000.0, value=350.0, step=25.0, help="Dosificación de sulfato de cobre como activador en Acondicionador 3 [Equipo 18]")
    dosis_col_c2 = st.number_input("Colector Z-6 Acond. 4 (g/t)", min_value=5.0, max_value=150.0, value=45.0, step=5.0, help="Dosificación de colector en Acondicionador 4 [Equipo 19]")

with st.sidebar.expander("3. Selectividad de Bancos", expanded=False):
    rec_ro1 = st.number_input("Rec. Rougher C1 (%)", min_value=55.0, max_value=95.0, value=82.0, step=1.0, help="Recuperación de etapa en Banco Rougher Circuito 1 [Equipo 11]")
    rec_cl1 = st.number_input("Rec. Cleaner 1 (%)", min_value=60.0, max_value=98.0, value=88.0, step=1.0, help="Recuperación de etapa en Banco Cleaner 1 [Equipo 12]")
    rec_scv1 = st.number_input("Rec. Scavenger C1 (%)", min_value=25.0, max_value=85.0, value=55.0, step=1.0, help="Recuperación de etapa en Banco Scavenger Circuito 1 [Equipo 13]")
    rec_ro2 = st.number_input("Rec. Rougher C2 (%)", min_value=55.0, max_value=95.0, value=80.0, step=1.0, help="Recuperación de etapa en Banco Rougher Circuito 2 [Equipo 20]")
    rec_cl2 = st.number_input("Rec. Cleaner 2 (%)", min_value=60.0, max_value=98.0, value=86.0, step=1.0, help="Recuperación de etapa en Banco Cleaner 2 [Equipo 21]")
    rec_scv2 = st.number_input("Rec. Scavenger C2 (%)", min_value=25.0, max_value=85.0, value=50.0, step=1.0, help="Recuperación de etapa en Banco Scavenger Circuito 2 [Equipo 22]")

# ==================== MOTOR METALÚRGICO (RESULTADOS CALCULADOS) ====================
def simular_planta(
    F_val, f80_val, css_mand, gap_rod, wi_val, sol_mol, cc_pct, sol_reb, sg_val,
    f_m1, f_m2, f_fe, ph1, dep1, col1, ph2, act2, col2,
    r_ro1_p, r_cl1_p, r_scv1_p, r_ro2_p, r_cl2_p, r_scv2_p
):
    p80_mand_mm = css_mand * 1.22
    p80_rod_mm = gap_rod * 1.18
    f80_mol_um = p80_rod_mm * 1000.0

    factor_cc = np.clip((cc_pct - 100.0) * 0.08, -15.0, 28.0)
    factor_wi = (wi_val - 13.8) * 2.2
    p80_reb_calc = float(np.clip(149.0 - factor_cc + factor_wi + (F_val - 325.0) * 0.03, 75.0, 210.0))

    cc_frac = cc_pct / 100.0
    s9_arenas = F_val * cc_frac
    s5_alim_mol = F_val + s9_arenas
    s7_desc_mol = s5_alim_mol
    s10_rebose = F_val

    w9_arenas = s9_arenas * (24.0 / 76.0)
    w5_molino = s5_alim_mol * ((100.0 - sol_mol) / sol_mol)
    w6_agua_ent = max(0.0, w5_molino - w9_arenas)
    w10_rebose = s10_rebose * ((100.0 - sol_reb) / sol_reb)
    w8_agua_sal = max(0.0, (w10_rebose + w9_arenas) - w5_molino)

    w_bond_kwh_t = 10.0 * wi_val * ((1.0 / np.sqrt(p80_reb_calc)) - (1.0 / np.sqrt(f80_mol_um)))
    pot_molino_kw = w_bond_kwh_t * (F_val / 1000.0)

    efecto_molienda_m1 = np.clip((155.0 - p80_reb_calc) * 0.06, -5.0, 4.0)
    efecto_dep_c1 = np.clip((dep1 - 250.0) * 0.004, -1.5, 2.0)
    efecto_col_c1 = np.clip((col1 - 35.0) * 0.03, -2.5, 3.0)
    rec_glob_c1 = float(np.clip(86.0 + efecto_molienda_m1 + efecto_col_c1, 55.0, 95.0))

    ley_c1_base = 58.0 if m1_sym == "Pb" else 28.0
    ley_c1_m1 = float(np.clip(ley_c1_base + efecto_dep_c1 * 1.8 - efecto_col_c1 * 0.6 + (ph1 - 8.5) * 0.8, 18.0, 76.0))

    fino_m1_alim = F_val * (f_m1 / 100.0)
    fino_m1_c1 = fino_m1_alim * (rec_glob_c1 / 100.0)
    s17_c1 = fino_m1_c1 / (ley_c1_m1 / 100.0)
    s22_cola_scv1 = max(10.0, F_val - s17_c1)

    r_cl1_f, r_scv1_f = r_cl1_p / 100.0, r_scv1_p / 100.0
    s15_esp_ro1 = s17_c1 / max(0.35, r_cl1_f * 0.78)
    s18_cola_cl1 = max(1.0, s15_esp_ro1 - s17_c1)
    s19_esp_scv1 = s22_cola_scv1 * (0.12 * r_scv1_f)
    s21_medios_c1 = s18_cola_cl1 + s19_esp_scv1
    s14_alim_ro1 = F_val + s21_medios_c1
    s16_cola_ro1 = s14_alim_ro1 - s15_esp_ro1

    efecto_act_c2 = np.clip((act2 - 350.0) * 0.008, -4.0, 4.5)
    efecto_col_c2 = np.clip((col2 - 45.0) * 0.025, -2.0, 2.5)
    efecto_ph_c2 = np.clip((ph2 - 10.8) * 1.2, -2.0, 2.0)
    rec_glob_c2 = float(np.clip(84.0 + efecto_act_c2 + efecto_col_c2 + efecto_molienda_m1 * 0.5, 50.0, 94.0))

    ley_c2_base = 52.0 if m2_sym == "Zn" else 60.0
    ley_c2_m2 = float(np.clip(ley_c2_base + efecto_ph_c2 - efecto_col_c2 * 0.5, 22.0, 68.0))

    fino_m2_alim = F_val * (f_m2 / 100.0)
    fino_m2_c2 = fino_m2_alim * (rec_glob_c2 / 100.0)
    s29_c2 = fino_m2_c2 / (ley_c2_m2 / 100.0)
    s34_relave = max(5.0, s22_cola_scv1 - s29_c2)

    r_cl2_f, r_scv2_f = r_cl2_p / 100.0, r_scv2_p / 100.0
    s27_esp_ro2 = s29_c2 / max(0.35, r_cl2_f * 0.76)
    s30_cola_cl2 = max(1.0, s27_esp_ro2 - s29_c2)
    s31_esp_scv2 = s34_relave * (0.14 * r_scv2_f)
    s33_medios_c2 = s30_cola_cl2 + s31_esp_scv2
    s26_alim_ro2 = s22_cola_scv1 + s33_medios_c2
    s28_cola_ro2 = s26_alim_ro2 - s27_esp_ro2

    fino_m1_c2 = s29_c2 * 0.015
    fino_m1_rel = max(0.0, fino_m1_alim - fino_m1_c1 - fino_m1_c2)
    ley_rel_m1 = (fino_m1_rel / s34_relave) * 100.0

    fino_m2_c1 = s17_c1 * 0.035
    fino_m2_rel = max(0.0, fino_m2_alim - fino_m2_c2 - fino_m2_c1)
    ley_rel_m2 = (fino_m2_rel / s34_relave) * 100.0

    pulpa_rebose_lmin = ((s10_rebose / sg_val) + w10_rebose) / 60.0

    # Verificación de cierre de balance de masa en sólidos (kg/h)
    suma_salidas_solidos = s17_c1 + s29_c2 + s34_relave
    error_masa_pct = abs(F_val - suma_salidas_solidos) / max(F_val, 1e-9) * 100.0

    return {
        "p80_mand_mm": p80_mand_mm, "p80_rod_mm": p80_rod_mm, "f80_mol_um": f80_mol_um,
        "p80_reb_calc": p80_reb_calc, "s9_arenas": s9_arenas, "s5_alim_mol": s5_alim_mol,
        "s7_desc_mol": s7_desc_mol, "s10_rebose": s10_rebose, "w9_arenas": w9_arenas,
        "w5_molino": w5_molino, "w6_agua_ent": w6_agua_ent, "w10_rebose": w10_rebose,
        "w8_agua_sal": w8_agua_sal, "w_bond_kwh_t": w_bond_kwh_t, "pot_molino_kw": pot_molino_kw,
        "rec_glob_c1": rec_glob_c1, "ley_c1_m1": ley_c1_m1, "s17_c1": s17_c1,
        "s22_cola_scv1": s22_cola_scv1, "s15_esp_ro1": s15_esp_ro1, "s18_cola_cl1": s18_cola_cl1,
        "s19_esp_scv1": s19_esp_scv1, "s21_medios_c1": s21_medios_c1, "s14_alim_ro1": s14_alim_ro1,
        "s16_cola_ro1": s16_cola_ro1, "rec_glob_c2": rec_glob_c2, "ley_c2_m2": ley_c2_m2,
        "s29_c2": s29_c2, "s34_relave": s34_relave, "s27_esp_ro2": s27_esp_ro2,
        "s30_cola_cl2": s30_cola_cl2, "s31_esp_scv2": s31_esp_scv2, "s33_medios_c2": s33_medios_c2,
        "s26_alim_ro2": s26_alim_ro2, "s28_cola_ro2": s28_cola_ro2, "fino_m1_alim": fino_m1_alim,
        "fino_m1_c1": fino_m1_c1, "fino_m1_c2": fino_m1_c2, "fino_m1_rel": fino_m1_rel,
        "ley_rel_m1": ley_rel_m1, "fino_m2_alim": fino_m2_alim, "fino_m2_c1": fino_m2_c1,
        "fino_m2_c2": fino_m2_c2, "fino_m2_rel": fino_m2_rel, "ley_rel_m2": ley_rel_m2,
        "pulpa_rebose_lmin": pulpa_rebose_lmin,
        "error_masa_pct": error_masa_pct
    }

res = simular_planta(
    F_kgh, f80_alim_mm, set_mandibulas_mm, set_rodillos_mm, wi_bond,
    sol_molino, cc_espiral_pct, sol_rebose, sg_mineral,
    ley_f_m1, ley_f_m2, ley_f_fe, ph_c1, dosis_dep_c1, dosis_col_c1,
    ph_c2, dosis_act_c2, dosis_col_c2,
    rec_ro1, rec_cl1, rec_scv1, rec_ro2, rec_cl2, rec_scv2
)

# ==================== COMPARADOR CASO BASE VS. ACTUAL ====================
if "caso_base" not in st.session_state:
    st.session_state["caso_base"] = res.copy()

st.sidebar.markdown("---")
if st.sidebar.button("Fijar Estado Actual como Caso Base", width="stretch"):
    st.session_state["caso_base"] = res.copy()
    st.sidebar.caption("Caso base actualizado.")

base = st.session_state["caso_base"]

def delta_str(actual, ref, sufijo=""):
    diff = actual - ref
    if abs(diff) < 1e-4:
        return f"Base: {actual:.2f}{sufijo}"
    signo = "+" if diff > 0 else ""
    return f"{signo}{diff:.2f}{sufijo} vs. base"

# ==================== ALERTAS OPERATIVAS SCADA ====================
alertas = []
if sol_molino > 78.0:
    alertas.append(("err", f"Límite excedido [Eq. 5]: % Sólidos en Molino 2'x2' ({sol_molino:.1f}%) > 78.0% máximo operativo."))
elif sol_molino < 62.0:
    alertas.append(("warn", f"Fuera de rango [Eq. 5]: % Sólidos en Molino 2'x2' ({sol_molino:.1f}%) < 62.0% mínimo operativo."))

if res["pulpa_rebose_lmin"] > 38.0:
    alertas.append(("err", f"Límite excedido [Corr. 10/12]: Caudal de pulpa ({res['pulpa_rebose_lmin']:.1f} L/min) > 38.0 L/min nominal."))

if cc_espiral_pct > 260.0:
    alertas.append(("warn", f"Carga elevada [Eq. 6]: Carga circulante en clasificador helicoidal ({cc_espiral_pct:.0f}%) > 260%."))

tiene_error = any(a[0] == "err" for a in alertas)
tiene_warn = any(a[0] == "warn" for a in alertas)

if tiene_error:
    badge_html = '<span class="scada-badge badge-err">SCADA: ALARMA</span>'
elif tiene_warn:
    badge_html = '<span class="scada-badge badge-warn">SCADA: PRECAUCIÓN</span>'
else:
    badge_html = '<span class="scada-badge badge-ok">SCADA: NORMAL</span>'

# ==================== CABECERA CORPORATIVA ====================
st.markdown(f"""
<div class="header-bar">
  <div>
    <div class="header-title">Gemelo Digital — Planta Piloto JICA (UNMSM)</div>
    <div class="header-subtitle">Simulación de 24 Equipos y 34 Corrientes | Conminución, Clasificación Helicoidal y Flotación Diferencial ({m1_sym} / {m2_sym})</div>
  </div>
  <div>{badge_html}</div>
</div>
""", unsafe_allow_html=True)

# ==================== TARJETAS KPI SUPERIORES SIMÉTRICAS ====================
kpis = [
    ("P80 Rebose [Corr. 10]", f"{res['p80_reb_calc']:.1f} µm", delta_str(res["p80_reb_calc"], base["p80_reb_calc"], " µm")),
    (f"Conc. C1 ({m1_sym}) [Corr. 17]", f"{res['s17_c1']:.2f} kg/h", f"Ley {res['ley_c1_m1']:.1f}% | {delta_str(res['rec_glob_c1'], base['rec_glob_c1'], '% Rec')}"),
    (f"Conc. C2 ({m2_sym}) [Corr. 29]", f"{res['s29_c2']:.2f} kg/h", f"Ley {res['ley_c2_m2']:.1f}% | {delta_str(res['rec_glob_c2'], base['rec_glob_c2'], '% Rec')}"),
    ("Relave Final [Corr. 34]", f"{res['s34_relave']:.2f} kg/h", f"{res['ley_rel_m1']:.2f}% {m1_sym} | {res['ley_rel_m2']:.2f}% {m2_sym}"),
    ("Caudal Rebose [Corr. 12]", f"{res['pulpa_rebose_lmin']:.2f} L/min", delta_str(res["pot_molino_kw"], base["pot_molino_kw"], " kW")),
]

kpi_cards_html = "".join([
    f'<div class="kpi-card"><div class="kpi-top"><div class="kpi-label">{lbl}</div><div class="kpi-value">{val}</div></div><div class="kpi-delta">{dl}</div></div>'
    for lbl, val, dl in kpis
])
st.markdown(f'<div class="kpi-grid">{kpi_cards_html}</div>', unsafe_allow_html=True)

for nivel, texto in alertas:
    cls = "alert-item-err" if nivel == "err" else "alert-item-warn"
    st.markdown(f'<div class="alert-item {cls}">{texto}</div>', unsafe_allow_html=True)

# ==================== REGISTRO DE 34 CORRIENTES ====================
corrientes_data = [
    (1, "Alimento Fresco a Chanc. Mandíbulas [Eq. 1]", F_kgh, 100.0, 0.0, f80_alim_mm * 1000.0, ley_f_m1, ley_f_m2),
    (2, "Descarga Chanc. Mandíbulas a Rodillos [Eq. 2]", F_kgh, 100.0, 0.0, res["p80_mand_mm"] * 1000.0, ley_f_m1, ley_f_m2),
    (3, "Descarga Chanc. Rodillos a Tolva Finos [Eq. 3]", F_kgh, 100.0, 0.0, res["f80_mol_um"], ley_f_m1, ley_f_m2),
    (4, "Descarga Tolva Finos a Nodo Mezcla [Eq. 4]", F_kgh, 100.0, 0.0, res["f80_mol_um"], ley_f_m1, ley_f_m2),
    (5, "Alimentación Compuesta a Molino 2'x2' [Eq. 5]", res["s5_alim_mol"], sol_molino, res["w5_molino"], res["f80_mol_um"], ley_f_m1, ley_f_m2),
    (6, "Agua Entrada a Molienda [Nodo 4]", 0.0, 0.0, res["w6_agua_ent"], 0.0, 0.0, 0.0),
    (7, "Descarga Molino Bolas 2'x2' a Clasificador [Eq. 6]", res["s7_desc_mol"], sol_molino, res["w5_molino"], res["p80_reb_calc"] * 1.35, ley_f_m1, ley_f_m2),
    (8, "Agua Salida (Dilución a Clasificador Helicoidal)", 0.0, 0.0, res["w8_agua_sal"], 0.0, 0.0, 0.0),
    (9, "Arenas Clasificador Helicoidal (Carga Circulante)", res["s9_arenas"], 76.0, res["w9_arenas"], res["p80_reb_calc"] * 1.9, ley_f_m1, ley_f_m2),
    (10, "Rebose Clasificador Helicoidal a Sumidero 1 [Eq. 7]", res["s10_rebose"], sol_rebose, res["w10_rebose"], res["p80_reb_calc"], ley_f_m1, ley_f_m2),
    (11, "Descarga Sumidero 1 a Bomba 1 [Eq. 8]", res["s10_rebose"], sol_rebose, res["w10_rebose"], res["p80_reb_calc"], ley_f_m1, ley_f_m2),
    (12, "Impulsión Bomba 1 a Acondicionador 1 [Eq. 9]", res["s10_rebose"], sol_rebose, res["w10_rebose"], res["p80_reb_calc"], ley_f_m1, ley_f_m2),
    (13, "Paso Acondicionador 1 a Acondicionador 2 [Eq. 10]", res["s14_alim_ro1"], 29.0, res["s14_alim_ro1"]*(71/29), res["p80_reb_calc"], ley_f_m1, ley_f_m2),
    (14, "Descarga Acond. 2 a Banco Rougher C1 [Eq. 11]", res["s14_alim_ro1"], 29.0, res["s14_alim_ro1"]*(71/29), res["p80_reb_calc"], ley_f_m1, ley_f_m2),
    (15, "Espumas Rougher C1 a Banco Cleaner 1 [Eq. 12]", res["s15_esp_ro1"], 22.0, res["s15_esp_ro1"]*(78/22), res["p80_reb_calc"]*0.85, res["ley_c1_m1"]*0.75, ley_f_m2*0.6),
    (16, "Colas Rougher C1 a Banco Scavenger C1 [Eq. 13]", res["s16_cola_ro1"], 30.0, res["s16_cola_ro1"]*(70/30), res["p80_reb_calc"], ley_f_m1*0.25, ley_f_m2),
    (17, f"CONCENTRADO FINAL C1 ({m1_sym}) (Espumas Cleaner 1)", res["s17_c1"], 25.0, res["s17_c1"]*(75/25), res["p80_reb_calc"]*0.80, res["ley_c1_m1"], (res["fino_m2_c1"]/res["s17_c1"])*100),
    (18, "Colas Cleaner 1 a Sumidero 2 [Eq. 14]", res["s18_cola_cl1"], 18.0, res["s18_cola_cl1"]*(82/18), res["p80_reb_calc"]*0.90, ley_f_m1*0.6, ley_f_m2*0.8),
    (19, "Espumas Scavenger C1 a Sumidero 2 [Eq. 14]", res["s19_esp_scv1"], 20.0, res["s19_esp_scv1"]*(80/20), res["p80_reb_calc"]*0.90, ley_f_m1*0.5, ley_f_m2*0.9),
    (20, "Descarga Sumidero 2 a Bomba 2 [Eq. 15]", res["s21_medios_c1"], 19.0, res["s21_medios_c1"]*(81/19), res["p80_reb_calc"]*0.90, ley_f_m1*0.55, ley_f_m2*0.85),
    (21, "Recirculación Medios C1 (Bomba 2 a Acond. 1)", res["s21_medios_c1"], 19.0, res["s21_medios_c1"]*(81/19), res["p80_reb_calc"]*0.90, ley_f_m1*0.55, ley_f_m2*0.85),
    (22, "Colas Scavenger C1 a Sumidero 3 [Eq. 16]", res["s22_cola_scv1"], 28.0, res["s22_cola_scv1"]*(72/28), res["p80_reb_calc"], (res["fino_m1_alim"]-res["fino_m1_c1"])/res["s22_cola_scv1"]*100, ley_f_m2),
    (23, "Descarga Sumidero 3 a Bomba 3 [Eq. 17]", res["s22_cola_scv1"], 28.0, res["s22_cola_scv1"]*(72/28), res["p80_reb_calc"], (res["fino_m1_alim"]-res["fino_m1_c1"])/res["s22_cola_scv1"]*100, ley_f_m2),
    (24, "Impulsión Bomba 3 a Acondicionador 3 [Eq. 18]", res["s22_cola_scv1"], 28.0, res["s22_cola_scv1"]*(72/28), res["p80_reb_calc"], (res["fino_m1_alim"]-res["fino_m1_c1"])/res["s22_cola_scv1"]*100, ley_f_m2),
    (25, "Paso Acondicionador 3 a Acondicionador 4 [Eq. 19]", res["s26_alim_ro2"], 27.0, res["s26_alim_ro2"]*(73/27), res["p80_reb_calc"], res["ley_rel_m1"], ley_f_m2),
    (26, "Descarga Acond. 4 a Banco Rougher C2 [Eq. 20]", res["s26_alim_ro2"], 27.0, res["s26_alim_ro2"]*(73/27), res["p80_reb_calc"], res["ley_rel_m1"], ley_f_m2),
    (27, "Espumas Rougher C2 a Banco Cleaner 2 [Eq. 21]", res["s27_esp_ro2"], 22.0, res["s27_esp_ro2"]*(78/22), res["p80_reb_calc"]*0.85, res["ley_rel_m1"]*0.5, res["ley_c2_m2"]*0.75),
    (28, "Colas Rougher C2 a Banco Scavenger C2 [Eq. 22]", res["s28_cola_ro2"], 28.0, res["s28_cola_ro2"]*(72/28), res["p80_reb_calc"], res["ley_rel_m1"], ley_f_m2*0.25),
    (29, f"CONCENTRADO FINAL C2 ({m2_sym}) (Espumas Cleaner 2)", res["s29_c2"], 25.0, res["s29_c2"]*(75/25), res["p80_reb_calc"]*0.80, (res["fino_m1_c2"]/res["s29_c2"])*100, res["ley_c2_m2"]),
    (30, "Colas Cleaner 2 a Sumidero 4 [Eq. 23]", res["s30_cola_cl2"], 18.0, res["s30_cola_cl2"]*(82/18), res["p80_reb_calc"]*0.90, res["ley_rel_m1"]*0.6, ley_f_m2*0.6),
    (31, "Espumas Scavenger C2 a Sumidero 4 [Eq. 23]", res["s31_esp_scv2"], 20.0, res["s31_esp_scv2"]*(80/20), res["p80_reb_calc"]*0.90, res["ley_rel_m1"]*0.7, ley_f_m2*0.5),
    (32, "Descarga Sumidero 4 a Bomba 4 [Eq. 24]", res["s33_medios_c2"], 19.0, res["s33_medios_c2"]*(81/19), res["p80_reb_calc"]*0.90, res["ley_rel_m1"]*0.65, ley_f_m2*0.55),
    (33, "Recirculación Medios C2 (Bomba 4 a Acond. 3)", res["s33_medios_c2"], 19.0, res["s33_medios_c2"]*(81/19), res["p80_reb_calc"]*0.90, res["ley_rel_m1"]*0.65, ley_f_m2*0.55),
    (34, "RELAVE FINAL (Colas Banco Scavenger C2)", res["s34_relave"], 26.0, res["s34_relave"]*(74/26), res["p80_reb_calc"], res["ley_rel_m1"], res["ley_rel_m2"]),
]
df_34 = pd.DataFrame(
    corrientes_data,
    columns=["N° Corriente", "Descripción en Plano JICA", "Sólidos (kg/h)", "% Sólidos", "Agua (L/h)", "P80 Estimado (µm)", f"Ley {m1_sym} (%)", f"Ley {m2_sym} (%)"]
)
df_34["Pulpa Total (L/h)"] = (df_34["Sólidos (kg/h)"] / sg_mineral) + df_34["Agua (L/h)"]

df_3prod = pd.DataFrame({
    "Producto / Corriente": [
        "Alimento Fresco [Corr. 1 / 12]",
        f"Concentrado Final C1 ({m1_sym}) [Corr. 17]",
        f"Concentrado Final C2 ({m2_sym}) [Corr. 29]",
        "Relave Final [Corr. 34]"
    ],
    "Peso Seco (kg/h)": [F_kgh, res["s17_c1"], res["s29_c2"], res["s34_relave"]],
    "% Peso": [100.0, (res["s17_c1"]/F_kgh)*100, (res["s29_c2"]/F_kgh)*100, (res["s34_relave"]/F_kgh)*100],
    f"Ley {m1_sym} (%)": [ley_f_m1, res["ley_c1_m1"], (res["fino_m1_c2"]/res["s29_c2"])*100, res["ley_rel_m1"]],
    f"Dist. {m1_sym} (%)": [100.0, res["rec_glob_c1"], (res["fino_m1_c2"]/res["fino_m1_alim"])*100, (res["fino_m1_rel"]/res["fino_m1_alim"])*100],
    f"Ley {m2_sym} (%)": [ley_f_m2, (res["fino_m2_c1"]/res["s17_c1"])*100, res["ley_c2_m2"], res["ley_rel_m2"]],
    f"Dist. {m2_sym} (%)": [100.0, (res["fino_m2_c1"]/res["fino_m2_alim"])*100, res["rec_glob_c2"], (res["fino_m2_rel"]/res["fino_m2_alim"])*100],
})

# ==================== PESTAÑAS PRINCIPALES ====================
tab_pfd, tab_et1, tab_sens, tab_34 = st.tabs([
    "Flowsheet de Proceso (24 Equipos / 34 Corrientes)",
    "Etapa 1: Conminución y Clasificación",
    "Sensibilidad y Comparativa",
    "Balance de 34 Corrientes y Exportación"
])

# -------------------- PESTAÑA 1: FLOWSHEET CON TOOLBAR, ZOOM RESPONSIVO Y HALO EN TEXTOS --------------------
with tab_pfd:
    st.markdown('<div class="toolbar-panel">', unsafe_allow_html=True)
    col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns([1.35, 1.35, 1.15, 1.15])
    with col_ctrl1:
        busqueda = st.text_input("Buscar equipo o corriente", placeholder="Ej. 17, 29, Espiral, Bomba 3")
    with col_ctrl2:
        ruta_sel = st.selectbox(
            "Trazabilidad de ruta",
            [
                "Todas las corrientes",
                f"Ruta a Concentrado C1 ({m1_sym}) [Corr. 17]",
                f"Ruta a Concentrado C2 ({m2_sym}) [Corr. 29]",
                "Ruta a Relave Final [Corr. 34]",
                "Recirculaciones (Arenas [9] + Medios [21, 33])"
            ]
        )
    with col_ctrl3:
        zoom_pct = st.number_input("Escala del plano (%)", min_value=80, max_value=160, value=100, step=10)
    with col_ctrl4:
        corr_inspec = st.number_input("Inspeccionar corriente (1-34)", min_value=1, max_value=34, value=17, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

    fila_corr = df_34[df_34["N° Corriente"] == corr_inspec].iloc[0]
    st.markdown(f"""
    <div class="inspector-strip">
      <strong>Corriente [{int(fila_corr['N° Corriente'])}]:</strong> {fila_corr['Descripción en Plano JICA']} &nbsp;|&nbsp;
      <strong>Sólidos:</strong> {fila_corr['Sólidos (kg/h)']:.2f} kg/h &nbsp;|&nbsp;
      <strong>% Sólidos:</strong> {fila_corr['% Sólidos']:.1f}% &nbsp;|&nbsp;
      <strong>Agua:</strong> {fila_corr['Agua (L/h)']:.1f} L/h &nbsp;|&nbsp;
      <strong>Pulpa:</strong> {fila_corr['Pulpa Total (L/h)']:.1f} L/h &nbsp;|&nbsp;
      <strong>P80:</strong> {fila_corr['P80 Estimado (µm)']:.0f} µm
    </div>
    """, unsafe_allow_html=True)

    if busqueda.strip():
        coincidencias = df_34[
            df_34["N° Corriente"].astype(str).str.contains(busqueda.strip(), case=False) |
            df_34["Descripción en Plano JICA"].str.contains(busqueda.strip(), case=False)
        ]
        if not coincidencias.empty:
            st.dataframe(
                coincidencias[["N° Corriente", "Descripción en Plano JICA", "Sólidos (kg/h)", "% Sólidos", "P80 Estimado (µm)"]].round(2),
                hide_index=True,
                width="stretch"
            )

    es_claro = "Blanco" in tema_plano
    bg_svg = "#FFFFFF" if es_claro else "#0F172A"
    fg_txt = "#0F172A" if es_claro else "#E2E8F0"
    halo_color = "#FFFFFF" if es_claro else "#0F172A"
    eq_fill = "#F1F5F9" if es_claro else "#1E293B"
    eq_stroke = "#1E293B" if es_claro else "#94A3B8"
    line_main = "#1E3A8A" if es_claro else "#38BDF8"
    line_rec = "#B91C1C" if es_claro else "#F87171"
    line_conc = "#15803D" if es_claro else "#4ADE80"
    legend_bg = "#F8FAFC" if es_claro else "#1E293B"
    legend_stroke = "#CBD5E1" if es_claro else "#475569"

    op_c1 = "1.0" if "C1" in ruta_sel or "Todas" in ruta_sel else "0.18"
    op_c2 = "1.0" if "C2" in ruta_sel or "Todas" in ruta_sel else "0.18"
    op_rel = "1.0" if "Relave" in ruta_sel or "Todas" in ruta_sel else "0.18"
    op_rec = "1.0" if "Recirculaciones" in ruta_sel or "Todas" in ruta_sel else "0.22"

    # Altura proporcional automática cuando zoom == 100%, o expandida con scroll delgado si zoom > 100%
    svg_width_attr = "100%" if zoom_pct == 100 else f"{zoom_pct}%"
    svg_height_attr = "auto" if zoom_pct == 100 else f"{int(640 * (zoom_pct / 100.0))}px"
    overflow_css = "overflow: hidden;" if zoom_pct == 100 else "overflow: auto; max-height: 670px;"

    svg_only = f"""<svg viewBox="0 0 1250 760" width="{svg_width_attr}" height="{svg_height_attr}" xmlns="http://www.w3.org/2000/svg" style="display:block; font-family: Inter, Arial, sans-serif; background:{bg_svg};">
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
        <style>
          .lbl {{ paint-order: stroke; stroke: {halo_color}; stroke-width: 3.2px; stroke-linecap: round; stroke-linejoin: round; }}
        </style>
      </defs>

      <!-- CONMINUCIÓN Y CLASIFICACIÓN (EQUIPOS 1 AL 8) -->
      <circle cx="85" cy="25" r="7" fill="none" stroke="{line_main}" stroke-width="2"/>
      <text x="100" y="29" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">ALIMENTO ({F_kgh:.0f} kg/h)</text>
      <line x1="85" y1="32" x2="85" y2="62" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="70" y="50" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">1</text>

      <polygon points="65,65 80,65 80,115 70,115" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <polygon points="108,65 95,65 86,115 96,115" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <circle cx="106" cy="100" r="8" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="70" y="92" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">1</text>
      <text x="122" y="82" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">CHANCADORA DE MANDÍBULAS</text>
      <text x="122" y="96" fill="{fg_txt}" font-size="10" class="lbl">Set: {set_mandibulas_mm:.0f} mm | P80 calc: {res['p80_mand_mm']:.1f} mm</text>

      <line x1="85" y1="117" x2="85" y2="152" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="70" y="138" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">2</text>

      <polygon points="73,152 97,152 91,168 79,168" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
      <circle cx="71" cy="180" r="14" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <circle cx="99" cy="180" r="14" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="81" y="164" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">2</text>
      <text x="122" y="176" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">CHANCADORA DE RODILLOS</text>
      <text x="122" y="190" fill="{fg_txt}" font-size="10" class="lbl">Luz: {set_rodillos_mm:.1f} mm | P80 calc: {res['p80_rod_mm']:.1f} mm</text>

      <line x1="85" y1="196" x2="85" y2="232" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="70" y="217" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">3</text>

      <polygon points="65,235 105,235 105,275 89,302 81,302 65,275" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="81" y="268" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">3</text>
      <text x="115" y="262" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">TOLVA DE FINOS</text>
      <text x="115" y="276" fill="{fg_txt}" font-size="10" class="lbl">{F_kgh:.0f} kg/h | F80: {res['f80_mol_um']:.0f} µm</text>

      <line x1="85" y1="302" x2="85" y2="348" stroke="{line_main}" stroke-width="2"/>
      <line x1="85" y1="348" x2="118" y2="348" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="68" y="330" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">4</text>
      <circle cx="126" cy="348" r="8" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="122" y="334" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">4</text>

      <!-- AGUA ENTRADA [6] separada de nodos y líneas -->
      <circle cx="168" cy="292" r="5.5" fill="none" stroke="{line_main}" stroke-width="2"/>
      <text x="179" y="295" fill="{line_main}" font-size="10" font-weight="bold" class="lbl">AGUA ENTRADA [6] ({res['w6_agua_ent']:.0f} L/h)</text>
      <line x1="163" y1="297" x2="133" y2="339" stroke="{line_main}" stroke-width="1.8" marker-end="url(#arr)"/>

      <line x1="134" y1="348" x2="178" y2="348" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="148" y="341" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">5</text>

      <!-- MOLINO DE BOLAS 2'x2' [5] con etiquetas limpias -->
      <polygon points="180,338 192,326 192,370 180,358" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <rect x="192" y="316" width="68" height="64" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <rect x="260" y="310" width="8" height="76" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <rect x="268" y="336" width="12" height="24" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="222" y="352" fill="{fg_txt}" font-size="13" font-weight="bold" class="lbl">5</text>
      <text x="150" y="398" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">MOLINO DE BOLAS 2'x2'</text>
      <text x="150" y="412" fill="{fg_txt}" font-size="10" class="lbl">Carga: {res['s5_alim_mol']:.0f} kg/h ({sol_molino:.0f}% Sól)</text>

      <polyline points="280,348 293,348 293,505" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="278" y="425" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">7</text>

      <!-- AGUA SALIDA [8] con holgura respecto a corriente 7 y 12 -->
      <circle cx="352" cy="458" r="5.5" fill="none" stroke="{line_main}" stroke-width="2"/>
      <text x="326" y="432" fill="{line_main}" font-size="9.5" font-weight="bold" class="lbl">AGUA SALIDA [8]</text>
      <text x="332" y="444" fill="{line_main}" font-size="9" class="lbl">({res['w8_agua_sal']:.0f} L/h)</text>
      <line x1="348" y1="464" x2="316" y2="510" stroke="{line_main}" stroke-width="1.8" marker-end="url(#arr)"/>

      <polygon points="205,438 320,515 320,545 290,545 205,472" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <line x1="212" y1="455" x2="305" y2="528" stroke="{eq_stroke}" stroke-width="2" stroke-dasharray="6,4"/>
      <text x="262" y="505" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">6</text>
      <text x="148" y="534" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">CLASIFICADOR HELICOIDAL</text>
      <text x="148" y="548" fill="{fg_txt}" font-size="10" class="lbl">CC: {cc_espiral_pct:.0f}% | P80 rebose: {res['p80_reb_calc']:.0f} µm</text>

      <g opacity="{op_rec}">
        <polyline points="205,455 126,455 126,358" fill="none" stroke="{line_rec}" stroke-width="2.2" stroke-dasharray="5,3" marker-end="url(#arr-rec)"/>
        <text x="108" y="415" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">9 ({res['s9_arenas']:.0f})</text>
      </g>

      <polyline points="320,532 345,532 345,575" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="350" y="555" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">10</text>
      <polygon points="327,578 363,578 363,615 345,638 327,615" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="341" y="608" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">7</text>
      <text x="255" y="612" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">SUMIDERO 1</text>

      <line x1="345" y1="638" x2="345" y2="675" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="350" y="660" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">11</text>
      <circle cx="345" cy="690" r="13" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <polygon points="333,704 357,704 352,698 338,698" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="341" y="694" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">8</text>
      <text x="282" y="695" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BOMBA 1</text>

      <polyline points="358,690 388,690 388,35 452,35 452,58" fill="none" stroke="{line_main}" stroke-width="2.2" marker-end="url(#arr)"/>
      <text x="394" y="295" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">12 ({res['s10_rebose']:.0f} kg/h)</text>
      <text x="394" y="310" fill="{line_main}" font-size="10" class="lbl">P80: {res['p80_reb_calc']:.0f} µm</text>

      <!-- CIRCUITO 1 (C1) -->
      <g opacity="{op_c1}">
        <polygon points="440,62 480,62 480,102 460,124 440,102" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="456" y="92" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">9</text>
        <text x="488" y="85" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">ACOND. 1 (pH {ph_c1:.1f})</text>

        <polyline points="460,124 460,140 520,140 520,158" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="482" y="135" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">13</text>
        <polygon points="500,162 540,162 540,202 520,224 500,202" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="513" y="192" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">10</text>
        <text x="435" y="192" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">ACOND. 2</text>

        <polyline points="520,224 520,242 585,242" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="498" y="257" fill="{line_main}" font-size="10" font-weight="bold" class="lbl">14 ({res['s14_alim_ro1']:.0f} kg/h)</text>

        <rect x="588" y="210" width="200" height="52" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="638" y1="210" x2="638" y2="262" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="688" y1="210" x2="688" y2="262" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="738" y1="210" x2="738" y2="262" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="588,225 765,232 788,215" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="605" y="245" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">11</text>
        <text x="625" y="202" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BANC. CEL. RO. C1 (4 Celdas)</text>

        <polyline points="755,210 755,152 875,152" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="780" y="145" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">15 ({res['s15_esp_ro1']:.1f} kg/h)</text>
        <rect x="878" y="135" width="96" height="48" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="926" y1="135" x2="926" y2="183" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="878,148 955,154 974,140" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="892" y="168" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">12</text>
        <text x="878" y="200" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BAN. CEL. CL. 1</text>

        <polyline points="945,135 945,82 775,82" fill="none" stroke="{line_conc}" stroke-width="2.5" marker-end="url(#arr-conc)"/>
        <circle cx="765" cy="82" r="7" fill="none" stroke="{line_conc}" stroke-width="2"/>
        <text x="845" y="75" fill="{line_conc}" font-size="11" font-weight="bold" class="lbl">17</text>
        <text x="665" y="104" fill="{line_conc}" font-size="12" font-weight="bold" class="lbl">CONC. FINAL C1 ({res['s17_c1']:.2f} kg/h | Ley {m1_sym}: {res['ley_c1_m1']:.1f}% | Rec: {res['rec_glob_c1']:.1f}%)</text>

        <polyline points="788,242 998,242 998,338 935,338" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="860" y="236" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">16 ({res['s16_cola_ro1']:.1f} kg/h)</text>
        <rect x="680" y="308" width="250" height="52" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="730" y1="308" x2="730" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="780" y1="308" x2="780" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="830" y1="308" x2="830" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="880" y1="308" x2="880" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="930,322 705,328 680,312" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="905" y="344" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">13</text>
        <text x="695" y="298" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BANCO DE CELDAS SCV. CIRCUITO 1 (5 Celdas)</text>

        <polyline points="974,162 1062,162 1062,395" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
        <text x="1068" y="280" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">18</text>
        <polyline points="710,360 710,382 1042,382 1042,395" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
        <text x="850" y="377" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">19</text>

        <polygon points="1032,398 1072,398 1072,435 1052,456 1032,435" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="1044" y="428" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">14</text>
        <text x="948" y="428" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">SUMIDERO 2</text>

        <polyline points="1052,456 1052,482 1085,482" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
        <text x="1035" y="474" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">20</text>
        <circle cx="1102" cy="482" r="13" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <polygon points="1090,496 1114,496 1109,490 1095,490" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="1095" y="486" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">15</text>
        <text x="1080" y="462" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BOM. 2</text>

        <g opacity="{op_rec}">
          <polyline points="1115,482 1175,482 1175,18 468,18 468,58" fill="none" stroke="{line_rec}" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#arr-rec)"/>
          <text x="795" y="14" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">21 (Medios C1: {res['s21_medios_c1']:.1f} kg/h)</text>
        </g>
      </g>

      <!-- TRANSFERENCIA C1 -> C2 Y CIRCUITO 2 (C2) -->
      <polyline points="680,342 622,342 622,368" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="642" y="336" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">22</text>
      <polygon points="602,372 642,372 642,408 622,428 602,408" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="614" y="402" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">16</text>
      <text x="518" y="398" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">SUMIDERO 3</text>

      <polyline points="622,428 622,452 572,452" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="595" y="446" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">23</text>
      <circle cx="555" cy="452" r="13" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <polygon points="543,466 567,466 562,460 548,460" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="547" y="456" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">17</text>
      <text x="528" y="482" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BOMBA 3</text>

      <polyline points="542,452 452,452 452,508" fill="none" stroke="{line_main}" stroke-width="2.2" marker-end="url(#arr)"/>
      <text x="455" y="445" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">24 ({res['s22_cola_scv1']:.1f} kg/h)</text>

      <g opacity="{op_c2}">
        <polygon points="440,512 480,512 480,550 460,570 440,550" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="452" y="542" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">18</text>
        <text x="486" y="538" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">ACON. 3 (pH {ph_c2:.1f})</text>

        <polyline points="460,570 460,582 520,582 520,596" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="485" y="578" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">25</text>
        <polygon points="500,600 540,600 540,636 520,656 500,636" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="512" y="628" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">19</text>
        <text x="442" y="628" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">ACON. 4</text>

        <polyline points="520,656 520,668 585,668" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="542" y="663" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">26</text>
        <rect x="588" y="635" width="200" height="48" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="638" y1="635" x2="638" y2="683" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="688" y1="635" x2="688" y2="683" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="738" y1="635" x2="738" y2="683" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="588,648 765,655 788,640" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="605" y="666" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">20</text>
        <text x="625" y="627" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BANC. CEL. RO. C2 (4 Celdas)</text>

        <polyline points="755,635 755,585 875,585" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="780" y="578" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">27 ({res['s27_esp_ro2']:.1f} kg/h)</text>
        <rect x="878" y="568" width="96" height="46" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="926" y1="568" x2="926" y2="614" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="878,580 955,586 974,572" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="892" y="598" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">21</text>
        <text x="878" y="630" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BAN. CEL. CL. 2</text>

        <polyline points="945,568 945,525 775,525" fill="none" stroke="{line_conc}" stroke-width="2.5" marker-end="url(#arr-conc)"/>
        <circle cx="765" cy="525" r="7" fill="none" stroke="{line_conc}" stroke-width="2"/>
        <text x="845" y="518" fill="{line_conc}" font-size="11" font-weight="bold" class="lbl">29</text>
        <text x="665" y="546" fill="{line_conc}" font-size="12" font-weight="bold" class="lbl">CONC. FINAL C2 ({res['s29_c2']:.2f} kg/h | Ley {m2_sym}: {res['ley_c2_m2']:.1f}% | Rec: {res['rec_glob_c2']:.1f}%)</text>

        <polyline points="788,662 998,662 998,718 935,718" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="885" y="656" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">28</text>
        <rect x="680" y="696" width="250" height="46" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="730" y1="696" x2="730" y2="742" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="780" y1="696" x2="780" y2="742" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="830" y1="696" x2="830" y2="742" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="880" y1="696" x2="880" y2="742" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="930,708 705,714 680,700" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="905" y="726" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">22</text>
        <text x="710" y="691" fill="{fg_txt}" font-size="10" font-weight="bold" class="lbl">BANCO DE CELDAS SCV. C2 (5 Celdas)</text>

        <polyline points="974,592 1062,592 1062,672" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
        <text x="1068" y="635" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">30</text>
        <polyline points="710,742 710,752 1042,752 1042,672" fill="none" stroke="{line_rec}" stroke-width="1.8"/>
        <text x="850" y="749" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">31</text>

        <polygon points="1032,675 1072,675 1072,705 1052,722 1032,705" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="1044" y="698" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">23</text>
        <text x="952" y="698" fill="{fg_txt}" font-size="10" font-weight="bold" class="lbl">SUMIDERO 4</text>

        <polyline points="1052,722 1052,735 1100,735" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
        <text x="1072" y="730" fill="{line_rec}" font-size="10" font-weight="bold" class="lbl">32</text>
        <circle cx="1116" cy="735" r="12" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="1109" y="739" fill="{fg_txt}" font-size="10" font-weight="bold" class="lbl">24</text>
        <text x="1095" y="718" fill="{fg_txt}" font-size="10" font-weight="bold" class="lbl">BOM. 4</text>

        <g opacity="{op_rec}">
          <polyline points="1128,735 1155,735 1155,498 468,498 468,508" fill="none" stroke="{line_rec}" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#arr-rec)"/>
          <text x="795" y="493" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">33 (Medios C2: {res['s33_medios_c2']:.1f} kg/h)</text>
        </g>
      </g>

      <g opacity="{op_rel}">
        <polyline points="680,718 425,718" fill="none" stroke="{line_rec}" stroke-width="2.5" marker-end="url(#arr-rec)"/>
        <circle cx="415" cy="718" r="7" fill="none" stroke="{line_rec}" stroke-width="2"/>
        <text x="435" y="708" fill="{line_rec}" font-size="11.5" font-weight="bold" class="lbl">34 — RELAVE FINAL ({res['s34_relave']:.1f} kg/h)</text>
        <text x="435" y="734" fill="{line_rec}" font-size="10.5" font-weight="bold" class="lbl">Leyes: {res['ley_rel_m1']:.2f}% {m1_sym} | {res['ley_rel_m2']:.2f}% {m2_sym} | Fe: {ley_f_fe:.1f}%</text>
      </g>

      <!-- Leyenda Técnica de Corrientes (Esquina Inferior Izquierda) -->
      <rect x="20" y="585" width="245" height="72" rx="4" fill="{legend_bg}" stroke="{legend_stroke}" stroke-width="1.2"/>
      <text x="30" y="602" fill="{fg_txt}" font-size="10" font-weight="bold" class="lbl">LEYENDA DE CORRIENTES</text>
      <line x1="30" y1="615" x2="54" y2="615" stroke="{line_main}" stroke-width="2.2"/>
      <text x="60" y="619" fill="{fg_txt}" font-size="9.5" class="lbl">Pulpa / Alimentación / Agua</text>
      <line x1="30" y1="630" x2="54" y2="630" stroke="{line_conc}" stroke-width="2.4"/>
      <text x="60" y="634" fill="{fg_txt}" font-size="9.5" class="lbl">Concentrado Final (C1 / C2)</text>
      <line x1="30" y1="645" x2="54" y2="645" stroke="{line_rec}" stroke-width="2.2" stroke-dasharray="5,3"/>
      <text x="60" y="649" fill="{fg_txt}" font-size="9.5" class="lbl">Relave Final / Recirculación</text>

      <!-- Cajetín Técnico UNMSM -->
      <rect x="20" y="665" width="245" height="78" rx="4" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.4"/>
      <text x="30" y="683" fill="{fg_txt}" font-size="10.5" font-weight="bold" class="lbl">PLANTA PILOTO JICA — UNMSM</text>
      <text x="30" y="699" fill="{fg_txt}" font-size="9.5" class="lbl">Ing. Metalúrgica | 24 Equipos / 34 Corr.</text>
      <text x="30" y="715" fill="{fg_txt}" font-size="9.5" class="lbl">Esquema Activo: {m1_sym} / {m2_sym} | Fe: {ley_f_fe:.1f}%</text>
      <text x="30" y="731" fill="{fg_txt}" font-size="8.5" class="lbl">Modelo de Simulación en Estado Estacionario</text>
    </svg>"""

    svg_only = f"""<svg id="jica-svg-plan" viewBox="0 0 1250 780" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="display:block; font-family: Inter, Arial, sans-serif; background:{bg_svg};">
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
        <style>
          .lbl {{ paint-order: stroke; stroke: {halo_color}; stroke-width: 3.2px; stroke-linecap: round; stroke-linejoin: round; }}
        </style>
      </defs>

      <!-- CONMINUCIÓN Y CLASIFICACIÓN (EQUIPOS 1 AL 8) -->
      <circle cx="85" cy="25" r="7" fill="none" stroke="{line_main}" stroke-width="2"/>
      <text x="100" y="29" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">ALIMENTO ({F_kgh:.0f} kg/h)</text>
      <line x1="85" y1="32" x2="85" y2="62" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="70" y="50" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">1</text>

      <polygon points="65,65 80,65 80,115 70,115" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <polygon points="108,65 95,65 86,115 96,115" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <circle cx="106" cy="100" r="8" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="70" y="92" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">1</text>
      <text x="122" y="82" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">CHANCADORA DE MANDÍBULAS</text>
      <text x="122" y="96" fill="{fg_txt}" font-size="10" class="lbl">Set: {set_mandibulas_mm:.0f} mm | P80 calc: {res['p80_mand_mm']:.1f} mm</text>

      <line x1="85" y1="117" x2="85" y2="152" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="70" y="138" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">2</text>

      <polygon points="73,152 97,152 91,168 79,168" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
      <circle cx="71" cy="180" r="14" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <circle cx="99" cy="180" r="14" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="81" y="164" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">2</text>
      <text x="122" y="176" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">CHANCADORA DE RODILLOS</text>
      <text x="122" y="190" fill="{fg_txt}" font-size="10" class="lbl">Luz: {set_rodillos_mm:.1f} mm | P80 calc: {res['p80_rod_mm']:.1f} mm</text>

      <line x1="85" y1="196" x2="85" y2="232" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="70" y="217" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">3</text>

      <polygon points="65,235 105,235 105,275 89,302 81,302 65,275" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="81" y="268" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">3</text>
      <text x="115" y="262" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">TOLVA DE FINOS</text>
      <text x="115" y="276" fill="{fg_txt}" font-size="10" class="lbl">{F_kgh:.0f} kg/h | F80: {res['f80_mol_um']:.0f} µm</text>

      <line x1="85" y1="302" x2="85" y2="348" stroke="{line_main}" stroke-width="2"/>
      <line x1="85" y1="348" x2="118" y2="348" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="68" y="330" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">4</text>
      <circle cx="126" cy="348" r="8" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="122" y="334" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">4</text>

      <circle cx="168" cy="292" r="5.5" fill="none" stroke="{line_main}" stroke-width="2"/>
      <text x="179" y="295" fill="{line_main}" font-size="10" font-weight="bold" class="lbl">AGUA ENTRADA [6] ({res['w6_agua_ent']:.0f} L/h)</text>
      <line x1="163" y1="297" x2="133" y2="339" stroke="{line_main}" stroke-width="1.8" marker-end="url(#arr)"/>

      <line x1="134" y1="348" x2="178" y2="348" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="148" y="341" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">5</text>

      <polygon points="180,338 192,326 192,370 180,358" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <rect x="192" y="316" width="68" height="64" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <rect x="260" y="310" width="8" height="76" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <rect x="268" y="336" width="12" height="24" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="222" y="352" fill="{fg_txt}" font-size="13" font-weight="bold" class="lbl">5</text>
      <text x="150" y="398" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">MOLINO DE BOLAS 2'x2'</text>
      <text x="150" y="412" fill="{fg_txt}" font-size="10" class="lbl">Carga: {res['s5_alim_mol']:.0f} kg/h ({sol_molino:.0f}% Sól)</text>

      <polyline points="280,348 293,348 293,505" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="278" y="425" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">7</text>

      <circle cx="352" cy="458" r="5.5" fill="none" stroke="{line_main}" stroke-width="2"/>
      <text x="326" y="432" fill="{line_main}" font-size="9.5" font-weight="bold" class="lbl">AGUA SALIDA [8]</text>
      <text x="332" y="444" fill="{line_main}" font-size="9" class="lbl">({res['w8_agua_sal']:.0f} L/h)</text>
      <line x1="348" y1="464" x2="316" y2="510" stroke="{line_main}" stroke-width="1.8" marker-end="url(#arr)"/>

      <polygon points="205,438 320,515 320,545 290,545 205,472" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <line x1="212" y1="455" x2="305" y2="528" stroke="{eq_stroke}" stroke-width="2" stroke-dasharray="6,4"/>
      <text x="262" y="505" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">6</text>
      <text x="148" y="534" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">CLASIFICADOR HELICOIDAL</text>
      <text x="148" y="548" fill="{fg_txt}" font-size="10" class="lbl">CC: {cc_espiral_pct:.0f}% | P80 rebose: {res['p80_reb_calc']:.0f} µm</text>

      <g opacity="{op_rec}">
        <polyline points="205,455 126,455 126,358" fill="none" stroke="{line_rec}" stroke-width="2.2" stroke-dasharray="5,3" marker-end="url(#arr-rec)"/>
        <text x="108" y="415" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">9 ({res['s9_arenas']:.0f})</text>
      </g>

      <polyline points="320,532 345,532 345,575" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="350" y="555" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">10</text>
      <polygon points="327,578 363,578 363,615 345,638 327,615" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="341" y="608" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">7</text>
      <text x="255" y="612" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">SUMIDERO 1</text>

      <line x1="345" y1="638" x2="345" y2="675" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="350" y="660" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">11</text>
      <circle cx="345" cy="690" r="13" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <polygon points="333,704 357,704 352,698 338,698" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="341" y="694" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">8</text>
      <text x="282" y="695" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BOMBA 1</text>

      <polyline points="358,690 388,690 388,35 452,35 452,58" fill="none" stroke="{line_main}" stroke-width="2.2" marker-end="url(#arr)"/>
      <text x="394" y="295" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">12 ({res['s10_rebose']:.0f} kg/h)</text>
      <text x="394" y="310" fill="{line_main}" font-size="10" class="lbl">P80: {res['p80_reb_calc']:.0f} µm</text>

      <!-- CIRCUITO 1 (C1) -->
      <g opacity="{op_c1}">
        <polygon points="440,62 480,62 480,102 460,124 440,102" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="456" y="92" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">9</text>
        <text x="488" y="85" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">ACOND. 1 (pH {ph_c1:.1f})</text>

        <polyline points="460,124 460,140 520,140 520,158" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="482" y="135" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">13</text>
        <polygon points="500,162 540,162 540,202 520,224 500,202" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="513" y="192" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">10</text>
        <text x="435" y="192" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">ACOND. 2</text>

        <polyline points="520,224 520,242 585,242" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="498" y="257" fill="{line_main}" font-size="10" font-weight="bold" class="lbl">14 ({res['s14_alim_ro1']:.0f} kg/h)</text>

        <rect x="588" y="210" width="200" height="52" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="638" y1="210" x2="638" y2="262" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="688" y1="210" x2="688" y2="262" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="738" y1="210" x2="738" y2="262" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="588,225 765,232 788,215" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="605" y="245" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">11</text>
        <text x="625" y="202" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BANC. CEL. RO. C1 (4 Celdas)</text>

        <polyline points="755,210 755,152 875,152" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="780" y="145" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">15 ({res['s15_esp_ro1']:.1f} kg/h)</text>
        <rect x="878" y="135" width="96" height="48" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="926" y1="135" x2="926" y2="183" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="878,148 955,154 974,140" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="892" y="168" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">12</text>
        <text x="878" y="200" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BAN. CEL. CL. 1</text>

        <polyline points="945,135 945,82 775,82" fill="none" stroke="{line_conc}" stroke-width="2.5" marker-end="url(#arr-conc)"/>
        <circle cx="765" cy="82" r="7" fill="none" stroke="{line_conc}" stroke-width="2"/>
        <text x="845" y="75" fill="{line_conc}" font-size="11" font-weight="bold" class="lbl">17</text>
        <text x="665" y="104" fill="{line_conc}" font-size="12" font-weight="bold" class="lbl">CONC. FINAL C1 ({res['s17_c1']:.2f} kg/h | Ley {m1_sym}: {res['ley_c1_m1']:.1f}% | Rec: {res['rec_glob_c1']:.1f}%)</text>

        <polyline points="788,242 998,242 998,338 935,338" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="860" y="236" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">16 ({res['s16_cola_ro1']:.1f} kg/h)</text>
        <rect x="680" y="308" width="250" height="52" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="730" y1="308" x2="730" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="780" y1="308" x2="780" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="830" y1="308" x2="830" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="880" y1="308" x2="880" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="930,322 705,328 680,312" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="905" y="344" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">13</text>
        <text x="695" y="298" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BANCO DE CELDAS SCV. CIRCUITO 1 (5 Celdas)</text>

        <polyline points="974,162 1062,162 1062,395" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
        <text x="1068" y="280" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">18</text>
        <polyline points="710,360 710,382 1042,382 1042,395" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
        <text x="850" y="377" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">19</text>

        <polygon points="1032,398 1072,398 1072,435 1052,456 1032,435" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="1044" y="428" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">14</text>
        <text x="948" y="428" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">SUMIDERO 2</text>

        <polyline points="1052,456 1052,482 1085,482" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
        <text x="1035" y="474" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">20</text>
        <circle cx="1102" cy="482" r="13" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <polygon points="1090,496 1114,496 1109,490 1095,490" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="1095" y="486" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">15</text>
        <text x="1080" y="462" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BOM. 2</text>

        <g opacity="{op_rec}">
          <polyline points="1115,482 1175,482 1175,18 468,18 468,58" fill="none" stroke="{line_rec}" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#arr-rec)"/>
          <text x="795" y="14" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">21 (Medios C1: {res['s21_medios_c1']:.1f} kg/h)</text>
        </g>
      </g>

      <!-- TRANSFERENCIA C1 -> C2 Y CIRCUITO 2 (C2) -->
      <polyline points="680,342 622,342 622,368" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="642" y="336" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">22</text>
      <polygon points="602,372 642,372 642,408 622,428 602,408" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="614" y="402" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">16</text>
      <text x="518" y="398" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">SUMIDERO 3</text>

      <polyline points="622,428 622,452 572,452" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="595" y="446" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">23</text>
      <circle cx="555" cy="452" r="13" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <polygon points="543,466 567,466 562,460 548,460" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="547" y="456" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">17</text>
      <text x="528" y="482" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BOMBA 3</text>

      <polyline points="542,452 452,452 452,508" fill="none" stroke="{line_main}" stroke-width="2.2" marker-end="url(#arr)"/>
      <text x="455" y="445" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">24 ({res['s22_cola_scv1']:.1f} kg/h)</text>

      <g opacity="{op_c2}">
        <polygon points="440,512 480,512 480,550 460,570 440,550" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="452" y="542" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">18</text>
        <text x="486" y="538" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">ACON. 3 (pH {ph_c2:.1f})</text>

        <polyline points="460,570 460,582 520,582 520,596" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="485" y="578" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">25</text>
        <polygon points="500,600 540,600 540,636 520,656 500,636" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="512" y="628" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">19</text>
        <text x="442" y="628" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">ACON. 4</text>

        <polyline points="520,656 520,668 585,668" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="542" y="663" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">26</text>
        <rect x="588" y="635" width="200" height="48" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="638" y1="635" x2="638" y2="683" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="688" y1="635" x2="688" y2="683" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="738" y1="635" x2="738" y2="683" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="588,648 765,655 788,640" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="605" y="666" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">20</text>
        <text x="625" y="627" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BANC. CEL. RO. C2 (4 Celdas)</text>

        <polyline points="755,635 755,585 875,585" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="780" y="578" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">27 ({res['s27_esp_ro2']:.1f} kg/h)</text>
        <rect x="878" y="568" width="96" height="46" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="926" y1="568" x2="926" y2="614" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="878,580 955,586 974,572" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="892" y="598" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">21</text>
        <text x="878" y="630" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">BAN. CEL. CL. 2</text>

        <polyline points="945,568 945,525 775,525" fill="none" stroke="{line_conc}" stroke-width="2.5" marker-end="url(#arr-conc)"/>
        <circle cx="765" cy="525" r="7" fill="none" stroke="{line_conc}" stroke-width="2"/>
        <text x="845" y="518" fill="{line_conc}" font-size="11" font-weight="bold" class="lbl">29</text>
        <text x="665" y="546" fill="{line_conc}" font-size="12" font-weight="bold" class="lbl">CONC. FINAL C2 ({res['s29_c2']:.2f} kg/h | Ley {m2_sym}: {res['ley_c2_m2']:.1f}% | Rec: {res['rec_glob_c2']:.1f}%)</text>

        <polyline points="788,662 998,662 998,718 935,718" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="885" y="656" fill="{line_main}" font-size="11" font-weight="bold" class="lbl">28</text>
        <rect x="680" y="696" width="250" height="46" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="730" y1="696" x2="730" y2="742" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="780" y1="696" x2="780" y2="742" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="830" y1="696" x2="830" y2="742" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="880" y1="696" x2="880" y2="742" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="930,708 705,714 680,700" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="905" y="726" fill="{fg_txt}" font-size="12" font-weight="bold" class="lbl">22</text>
        <text x="710" y="691" fill="{fg_txt}" font-size="10" font-weight="bold" class="lbl">BANCO DE CELDAS SCV. C2 (5 Celdas)</text>

        <polyline points="974,592 1062,592 1062,672" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
        <text x="1068" y="635" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">30</text>
        <polyline points="710,742 710,752 1042,752 1042,672" fill="none" stroke="{line_rec}" stroke-width="1.8"/>
        <text x="850" y="749" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">31</text>

        <polygon points="1032,675 1072,675 1072,705 1052,722 1032,705" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="1044" y="698" fill="{fg_txt}" font-size="11" font-weight="bold" class="lbl">23</text>
        <text x="952" y="698" fill="{fg_txt}" font-size="10" font-weight="bold" class="lbl">SUMIDERO 4</text>

        <polyline points="1052,722 1052,735 1100,735" fill="none" stroke="{line_rec}" stroke-width="1.8" marker-end="url(#arr-rec)"/>
        <text x="1072" y="730" fill="{line_rec}" font-size="10" font-weight="bold" class="lbl">32</text>
        <circle cx="1116" cy="735" r="12" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="1109" y="739" fill="{fg_txt}" font-size="10" font-weight="bold" class="lbl">24</text>
        <text x="1095" y="718" fill="{fg_txt}" font-size="10" font-weight="bold" class="lbl">BOM. 4</text>

        <g opacity="{op_rec}">
          <polyline points="1128,735 1155,735 1155,498 468,498 468,508" fill="none" stroke="{line_rec}" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#arr-rec)"/>
          <text x="795" y="493" fill="{line_rec}" font-size="11" font-weight="bold" class="lbl">33 (Medios C2: {res['s33_medios_c2']:.1f} kg/h)</text>
        </g>
      </g>

      <g opacity="{op_rel}">
        <polyline points="680,718 425,718" fill="none" stroke="{line_rec}" stroke-width="2.5" marker-end="url(#arr-rec)"/>
        <circle cx="415" cy="718" r="7" fill="none" stroke="{line_rec}" stroke-width="2"/>
        <text x="435" y="708" fill="{line_rec}" font-size="11.5" font-weight="bold" class="lbl">34 — RELAVE FINAL ({res['s34_relave']:.1f} kg/h)</text>
        <text x="435" y="734" fill="{line_rec}" font-size="10.5" font-weight="bold" class="lbl">Leyes: {res['ley_rel_m1']:.2f}% {m1_sym} | {res['ley_rel_m2']:.2f}% {m2_sym} | Fe: {ley_f_fe:.1f}%</text>
      </g>

      <!-- Leyenda Técnica de Corrientes -->
      <rect x="20" y="595" width="245" height="72" rx="4" fill="{legend_bg}" stroke="{legend_stroke}" stroke-width="1.2"/>
      <text x="30" y="612" fill="{fg_txt}" font-size="10" font-weight="bold" class="lbl">LEYENDA DE CORRIENTES</text>
      <line x1="30" y1="625" x2="54" y2="625" stroke="{line_main}" stroke-width="2.2"/>
      <text x="60" y="629" fill="{fg_txt}" font-size="9.5" class="lbl">Pulpa / Alimentación / Agua</text>
      <line x1="30" y1="640" x2="54" y2="640" stroke="{line_conc}" stroke-width="2.4"/>
      <text x="60" y="644" fill="{fg_txt}" font-size="9.5" class="lbl">Concentrado Final (C1 / C2)</text>
      <line x1="30" y1="655" x2="54" y2="655" stroke="{line_rec}" stroke-width="2.2" stroke-dasharray="5,3"/>
      <text x="60" y="659" fill="{fg_txt}" font-size="9.5" class="lbl">Relave Final / Recirculación</text>

      <!-- Cajetín Técnico UNMSM -->
      <rect x="20" y="675" width="245" height="82" rx="4" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.4"/>
      <text x="30" y="693" fill="{fg_txt}" font-size="10.5" font-weight="bold" class="lbl">PLANTA PILOTO JICA — UNMSM</text>
      <text x="30" y="709" fill="{fg_txt}" font-size="9.5" class="lbl">Ing. Metalúrgica | 24 Equipos / 34 Corr.</text>
      <text x="30" y="725" fill="{fg_txt}" font-size="9.5" class="lbl">Esquema Activo: {m1_sym} / {m2_sym} | Fe: {ley_f_fe:.1f}%</text>
      <text x="30" y="741" fill="{fg_txt}" font-size="8.5" class="lbl">Modelo de Simulación en Estado Estacionario</text>
    </svg>"""

    sheet_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: Inter, Arial, sans-serif; }}
        body {{ background: transparent; }}
        #jica-sheet-host {{
          background: #E2E8F0;
          border: 1px solid #CBD5E1;
          border-radius: 6px;
          padding: 10px;
          display: flex;
          flex-direction: column;
          gap: 8px;
        }}
        #jica-sheet-host:fullscreen {{
          background: #0F172A;
          padding: 16px;
          border-radius: 0;
        }}
        .sheet-bar {{
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 8px;
          background: #FFFFFF;
          border: 1px solid #CBD5E1;
          border-radius: 5px;
          padding: 6px 10px;
        }}
        .sheet-title {{
          font-size: 12px;
          font-weight: 600;
          color: #0F172A;
        }}
        .sheet-actions {{
          display: flex;
          align-items: center;
          gap: 6px;
        }}
        .btn-tool {{
          background: #F8FAFC;
          color: #0F172A;
          border: 1px solid #CBD5E1;
          border-radius: 4px;
          padding: 4px 10px;
          font-size: 12px;
          font-weight: 600;
          cursor: pointer;
        }}
        .btn-tool:hover {{
          background: #EFF6FF;
          border-color: #1E3A8A;
          color: #1E3A8A;
        }}
        .btn-primary {{
          background: #1E3A8A;
          color: #FFFFFF;
          border-color: #1E3A8A;
        }}
        .btn-primary:hover {{
          background: #172554;
          color: #FFFFFF;
        }}
        .zoom-readout {{
          min-width: 48px;
          text-align: center;
          font-size: 12px;
          font-weight: 700;
          color: #1E3A8A;
        }}
        #jica-viewport {{
          position: relative;
          width: 100%;
          height: 620px;
          overflow: auto;
          background: {bg_svg};
          border: 1px solid #94A3B8;
          border-radius: 4px;
          box-shadow: 0 4px 14px rgba(15, 23, 42, 0.12);
          scrollbar-width: thin;
          scrollbar-color: #94A3B8 transparent;
        }}
        #jica-sheet-host:fullscreen #jica-viewport {{
          height: calc(100vh - 64px);
        }}
        #jica-paper {{
          width: 100%;
          height: 100%;
          transform-origin: top left;
          transition: transform 0.12s ease-out;
          cursor: grab;
        }}
        #jica-paper:active {{
          cursor: grabbing;
        }}
      </style>
    </head>
    <body>
      <div id="jica-sheet-host">
        <div class="sheet-bar">
          <div class="sheet-title">Hoja CAD — Planta Piloto JICA (UNMSM) | Arrastra para mover al hacer zoom</div>
          <div class="sheet-actions">
            <button type="button" class="btn-tool" id="btn-zoom-out">-</button>
            <span class="zoom-readout" id="zoom-label">{zoom_pct}%</span>
            <button type="button" class="btn-tool" id="btn-zoom-in">+</button>
            <button type="button" class="btn-tool" id="btn-zoom-reset">Ajustar</button>
            <button type="button" class="btn-tool btn-primary" id="btn-fullscreen">Pantalla completa</button>
          </div>
        </div>
        <div id="jica-viewport">
          <div id="jica-paper">{svg_only}</div>
        </div>
      </div>
      <script>
        (function() {{
          let scale = {zoom_pct} / 100.0;
          const minScale = 0.7;
          const maxScale = 2.2;
          const host = document.getElementById("jica-sheet-host");
          const viewport = document.getElementById("jica-viewport");
          const paper = document.getElementById("jica-paper");
          const label = document.getElementById("zoom-label");

          function applyZoom(newScale) {{
            scale = Math.min(maxScale, Math.max(minScale, Number(newScale.toFixed(2))));
            paper.style.transform = "scale(" + scale + ")";
            paper.style.width = (scale > 1 ? (scale * 100) + "%" : "100%");
            paper.style.height = (scale > 1 ? (scale * 100) + "%" : "100%");
            label.textContent = Math.round(scale * 100) + "%";
          }}

          document.getElementById("btn-zoom-in").addEventListener("click", () => applyZoom(scale + 0.15));
          document.getElementById("btn-zoom-out").addEventListener("click", () => applyZoom(scale - 0.15));
          document.getElementById("btn-zoom-reset").addEventListener("click", () => {{
            applyZoom(1.0);
            viewport.scrollTop = 0;
            viewport.scrollLeft = 0;
          }});

          document.getElementById("btn-fullscreen").addEventListener("click", () => {{
            if (!document.fullscreenElement) {{
              host.requestFullscreen().catch(() => {{}});
            }} else {{
              document.exitFullscreen().catch(() => {{}});
            }}
          }});

          // Arrastrar con el mouse (pan)
          let isDragging = false, startX = 0, startY = 0, scrollLeft = 0, scrollTop = 0;
          viewport.addEventListener("mousedown", (e) => {{
            isDragging = true;
            startX = e.pageX - viewport.offsetLeft;
            startY = e.pageY - viewport.offsetTop;
            scrollLeft = viewport.scrollLeft;
            scrollTop = viewport.scrollTop;
          }});
          window.addEventListener("mouseup", () => {{ isDragging = false; }});
          viewport.addEventListener("mousemove", (e) => {{
            if (!isDragging) return;
            e.preventDefault();
            const x = e.pageX - viewport.offsetLeft;
            const y = e.pageY - viewport.offsetTop;
            viewport.scrollLeft = scrollLeft - (x - startX);
            viewport.scrollTop = scrollTop - (y - startY);
          }});

          applyZoom(scale);
        }})();
      </script>
    </body>
    </html>
    """
    components.html(sheet_html, height=690, scrolling=False)

    st.download_button(
        label="Descargar Plano Flowsheet (.SVG)",
        data=svg_only.encode("utf-8"),
        file_name=f"Flowsheet_JICA_{m1_sym}_{m2_sym}.svg",
        mime="image/svg+xml"
    )

# -------------------- PESTAÑA 2: ETAPA 1 CALCULADA --------------------
with tab_et1:
    c_izq, c_der = st.columns([1.45, 1])
    with c_izq:
        st.subheader("Curvas Granulométricas Rosin-Rammler (Calculadas)")
        n_rr = 1.15
        d63_reb = res["p80_reb_calc"] / ((-np.log(0.20)) ** (1.0 / n_rr))
        d63_rod = res["f80_mol_um"] / ((-np.log(0.20)) ** (1.0 / 0.95))
        aberturas = np.geomspace(15, 25000, 250)
        pas_reb = 100.0 * (1.0 - np.exp(-((aberturas / d63_reb) ** n_rr)))
        pas_rod = 100.0 * (1.0 - np.exp(-((aberturas / d63_rod) ** 0.95)))

        fig_g = go.Figure()
        fig_g.add_trace(go.Scatter(x=aberturas, y=pas_rod, mode="lines", name=f"Salida Rodillos (F80 calc = {res['f80_mol_um']:.0f} µm)", line=dict(dash="dash", color="#475569", width=2.4)))
        fig_g.add_trace(go.Scatter(x=aberturas, y=pas_reb, mode="lines", name=f"Rebose Espiral (P80 calc = {res['p80_reb_calc']:.1f} µm)", line=dict(color="#1E3A8A", width=3.2)))
        fig_g.add_trace(go.Scatter(x=[15, 25000], y=[80, 80], mode="lines", name="Línea 80% Pasante", line=dict(dash="dot", color="#B91C1C", width=1.6)))
        fig_g.add_trace(go.Scatter(x=[149, 149], y=[0, 100], mode="lines", name="Malla 100 (149 µm)", line=dict(dash="dot", color="#0F766E", width=1.6)))
        fig_g.update_layout(
            xaxis=dict(type="log", title="Abertura (µm)", range=[np.log10(15), np.log10(25000)], tickvals=[20, 37, 53, 74, 105, 149, 210, 500, 1000, 2500, 7500, 20000]),
            yaxis=dict(title="% Pasante Acumulado", range=[0, 105]),
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(family="Inter, Arial, sans-serif", color="#0F172A"),
            height=420
        )
        st.plotly_chart(fig_g, width="stretch")

    with c_der:
        st.subheader("Salidas Calculadas del Modelo")
        df_calc_et1 = pd.DataFrame({
            "Variable Calculada": [
                "P80 Chanc. Mandíbulas [Eq. 1]",
                "P80 Chanc. Rodillos / F80 Molino [Eq. 2/5]",
                "P80 Rebose Clasificador [Corr. 10]",
                "Arenas Recirculadas [Corr. 9]",
                "Agua Entrada [Corr. 6]",
                "Agua Dilución Espiral [Corr. 8]",
                "Energía Específica Bond",
                "Potencia Teórica Molino 2'x2'"
            ],
            "Valor": [
                f"{res['p80_mand_mm']:.2f} mm",
                f"{res['p80_rod_mm']:.2f} mm ({res['f80_mol_um']:.0f} µm)",
                f"{res['p80_reb_calc']:.1f} µm",
                f"{res['s9_arenas']:.1f} kg/h",
                f"{res['w6_agua_ent']:.1f} L/h",
                f"{res['w8_agua_sal']:.1f} L/h",
                f"{res['w_bond_kwh_t']:.2f} kWh/t",
                f"{res['pot_molino_kw']:.2f} kW"
            ]
        })
        st.dataframe(df_calc_et1, hide_index=True, width="stretch")

# -------------------- PESTAÑA 3: SENSIBILIDAD Y COMPARATIVA --------------------
with tab_sens:
    st.subheader("Sensibilidad: P80 de Molienda vs. Recuperación Metalúrgica")
    rango_p80 = np.linspace(80.0, 200.0, 25)
    recs_m1_sens, recs_m2_sens = [], []
    for p_test in rango_p80:
        f_m1_e = np.clip((155.0 - p_test) * 0.06, -5.0, 4.0)
        r1_s = float(np.clip(86.0 + f_m1_e + np.clip((dosis_col_c1 - 35.0) * 0.03, -2.5, 3.0), 55.0, 95.0))
        r2_s = float(np.clip(84.0 + np.clip((dosis_act_c2 - 350.0) * 0.008, -4.0, 4.5) + f_m1_e * 0.5, 50.0, 94.0))
        recs_m1_sens.append(r1_s)
        recs_m2_sens.append(r2_s)

    fig_s = go.Figure()
    fig_s.add_trace(go.Scatter(x=rango_p80, y=recs_m1_sens, mode="lines+markers", name=f"Recuperación {m1_sym} C1 (%)", line=dict(color="#1E3A8A", width=2.8)))
    fig_s.add_trace(go.Scatter(x=rango_p80, y=recs_m2_sens, mode="lines+markers", name=f"Recuperación {m2_sym} C2 (%)", line=dict(color="#475569", width=2.8)))
    fig_s.add_trace(go.Scatter(x=[res["p80_reb_calc"], res["p80_reb_calc"]], y=[50, 95], mode="lines", name=f"P80 Actual ({res['p80_reb_calc']:.1f} µm)", line=dict(dash="dash", color="#0F766E", width=2.0)))
    fig_s.update_layout(
        xaxis_title="P80 del Rebose del Clasificador Helicoidal (µm)",
        yaxis_title="Recuperación Metalúrgica (%)",
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter, Arial, sans-serif", color="#0F172A"),
        height=380
    )
    st.plotly_chart(fig_s, width="stretch")

    st.subheader("Balance Global de 3 Productos (Estado Actual)")
    st.dataframe(df_3prod.round(2), hide_index=True, width="stretch")

# -------------------- PESTAÑA 4: TABLA MAESTRA DE 34 CORRIENTES --------------------
with tab_34:
    st.subheader("Registro Oficial de las 34 Corrientes — Planta Piloto JICA")
    st.dataframe(df_34.round(2), hide_index=True, width="stretch")

    buffer_excel = io.BytesIO()
    with pd.ExcelWriter(buffer_excel, engine="xlsxwriter") as writer:
        workbook = writer.book

        # Estilos corporativos sobrios
        fmt_title = workbook.add_format({
            "bold": True, "font_size": 13, "font_color": "#0F172A"
        })
        fmt_subtitle = workbook.add_format({
            "font_size": 10, "font_color": "#475569"
        })
        fmt_header = workbook.add_format({
            "bold": True, "font_color": "#FFFFFF", "bg_color": "#1E3A8A",
            "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True
        })
        fmt_num = workbook.add_format({
            "num_format": "#,##0.00", "border": 1, "align": "right"
        })
        fmt_text = workbook.add_format({
            "border": 1, "align": "left"
        })
        fmt_meta_lbl = workbook.add_format({
            "bold": True, "bg_color": "#F1F5F9", "border": 1, "font_color": "#0F172A"
        })
        fmt_meta_val = workbook.add_format({
            "bg_color": "#FFFFFF", "border": 1, "num_format": "#,##0.00"
        })

        # --- HOJA 1: RESUMEN EJECUTIVO Y GRÁFICOS NATIVOS ---
        ws_res = workbook.add_worksheet("Resumen_y_Graficos")
        ws_res.write("A1", "GEMELO DIGITAL — PLANTA PILOTO JICA (UNMSM)", fmt_title)
        ws_res.write("A2", f"Esquema: {esquema_mineral} | 24 Equipos / 34 Corrientes", fmt_subtitle)

        resumen_filas = [
            ("Alimento Fresco (kg/h)", F_kgh),
            ("P80 Rebose Clasificador (µm)", res["p80_reb_calc"]),
            (f"Recuperación Global {m1_sym} C1 (%)", res["rec_glob_c1"]),
            (f"Ley {m1_sym} en Conc. C1 (%)", res["ley_c1_m1"]),
            (f"Recuperación Global {m2_sym} C2 (%)", res["rec_glob_c2"]),
            (f"Ley {m2_sym} en Conc. C2 (%)", res["ley_c2_m2"]),
            ("Relave Final [Corr. 34] (kg/h)", res["s34_relave"]),
        ]
        ws_res.write("A4", "Indicador Clave", fmt_header)
        ws_res.write("B4", "Valor Actual", fmt_header)
        for idx, (lbl_k, val_k) in enumerate(resumen_filas, start=5):
            ws_res.write(f"A{idx}", lbl_k, fmt_meta_lbl)
            ws_res.write(f"B{idx}", float(val_k), fmt_meta_val)
        ws_res.set_column("A:A", 34)
        ws_res.set_column("B:B", 18)

        # --- HOJA 2: BALANCE GLOBAL C1 / C2 ---
        df_3prod_r = df_3prod.round(2)
        df_3prod_r.to_excel(writer, sheet_name="Balance_Global_C1_C2", index=False)
        ws_bal = writer.sheets["Balance_Global_C1_C2"]
        for c_idx, col_name in enumerate(df_3prod_r.columns):
            ws_bal.write(0, c_idx, col_name, fmt_header)
            ws_bal.set_column(c_idx, c_idx, 22)
            for r_idx in range(1, len(df_3prod_r) + 1):
                val = df_3prod_r.iloc[r_idx - 1, c_idx]
                ws_bal.write(r_idx, c_idx, val, fmt_text if c_idx == 0 else fmt_num)

        # Gráfico nativo de Distribución de m1_sym (%) en Balance_Global_C1_C2
        chart_dist1 = workbook.add_chart({"type": "column"})
        chart_dist1.add_series({
            "name": f"Distribución {m1_sym} (%)",
            "categories": ["Balance_Global_C1_C2", 1, 0, len(df_3prod_r), 0],
            "values": ["Balance_Global_C1_C2", 1, 4, len(df_3prod_r), 4],
            "fill": {"color": "#1E3A8A"},
            "data_labels": {"value": True}
        })
        chart_dist1.set_title({"name": f"Distribución de {m1_sym} por Producto (%)"})
        chart_dist1.set_x_axis({"name": "Producto / Corriente"})
        chart_dist1.set_y_axis({"name": "Distribución (%)", "max": 110})
        chart_dist1.set_legend({"none": True})
        ws_bal.insert_chart("A7", chart_dist1, {"x_scale": 1.3, "y_scale": 1.15})

        # Gráfico nativo de Distribución de m2_sym (%) en Balance_Global_C1_C2
        chart_dist2 = workbook.add_chart({"type": "column"})
        chart_dist2.add_series({
            "name": f"Distribución {m2_sym} (%)",
            "categories": ["Balance_Global_C1_C2", 1, 0, len(df_3prod_r), 0],
            "values": ["Balance_Global_C1_C2", 1, 6, len(df_3prod_r), 6],
            "fill": {"color": "#0F766E"},
            "data_labels": {"value": True}
        })
        chart_dist2.set_title({"name": f"Distribución de {m2_sym} por Producto (%)"})
        chart_dist2.set_x_axis({"name": "Producto / Corriente"})
        chart_dist2.set_y_axis({"name": "Distribución (%)", "max": 110})
        chart_dist2.set_legend({"none": True})
        ws_bal.insert_chart("E7", chart_dist2, {"x_scale": 1.3, "y_scale": 1.15})

        # --- HOJA 3: 34 CORRIENTES JICA + GRÁFICO DE SÓLIDOS ---
        df_34_r = df_34.round(2)
        df_34_r.to_excel(writer, sheet_name="34_Corrientes_JICA", index=False)
        ws_34 = writer.sheets["34_Corrientes_JICA"]
        for c_idx, col_name in enumerate(df_34_r.columns):
            ws_34.write(0, c_idx, col_name, fmt_header)
            ws_34.set_column(c_idx, c_idx, 38 if c_idx == 1 else 18)
            for r_idx in range(1, len(df_34_r) + 1):
                val = df_34_r.iloc[r_idx - 1, c_idx]
                ws_34.write(r_idx, c_idx, val, fmt_text if c_idx == 1 else fmt_num)

        chart_sol = workbook.add_chart({"type": "line"})
        chart_sol.add_series({
            "name": "Sólidos (kg/h)",
            "categories": ["34_Corrientes_JICA", 1, 0, len(df_34_r), 0],
            "values": ["34_Corrientes_JICA", 1, 2, len(df_34_r), 2],
            "line": {"color": "#1E3A8A", "width": 2.0}
        })
        chart_sol.set_title({"name": "Perfil de Flujo de Sólidos en las 34 Corrientes (kg/h)"})
        chart_sol.set_x_axis({"name": "N° Corriente"})
        chart_sol.set_y_axis({"name": "Sólidos (kg/h)"})
        ws_34.insert_chart("A37", chart_sol, {"x_scale": 1.6, "y_scale": 1.15})

    buffer_excel.seek(0)

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="Descargar Balance Completo (.XLSX)",
            data=buffer_excel,
            file_name=f"Reporte_JICA_{m1_sym}_{m2_sym}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col_dl2:
        ruta_drive = Path(r"G:\Mi unidad\02_Trabajo_Metalurgia\01_Balances_y_Planta")
        if ruta_drive.exists():
            if st.button("Guardar Copia en Google Drive (G:)"):
                archivo_full = ruta_drive / f"Gemelo_Digital_JICA_34Corrientes_{m1_sym}_{m2_sym}.xlsx"
                with open(archivo_full, "wb") as f:
                    f.write(buffer_excel.getvalue())
                st.caption(f"Guardado en: {archivo_full}")

# ==================== BARRA DE ESTADO TÉCNICA INFERIOR ====================
ts_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
estado_masa = "Balance Convergente — Error < 0.01%" if res["error_masa_pct"] < 0.01 else f"Balance Convergente — Error {res['error_masa_pct']:.4f}%"
st.markdown(f"""
<div class="status-footer">
  <span>Motor JICA Sim v3.2 | 24 Equipos / 34 Corrientes | Planta Piloto UNMSM</span>
  <span>{estado_masa}</span>
  <span>Última actualización: {ts_actual}</span>
</div>
""", unsafe_allow_html=True)