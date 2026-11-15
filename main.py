import pandas as pd
from pathlib import Path

# Conectar directo a tu carpeta 02_Trabajo_Metalurgia en tu 1 TB de Google One
ruta_planta = Path(r"G:\Mi unidad\02_Trabajo_Metalurgia\01_Balances_y_Planta")
ruta_planta.mkdir(parents=True, exist_ok=True)

# Crear balance metalúrgico de prueba (Circuito de Flotación de Cobre)
df = pd.DataFrame({
    "Flujo": ["Cabeza (Alimentacion)", "Concentrado Cu", "Relave Final"],
    "TMS (Toneladas)": [1000.0, 42.5, 957.5],
    "Ley Cu (%)": [1.15, 24.80, 0.10]
})
df["Cu Fino (TM)"] = (df["TMS (Toneladas)"] * df["Ley Cu (%)"]) / 100

archivo_excel = ruta_planta / "Balance_Flotacion_Prueba.xlsx"
df.to_excel(archivo_excel, index=False)

recuperacion = (df.loc[1, "Cu Fino (TM)"] / df.loc[0, "Cu Fino (TM)"]) * 100
print("\n" + "="*55)
print(" LABORATORIO METALÚRGICO LOQ - CONECTADO A GOOGLE ONE 1TB")
print("="*55)
print(df.to_string(index=False))
print("-" * 55)
print(f"Recuperación Metalúrgica Cu : {recuperacion:.2f}%")
print(f"Archivo guardado en Drive   : {archivo_excel}")
print("="*55 + "\n")
