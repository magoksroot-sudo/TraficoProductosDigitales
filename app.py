import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Dashboard de KPIs", page_icon="📊", layout="wide")

# Título de la aplicación
st.title("📊 Dashboard Profesional de KPIs de Marketing Digital")

# Entrada de datos
st.sidebar.header("Parámetros de Entrada")
visitas = st.sidebar.number_input("Número de visitas", min_value=1, value=10000)
ventas = st.sidebar.number_input("Número de ventas", min_value=0, value=100)
gasto_ads = st.sidebar.number_input("Gasto en publicidad ($)", min_value=0.0, value=500.0)
precio = st.sidebar.number_input("Precio del producto ($)", min_value=1.0, value=50.0)
costos_fijos = st.sidebar.number_input("Costos fijos mensuales ($)", min_value=0.0, value=1000.0)
costos_variables = st.sidebar.number_input("Costos variables por unidad ($)", min_value=0.0, value=10.0)

# Cálculos de KPIs
tasa_conversion = (ventas / visitas) * 100
cpa = gasto_ads / ventas if ventas > 0 else 0
ingresos = ventas * precio
roas = ingresos / gasto_ads if gasto_ads > 0 else 0
margen_unitario = precio - costos_variables
ventas_necesarias = costos_fijos / margen_unitario if margen_unitario > 0 else 0

# Mostrar métricas clave
st.subheader("📈 Métricas Clave")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Tasa de Conversión", f"{tasa_conversion:.2f}%", delta=f"{tasa_conversion - 1:.2f}%")
with col2:
    st.metric("CPA", f"${cpa:.2f}", delta=f"${cpa - precio:.2f}")
with col3:
    st.metric("ROAS", f"{roas:.2f}x", delta=f"{roas - 1:.2f}x")
with col4:
    st.metric("Ventas Necesarias", f"{ventas_necesarias:.0f} ventas")

# Gráfico interactivo de ventas vs. ventas necesarias
fig = go.Figure()
fig.add_trace(go.Bar(x=["Ventas Actuales", "Ventas Necesarias"], y=[ventas, ventas_necesarias],
                    marker_color=["blue", "orange"]))
fig.update_layout(title="Comparación: Ventas Actuales vs. Ventas Necesarias",
                  xaxis_title="Categoría", yaxis_title="Número de Ventas")
st.plotly_chart(fig)

# Explicación de KPIs
st.subheader("ℹ️ Explicación de cada KPI")
st.write("""
- **Tasa de Conversión**: Mide el porcentaje de visitantes que realizan una compra. Fórmula: (Ventas / Visitas) * 100.
- **CPA (Costo por Adquisición)**: Indica cuánto cuesta adquirir un cliente. Fórmula: Gasto en Ads / Ventas.
- **ROAS (Retorno sobre Gasto en Ads)**: Mide la rentabilidad de tus campañas publicitarias. Fórmula: Ingresos / Gasto en Ads.
- **Ventas Necesarias**: Número de ventas requeridas para cubrir los costos fijos. Fórmula: Costos Fijos / (Precio - Costos Variables).
""")
