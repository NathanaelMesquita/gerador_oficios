import os
from datetime import datetime
from docx import Document
from fpdf import FPDF
import streamlit as st

# Caminho para o modelo
TEMPLATE_PATH = "modelo.docx"

# Função para preencher o modelo DOCX
def preencher_modelo(template_path, context):
    """Preenche o modelo DOCX com os dados fornecidos no contexto."""
    doc = Document(template_path)
    for paragraph in doc.paragraphs:
        for key, value in context.items():
            if f"{{{key}}}" in paragraph.text:
                paragraph.text = paragraph.text.replace(f"{{{key}}}", value)
    return doc

# Função para salvar o conteúdo preenchido como PDF
def salvar_docx_como_pdf(doc: Document, nome_pdf: str):
    """Converte o conteúdo do DOCX preenchido em PDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for paragraph in doc.paragraphs:
        pdf.multi_cell(0, 10, paragraph.text)
    pdf.output(nome_pdf)

# Função principal para gerar ofício e permitir download
def gerar_oficio(context):
    """Gera um ofício preenchido e converte para PDF."""
    # Preencher o modelo com os dados fornecidos
    doc = preencher_modelo(TEMPLATE_PATH, context)

    # Salvar como PDF
    pdf_path = "oficio_preenchido.pdf"
    salvar_docx_como_pdf(doc, pdf_path)

    # Exibir o PDF como botão de download
    with open(pdf_path, "rb") as pdf_file:
        st.download_button(
            label="Baixar Ofício em PDF",
            data=pdf_file,
            file_name="oficio_preenchido.pdf",
            mime="application/pdf"
        )

# Interface Streamlit
st.title("Gerador de Ofícios Automáticos")

# Coleta de Dados
st.header("Preencha os dados abaixo para gerar o ofício:")

numero_oficio = st.text_input("Número do Ofício", "001")
ano_atual = datetime.now().year
operadora = st.selectbox("Operadora", ["Vivo", "Claro", "TIM"])
tipo_referencia = st.selectbox("Tipo de Referência", ["IP", "VPI"])
numero_referencia = st.text_input(f"Número do {tipo_referencia}", "12345")
ano_referencia = st.text_input("Ano do IP/VPI", str(ano_atual))
cpf = st.text_area("Lista de CPFs (um por linha)", "000.000.000-00")
email = st.text_input("E-mail para Resposta", "delegado@exemplo.com")
nome_delegado = st.text_input("Nome do Delegado", "Delegado Exemplo")

# Gerar Ofício ao clicar no botão
if st.button("Gerar Ofício"):
    # Preparar o contexto para substituição
    context = {
        "número_oficio": numero_oficio,
        "ano_atual": str(ano_atual),
        "operadora": operadora,
        "IP/VPI": tipo_referencia,
        "Número_ip_vpi": numero_referencia,
        "ano_ip_vpi": ano_referencia,
        "email_delegacia": email,
        "nome_delegado": nome_delegado,
        "cpf_lista": "\n".join([f"  - {c.strip()}" for c in cpf.splitlines() if c.strip()]),
    }

    # Gerar o documento e oferecer download
    gerar_oficio(context)
