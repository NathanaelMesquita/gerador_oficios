import streamlit as st
import os
import streamlit as st
from hash_module import gerar_pdf_tabela, carregar_arquivos
from login_module import verificar_login

# Configurações iniciais da página
st.set_page_config(page_title="Análise Sintética de RIF", layout="wide")

# Inicializa o estado de login

if "login" not in st.session_state:
    st.session_state["login"] = False
    
if "program" not in st.session_state:  # Adiciona essa linha para garantir que a funcionalidade não mantenha o estado
    st.session_state["program"] = None
    
# Interface de login
if not st.session_state["login"]:
    
    col1, _, col2 = st.columns([1, 5, 1])
    
    with col1:
        st.image("logo_esquerda.png", width=100)

    with col2:
        st.image("logo_direita.png", width=100)
        
    st.title("Lab Tools")
    usuario = st.text_input("Nome de Usuário")
    senha = st.text_input("Senha", type="password") 
    
    if st.button("Entrar"):
        
        if verificar_login(usuario, senha):
            st.session_state["login"] = True  # Define o estado de login como verdadeiro
            st.session_state["program"] = "analisador"
            st.success("Login realizado com sucesso!")
            st.rerun()  # Recarrega a página para atualizar o estado
        else:
            st.error("Usuário ou senha incorretos.")
else:
    # Se o login for bem-sucedido, essa parte será executada
    st.success("Você está logado!")
      
    if st.button("Sair"):
        st.session_state["login"] = False
        st.session_state["program"] = None  # Adiciona esta linha para redefinir a funcionalidade ao sair
        st.rerun()  # Recarrega a página ao sair

    col1, _, col2 = st.columns([1, 5, 1])  # Configuração para exibir dois logotipos nas extremidades superior esquerda e direita

    with col1:
        st.image("logo_esquerda.png", width=100)

    with col2:
        st.image("logo_direita.png", width=100)
    # Criar botões para selecionar entre o analisador de RIF e o gerador de hash
    col1_2, col2_1 = st.columns([1 , 5], gap = "small")  # Cria duas colunas para os botões

    with col1_2:
        if st.button("Analisador de RIF"):
            st.session_state["program"] = "analisador"
            st.rerun()  # Recarrega a página

    with col2_1:
        if st.button("Gerador de Hash"):
            st.session_state["program"] = "gerador"
            st.rerun()  # Recarrega a página
    # Código principal só será executado após a seleção de programa
    if "program" in st.session_state:
        if st.session_state["program"] == "analisador":
            # # Código para o analisador de RIF
            # # Clonar o repositório privado do GitHub
            # repo_url = "https://github.com/Rudsonrocha0609/analise.git"
            # local_path = "./repo"

            # # Obtenha o token do ambiente
            # token = os.getenv("GITHUB_TOKEN")

            # # Montar URL autenticada
            # authenticated_url = repo_url.replace("https://", f"https://{token}@")

            # # Clonar o repositório
            # if not os.path.exists(local_path):
            #     Repo.clone_from(authenticated_url, local_path)
            #     st.write("Leia as instruções.")
            # else:
            st.write("Leia as instruções, cuidadosamente.")
            st.title("Análise Sintética de RIF")
           # Carregar arquivos de entrada
            principais_envolvidos = st.file_uploader("Carregue o arquivo 'Principais Envolvidos.xlsx'", type="xlsx")
            informacoes_adicionais = st.file_uploader("Carregue o arquivo 'InformacoesAdicionais.xlsx'", type="xlsx")

            # Caminho do arquivo de saída
            output_file = os.path.join(os.getcwd(), "análises_sintéticas.xlsx")

            # Botão para iniciar a análise
            if st.button("Gerar Análise"):
                # Função para processar e gerar a análise sintética
                gerar_analise_e_baixar(principais_envolvidos, informacoes_adicionais)

            # Botão para gerar o relatório final
            st.title("Gerador de Relatório")
            arquivo_analise = st.file_uploader("Carregue o arquivo de análise 'análises_sintéticas.xlsx' para gerar o relatório", type="xlsx")
            if arquivo_analise is not None:
                relatorio = gerar_relatorio(arquivo_analise)
                st.download_button(
                    label="Baixar Relatório Final",
                    data=relatorio,
                    file_name="relatorio_final.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

        elif st.session_state["program"] == "gerador":
            # Código para o gerador de hash
            st.title("Leitor de Arquivos e Gerador de Hash")
            st.write("Carregue seus arquivos para gerar os hashes correspondentes.")

            arquivos_upload = st.file_uploader("Escolha os arquivos", type=["xlsx", "xls", "txt", "pdf"], accept_multiple_files=True)
            if arquivos_upload:
                resultados = carregar_arquivos(arquivos_upload)
                if resultados:
                    st.write("**Resultados:**")
                    for nome_arquivo, hash_gerado in resultados:
                        st.write(f"{nome_arquivo}: {hash_gerado}")

                    # Gerar PDF automaticamente
                    pdf_buffer = gerar_pdf_tabela(resultados)
                    if pdf_buffer:
                        st.success("PDF gerado com sucesso!")

                        # Campo de entrada para o nome do arquivo
                        nome_arquivo = st.text_input("Digite o nome do arquivo para download", value="hashes")

                        # Botão para baixar o PDF com o nome especificado pelo usuário
                        st.download_button("Baixar PDF com Hashes", pdf_buffer, file_name=f"{nome_arquivo}.pdf", mime='application/pdf')
                else:
                    st.warning("Nenhum arquivo válido carregado.")
