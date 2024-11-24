import hashlib
import io
import streamlit as st
import PyPDF2
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image

def gerar_hash(conteudo):
    '''
    Gera o hash SHA-256 a partir do conteúdo fornecido.

    Esta função recebe uma string como entrada, calcula seu hash utilizando o algoritmo SHA-256
    e retorna o valor hexadecimal do hash gerado.

    Args:
        conteudo (str): O conteúdo a ser usado para gerar o hash.

    Returns:
        str: O hash SHA-256 do conteúdo, representado como uma string hexadecimal.
    '''
    return hashlib.sha256(conteudo.encode()).hexdigest()


# Função para ler o conteúdo de um arquivo PDF
def ler_pdf(arquivo):
    '''Lê o conteúdo de um arquivo PDF e extrai o texto.

    Esta função tenta abrir um arquivo PDF e extrair seu conteúdo textual, retornando o texto
    extraído de todas as páginas do PDF. Se houver algum erro durante a leitura do PDF, 
    uma mensagem de erro é exibida.

    Args:
        arquivo (file-like object): O arquivo PDF a ser lido.

    Returns:
        str: O conteúdo textual extraído do PDF.'''
    conteudo = ""
    try:
        with io.BytesIO(arquivo.read()) as pdf_buffer:
            pdf_reader = PyPDF2.PdfReader(pdf_buffer)
            for page in pdf_reader.pages:
                texto = page.extract_text()
                if texto:
                    conteudo += texto + "\n"
    except Exception as e:
        st.error(f"Erro ao ler o PDF: {e}")
    return conteudo.strip()


# Função para carregar múltiplos arquivos e gerar os hashes
def carregar_arquivos(arquivos):
    '''Carrega múltiplos arquivos e gera os hashes SHA-256 para cada um.

    Esta função percorre uma lista de arquivos, lê seu conteúdo dependendo do tipo de arquivo
    (PDF, texto ou Excel) e gera um hash SHA-256 para cada conteúdo. Os resultados são retornados
    em uma lista de tuplas contendo o nome do arquivo e o hash gerado.

    Args:
        arquivos (list of file-like objects): A lista de arquivos a serem processados.

    Returns:
        list of tuple: Uma lista de tuplas, onde cada tupla contém o nome do arquivo e o hash SHA-256 gerado.'''
    resultados = []
    for arquivo in arquivos:
        conteudo = None
        if arquivo.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(arquivo)
            conteudo = df.to_string(index=False)
        elif arquivo.name.endswith('.txt'):
            conteudo = arquivo.read().decode("utf-8")
        elif arquivo.name.endswith('.pdf'):
            conteudo = ler_pdf(arquivo)

        if conteudo:
            hash_gerado = gerar_hash(conteudo)
            resultados.append((arquivo.name, hash_gerado))
    return resultados


# Função para gerar e retornar o PDF com os hashes
def gerar_pdf_tabela(dados):
    '''Gera um PDF contendo uma tabela com os hashes SHA-256 de arquivos.

    Esta função cria um PDF com uma tabela que lista o nome dos arquivos e seus respectivos
    hashes SHA-256 gerados. O PDF também inclui um cabeçalho com uma imagem e uma mensagem de
    geração com a data e hora atuais.

    Args:
        dados (list of tuple): Lista de tuplas contendo o nome do arquivo e o hash gerado.

    Returns:
        io.BytesIO: O buffer de bytes contendo o PDF gerado. Retorna None se ocorrer um erro.
    """'''
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1, bottomMargin=1 * cm, leftMargin=1 * cm, rightMargin=1 * cm)

    dados_tabela = [["Nome do Arquivo", "Hash Gerado (SHA-256)"]]
    
    max_len = 55
    for nome, hash_code in dados:
        nome_quebrado = '\n'.join([nome[i:i+max_len] for i in range(0, len(nome), max_len)])
        dados_tabela.append([nome_quebrado, hash_code])

    tabela = Table(dados_tabela, colWidths=[10*cm, 10*cm])
    estilo_tabela = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('LEADING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ])
    tabela.setStyle(estilo_tabela)

    data_atual = datetime.now().strftime("%d/%m/%Y")
    hora_atual = datetime.now().strftime("%H:%M:%S")
    mensagem = f'A tabela contendo o código hash referente a cada arquivo foi gerada na data "{data_atual}" às "{hora_atual}".'
    estilo = getSampleStyleSheet()["Normal"]
    paragrafo_mensagem = Paragraph(mensagem, estilo)

    cabecalho_imagem = Image("cabeçalho_pol_gov.jpg", width=22 * cm, height=3 * cm)

    elementos = [cabecalho_imagem, paragrafo_mensagem, tabela]

    try:
        pdf.build(elementos)
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"Erro ao gerar o PDF: {e}")
        return None
    
    