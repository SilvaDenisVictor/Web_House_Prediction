
ALTER DATABASE houses_db SET datestyle TO SQL, DMY;
SET datestyle TO SQL, DMY;

CREATE TABLE IF NOT EXISTS House(
    id SERIAL PRIMARY KEY,
    preco DECIMAL,
    iptu DECIMAL,
    condominio DECIMAL,
    metro_quadrado DECIMAL,
    quarto DECIMAL,
    banheiro DECIMAL,
    garagem DECIMAL,
    regiao VARCHAR(100),
    data DATE,
    vendedor CHAR(20),
    descricao VARCHAR(500)
);

COPY House(preco, iptu, condominio, metro_quadrado, quarto, banheiro, garagem, regiao, data, vendedor, descricao)
FROM '/casas.csv'
DELIMITER ';'
CSV HEADER;