import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Function to generate the PDF
def generar_pdf(paciente, fecha, pruebas, precios):
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Unilab - Laboratorio Clínico Especializado", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Cochabamba, {fecha}", ln=True, align="R")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "REF: COTIZACIÓN EXÁMENES DE LABORATORIO", ln=True, align="L")
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Paciente: {paciente}", ln=True)
    pdf.cell(200, 10, "Presente.-", ln=True)
    pdf.ln(5)

    # Table with tests and prices
    pdf.set_font("Arial", "B", 12)
    pdf.cell(130, 10, "EXAMEN DE LABORATORIO", border=1)
    pdf.cell(50, 10, "PRECIO Bs", border=1, ln=True)

    pdf.set_font("Arial", "", 12)
    total = 0
    for i in range(len(pruebas)):
        pdf.cell(130, 10, pruebas[i], border=1)
        pdf.cell(50, 10, str(precios[i]), border=1, ln=True)
        total += precios[i]

    # Total price
    pdf.cell(130, 10, "TOTAL", border=1)
    pdf.cell(50, 10, f"{total} Bs", border=1, ln=True)

    return pdf

# Streamlit App
st.title("Generador de Cotizaciones de Laboratorio")

# Get user input
paciente = st.text_input("Nombre del Paciente")
fecha = st.date_input("Fecha", value=datetime.today())

# Dictionary of available tests and prices
pruebas_dict = {
    "IgA Total": 100,
    "Anti Transglutaminasa IgA": 150,
    "DPG Deaminado IgG": 220,
}

# Allow users to select tests
pruebas_seleccionadas = st.multiselect("Selecciona las pruebas", list(pruebas_dict.keys()))
precios_seleccionados = [pruebas_dict[prueba] for prueba in pruebas_seleccionadas]

if st.button("Generar Cotización"):
    if paciente and pruebas_seleccionadas:
        pdf = generar_pdf(paciente, fecha.strftime("%d/%m/%Y"), pruebas_seleccionadas, precios_seleccionados)
        pdf_output = f"{paciente}_cotizacion.pdf"
        pdf.output(pdf_output)
        with open(pdf_output, "rb") as file:
            st.download_button("Descargar Cotización", file, file_name=pdf_output)
    else:
        st.error("Por favor, ingresa el nombre del paciente y selecciona al menos una prueba.")
