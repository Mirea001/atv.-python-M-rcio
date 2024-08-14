agenda = []  # Inicializa a lista

alterada = False  # Variável para marcar uma alteração na agenda

def pede_nome(padrao=""):    # Solicita ao usuário o nome de um contato
    nome = input("Nome: ")
    if nome == "":   # Se o usuário não digitar nada, usa o valor padrão
        nome = padrao
    return nome

def pede_telefone(padrao=""):     # Solicita ao usuário o telefone de um contato
    telefone = input("Telefone: ")
    if telefone == "":      # Se o usuário não digitar nada, usa o valor padrão
        telefone = padrao
    return telefone

def pede_endereco(padrao=""):     # Solicita ao usuário o endereço de um contato
    endereco = input("Endereço: ")
    if endereco == "":      # Se o usuário não digitar nada, usa o valor padrão
        endereco = padrao
    return endereco

def pede_cidade(padrao=""):     # Solicita ao usuário a cidade de um contato
    cidade = input("Cidade: ")
    if cidade == "":      # Se o usuário não digitar nada, usa o valor padrão
        cidade = padrao
    return cidade

def pede_estado(padrao=""):     # Solicita ao usuário o estado de um contato
    estado = input("Estado: ")
    if estado == "":      # Se o usuário não digitar nada, usa o valor padrão
        estado = padrao
    return estado

def mostra_dados(nome, telefone, endereco, cidade, estado):
    print(f"Nome: {nome} | Telefone: {telefone} | Endereço: {endereco} | Cidade: {cidade} | Estado: {estado}")

def pede_nome_arquivo():
    return input("Nome do arquivo: ")  # Solicita ao usuário o nome de um arquivo para leitura ou gravação

def pesquisa(nome):
    mnome = nome.lower()  # Pesquisa por um contato na agenda
    for p, e in enumerate(agenda):  # Percorre a agenda e verifica se o nome (em minúsculas) existe
        if e[0].lower() == mnome:
            return p
    return None  # Retorna None se o contato não for encontrado

def nome_duplicado(nome):
    if pesquisa(nome) is not None:  # Verifica se o nome já existe na agenda
        print("Erro: Já existe um contato com esse nome na agenda.")
        return True
    return False

def novo():
    global agenda, alterada  # Cria um novo contato e o adiciona à agenda
    nome = pede_nome()
    if nome_duplicado(nome):  # Verifica se o nome já existe antes de prosseguir
        return
    telefone = pede_telefone()
    endereco = pede_endereco()
    cidade = pede_cidade()
    estado = pede_estado()
    agenda.append([nome, telefone, endereco, cidade, estado])
    alterada = True  # Marca que houve alteração

def confirma(operacao):
    while True:  # Pede confirmação ao usuário para realizar uma operação
        opcao = input(f"Confirma {operacao} (S/N)? ").upper()
        if opcao in "SN":
            return opcao
        else:
            print("Resposta inválida. Escolha S ou N.")

def apaga():
    global agenda, alterada  # Apaga um contato da agenda
    nome = pede_nome()
    p = pesquisa(nome)
    if p is not None:  # Se o contato for encontrado, pede confirmação antes de apagar
        if confirma("apagamento") == "S":
            del agenda[p]
            alterada = True  # Marca que houve alteração
    else:
        print("Nome não encontrado.")

def altera():
    global alterada  # Altera os dados de um contato existente na agenda
    p = pesquisa(pede_nome())
    if p is not None:
        nome = agenda[p][0]
        telefone = agenda[p][1]
        endereco = agenda[p][2]
        cidade = agenda[p][3]
        estado = agenda[p][4]
        print("Encontrado:")
        mostra_dados(nome, telefone, endereco, cidade, estado)
        nome = pede_nome(nome)  # Se nada for digitado, mantém o valor
        telefone = pede_telefone(telefone)
        endereco = pede_endereco(endereco)
        cidade = pede_cidade(cidade)
        estado = pede_estado(estado)
        if confirma("alteração") == "S":  # Pede confirmação antes de salvar as alterações
            agenda[p] = [nome, telefone, endereco, cidade, estado]
            alterada = True  # Marca que houve alteração
    else:
        print("Nome não encontrado.")

def lista():
    print("\nAgenda\n\n------")  # Lista todos os contatos da agenda
    for posicao, e in enumerate(agenda):  # Usamos a função enumerate para obter a posição na agenda
        print(f"Posição: {posicao} ", end="")  # Imprimimos a posição, sem saltar linha
        mostra_dados(e[0], e[1], e[2], e[3], e[4])
    print("------\n")

def le_ultima_agenda_gravada():
    ultima = ultima_agenda()  # Lê a última agenda que foi gravada no arquivo de controle
    if ultima is not None:
        leia_arquivo(ultima)

def ultima_agenda():
    try:  # Lê o nome do último arquivo de agenda gravado
        with open("ultima_agenda.dat", "r", encoding="utf-8") as arquivo:
            ultima = arquivo.readline().strip()  # Lê o nome do arquivo
    except FileNotFoundError:
        return None  # Se o arquivo não existir, retorna None
    return ultima

def atualiza_ultima(nome):
    with open("ultima_agenda.dat", "w", encoding="utf-8") as arquivo:  # Atualiza o nome do último arquivo de agenda gravado
        arquivo.write(f"{nome}\n")

def leia_arquivo(nome_arquivo):
    global agenda, alterada  # Lê os contatos de um arquivo e carrega na agenda
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        agenda = []
        for l in arquivo.readlines():
            nome, telefone, endereco, cidade, estado = l.strip().split("#")
            agenda.append([nome, telefone, endereco, cidade, estado])
    alterada = False  # Após a leitura, a agenda não está alterada

def le():
    global alterada  # Carrega uma nova agenda a partir de um arquivo
    if alterada:
        print("Você não salvou a lista desde a última alteração. Deseja gravá-la agora?")
        if confirma("gravação") == "S":
            grava()
    print("Ler\n---")
    nome_arquivo = pede_nome_arquivo()
    leia_arquivo(nome_arquivo)
    atualiza_ultima(nome_arquivo)  # Atualiza o nome do último arquivo lido

def ordena():
    global alterada  # Ordena a agenda por nome
    agenda.sort(key=lambda e: e[0])  # Usando o método sort do Python com lambdas para definir a chave de ordenação
    alterada = True

def grava():
    global alterada
    if not alterada:
        print("Você não alterou a lista. Deseja gravá-la mesmo assim?")
        if confirma("gravação") == "N":
            return
    print("Gravar\n------")
    nome_arquivo = pede_nome_arquivo()
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        for e in agenda:
            arquivo.write(f"{e[0]}#{e[1]}#{e[2]}#{e[3]}#{e[4]}\n")
    atualiza_ultima(nome_arquivo)
    alterada = False

def valida_faixa_inteiro(pergunta, inicio, fim):
    while True:
        try:
            valor = int(input(pergunta))
            if inicio <= valor <= fim:
                return valor
        except ValueError:
            print(f"Valor inválido, favor digitar entre {inicio} e {fim}")

def menu():
    print("""
1 - Novo
2 - Altera
3 - Apaga
4 - Lista
5 - Grava
6 - Lê
7 - Ordena por nome
0 - Sai
""")
    print(f"\nNomes na agenda: {len(agenda)} Alterada: {alterada}\n")
    return valida_faixa_inteiro("Escolha uma opção: ", 0, 7)

le_ultima_agenda_gravada()

while True:
    opcao = menu()
    if opcao == 0:
        break
    elif opcao == 1:
        novo()
    elif opcao == 2:
        altera()
    elif opcao == 3:
        apaga()
    elif opcao == 4:
        lista()
    elif opcao == 5:
        grava()
    elif opcao == 6:
        le()
    elif opcao == 7:
        ordena()
