-- VERIFICAR DATA | atributo da tabela reserva
CREATE OR REPLACE FUNCTION verificacao_data() RETURNS TRIGGER AS $$
BEGIN
    IF EXTRACT(DAY FROM NEW.data_entrada) <> NEW.dia_entrada THEN
        RAISE EXCEPTION 'O valor do campo dia_entrada não corresponde ao dia da data_entrada';
    END IF;
    IF EXTRACT(MONTH FROM NEW.data_entrada) <> NEW.mes_entrada THEN
        RAISE EXCEPTION 'O valor do campo mes_entrada não corresponde ao mes da data_entrada';
    END IF;
    IF EXTRACT(YEAR FROM NEW.data_entrada) <> NEW.ano_entrada THEN
        RAISE EXCEPTION 'O valor do campo ano_entrada não corresponde ao ano da data_entrada';
    END IF;

    IF EXTRACT(DAY FROM NEW.data_saida) <> NEW.dia_saida THEN
        RAISE EXCEPTION 'O valor do campo dia_saida não corresponde ao dia da data_saida';
    END IF;
    IF EXTRACT(MONTH FROM NEW.data_saida) <> NEW.mes_saida THEN
        RAISE EXCEPTION 'O valor do campo mes_saida não corresponde ao mes da data_saida';
    END IF;
    IF EXTRACT(YEAR FROM NEW.data_saida) <> NEW.ano_saida THEN
        RAISE EXCEPTION 'O valor do campo ano_saida não corresponde ao ano da data_saida';
    END IF;

    IF NEW.data_saida < NEW.data_entrada THEN
        RAISE EXCEPTION 'A data de saída deve ser posterior à data de entrada';
    END IF;

    IF NEW.data_saida > NEW.data_entrada + INTERVAL '16 days' THEN
        RAISE EXCEPTION 'A diferença entre a data de saída e a data de entrada não pode ser maior do que 1 ano';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_verificacao_data
BEFORE INSERT ON reserva
FOR EACH ROW
EXECUTE FUNCTION verificacao_data();

-- VERIFICAR SE UM QUARTO JÁ NÃO ESTÁ OCUPADO PARA RESERVAR | tabela reserva 
CREATE OR REPLACE FUNCTION verificacao_quarto_ocupado() RETURNS TRIGGER AS $$
DECLARE
    qtd_reservas INTEGER;
BEGIN
    SELECT COUNT(*) INTO qtd_reservas
    FROM reserva
    WHERE numero_quarto = NEW.numero_quarto AND id_hotel = NEW.id_hotel
        AND (NEW.data_entrada, NEW.data_saida) OVERLAPS (data_entrada, data_saida)
        AND cpf_hospede <> NEW.cpf_hospede;

    IF qtd_reservas > 0 THEN
        RAISE EXCEPTION 'O quarto já está reservado durante o mesmo período.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_verificar_quarto_disponivel
BEFORE INSERT ON reserva
FOR EACH ROW
EXECUTE FUNCTION verificacao_quarto_ocupado();

-- VERIFICAR SE O ENDEREÇO DE HOSPEDE NÃO É UM ENDEREÇO DE UM HOTEL | tabela hotel e tabela hospede
CREATE OR REPLACE FUNCTION verificar_endereco_hospede()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.endereco in (
        SELECT endereco
        FROM hotel
    ) THEN
        RAISE EXCEPTION 'O endereço do hóspede não pode ser igual ao endereço de algum hotel.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_verificar_endereco_hospede
BEFORE INSERT OR UPDATE ON hospede
FOR EACH ROW
EXECUTE FUNCTION verificar_endereco_hospede();