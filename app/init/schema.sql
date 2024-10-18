DROP TABLE users;
DROP TABLE empresas;
DROP TABLE produtos;
DROP TABLE pedidos;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    create_at TIMESTAMP,
    userpassword VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS empresas (
    id SERIAL PRIMARY KEY,
    owner_email VARCHAR(255) NOT NULL,
    data_created TIMESTAMP,
    cnpj VARCHAR(255)NOT NULL,
    superadmin BOOLEAN NOT NULL,
    owner_password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS produtos (
    id SERIAL PRIMARY KEY,
    produto_nome VARCHAR(255) NOT NULL,
    produto_preco FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    pedido_nome VARCHAR(255) NOT NULL,
    data_create TIMESTAMP,
    status_pedido INT NOT NULL,
    frete FLOAT NOT NULL,
    custo_total FLOAT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);