# === Plataforma Diagnóstico Energético — Versión Avanzada ===

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Diagnóstico Energético Avanzado", layout="centered")
st.title("🔋 Plataforma de Diagnóstico Energético para Empresas y Viviendas")
st.write("Completa los datos de tu instalación para recibir un informe con recomendaciones energéticas personalizadas.")

# === 1. Antecedentes de la instalación ===
st.header("1. Antecedentes de la Instalación")
col1, col2 = st.columns(2)
with col1:
    rut = st.text_input("RUT")
    nombre = st.text_input("Nombre empresa/persona")
    rubro = st.text_input("Rubro")
    subrubro = st.text_input("Sub-rubro")
    empleados = st.number_input("Nº de empleados / habitantes", min_value=0)
with col2:
    direccion = st.text_input("Dirección")
    region = st.selectbox("Región", ["Metropolitana", "Valparaíso", "Biobío", "Araucanía", "Otra"])
    tipo_instalacion = st.selectbox("Tipo de instalación", ["Oficina", "Galpón", "Refrigeración", "Edificio", "Fábrica", "Terreno rural", "Agrícola", "Casa residencial"])
    tamanio = st.text_input("Tamaño (m² o descripción)")

# === 2. Consumo y gasto energético ===
st.header("2. Consumo y Gasto Energético")
st.subheader("Electricidad")
kwh_mes = st.number_input("Consumo eléctrico mensual (kWh)", min_value=0.0)
clp_mes_elec = st.number_input("Costo mensual electricidad (CLP)", min_value=0.0)
clp_anio_elec = st.number_input("Costo anual electricidad (CLP)", min_value=0.0)

st.subheader("Gas")
m3_mes_gas = st.number_input("Consumo gas mensual (m³)", min_value=0.0)
clp_mes_gas = st.number_input("Costo mensual gas (CLP)", min_value=0.0)
clp_anio_gas = st.number_input("Costo anual gas (CLP)", min_value=0.0)

# Gráfico de torta
if (clp_mes_elec + clp_mes_gas) > 0:
    st.subheader("Distribución de consumo mensual")
    labels = ['Electricidad', 'Gas']
    sizes = [clp_mes_elec, clp_mes_gas]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# === 3. Usos de la energía ===
st.header("3. Usos de la Energía")
usos = st.multiselect("Selecciona los principales usos de la energía:", [
    "Iluminación", "Agua caliente", "Calefacción/Climatización", "Riego", "Riego industrial",
    "Fundición", "Hornos", "Oficina", "Tratamiento de aguas"])

# === 4. Oportunidades de ahorro ===
st.header("4. Oportunidades de Ahorro (IA)")
st.info("En la próxima versión, aquí se generarán recomendaciones personalizadas usando inteligencia artificial.")

# === 5. Autoconsumo Solar (Estimación) ===
st.header("5. Potencial de Autoconsumo Solar")
st.info("En esta sección se mostrará el potencial de generación solar estimado en base a tu región y consumo.")

# === 6. Informe final ===
st.header("6. Informe Final")
st.warning("El informe completo será generado aquí en formato texto o PDF en la siguiente versión.")

# === Placeholder para botón ===
st.button("Generar Informe (Próximamente)")
