CREATE DATABASE Hamptons;

CREATE TABLE hotel(
    id_hotel INTEGER PRIMARY KEY,
    nome_hotel TEXT NOT NULL,
    estrelas INTEGER NOT NULL CHECK (estrelas >= 1 AND estrelas <= 5),
    endereco TEXT NOT NULL UNIQUE,
    estado VARCHAR(2) NOT NULL CHECK (estado IN('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
                                                'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
                                                'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'))
);

CREATE TABLE quarto(
    numero INTEGER,
    id_hotel INTEGER,
    capacidade INTEGER NOT NULL CHECK (capacidade >= 2 AND capacidade <= 6),
    categoria TEXT NOT NULL CHECK (categoria IN ('Suite simples', 'Suite dupla', 'Presidencial', 'Cobertura')),
    preco NUMERIC(7,2) NOT NULL CHECK (preco >= 150.00 AND preco <= 5000.00),

    PRIMARY KEY(numero, id_hotel),
    FOREIGN KEY (id_hotel) REFERENCES hotel(id_hotel)
);

CREATE TABLE hospede(
    cpf_hospede VARCHAR(11) PRIMARY KEY,
    nome TEXT NOT NULL,
    endereco TEXT NOT NULL,
    estado VARCHAR(2) NOT NULL CHECK (estado IN('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
                                                'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
                                                'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'))
);

CREATE TABLE reserva(
    cpf_hospede VARCHAR(11) NOT NULL,
    numero_quarto INTEGER NOT NULL,
    id_hotel INTEGER NOT NULL,
    data_entrada DATE NOT NULL CHECK(data_entrada > '1999-12-31'),
    data_saida DATE NOT NULL CHECK(data_saida < '2030-01-16'),
    dia_entrada INTEGER NOT NULL,
    mes_entrada INTEGER NOT NULL,
    ano_entrada INTEGER NOT NULL,
    dia_saida INTEGER NOT NULL,
    mes_saida INTEGER NOT NULL,
    ano_saida INTEGER NOT NULL,
    modo_pagamento TEXT NOT NULL CHECK (modo_pagamento IN ('Credito', 'Debito', 'Dinheiro')),

    PRIMARY KEY(numero_quarto, id_hotel, data_entrada),
    FOREIGN KEY(cpf_hospede) REFERENCES hospede(cpf_hospede),
    FOREIGN KEY(numero_quarto, id_hotel) REFERENCES quarto(numero, id_hotel),
    FOREIGN KEY(id_hotel) REFERENCES hotel(id_hotel)
);