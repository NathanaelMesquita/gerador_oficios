from docx import Document
import streamlit as st
from datetime import datetime

# Caminho do modelo
TEMPLATE_PATH = "modelo.docx"

def preencher_modelo(template_path, context, output_path):
    """
    Preenche o modelo DOCX substituindo os placeholders pelos valores fornecidos.
    """
    doc = Document(template_path)
    for paragraph in doc.paragraphs:
        for key, value in context.items():
            if f"{{{key}}}" in paragraph.text:
                paragraph.text = paragraph.text.replace(f"{{{key}}}", value)

    # Verificar também placeholders em tabelas
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in context.items():
                    if f"{{{key}}}" in cell.text:
                        cell.text = cell.text.replace(f"{{{key}}}", value)

    doc.save(output_path)

def gerar_oficio(context):
    """
    Preenche o modelo DOCX e oferece o arquivo para download.
    """
    # Caminho para salvar o DOCX preenchido
    preenchido_path = "oficio_preenchido.docx"

    # Preencher o modelo
    preencher_modelo(TEMPLATE_PATH, context, preenchido_path)

    # Oferecer o DOCX para download
    with open(preenchido_path, "rb") as docx_file:
        st.download_button(
            label="Baixar Ofício em DOCX",
            data=docx_file,
            file_name="oficio_preenchido.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

# Interface Streamlit
st.title("Gerador de Ofícios Automáticos")
st.header("Preencha os dados abaixo para gerar o ofício:")

# Entradas do usuário
numero_oficio = st.text_input("Número do Ofício", "001")
ano_atual = datetime.now().year
operadora = st.selectbox("Operadora", ["Vivo", "Claro", "TIM"])
tipo_referencia = st.selectbox("Tipo de Referência", ["IP", "VPI"])
numero_referencia = st.text_input(f"Número do {tipo_referencia}", "12345")
ano_referencia = st.text_input("Ano do IP/VPI", str(ano_atual))
cpf = st.text_area("Lista de CPFs (um por linha)", "000.000.000-00")
email = st.text_input("E-mail para Resposta", "delegado@exemplo.com")
nome_delegado = st.text_input("Nome do Delegado", "Delegado Exemplo")
nome_delegacia = st.text_input("Nome da Delegacia", "Delegacia Exemplo")

# Data atual formatada
data_atual = datetime.now()
data_formatada = data_atual.strftime("%d de %B de %Y")

# Gerar Ofício
if st.button("Gerar Ofício"):
    # Criar o contexto para substituição
    context = {
        "numero_oficio": numero_oficio,
        "ano_atual": str(ano_atual),
        "data_atual": data_formatada,
        "operadora": operadora,
        "IP/VPI": tipo_referencia,
        "numero_ip_vpi": numero_referencia,
        "ano_ip_vpi": ano_referencia,
        "email_delegacia": email,
        "nome_delegado": nome_delegado,
        "cpf_lista": "\n".join([f"  - {c.strip()}" for c in cpf.splitlines() if c.strip()]),
        "nome_delegacia": nome_delegacia,
    }

    # Gerar o documento e permitir download
    gerar_oficio(context)
