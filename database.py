import sqlite3

# Função para conectar ao banco
def conectar():
    return sqlite3.connect('pontos.db')

# Função para criar a tabela (se não existir ainda)
def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pontos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jogador TEXT,
            pontos INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Função para adicionar um ponto
def adicionar_ponto(jogador):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pontos (jogador, pontos) VALUES (?, ?)', (jogador, 1))
    conn.commit()
    conn.close()

# Função para buscar todos os pontos
def buscar_pontos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT jogador, COUNT(*) FROM pontos GROUP BY jogador')
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# Função para deletar todos os pontos
def resetar_pontos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pontos')
    conn.commit()
    conn.close()
