DELETE FROM clients;
DROP TABLE sales;

CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    FOREIGN KEY(client_id) REFERENCES clients(id)
);