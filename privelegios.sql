-- Criação do usuario que será o perfil administrador do banco de dados
CREATE USER administrador WITH PASSWORD 'vyv$q#TqPY2UTFoX' CREATEDB CREATEROLE;

-- Alterando o dono do banco de dados ja existente para o perfil administrador
set role postgres;
ALTER DATABASE hamptons OWNER TO administrador;

set role postgres; -- dono das tabelas
-- privilegios administrador
GRANT ALL PRIVILEGES ON TABLE hotel TO administrador WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON TABLE quarto TO administrador WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON TABLE hospede TO administrador WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON TABLE reserva TO administrador WITH GRANT OPTION;