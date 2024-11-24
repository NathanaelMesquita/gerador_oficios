import bcrypt
import yaml

def carregar_credenciais():
    ''' Carrega as credenciais de autenticação a partir do arquivo YAML de configuração.

    Esta função abre o arquivo 'config.yaml', carrega seu conteúdo e retorna as credenciais
    de autenticação armazenadas nele.

    Returns:
        dict: Dicionário contendo as credenciais de autenticação.'''
    with open("config.yaml", "r") as file:
        credenciais = yaml.safe_load(file)
        return credenciais

def verificar_login(usuario, senha):
    '''
    Verifica se as credenciais de login fornecidas estão corretas.

    Esta função compara o nome de usuário e a senha fornecidos com os dados armazenados 
    nas credenciais carregadas do arquivo 'config.yaml'. A senha é verificada com base 
    em seu hash armazenado usando bcrypt.

    Args:
        usuario (str): O nome de usuário a ser verificado.
        senha (str): A senha a ser verificada.

    Returns:
        bool: Retorna True se o nome de usuário e a senha estiverem corretos, 
              caso contrário, retorna False.
    '''
    credenciais = carregar_credenciais()
    usuario_data = credenciais["credentials"]["usernames"].get(usuario)
    if usuario_data:
        senha_hash = usuario_data["password"].encode()
        if bcrypt.checkpw(senha.encode(), senha_hash):
            return True
    return False
