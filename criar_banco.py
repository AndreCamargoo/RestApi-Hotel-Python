import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()

tabela = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY, \
    nome text, estrelas real, diaria real, cidade text)"
    
cria_hotel = "INSERT INTO hoteis VALUES ('alpha', 'Alpha', 4.3, \
    345.30, 'Araçatuba')"
    
cursor.execute(tabela)
cursor.execute(cria_hotel)

connection.commit()
connection.close()