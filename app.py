import streamlit as st
from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('logo.png', 10, 8, 30)
        # Título del laboratorio
        self.set_font('Arial', 'B', 12)
        self.cell(0, 5, 'Unilab', 0, 1, 'R')
        self.set_font('Arial', '', 8)
        self.cell(0, 5, 'Laboratorio Clínico Especializado', 0, 1, 'R')
        # Fecha
        self.set_font('Arial', '', 10)
        self.cell(0, 5, f"Cochabamba, {fecha.strftime('%d de %B de %Y')}", 0, 1, 'R')
        # Línea separadora
        self.ln(5)

def generar_pdf(paciente, fecha, pruebas, precios):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Destinatario y referencia
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, "Señores:", 0, 1)
    pdf.cell(0, 5, "Hospital Cossmil", 0, 1)
    pdf.cell(0, 5, f"Paciente: {paciente}", 0, 1)
    pdf.cell(0, 5, "Presente.-", 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 5, "REF: COTIZACIÓN EXÁMENES DE LABORATORIO", 0, 1)
    pdf.ln(5)

    # Introducción
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, "Atendiendo su solicitud, le cotizamos los siguientes exámenes:", 0, 1)
    pdf.ln(5)

    # Tabla de exámenes
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(140, 7, "EXAMEN DE LABORATORIO", 1, 0, 'L')
    pdf.cell(50, 7, "PRECIO Bs", 1, 1, 'C')
    
    pdf.set_font('Arial', '', 10)
    total = 0
    for i in range(len(pruebas)):
        pdf.cell(140, 7, pruebas[i], 1, 0, 'L')
        pdf.cell(50, 7, str(precios[i]), 1, 1, 'R')
        total += precios[i]
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(140, 7, "TOTAL:", 1, 0, 'R')
    pdf.cell(50, 7, f"{total} Bs", 1, 1, 'R')

    # Cierre
    pdf.ln(5)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, "Esperamos de ustedes una respuesta positiva, saludos cordiales.", 0, 1)
    pdf.ln(10)

    # Firma
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, "Atentamente", 0, 1)
    pdf.ln(10)
    pdf.cell(0, 5, "Dra. Susana R. Panozo Melgares", 0, 1)
    pdf.cell(0, 5, "Regente Bioquímica", 0, 1)
    pdf.cell(0, 5, "MP P-556", 0, 1)
    pdf.cell(0, 5, "Cel. 62723377", 0, 1)

    return pdf

# Interfaz de Streamlit
st.title("Generador de Cotizaciones de Laboratorio")

paciente = st.text_input("Nombre del Paciente")
fecha = st.date_input("Fecha", value=datetime.today())

pruebas_dict = {
    "IgA Total": 100,
    "Anti Transglutaminasa IgA": 150,
    "DPG Deaminado IgG": 220,
}

pruebas_seleccionadas = st.multiselect("Selecciona las pruebas", list(pruebas_dict.keys()))
precios_seleccionados = [pruebas_dict[prueba] for prueba in pruebas_seleccionadas]

if st.button("Generar Cotización"):
    if paciente and pruebas_seleccionadas:
        pdf = generar_pdf(paciente, fecha, pruebas_seleccionadas, precios_seleccionados)
        pdf_output = f"{paciente}_cotizacion.pdf"
        pdf.output(pdf_output)
        with open(pdf_output, "rb") as f:
            st.download_button("Descargar PDF", data=f, file_name=pdf_output, mime="application/pdf")
    else:
        st.error("Por favor, ingresa el nombre del paciente y selecciona al menos una prueba.")
