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

# Inserção de hospedes
cpfs_gerados = []

def gerar_cpfs_unicos():
    cpf = ''.join(str(random.randint(0, 9)) for _ in range(11)) 
    while cpf in cpfs_gerados:
        cpf = ''.join(str(random.randint(0, 9)) for _ in range(11))
    cpfs_gerados.append(cpf)
    return cpf

estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
           'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
           'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

i = 0
while i < 500000:
    cpf_hospede = gerar_cpfs_unicos() 
    nome = fake.name()
    estado = random.choice(estados)
    endereco_hospede = endereco_hospede = f"{fake.street_name()}, {random.randint(101, 1850)} / {fake.city()} - {estado} , Brasil"#f"{fake.address()}, Brasil"
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO hospede (cpf_hospede, nome, endereco, estado) VALUES (%s, %s, %s, %s)", (cpf_hospede, nome,  endereco_hospede, estado)) 
        cursor.close()
        print(f"Inserção hospede {i} concluída.")
        conn.commit()
        i += 1
    except psycopg2.DatabaseError as e:
        # Captura a exceção e imprime a mensagem de erro, mas continua o loop
        print(f"Erro durante a inserção {i}: {e}")
        conn.rollback()

# Fechar a conexão com o banco de dados
conn.close()