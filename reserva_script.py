import psycopg2 # Para se conectar ao banco de dados e realizar inserções na tabela 
import random
from datetime import date, timedelta
from faker import Faker
fake = Faker('pt_BR')

# Criação da conexão com o pgAdmin
conn = psycopg2.connect(
    host="localhost",  # ou o endereço IP do servidor
    port="5432",  # porta padrão do PostgreSQL
    database="teste2",
    user="postgres",
    password="labbd"
)    

# Inserção de reservas
""" Função para saber se o ano eh bissexto """
def eh_bissexto(ano):
    if ano % 400 == 0:
        return True
    if ano % 100 == 0:
        return False
    if ano % 4 == 0:
        return True
    return False

""" Função para gerar as datas de entrada e saida """
def gerar_datas():
    ano_min = 2000
    ano_max = 2029
    dias_por_mes = [
        31,  # Janeiro
        28,  # Fevereiro (considerando não bissexto)
        31,  # Março
        30,  # Abril
        31,  # Maio
        30,  # Junho
        31,  # Julho
        31,  # Agosto
        30,  # Setembro
        31,  # Outubro
        30,  # Novembro
        31   # Dezembro
    ]

    ano_entrada = random.randint(ano_min, ano_max)
    mes_entrada = random.randint(1, 12)
    ultimo_dia_mes_entrada = dias_por_mes[mes_entrada - 1]
    if mes_entrada == 2 and eh_bissexto(ano_entrada):
        ultimo_dia_mes_entrada = 29
    dia_entrada = random.randint(1, ultimo_dia_mes_entrada)
    data_entrada = date(ano_entrada, mes_entrada, dia_entrada)

    delta = timedelta(days=random.randint(1, 15))
    data_saida = data_entrada + delta
    return data_entrada, data_saida
    
def obter_cpfs_existentes():
    cursor = conn.cursor()
    cursor.execute("SELECT cpf_hospede FROM hospede")
    cpfs_existentes = cursor.fetchall()
    cursor.close()
    return cpfs_existentes

def obter_hoteis_existentes():
    cursor = conn.cursor()
    cursor.execute("SELECT id_hotel FROM hotel ORDER BY id_hotel")
    hoteis_existentes = cursor.fetchall()
    cursor.close()
    return hoteis_existentes

cpfs_disponiveis = obter_cpfs_existentes()
hoteis_disponiveis = obter_hoteis_existentes()

i = 0
while i < 200000:
    cpf_hospede = random.choice(cpfs_disponiveis)[0]

    data_entrada, data_saida = gerar_datas()
    dia_entrada = data_entrada.day
    mes_entrada = data_entrada.month
    ano_entrada = data_entrada.year
    dia_saida = data_saida.day
    mes_saida = data_saida.month
    ano_saida = data_saida.year
    
    numero_quarto = random.choice([100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1100])
    id_hotel = random.choice(hoteis_disponiveis)[0]
    #registros_quarto = obter_quartos_disponiveis(data_entrada, data_saida)
    #id_hotel, numero_quarto = random.choice(registros_quarto)

    modo_pagamento = random.choice(['Credito', 'Debito', 'Dinheiro'])
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reserva (cpf_hospede, numero_quarto, id_hotel, data_entrada, data_saida, dia_entrada, mes_entrada, ano_entrada, dia_saida, mes_saida, ano_saida, modo_pagamento) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s)", (cpf_hospede, numero_quarto, id_hotel, data_entrada, data_saida, dia_entrada, mes_entrada, ano_entrada, dia_saida, mes_saida, ano_saida, modo_pagamento))
        cursor.close()
        print(f"Inserção reserva {i} concluída.")
        conn.commit()
        i += 1
    except psycopg2.DatabaseError as e:
        # Captura a exceção e imprime a mensagem de erro, mas continua o loop
        print(f"Erro durante a inserção {i}: {e}")
        conn.rollback()

# Fechar a conexão com o banco de dados
conn.close()