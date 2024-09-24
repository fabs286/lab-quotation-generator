import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Función para generar el PDF con el logo y el formato similar al ejemplo proporcionado
def generar_pdf(paciente, fecha, pruebas, precios):
    pdf = FPDF()
    pdf.add_page()

    # Añadir el logo en la esquina superior izquierda (ajusta el nombre del archivo y la ruta si es necesario)
    pdf.image('logo.png', 10, 8, 33)  # Coloca el logo en la parte superior izquierda, tamaño 33
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Unilab - Laboratorio Clínico Especializado", ln=True, align="C")  # Título centrado
    
    # Fecha y ciudad alineada a la derecha
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Cochabamba, {fecha}", ln=True, align="R")
    pdf.ln(10)
    
    # Título de la cotización
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "REF: COTIZACIÓN EXÁMENES DE LABORATORIO", ln=True, align="L")
    pdf.ln(5)

    # Información del paciente y destinatario
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Señores:", ln=True)
    pdf.cell(200, 10, f"Hospital: Cossmil", ln=True)
    pdf.cell(200, 10, f"Paciente: {paciente}", ln=True)
    pdf.cell(200, 10, "Presente.-", ln=True)
    pdf.ln(5)

    # Introducción de la tabla
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, "Atendiendo su solicitud, le cotizamos los siguientes exámenes:", ln=True)
    pdf.ln(5)
    
    # Tabla de exámenes y precios
    pdf.set_font("Arial", "B", 12)
    pdf.cell(130, 10, "EXAMEN DE LABORATORIO", border=1)
    pdf.cell(50, 10, "PRECIO Bs", border=1, ln=True)

    pdf.set_font("Arial", "", 12)
    total = 0
    for i in range(len(pruebas)):
        pdf.cell(130, 10, pruebas[i], border=1)
        pdf.cell(50, 10, str(precios[i]), border=1, ln=True)
        total += precios[i]

    # Total de la cotización
    pdf.cell(130, 10, "TOTAL", border=1)
    pdf.cell(50, 10, f"{total} Bs", border=1, ln=True)
    pdf.ln(10)

    # Mensaje de cierre
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, "Esperamos de ustedes una respuesta positiva, saludos cordiales.", ln=True)
    pdf.ln(15)

    # Firma y contacto
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Atentamente,", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, "Dra. Susana R. Ranozo Melgares", ln=True)
    pdf.cell(200, 10, "Regente Bioquímica", ln=True)
    pdf.cell(200, 10, "MP P-555", ln=True)
    pdf.cell(200, 10, "Cel. 62723377", ln=True)

    return pdf

# Streamlit App para generar la cotización y descargar el PDF
st.title("Generador de Cotizaciones de Laboratorio")

# Entrada de datos para el paciente y la fecha
paciente = st.text_input("Nombre del Paciente")
fecha = st.date_input("Fecha", value=datetime.today())

# Diccionario de pruebas y precios
pruebas_dict = {
    "IgA Total": 100,
    "Anti Transglutaminasa IgA": 150,
    "DPG Deaminado IgG": 220,
}

# Selección dinámica de las pruebas
pruebas_seleccionadas = st.multiselect("Selecciona las pruebas", list(pruebas_dict.keys()))
precios_seleccionados = [pruebas_dict[prueba] for prueba in pruebas_seleccionadas]

# Botón para generar el PDF
if st.button("Generar Cotización"):
    if paciente and pruebas_seleccionadas:
        # Generar PDF
        pdf = generar_pdf(paciente, fecha.strftime("%d de %B de %Y"), pruebas_seleccionadas, precios_seleccionados)
        
        # Guardar el archivo PDF
        pdf_output = f"{paciente}_cotizacion.pdf"
        pdf.output(pdf_output)

        # Descargar el PDF generado
        with open(pdf_output, "rb") as f:
            st.download_button("Descargar PDF", data=f, file_name=pdf_output, mime="application/pdf")
    else:
        st.error("Por favor, ingresa el nombre del paciente y selecciona al menos una prueba.")
