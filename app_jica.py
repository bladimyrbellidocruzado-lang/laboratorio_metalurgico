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

st.markdown("""
<style>
.block-container { padding-top: 1.0rem; padding-bottom: 1.0rem; }
div[data-testid="stMetricValue"] { font-size: 1.25rem; }
</style>
""", unsafe_allow_html=True)

st.title("⚒️ Gemelo Digital: Planta Piloto JICA — UNMSM (v3.0)")
st.caption("24 Equipos y 34 Corrientes | Trazabilidad de Rutas, Modelo Químico Pb-Zn-Fe, Alertas SCADA y Análisis de Sensibilidad")

# ==================== BARRA LATERAL: ENTRADAS OPERATIVAS Y QUÍMICAS ====================
st.sidebar.header("🎛️ Panel Operativo y Químico JICA")

tema_plano = st.sidebar.radio(
    "Estilo del Flowsheet",
    ["Modo Plano CAD (Blanco UNMSM)", "Modo SCADA (Oscuro)"],
    index=0
)

esquema_mineral = st.sidebar.selectbox(
    "Circuito Diferencial (C1 / C2)",
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

with st.sidebar.expander("1. Entradas Chancado y Molienda (Eq. 1-8)", expanded=True):
    F_kgh = st.slider("1. Alimento Fresco [Corr. 1] (kg/h)", 100.0, 800.0, 325.0, 25.0)
    f80_alim_mm = st.slider("F80 Alimento Fresco (mm)", 25.0, 127.0, 105.0, 5.0)
    set_mandibulas_mm = st.slider("Set Chanc. Mandíbulas [Eq. 1] (mm)", 12.0, 38.0, 26.0, 1.0)
    set_rodillos_mm = st.slider("Set Chanc. Rodillos [Eq. 2] (mm)", 3.0, 15.0, 6.5, 0.5)
    wi_bond = st.number_input("Work Index Bond Wi (kWh/t)", 8.0, 25.0, 13.8, 0.2)
    sol_molino = st.slider("% Sólidos Molino 2'x2' [Eq. 5]", 55.0, 84.0, 72.0, 1.0)
    cc_espiral_pct = st.slider("Carga Circulante Espiral [Eq. 6] (%)", 80.0, 320.0, 210.0, 10.0)
    sol_rebose = st.slider("% Sólidos Rebose [Corr. 10/12]", 20.0, 45.0, 30.0, 1.0)
    sg_mineral = st.number_input("Gravedad Específica Mineral (SG)", 2.5, 4.5, 2.95, 0.05)

with st.sidebar.expander(f"2. Leyes de Cabeza ({m1_sym}, {m2_sym}, Fe) y Reactivos", expanded=False):
    ley_f_m1 = st.number_input(f"Ley Cabeza {m1_sym} (%)", 0.2, 20.0, d_m1_f, 0.1)
    ley_f_m2 = st.number_input(f"Ley Cabeza {m2_sym} (%)", 0.5, 25.0, d_m2_f, 0.1)
    ley_f_fe = st.number_input("Ley Cabeza Fe / Pirita (%)", 1.0, 45.0, d_fe_f, 0.5)
    ph_c1 = st.slider("pH Acondicionamiento C1 [Eq. 9-10]", 6.5, 11.5, 8.5, 0.1)
    dosis_dep_c1 = st.number_input("Depresor ZnSO4 Acond. 1 (g/t)", 0.0, 800.0, 250.0, 25.0)
    dosis_col_c1 = st.number_input("Colector Z-11 Acond. 2 (g/t)", 5.0, 150.0, 35.0, 5.0)
    ph_c2 = st.slider("pH Acondicionamiento C2 [Eq. 18-19]", 8.0, 12.5, 10.8, 0.1)
    dosis_act_c2 = st.number_input("Activador CuSO4 Acond. 3 (g/t)", 50.0, 1000.0, 350.0, 25.0)
    dosis_col_c2 = st.number_input("Colector Z-6 Acond. 4 (g/t)", 5.0, 150.0, 45.0, 5.0)

with st.sidebar.expander("3. Selectividad de Bancos (Eq. 11-22)", expanded=False):
    rec_ro1 = st.slider("Rec. Rougher C1 [Eq. 11] (%)", 55.0, 95.0, 82.0, 1.0)
    rec_cl1 = st.slider("Rec. Cleaner 1 [Eq. 12] (%)", 60.0, 98.0, 88.0, 1.0)
    rec_scv1 = st.slider("Rec. Scavenger C1 [Eq. 13] (%)", 25.0, 85.0, 55.0, 1.0)
    rec_ro2 = st.slider("Rec. Rougher C2 [Eq. 20] (%)", 55.0, 95.0, 80.0, 1.0)
    rec_cl2 = st.slider("Rec. Cleaner 2 [Eq. 21] (%)", 60.0, 98.0, 86.0, 1.0)
    rec_scv2 = st.slider("Rec. Scavenger C2 [Eq. 22] (%)", 25.0, 85.0, 50.0, 1.0)

# ==================== MOTOR METALÚRGICO (RESULTADOS CALCULADOS) ====================
def simular_planta(
    F_val, f80_val, css_mand, gap_rod, wi_val, sol_mol, cc_pct, sol_reb, sg_val,
    f_m1, f_m2, f_fe, ph1, dep1, col1, ph2, act2, col2,
    r_ro1_p, r_cl1_p, r_scv1_p, r_ro2_p, r_cl2_p, r_scv2_p
):
    # Conminución y clasificación (valores calculados a partir de variables operativas)
    p80_mand_mm = css_mand * 1.22
    p80_rod_mm = gap_rod * 1.18
    f80_mol_um = p80_rod_mm * 1000.0

    # P80 de rebose calculado según carga circulante, Wi y eficiencia de clasificación
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

    # Efecto químico y granulométrico en recuperaciones y leyes
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

    # Circuito 2 (activación CuSO4 + pH alcalino)
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
        "pulpa_rebose_lmin": pulpa_rebose_lmin
    }

res = simular_planta(
    F_kgh, f80_alim_mm, set_mandibulas_mm, set_rodillos_mm, wi_bond,
    sol_molino, cc_espiral_pct, sol_rebose, sg_mineral,
    ley_f_m1, ley_f_m2, ley_f_fe, ph_c1, dosis_dep_c1, dosis_col_c1,
    ph_c2, dosis_act_c2, dosis_col_c2,
    rec_ro1, rec_cl1, rec_scv1, rec_ro2, rec_cl2, rec_scv2
)

# ==================== COMPARADOR CASO BASE vs. ACTUAL ====================
if "caso_base" not in st.session_state:
    st.session_state["caso_base"] = res.copy()

st.sidebar.markdown("---")
if st.sidebar.button("📌 Fijar Estado Actual como Caso Base"):
    st.session_state["caso_base"] = res.copy()
    st.sidebar.success("Caso Base actualizado.")

base = st.session_state["caso_base"]

def delta_str(actual, ref, sufijo=""):
    diff = actual - ref
    if abs(diff) < 1e-4:
        return f"Sin cambio ({actual:.2f}{sufijo})"
    signo = "+" if diff > 0 else ""
    return f"{signo}{diff:.2f}{sufijo} vs Base"

# ==================== KPIS CON COMPARATIVA VS CASO BASE ====================
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("P80 Rebose [Corr. 10]", f"{res['p80_reb_calc']:.1f} µm", delta_str(res["p80_reb_calc"], base["p80_reb_calc"], " µm"))
k2.metric(f"Conc. C1 ({m1_sym}) [17]", f"{res['s17_c1']:.2f} kg/h", delta_str(res["rec_glob_c1"], base["rec_glob_c1"], "% Rec"))
k3.metric(f"Conc. C2 ({m2_sym}) [29]", f"{res['s29_c2']:.2f} kg/h", delta_str(res["rec_glob_c2"], base["rec_glob_c2"], "% Rec"))
k4.metric("Relave Final [Corr. 34]", f"{res['s34_relave']:.2f} kg/h", delta_str(res["ley_rel_m1"], base["ley_rel_m1"], f"% {m1_sym}"))
k5.metric("Caudal Rebose [10/12]", f"{res['pulpa_rebose_lmin']:.2f} L/min", delta_str(res["pot_molino_kw"], base["pot_molino_kw"], " kW"))

# ==================== ALERTAS OPERATIVAS SCADA ====================
alertas = []
if sol_molino > 78.0:
    alertas.append(("error", f"🔴 ALERTA SCADA [Eq. 5]: % Sólidos en Molino 2'x2' ({sol_molino:.0f}%) supera el límite operativo de 78% (riesgo de atoramiento/sobrecarga)."))
elif sol_molino < 62.0:
    alertas.append(("warning", f"🟡 AVISO SCADA [Eq. 5]: % Sólidos en Molino 2'x2' ({sol_molino:.0f}%) es bajo (<62%); puede reducir eficiencia de molienda."))

if res["pulpa_rebose_lmin"] > 38.0:
    alertas.append(("error", f"🔴 ALERTA SCADA [Eq. 8 / 12]: Caudal de pulpa ({res['pulpa_rebose_lmin']:.1f} L/min) supera la capacidad nominal de bombeo/celdas piloto (~38 L/min)."))

if cc_espiral_pct > 260.0:
    alertas.append(("warning", f"🟡 AVISO SCADA [Eq. 6]: Carga circulante en Clasificador Helicoidal ({cc_espiral_pct:.0f}%) es elevada."))

if not alertas:
    st.success("🟢 **ESTADO SCADA NORMAL:** Todos los parámetros operativos (sólidos de molino, carga circulante y caudal de pulpa) están dentro de los rangos de la Planta Piloto JICA — UNMSM.")
else:
    for nivel, msg in alertas:
        if nivel == "error":
            st.error(msg)
        else:
            st.warning(msg)

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
    "🗺️ Flowsheet Interactivo (Trazabilidad, Zoom y Buscador)",
    "⚙️ Etapa 1: Conminución y Clasificador Helicoidal",
    "📊 Sensibilidad y Comparativa (Caso Base vs. Actual)",
    "📋 Tabla Maestra de las 34 Corrientes y Descargas"
])

# -------------------- PESTAÑA 1: FLOWSHEET CON ZOOM, BUSCADOR Y TRAZABILIDAD --------------------
with tab_pfd:
    col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns([1.3, 1.3, 1.2, 1.2])
    with col_ctrl1:
        busqueda = st.text_input("🔎 Buscador rápido (Eq. o Corr.)", placeholder="Ej: 17, 29, Espiral, Bomba 3...")
    with col_ctrl2:
        ruta_sel = st.selectbox(
            "🔦 Trazabilidad de Ruta (Resaltar trayectoria)",
            [
                "Todas las corrientes (Sin filtro)",
                f"Ruta a Concentrado Final C1 ({m1_sym}) [Corr. 17]",
                f"Ruta a Concentrado Final C2 ({m2_sym}) [Corr. 29]",
                "Ruta a Relave Final [Corr. 34]",
                "Lazos de Recirculación (Arenas [9] + Medios [21, 33])"
            ]
        )
    with col_ctrl3:
        zoom_pct = st.slider("🔍 Escala / Zoom del Lienzo (%)", 80, 160, 100, 10)
    with col_ctrl4:
        corr_inspec = st.number_input("📌 Inspeccionar Corriente N° (1-34)", 1, 34, 17, 1)

    # Tarjeta de inspección de corriente seleccionada
    fila_corr = df_34[df_34["N° Corriente"] == corr_inspec].iloc[0]
    st.info(
        f"**Corriente [{int(fila_corr['N° Corriente'])}]:** {fila_corr['Descripción en Plano JICA']}  |  "
        f"**Sólidos:** {fila_corr['Sólidos (kg/h)']:.2f} kg/h  |  "
        f"**% Sólidos:** {fila_corr['% Sólidos']:.1f}%  |  "
        f"**Agua:** {fila_corr['Agua (L/h)']:.1f} L/h  |  "
        f"**Pulpa:** {fila_corr['Pulpa Total (L/h)']:.1f} L/h  |  "
        f"**P80:** {fila_corr['P80 Estimado (µm)']:.0f} µm"
    )

    if busqueda.strip():
        coincidencias = df_34[
            df_34["N° Corriente"].astype(str).str.contains(busqueda.strip(), case=False) |
            df_34["Descripción en Plano JICA"].str.contains(busqueda.strip(), case=False)
        ]
        if not coincidencias.empty:
            st.caption("Coincidencias encontradas:")
            st.dataframe(coincidencias[["N° Corriente", "Descripción en Plano JICA", "Sólidos (kg/h)", "% Sólidos", "P80 Estimado (µm)"]].round(2), hide_index=True, width="stretch")

    # Definir opacidad de rutas según trazabilidad
    es_claro = "Blanco" in tema_plano
    bg_svg = "#ffffff" if es_claro else "#0b0f17"
    fg_txt = "#111827" if es_claro else "#e5e7eb"
    eq_fill = "#e5e7eb" if es_claro else "#1e293b"
    eq_stroke = "#111827" if es_claro else "#94a3b8"
    line_main = "#111827" if es_claro else "#38bdf8"
    line_rec = "#dc2626" if es_claro else "#f87171"
    line_conc = "#15803d" if es_claro else "#4ade80"

    op_c1 = "1.0" if "C1" in ruta_sel or "Todas" in ruta_sel else "0.18"
    op_c2 = "1.0" if "C2" in ruta_sel or "Todas" in ruta_sel else "0.18"
    op_rel = "1.0" if "Relave" in ruta_sel or "Todas" in ruta_sel else "0.18"
    op_rec = "1.0" if "Recirculación" in ruta_sel or "Todas" in ruta_sel else "0.25"

    svg_only = f"""<svg viewBox="0 0 1250 760" width="{zoom_pct}%" height="680" xmlns="http://www.w3.org/2000/svg" style="font-family: Arial, sans-serif; background:{bg_svg};">
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

      <!-- CONMINUCIÓN Y CLASIFICACIÓN (EQUIPOS 1 AL 8) -->
      <circle cx="85" cy="25" r="7" fill="none" stroke="{line_main}" stroke-width="2"/>
      <text x="100" y="29" fill="{fg_txt}" font-size="11" font-weight="bold">ALIMENTO ({F_kgh:.0f} kg/h)</text>
      <line x1="85" y1="32" x2="85" y2="62" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="72" y="50" fill="{line_main}" font-size="11" font-weight="bold">1</text>

      <polygon points="65,65 80,65 80,115 70,115" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <polygon points="108,65 95,65 86,115 96,115" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <circle cx="106" cy="100" r="8" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="70" y="92" fill="{fg_txt}" font-size="11" font-weight="bold">1</text>
      <text x="122" y="82" fill="{fg_txt}" font-size="11" font-weight="bold">CHANCADORA DE MANDÍBULAS</text>
      <text x="122" y="96" fill="{fg_txt}" font-size="10">Set: {set_mandibulas_mm:.0f} mm | P80 calc: {res['p80_mand_mm']:.1f} mm</text>

      <line x1="85" y1="117" x2="85" y2="152" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="72" y="138" fill="{line_main}" font-size="11" font-weight="bold">2</text>

      <polygon points="73,152 97,152 91,168 79,168" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
      <circle cx="71" cy="180" r="14" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <circle cx="99" cy="180" r="14" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="81" y="164" fill="{fg_txt}" font-size="11" font-weight="bold">2</text>
      <text x="122" y="176" fill="{fg_txt}" font-size="11" font-weight="bold">CHANCADORA DE RODILLOS</text>
      <text x="122" y="190" fill="{fg_txt}" font-size="10">Luz: {set_rodillos_mm:.1f} mm | P80 calc: {res['p80_rod_mm']:.1f} mm</text>

      <line x1="85" y1="196" x2="85" y2="232" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="72" y="217" fill="{line_main}" font-size="11" font-weight="bold">3</text>

      <polygon points="65,235 105,235 105,275 89,302 81,302 65,275" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="81" y="268" fill="{fg_txt}" font-size="12" font-weight="bold">3</text>
      <text x="115" y="262" fill="{fg_txt}" font-size="11" font-weight="bold">TOLVA DE FINOS</text>
      <text x="115" y="276" fill="{fg_txt}" font-size="10">{F_kgh:.0f} kg/h | F80: {res['f80_mol_um']:.0f} µm</text>

      <line x1="85" y1="302" x2="85" y2="348" stroke="{line_main}" stroke-width="2"/>
      <line x1="85" y1="348" x2="118" y2="348" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="72" y="330" fill="{line_main}" font-size="11" font-weight="bold">4</text>
      <circle cx="126" cy="348" r="8" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="123" y="334" fill="{fg_txt}" font-size="11" font-weight="bold">4</text>

      <circle cx="165" cy="298" r="6" fill="none" stroke="#0284c7" stroke-width="2"/>
      <text x="176" y="302" fill="#0284c7" font-size="10" font-weight="bold">AGUA ENTRADA [6] ({res['w6_agua_ent']:.0f} L/h)</text>
      <line x1="160" y1="304" x2="132" y2="340" stroke="#0284c7" stroke-width="1.8" marker-end="url(#arr)"/>

      <line x1="134" y1="348" x2="178" y2="348" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="152" y="342" fill="{line_main}" font-size="11" font-weight="bold">5</text>

      <polygon points="180,338 192,326 192,370 180,358" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <rect x="192" y="316" width="68" height="64" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <rect x="260" y="310" width="8" height="76" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <rect x="268" y="336" width="12" height="24" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="222" y="352" fill="{fg_txt}" font-size="13" font-weight="bold">5</text>
      <text x="155" y="400" fill="{fg_txt}" font-size="11" font-weight="bold">MOLINO DE BOLAS 2'x2'</text>
      <text x="155" y="414" fill="{fg_txt}" font-size="10">Carga: {res['s5_alim_mol']:.0f} kg/h ({sol_molino:.0f}% Sól)</text>

      <polyline points="280,348 293,348 293,505" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="280" y="425" fill="{line_main}" font-size="11" font-weight="bold">7</text>

      <circle cx="348" cy="462" r="5.5" fill="none" stroke="#0284c7" stroke-width="2"/>
      <text x="315" y="438" fill="#0284c7" font-size="9" font-weight="bold">AGUA SALIDA [8]</text>
      <text x="322" y="450" fill="#0284c7" font-size="9">({res['w8_agua_sal']:.0f} L/h)</text>
      <line x1="344" y1="468" x2="315" y2="510" stroke="#0284c7" stroke-width="1.8" marker-end="url(#arr)"/>

      <polygon points="205,438 320,515 320,545 290,545 205,472" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <line x1="212" y1="455" x2="305" y2="528" stroke="{eq_stroke}" stroke-width="2" stroke-dasharray="6,4"/>
      <text x="262" y="505" fill="{fg_txt}" font-size="12" font-weight="bold">6</text>
      <text x="155" y="535" fill="{fg_txt}" font-size="11" font-weight="bold">CLASIFICADOR HELICOIDAL</text>
      <text x="155" y="549" fill="{fg_txt}" font-size="10">CC: {cc_espiral_pct:.0f}% | P80 rebose: {res['p80_reb_calc']:.0f} µm</text>

      <g opacity="{op_rec}">
        <polyline points="205,455 126,455 126,358" fill="none" stroke="{line_rec}" stroke-width="2.2" stroke-dasharray="5,3" marker-end="url(#arr-rec)"/>
        <text x="112" y="415" fill="{line_rec}" font-size="11" font-weight="bold">9 ({res['s9_arenas']:.0f})</text>
      </g>

      <polyline points="320,532 345,532 345,575" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="350" y="555" fill="{line_main}" font-size="11" font-weight="bold">10</text>
      <polygon points="327,578 363,578 363,615 345,638 327,615" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <text x="341" y="608" fill="{fg_txt}" font-size="12" font-weight="bold">7</text>
      <text x="250" y="612" fill="{fg_txt}" font-size="11" font-weight="bold">SUMIDERO 1</text>

      <line x1="345" y1="638" x2="345" y2="675" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
      <text x="350" y="660" fill="{line_main}" font-size="11" font-weight="bold">11</text>
      <circle cx="345" cy="690" r="13" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
      <polygon points="333,704 357,704 352,698 338,698" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.8"/>
      <text x="341" y="694" fill="{fg_txt}" font-size="11" font-weight="bold">8</text>
      <text x="275" y="695" fill="{fg_txt}" font-size="11" font-weight="bold">BOMBA 1</text>

      <polyline points="358,690 388,690 388,35 452,35 452,58" fill="none" stroke="{line_main}" stroke-width="2.2" marker-end="url(#arr)"/>
      <text x="394" y="295" fill="{line_main}" font-size="11" font-weight="bold">12 ({res['s10_rebose']:.0f} kg/h)</text>
      <text x="394" y="310" fill="{line_main}" font-size="10">P80: {res['p80_reb_calc']:.0f} µm</text>

      <!-- CIRCUITO 1 (C1) -->
      <g opacity="{op_c1}">
        <polygon points="440,62 480,62 480,102 460,124 440,102" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="456" y="92" fill="{fg_txt}" font-size="12" font-weight="bold">9</text>
        <text x="488" y="85" fill="{fg_txt}" font-size="11" font-weight="bold">ACOND. 1 (pH {ph_c1:.1f})</text>

        <polyline points="460,124 460,140 520,140 520,158" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="482" y="135" fill="{line_main}" font-size="11" font-weight="bold">13</text>
        <polygon points="500,162 540,162 540,202 520,224 500,202" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="513" y="192" fill="{fg_txt}" font-size="12" font-weight="bold">10</text>
        <text x="435" y="192" fill="{fg_txt}" font-size="11" font-weight="bold">ACOND. 2</text>

        <polyline points="520,224 520,242 585,242" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="498" y="257" fill="{line_main}" font-size="10" font-weight="bold">14 ({res['s14_alim_ro1']:.0f} kg/h)</text>

        <rect x="588" y="210" width="200" height="52" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="638" y1="210" x2="638" y2="262" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="688" y1="210" x2="688" y2="262" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="738" y1="210" x2="738" y2="262" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="588,225 765,232 788,215" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="605" y="245" fill="{fg_txt}" font-size="12" font-weight="bold">11</text>
        <text x="625" y="202" fill="{fg_txt}" font-size="11" font-weight="bold">BANC. CEL. RO. C1 (4 Celdas)</text>

        <polyline points="755,210 755,152 875,152" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="780" y="145" fill="{line_main}" font-size="11" font-weight="bold">15 ({res['s15_esp_ro1']:.1f} kg/h)</text>
        <rect x="878" y="135" width="96" height="48" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="926" y1="135" x2="926" y2="183" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="878,148 955,154 974,140" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="892" y="168" fill="{fg_txt}" font-size="12" font-weight="bold">12</text>
        <text x="878" y="200" fill="{fg_txt}" font-size="11" font-weight="bold">BAN. CEL. CL. 1</text>

        <polyline points="945,135 945,82 775,82" fill="none" stroke="{line_conc}" stroke-width="2.5" marker-end="url(#arr-conc)"/>
        <circle cx="765" cy="82" r="7" fill="none" stroke="{line_conc}" stroke-width="2"/>
        <text x="845" y="75" fill="{line_conc}" font-size="11" font-weight="bold">17</text>
        <text x="665" y="104" fill="{line_conc}" font-size="12" font-weight="bold">CONC. FINAL C1 ({res['s17_c1']:.2f} kg/h | Ley {m1_sym}: {res['ley_c1_m1']:.1f}% | Rec: {res['rec_glob_c1']:.1f}%)</text>

        <polyline points="788,242 998,242 998,338 935,338" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="860" y="236" fill="{line_main}" font-size="11" font-weight="bold">16 ({res['s16_cola_ro1']:.1f} kg/h)</text>
        <rect x="680" y="308" width="250" height="52" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="730" y1="308" x2="730" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="780" y1="308" x2="780" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="830" y1="308" x2="830" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="880" y1="308" x2="880" y2="360" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="930,322 705,328 680,312" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="905" y="344" fill="{fg_txt}" font-size="12" font-weight="bold">13</text>
        <text x="695" y="298" fill="{fg_txt}" font-size="11" font-weight="bold">BANCO DE CELDAS SCV. CIRCUITO 1 (5 Celdas)</text>

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

        <g opacity="{op_rec}">
          <polyline points="1115,482 1175,482 1175,18 468,18 468,58" fill="none" stroke="{line_rec}" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#arr-rec)"/>
          <text x="795" y="14" fill="{line_rec}" font-size="11" font-weight="bold">21 (Medios C1: {res['s21_medios_c1']:.1f} kg/h)</text>
        </g>
      </g>

      <!-- TRANSFERENCIA C1 -> C2 Y CIRCUITO 2 (C2) -->
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
      <text x="455" y="445" fill="{line_main}" font-size="11" font-weight="bold">24 ({res['s22_cola_scv1']:.1f} kg/h)</text>

      <g opacity="{op_c2}">
        <polygon points="440,512 480,512 480,550 460,570 440,550" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="452" y="542" fill="{fg_txt}" font-size="12" font-weight="bold">18</text>
        <text x="486" y="538" fill="{fg_txt}" font-size="11" font-weight="bold">ACON. 3 (pH {ph_c2:.1f})</text>

        <polyline points="460,570 460,582 520,582 520,596" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="485" y="578" fill="{line_main}" font-size="11" font-weight="bold">25</text>
        <polygon points="500,600 540,600 540,636 520,656 500,636" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <text x="512" y="628" fill="{fg_txt}" font-size="12" font-weight="bold">19</text>
        <text x="442" y="628" fill="{fg_txt}" font-size="11" font-weight="bold">ACON. 4</text>

        <polyline points="520,656 520,668 585,668" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="542" y="663" fill="{line_main}" font-size="11" font-weight="bold">26</text>
        <rect x="588" y="635" width="200" height="48" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="638" y1="635" x2="638" y2="683" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="688" y1="635" x2="688" y2="683" stroke="{eq_stroke}" stroke-width="1.5"/>
        <line x1="738" y1="635" x2="738" y2="683" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="588,648 765,655 788,640" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="605" y="666" fill="{fg_txt}" font-size="12" font-weight="bold">20</text>
        <text x="625" y="627" fill="{fg_txt}" font-size="11" font-weight="bold">BANC. CEL. RO. C2 (4 Celdas)</text>

        <polyline points="755,635 755,585 875,585" fill="none" stroke="{line_main}" stroke-width="2" marker-end="url(#arr)"/>
        <text x="780" y="578" fill="{line_main}" font-size="11" font-weight="bold">27 ({res['s27_esp_ro2']:.1f} kg/h)</text>
        <rect x="878" y="568" width="96" height="46" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="2"/>
        <line x1="926" y1="568" x2="926" y2="614" stroke="{eq_stroke}" stroke-width="1.5"/>
        <polyline points="878,580 955,586 974,572" fill="none" stroke="{eq_stroke}" stroke-width="1.8"/>
        <text x="892" y="598" fill="{fg_txt}" font-size="12" font-weight="bold">21</text>
        <text x="878" y="630" fill="{fg_txt}" font-size="11" font-weight="bold">BAN. CEL. CL. 2</text>

        <polyline points="945,568 945,525 775,525" fill="none" stroke="{line_conc}" stroke-width="2.5" marker-end="url(#arr-conc)"/>
        <circle cx="765" cy="525" r="7" fill="none" stroke="{line_conc}" stroke-width="2"/>
        <text x="845" y="518" fill="{line_conc}" font-size="11" font-weight="bold">29</text>
        <text x="665" y="546" fill="{line_conc}" font-size="12" font-weight="bold">CONC. FINAL C2 ({res['s29_c2']:.2f} kg/h | Ley {m2_sym}: {res['ley_c2_m2']:.1f}% | Rec: {res['rec_glob_c2']:.1f}%)</text>

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

        <g opacity="{op_rec}">
          <polyline points="1128,735 1155,735 1155,498 468,498 468,508" fill="none" stroke="{line_rec}" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#arr-rec)"/>
          <text x="795" y="493" fill="{line_rec}" font-size="11" font-weight="bold">33 (Medios C2: {res['s33_medios_c2']:.1f} kg/h)</text>
        </g>
      </g>

      <g opacity="{op_rel}">
        <polyline points="680,718 425,718" fill="none" stroke="{line_rec}" stroke-width="2.5" marker-end="url(#arr-rec)"/>
        <circle cx="415" cy="718" r="7" fill="none" stroke="{line_rec}" stroke-width="2"/>
        <text x="435" y="708" fill="{line_rec}" font-size="11.5" font-weight="bold">34 — RELAVE FINAL ({res['s34_relave']:.1f} kg/h)</text>
        <text x="435" y="734" fill="{line_rec}" font-size="10.5" font-weight="bold">Leyes: {res['ley_rel_m1']:.2f}% {m1_sym} | {res['ley_rel_m2']:.2f}% {m2_sym} | Fe: {ley_f_fe:.1f}%</text>
      </g>

      <rect x="20" y="655" width="235" height="85" fill="{eq_fill}" stroke="{eq_stroke}" stroke-width="1.5"/>
      <text x="32" y="675" fill="{fg_txt}" font-size="11" font-weight="bold">DIAGRAMA DE FLUJO</text>
      <text x="32" y="692" fill="{fg_txt}" font-size="11" font-weight="bold">"PLANTA PILOTO JICA"</text>
      <text x="32" y="708" fill="{fg_txt}" font-size="10">INGENIERÍA METALÚRGICA - UNMSM</text>
      <text x="32" y="726" fill="{fg_txt}" font-size="9">GEMELO DIGITAL v3.0 (24 EQ / 34 CORR)</text>
    </svg>"""

    svg_box = f'<div style="background:{bg_svg}; border:1px solid {eq_stroke}; border-radius:8px; padding:6px; overflow:auto; max-height:690px;">{svg_only}</div>'
    components.html(svg_box, height=700, scrolling=True)

    st.download_button(
        label="📐 Descargar Plano Flowsheet JICA Vectorial (.SVG)",
        data=svg_only.encode("utf-8"),
        file_name=f"Flowsheet_JICA_v3_{m1_sym}_{m2_sym}.svg",
        mime="image/svg+xml"
    )

# -------------------- PESTAÑA 2: ETAPA 1 CALCULADA --------------------
with tab_et1:
    c_izq, c_der = st.columns([1.45, 1])
    with c_izq:
        st.subheader("📈 Curvas Granulométricas Rosin-Rammler (Valores Calculados)")
        n_rr = 1.15
        d63_reb = res["p80_reb_calc"] / ((-np.log(0.20)) ** (1.0 / n_rr))
        d63_rod = res["f80_mol_um"] / ((-np.log(0.20)) ** (1.0 / 0.95))
        aberturas = np.geomspace(15, 25000, 250)
        pas_reb = 100.0 * (1.0 - np.exp(-((aberturas / d63_reb) ** n_rr)))
        pas_rod = 100.0 * (1.0 - np.exp(-((aberturas / d63_rod) ** 0.95)))

        fig_g = go.Figure()
        fig_g.add_trace(go.Scatter(x=aberturas, y=pas_rod, mode="lines", name=f"Salida Rodillos (F80 calc = {res['f80_mol_um']:.0f} µm)", line=dict(dash="dash", color="#ffa726", width=2.8)))
        fig_g.add_trace(go.Scatter(x=aberturas, y=pas_reb, mode="lines", name=f"Rebose Espiral (P80 calc = {res['p80_reb_calc']:.1f} µm)", line=dict(color="#29b6f6", width=3.5)))
        fig_g.add_trace(go.Scatter(x=[15, 25000], y=[80, 80], mode="lines", name="Línea 80% Pasante", line=dict(dash="dot", color="#ef5350", width=1.8)))
        fig_g.add_trace(go.Scatter(x=[149, 149], y=[0, 100], mode="lines", name="Malla 100 (149 µm)", line=dict(dash="dot", color="#66bb6a", width=1.8)))
        fig_g.update_layout(
            xaxis=dict(type="log", title="Abertura (µm)", range=[np.log10(15), np.log10(25000)], tickvals=[20, 37, 53, 74, 105, 149, 210, 500, 1000, 2500, 7500, 20000]),
            yaxis=dict(title="% Pasante Acumulado", range=[0, 105]),
            template="plotly_dark", height=420
        )
        st.plotly_chart(fig_g, width="stretch")

    with c_der:
        st.subheader("🧮 Salidas Calculadas del Modelo (No Editables)")
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
    st.subheader("📊 Análisis de Sensibilidad: P80 de Molienda vs. Recuperación y Ley")
    rango_p80 = np.linspace(80.0, 200.0, 25)
    recs_m1_sens, leyes_m1_sens, recs_m2_sens = [], [], []
    for p_test in rango_p80:
        f_m1_e = np.clip((155.0 - p_test) * 0.06, -5.0, 4.0)
        r1_s = float(np.clip(86.0 + f_m1_e + np.clip((dosis_col_c1 - 35.0) * 0.03, -2.5, 3.0), 55.0, 95.0))
        l1_s = float(np.clip((58.0 if m1_sym == "Pb" else 28.0) + np.clip((dosis_dep_c1 - 250.0) * 0.004, -1.5, 2.0) * 1.8, 18.0, 76.0))
        r2_s = float(np.clip(84.0 + np.clip((dosis_act_c2 - 350.0) * 0.008, -4.0, 4.5) + f_m1_e * 0.5, 50.0, 94.0))
        recs_m1_sens.append(r1_s)
        leyes_m1_sens.append(l1_s)
        recs_m2_sens.append(r2_s)

    fig_s = go.Figure()
    fig_s.add_trace(go.Scatter(x=rango_p80, y=recs_m1_sens, mode="lines+markers", name=f"Recuperación {m1_sym} C1 (%)", line=dict(color="#29b6f6", width=3)))
    fig_s.add_trace(go.Scatter(x=rango_p80, y=recs_m2_sens, mode="lines+markers", name=f"Recuperación {m2_sym} C2 (%)", line=dict(color="#ffa726", width=3)))
    fig_s.add_vline(x=res["p80_reb_calc"], line_dash="dash", line_color="#66bb6a", annotation_text=f"P80 Actual ({res['p80_reb_calc']:.1f} µm)")
    fig_s.update_layout(
        xaxis_title="P80 del Rebose del Clasificador Helicoidal (µm)",
        yaxis_title="Recuperación Metalúrgica (%)",
        template="plotly_dark", height=380
    )
    st.plotly_chart(fig_s, width="stretch")

    st.markdown("#### ⚖️ Balance Global de 3 Productos (Actual)")
    st.dataframe(df_3prod.round(2), hide_index=True, width="stretch")

# -------------------- PESTAÑA 4: TABLA MAESTRA DE 34 CORRIENTES --------------------
with tab_34:
    st.subheader("📋 Registro Oficial de las 34 Corrientes — Planta Piloto JICA")
    st.dataframe(df_34.round(2), hide_index=True, width="stretch")

    buffer_excel = io.BytesIO()
    with pd.ExcelWriter(buffer_excel, engine="xlsxwriter") as writer:
        df_3prod.round(2).to_excel(writer, sheet_name="Balance_Global_C1_C2", index=False)
        df_34.round(2).to_excel(writer, sheet_name="34_Corrientes_JICA", index=False)
    buffer_excel.seek(0)

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            label="🌐 Descargar Excel Completo (34 Corrientes + Balance)",
            data=buffer_excel,
            file_name=f"Reporte_JICA_v3_{m1_sym}_{m2_sym}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col_dl2:
        ruta_drive = Path(r"G:\Mi unidad\02_Trabajo_Metalurgia\01_Balances_y_Planta")
        if ruta_drive.exists():
            if st.button("💾 Guardar Copia en Google Drive Local (G:)"):
                archivo_full = ruta_drive / f"Gemelo_Digital_JICA_v3_{m1_sym}_{m2_sym}.xlsx"
                with open(archivo_full, "wb") as f:
                    f.write(buffer_excel.getvalue())
                st.success(f"Guardado en: {archivo_full}")
