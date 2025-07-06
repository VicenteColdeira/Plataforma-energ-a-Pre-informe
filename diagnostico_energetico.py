# === Plataforma Diagnóstico Energético — Versión Avanzada ===

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import openai
import os
from fpdf import FPDF
import base64

st.set_page_config(page_title="Diagnóstico Energético Avanzado", layout="centered")
st.title("🔋 Plataforma de Diagnóstico Energético para Empresas y Viviendas")
st.write("Completa los datos de tu instalación para recibir un informe con recomendaciones energéticas personalizadas.")

# === 1. Antecedentes de la instalación ===
st.header("1. Antecedentes de la Instalación")
col1, col2 = st.columns(2)
with col1:
    rut = st.text_input("RUT")
    nombre = st.text_input("Nombre empresa/persona")
    rubro = st.selectbox("Rubro", ["Oficinas", "Agrícolas", "Distribución", "Refrigeración", "Casa residencial", "Industrial"])
    subrubro = st.text_input("Sub-rubro")
    empleados = st.number_input("Nº de empleados / habitantes", min_value=0)
with col2:
    direccion = st.text_input("Dirección")
    region = st.selectbox("Región", [
        "Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama", "Coquimbo",
        "Valparaíso", "Metropolitana", "Libertador General Bernardo O’Higgins",
        "Maule", "Ñuble", "Biobío", "Araucanía", "Los Ríos", "Los Lagos",
        "Aysén del General Carlos Ibáñez del Campo", "Magallanes y de la Antártica Chilena"
    ])
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

# === 3. Usos de la energía ===
st.header("3. Usos de la Energía")
usos = st.multiselect("Selecciona los principales usos de la energía:", [
    "Iluminación", "Agua caliente", "Calefacción/Climatización", "Riego", "Riego industrial",
    "Fundición", "Hornos", "Oficina", "Tratamiento de aguas"])

# === 6. Informe final ===
st.header("6. Informe Final")
if st.button("Generar Informe"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.image("https://i.imgur.com/H9WgT0z.png", 10, 8, 33)  # Logo referencial
    pdf.cell(200, 10, txt="Informe de Diagnóstico Energético", ln=1, align='C')

    pdf.set_font("Arial", '', 11)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"**Nombre/RUT:** {nombre} / {rut}\n**Dirección:** {direccion}, {region}\n**Rubro:** {rubro} - {subrubro}\n**Tipo instalación:** {tipo_instalacion}, Tamaño: {tamanio}\n**Personas/empleados:** {empleados}")

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, txt="Resumen de Consumos", ln=1)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, f"Electricidad: {kwh_mes} kWh/mes, {clp_mes_elec} CLP/mes, {clp_anio_elec} CLP/año\nGas: {m3_mes_gas} m³/mes, {clp_mes_gas} CLP/mes, {clp_anio_gas} CLP/año")

    if (clp_mes_elec + clp_mes_gas) > 0:
        labels = ['Electricidad', 'Gas']
        sizes = [clp_mes_elec, clp_mes_gas]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        img = BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        with open("grafico_pie.png", "wb") as f:
            f.write(img.read())
        pdf.image("grafico_pie.png", x=10, w=100)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, txt="Usos principales de energía", ln=1)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, ", ".join(usos))

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, txt="Oportunidades de Ahorro (IA)", ln=1)
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f"""
        Analiza los siguientes datos de consumo energético y tipo de instalación, y entrega recomendaciones para ahorrar energía y considerar eficiencia energética (EE):\n
        Tipo: {tipo_instalacion}, Rubro: {rubro}, Región: {region}, Tamaño: {tamanio},\n        Consumo eléctrico mensual: {kwh_mes} kWh, CLP mensual: {clp_mes_elec},\n        Consumo gas mensual: {m3_mes_gas} m³, CLP mensual: {clp_mes_gas},\n        Usos: {', '.join(usos)}.
        """
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        recomendaciones = respuesta.choices[0].message.content
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 10, recomendaciones)
    except Exception as e:
        pdf.multi_cell(0, 10, f"No se pudieron generar recomendaciones: {e}")

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 10, txt="Potencial de Autoconsumo Solar", ln=1)
    try:
        if kwh_mes > 0:
            costo_instalacion_kwp = 900000
            produccion_kwh_mes_kwp = 120
            kwp_sugerido = round(kwh_mes / produccion_kwh_mes_kwp, 1)
            inversion = round(kwp_sugerido * costo_instalacion_kwp)
            ahorro_anual = round(clp_mes_elec * 12)
            payback = round(inversion / ahorro_anual, 1) if ahorro_anual else 0

            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 10, f"Potencia sugerida: {kwp_sugerido} kWp\nInversión estimada: {inversion:,} CLP\nAhorro anual estimado: {ahorro_anual:,} CLP\nRetorno estimado (payback): {payback} años")
        else:
            pdf.multi_cell(0, 10, "Ingresa consumo eléctrico mensual para calcular potencial solar.")
    except Exception as e:
        pdf.multi_cell(0, 10, f"No se pudo calcular el potencial solar: {e}")

    # === Guardar PDF ===
    output_path = "informe_diagnostico.pdf"
    pdf.output(output_path)

    with open(output_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="Informe_Diagnostico_Energetico.pdf">📥 Descargar Informe PDF</a>'
    st.markdown(href, unsafe_allow_html=True)
    st.success("Informe PDF generado con éxito.")
