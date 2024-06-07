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

# Inserção de quartos
cur = conn.cursor()
cur.execute("SELECT id_hotel FROM hotel")
hotels = cur.fetchall()

for hotel in hotels: # vai preencher os quartos por hotel
    id_hotel = hotel[0]
    andar = 100
    for i in range(0, 101): # (0, numero de quartos por hotel)
        if(i == 0):
            numero = 100
        elif(i % 10 == 0):
            numero = numero - 9 + 100
            andar = andar + 100
        else:
            numero = numero + 1

        if(numero == 1100):
            categoria = 'Cobertura'
        else:
            categoria = random.choice(['Suite simples', 'Suite dupla', 'Presidencial'])

        if(categoria == 'Suite simples'):
            preco = round(random.uniform(150.00, 500.00), 2)
            capacidade = 2
        elif(categoria == 'Suite dupla'):
            preco = round(random.uniform(500.00, 1200.00), 2)
            capacidade = random.randint(3, 4)
        elif(categoria == 'Presidencial'):
            preco = round(random.uniform(1200.00, 3000.00), 2)
            capacidade = random.randint(4, 6)
        elif(categoria == 'Cobertura'):
            preco = round(random.uniform(3000.00, 5000.00), 2)
            capacidade = random.randint(2, 6)   
        cursor = conn.cursor()
        cursor.execute("INSERT INTO quarto (numero, id_hotel, capacidade, categoria, preco) VALUES (%s, %s, %s, %s, %s)", (numero, id_hotel, capacidade, categoria, preco))
        cursor.close()   
        print(f"Inserção quarto {i} concluída para o hotel com ID {id_hotel}.")
        conn.commit() 


cur.close()     
# Fechar a conexão com o banco de dados
conn.close()