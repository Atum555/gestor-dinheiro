from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import pandas as pd
import os
import time

# ---- Banco de dados  ----

Base = declarative_base()

class Banco(Base):
    __tablename__ = 'banco'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    idade = Column(Integer)
    senha = Column(String)


class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    id_conta = Column(Integer)
    valor = Column(Float)
    tipo = Column(String)
    categoria = Column(String)
    descricao = Column(String)
    data = Column(String)  

class Emails_bloqueado(Base):
    __tablename__ = 'emails_bloqueado' 
    id = Column(Integer, primary_key=True)
    email = Column(String)
    idade = Column(String)

engine = create_engine("sqlite:///gestor.db")
Base.metadata.create_all(engine)      

Session = sessionmaker(bind=engine)
sessao = Session()

# ---- Codigo  aussilair ----

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def continuar(print_continuar, apagar=True):
    while True:
        if apagar:
            limpar()
        print(print_continuar)
        resposta = input("Continuar [Y]:  ").upper()
        if resposta != "Y":
            print("\n---- ESCOLHA INDESPONIVEL -----\n")
            continue
        return 
    
def pedir_idade(nome, email):
    while True:
        idade_conta = input("Digite sua idade: ")
        try:
            return int(idade_conta)
        except ValueError:
            continuar("\n---- SUA IDADE NÃO É UM NUMERO ----\n")
            limpar()
            print(f"---- CRIAR CONTA ----\nDigite o seu nome: {nome}\nDigite seu email: {email}")

def verificar(email_conta):
    email_verificacao = sessao.query(Banco).filter_by(email=email_conta).first()

    if email_verificacao is not None:
        continuar("\n---- ESSE EMAIL JÁ ESTA ASSUCIADO A UMA CONTA ----\n")
        return True
    return False

def idade_insufeciente(email_bloqueado, idade_insufeciente):
    email_procura = sessao.query(Emails_bloqueado).filter_by(email=email_bloqueado).first()
    if email_procura is None and idade_insufeciente >= 18:
        return False
    
    if email_procura is None:
        continuar("\n---- NÃO TENS IDADE SUFECIENTE ----\n")
        p = Emails_bloqueado(email=email_bloqueado, idade=idade_insufeciente)
        sessao.add(p)
        sessao.commit()
    else:
        print(f"\n---- IDADE FALSA ----") 
    return True

def continuar_criar_conta():
    while True:
        try:
            escolha_continuar = int(input("\n1. Continuar\n2. Refazer\n3. Sair\nEscolha: "))
        except ValueError:
            print("\n---- ISSO NÃO É UM NUMERO ----")
            continue
        if escolha_continuar not in [1, 2, 3]:
            print("\n---- ESCOLHA ÍNDESPONIVEL ----")
            continue
        return escolha_continuar

def continuar_iniciar_sessao():
    while True:
        limpar()
        print("\n---- EMAIL OU SENHA INCORRETO ----")
        try:
            escolha = int(input("1. Tentar novamente\n2. Criar conta\nEscolha: "))
        except ValueError:
            continuar("\n---- ISSO NÃO É UM NUMERO ----\n")
            continue
        if escolha not in [1, 2]:
            continuar("\n---- ESCOLHA ÍNDESPONIVEL ----\n")
            continue
        return escolha
    
def verificar_valor_escolha(valor_escolha1, data_escolha1):
    global valor_escolha, data_escolha
    try:
        valor_escolha = float(valor_escolha1)
        data_escolha = int(data_escolha1)
    except ValueError:
        continuar("\n---- VALOR OU ESCOOLHA NÃO SÃO NUMEROS ----\n")
        return True
    return False

def adicionar_movimento_erro():
    while True:
        try:
            escolha_erro = int(input("1. Refazer tudo\n2. Sair\nEscolha: "))
        except ValueError:
            continuar("\n---- ISSO NÃO É UM NUMERO ----\n")
            continue
        if escolha_erro not in [1, 2]:
            continuar("\n---- ESCOLHA ÍNDESPONIVEL ----\n")
            continue
        return escolha_erro
    
def tipo():
    while True:
        tipo_escolha = input("Digite o Tipo ['Gasto' ou 'Reccebido']: ").strip().title()
        if tipo_escolha not in ['Gasto', 'Recebido']:
            continuar("\n---- NÃO ESTA NAS OPÇÕES ----\n")
            limpar()
            continue
        return tipo_escolha

# ---- Codigo principal ----

def menu_inicial():
    global sessao_iniciada
    while True:
        limpar()
        print("\n---- MENU INICIAL ----")
        try:
            escolha_inicial = int(input("1. Criar conta\n2. Iniciar sessão\n3. Sair\nEscolha: "))
        except ValueError:
            continuar("\n---- ISSO NÃO É UM NUMERO ----\n")
            continue
        if escolha_inicial not in [1, 2, 3]:
            continuar("\n---- ESCOLHA INDESPONIVEL -----\n")
            continue

        if escolha_inicial == 1:
            while True:
                limpar()
                print("\n---- CRIAR CONTA ----")
                nome_conta = input("Digite o seu nome: ").strip().title()
                email_conta = input("Digite seu email: ").strip()
                idade_conta = pedir_idade(nome=nome_conta, email=email_conta)
                senha_conta = input("Digite sua senha: ").strip()

                email_verificacao = verificar(email_conta)
                nao_pode_criar_conta = idade_insufeciente(email_bloqueado=email_conta, idade_insufeciente=idade_conta)
                
                if nao_pode_criar_conta or email_verificacao:
                    continue
                
                escolha_continuar = continuar_criar_conta()
                if escolha_continuar == 2:
                    continue
                elif escolha_continuar == 3:
                    return

                p = Banco(nome=nome_conta, email=email_conta, idade=idade_conta, senha=senha_conta)
                sessao.add(p)
                sessao.commit() 
                limpar()
                print("\n---- CONTA CRIADA COM SUCESSO ----")
                time.sleep(1)
                return
            
        elif escolha_inicial == 2:
            while True:
                limpar()
                print("\n---- INICIAR SESSÃO ----")
                email_conta = input("Digite seu email: ").strip()
                senha_conta = input("Digite sua senha: ").strip()

                procura = sessao.query(Banco).filter_by(email=email_conta, senha=senha_conta).first()
            
                if procura is None:
                    resultado = continuar_iniciar_sessao()
                    if resultado == 1:
                        continue
                    else:
                        return
                else:
                    sessao_iniciada = True
                    return procura
                
        elif escolha_inicial == 3:
            limpar()
            print("\n---------- ADEUS ----------\n")
            return escolha_inicial
        else:
            continuar("\n---- ESCOLHA ÍNDESPONIVEL ----\n")
            continue

def menu(utilizador):
    global sessao_iniciada
    while True:
        limpar()
        print("\n---- MENU ----")
        try:
            escolha = int(input("1. Adicionar um movimento\n2. Ver todos os movimentos\n3. Ver quanto gasto por categoria\n4. Terminar sessão\nEscolha: "))
        except ValueError:
            continuar("\n---- ESCOLHA ÍNDESPONIVEL ----\n")
            return
        if escolha not in [1, 2, 3, 4]:
            continuar("\n---- ESCOLHA ÍNDESPONIVEL ----\n")
            return
        
        if escolha == 1:
            while True:
                limpar()
                print("\n---- ADICIONAR MOVIMENTO ----")
                valor_escolha = input("Digite o Valor: ")
                tipo_escolha = tipo()
                categoria_escolha = input("Digite a Categoria: ").strip().title()
                descricao_escolha = input("Digite a Descrição: ").strip().title()
                data_escolha = input("Data da ação (Exemplo[22062025]): ")

                resultado = verificar_valor_escolha(valor_escolha1=valor_escolha, data_escolha1=data_escolha)
        
                if resultado:
                    resultado2 = adicionar_movimento_erro()
                    if resultado2 == 1:
                        continue
                    else:
                        return
            
                p = Cliente(id_conta=utilizador.id, valor=valor_escolha, tipo=tipo_escolha, categoria=categoria_escolha, descricao=descricao_escolha, data=data_escolha)
                sessao.add(p)
                sessao.commit()
                continuar("\n---- MOVIMENTO ADICIONADO COM SUCESSO ----")
                return
        
        elif escolha == 2:
            limpar()
            numero = 0
            cliente = sessao.query(Cliente).filter_by(id_conta=utilizador.id).all()
            if not cliente:
                continuar("\n---- NENHUMA COMPRA ASSOCIADA NA SUA CONTA ----\n")
                continue
            for compra in cliente:
                numero += 1
                formato = str(compra.data)
                print(f"---- COMPRA {numero} ----")
                print(f"Valor: {compra.valor}\nTipo: {compra.tipo}\nCategoria: {compra.categoria}\nDescrição: {compra.descricao}\nData: {formato[0:2]}-{formato[2:4]}-{formato[4:]}\n")

            continuar("\n---- DESEJA CONTINUAR ----\n", False)
            continue

        elif escolha == 3:
            df = pd.read_sql(f"SELECT * FROM cliente WHERE id_conta = {utilizador.id}", engine)
            df_gastos = df[df['tipo'] == 'Gasto']

            if df_gastos.empty:
                continuar("\n---- NENHUM GASTO NA SUA CONTA ----\n")
                continue

            por_categoria = df_gastos.groupby("categoria")["valor"].sum()

            por_categoria = df_gastos.groupby("categoria")["valor"].sum()
            print("\n---- GASTOS POR CATEGORIA ----")
            print(por_categoria)
            continuar("\n---- DESEJA CONTINUAR ----\n")
            continue

        elif escolha == 4:
            sessao_iniciada = False
            continuar("\n---- SESSÃO TERMINADA COM SUCESSO ----\n")
            return

# ---- INICIO -----

sessao_iniciada = False

while True:
    if sessao_iniciada is False:
        utilizador = menu_inicial()
        if utilizador == 3:
            break
    menu(utilizador)
    