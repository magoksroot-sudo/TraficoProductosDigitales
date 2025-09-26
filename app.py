import streamlit as st
import plotly.graph_objects as go
import numpy as np
import requests

# -----------------------------
# Configuración de página
# -----------------------------
st.set_page_config(page_title="Dashboard Profesional KPIs", layout="wide")
st.title("📊 Dashboard Profesional de KPIs con Proyecciones y Chat AI")

# -----------------------------
# Barra lateral: Inputs
# -----------------------------
st.sidebar.header("Parámetros de Entrada")
visitas = st.sidebar.number_input("Número de visitas actuales", min_value=1, value=10000)
ventas = st.sidebar.number_input("Número de ventas actuales", min_value=0, value=100)
gasto_ads = st.sidebar.number_input("Gasto en publicidad ($)", min_value=0.0, value=500.0)
precio = st.sidebar.number_input("Precio del producto ($)", min_value=1.0, value=50.0)
costos_fijos = st.sidebar.number_input("Costos fijos ($)", min_value=0.0, value=1000.0)
costos_variables = st.sidebar.number_input("Costos variables ($)", min_value=0.0, value=10.0)
frecuencia_compra = st.sidebar.number_input("Compras promedio por cliente (LTV)", min_value=1, value=3)
meses_proyeccion = st.sidebar.number_input("Meses a proyectar", min_value=1, value=6)
crecimiento_pct = st.sidebar.slider("Crecimiento mensual estimado (%)", 0, 100, 10)

# -----------------------------
# Cálculo de KPIs
# -----------------------------
tasa_conversion = (ventas / visitas) * 100
cpa = gasto_ads / ventas if ventas > 0 else 0
ingresos = ventas * precio
roas = ingresos / gasto_ads if gasto_ads > 0 else 0
margen_unitario = precio - costos_variables
ventas_necesarias = costos_fijos / margen_unitario if margen_unitario > 0 else 0
ltv = precio * frecuencia_compra
drop_off = ((visitas - ventas) / visitas) * 100

# -----------------------------
# Proyecciones con crecimiento
# -----------------------------
meses = np.arange(1, meses_proyeccion + 1)
proy_ventas = [ventas]
proy_ingresos = [ingresos]
proy_cpa = [cpa]

for i in range(1, meses_proyeccion):
    nueva_venta = proy_ventas[-1] * (1 + crecimiento_pct / 100)
    proy_ventas.append(nueva_venta)
    proy_ingresos.append(nueva_venta * precio)
    proy_cpa.append(cpa)

# Bandas de incertidumbre (+/-10%)
ingresos_min = [x*0.9 for x in proy_ingresos]
ingresos_max = [x*1.1 for x in proy_ingresos]

# -----------------------------
# Mostrar KPIs principales
# -----------------------------
st.subheader("📈 KPIs Clave")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Tasa de Conversión", f"{tasa_conversion:.2f}%")
col2.metric("CPA", f"${cpa:.2f}")
col3.metric("ROAS", f"{roas:.2f}x")
col4.metric("Ventas Necesarias", f"{ventas_necesarias:.0f}")

st.subheader("ℹ️ Otros KPIs")
col5, col6 = st.columns(2)
col5.metric("Lifetime Value (LTV)", f"${ltv:.2f}")
col6.metric("Drop-off Rate", f"{drop_off:.2f}%")

# -----------------------------
# Gráfico profesional de proyección
# -----------------------------
st.subheader("📈 Proyección Profesional de KPIs")
fig = go.Figure()
fig.add_trace(go.Scatter(x=meses, y=proy_ingresos, mode='lines+markers', name='Ingresos Esperados', line=dict(color='green', width=3)))
fig.add_trace(go.Scatter(x=meses, y=proy_ventas, mode='lines+markers', name='Ventas Esperadas', line=dict(color='blue', width=3)))
fig.add_trace(go.Scatter(x=meses, y=proy_cpa, mode='lines+markers', name='CPA', line=dict(color='red', width=3, dash='dash')))
fig.add_trace(go.Scatter(x=meses, y=ingresos_max, mode='lines', line=dict(width=0), showlegend=False))
fig.add_trace(go.Scatter(x=meses, y=ingresos_min, mode='lines', fill='tonexty', fillcolor='rgba(0,255,0,0.2)', line=dict(width=0), name='Rango Ingresos'))
fig.update_layout(title='Proyección de KPIs con Curvas Suavizadas y Rango de Incertidumbre',
                  xaxis_title='Mes',
                  yaxis_title='Valor',
                  legend=dict(x=0, y=1.1, orientation='h'))
st.plotly_chart(fig)

# -----------------------------
# Explicación de KPIs
# -----------------------------
st.subheader("ℹ️ Explicación de Fórmulas")
st.write("""
- **Tasa de Conversión**: `(Ventas / Visitas) * 100`
- **CPA**: `Gasto en Ads / Ventas`
- **ROAS**: `Ingresos / Gasto en Ads`
- **Ventas Necesarias**: `Costos Fijos / (Precio - Costos Variables)`
- **LTV**: `Precio * Frecuencia de Compra`
- **Drop-off Rate**: `((Visitas - Ventas) / Visitas) * 100`
- **Proyección de Ingresos y Ventas**: calculada mes a mes según crecimiento porcentual
""")

# -----------------------------
# Chat AI con contexto usando Hugging Face Inference API
# -----------------------------
st.subheader("💬 Pregunta a la AI sobre tus KPIs (contexto incluido)")

pregunta = st.text_input("Escribe tu pregunta sobre tus KPIs:")

if pregunta:
    with st.spinner("La AI está respondiendo..."):
        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"
        headers = {"Authorization": "Bearer TU_TOKEN_HUGGINGFACE"}  # reemplaza con tu token gratuito

        contexto = f"""
        Visitas: {visitas}
        Ventas: {ventas}
        Gasto Ads: {gasto_ads}
        Precio: {precio}
        CPA: {cpa:.2f}
        ROAS: {roas:.2f}x
        LTV: {ltv:.2f}
        Drop-off: {drop_off:.2f}%
        Proyección {meses_proyeccion} meses con {crecimiento_pct}% mensual
        """

        payload = {
            "inputs": f"Estos son los KPIs: {contexto}\nUsuario pregunta: {pregunta}\nRespuesta experta:"
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        data = response.json()
        st.write(data[0]['generated_text'])
