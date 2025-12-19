-- Exemplo de inserts contendo endereços
CREATE TABLE IF NOT EXISTS input_addresses(id INTEGER PRIMARY KEY, address TEXT);
INSERT INTO input_addresses(id, address) VALUES (1, 'Avenida Paulista, 1000, Bela Vista, São Paulo, SP');
INSERT INTO input_addresses(id, address) VALUES (2, 'Rua XV de Novembro, 50, Centro, Curitiba, PR');
INSERT INTO input_addresses(id, address) VALUES (3, 'Praia de Botafogo, 300, Botafogo, Rio de Janeiro, RJ');
