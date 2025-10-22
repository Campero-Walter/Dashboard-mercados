# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 12:13:11 2025

@author: walte
"""
# Librerias
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# Nombre del archivo
name_file = "Newsletter_Semanal.pdf"

# Crear el documento
pdf = SimpleDocTemplate(name_file, pagesizes=A4)

# Estilos de texto
styles = getSampleStyleSheet()
titulo = styles["Heading1"]
subtitulo = styles["Heading2"]
parrafo = styles["BodyText"]

# Contenido del PDF
elementos = []


# Agregar título
elementos.append(Paragraph("Newsletter Semanal", titulo))
elementos.append(Spacer(1, 12))

# Subtitulo
elementos.append(Spacer(1, 12))

# Texto = 
texto = """
El sp subió 10%
"""

elementos.append(Paragraph(texto, parrafo))
elementos.append(Spacer(1, 12))

# Tabla de ejemplo
datos = [
    ["Indicador", "2023", "2024", "Var. %"],
    ["PBG (millones $)", "4.500", "4.830", "7.3%"],
    ["Empleo registrado", "120.000", "124.800", "4.0%"],
    ["Inversión pública ($ millones)", "900", "1.050", "16.7%"]
]

tabla = Table(datos)
tabla.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#d3d3d3")),
    ('TEXTCOLOR', (0,0), (-1,0), colors.black),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0,0), (-1,0), 10)
]))
elementos.append(tabla)

# Construir el PDF
pdf.build(elementos)

print(f"✅ Informe generado: {name_file}")














