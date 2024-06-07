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

# Inserção de hoteis
numeros_gerados = []
enderecos_hoteis = []
parte1 = ['Bela', 'Grande', 'Maria', 'Golden', 'Boutique', 'Charmosa', 'Relaxante', 'Serena', 'Graciosa', 'Santa', 'Pequena', 'Lorde']
parte2 = ['Vista', 'Lua', 'Mar', 'Montanha', 'Nascente', 'Azul', 'Natureza', 'Fonte', 'Esmeralda', 'Prata', 'Dourada', 'Paradise', 'Scarpelli', 'Village', 'Montenegro','Montecarlo', 'Del Rey', 'Martinez', 'Carter', 'Oasis', 'Devonne', 'De Angelis','Thompson', 'Rodriguez', "O'Connel", 'Lee', 'Cabello', 'Uchis', 'Ocean']

def gerar_numeros_unicos():
    num = random.randint(100, 999)  
    while num in numeros_gerados:
        num = random.randint(100, 999)  
    numeros_gerados.append(num)
    return num

estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
           'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
           'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

cursor = conn.cursor()

for i in range(0, 100):
    id_hotel = gerar_numeros_unicos()
    nome_hotel = f"Hamptons " + random.choice(parte1) + " " + random.choice(parte2)
    estrelas = random.randint(1, 5) 
    estado = random.choice(estados)
    endereco = f"{fake.street_name()}, {random.randint(101, 1850)} / {fake.city()} - {estado} , Brasil"#f"{fake.address()}, Brasil"
    enderecos_hoteis.append(endereco)
    cursor.execute("INSERT INTO hotel (id_hotel, nome_hotel, estrelas, endereco, estado) VALUES (%s, %s, %s, %s, %s)", (id_hotel, nome_hotel, estrelas, endereco, estado))
    print(f"Inserção Hotel {i} concluída.")
    conn.commit()


cursor.close()
# Fechar a conexão com o banco de dados
conn.close()