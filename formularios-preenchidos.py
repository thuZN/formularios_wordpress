# Banco de Dados
import mysql.connector
from flask import Flask, request, jsonify

# Conexão com o banco
wordpress_bd = mysql.connector.connect(
    host='localhost',
    user='root',
    port=3307,
    password='',
    database='formularios_wordpress'
)

cursor = wordpress_bd.cursor()

# API Flask
app = Flask(__name__)

@app.route('/inserir_dados', methods=['POST'])
def inserir_dados():
    try:
        dados_json = request.get_json()

        # Validação dos campos obrigatórios
        if not all(k in dados_json for k in ['nome', 'email', 'telefone', 'cnpj']):
            return jsonify({'erro': 'Campos nome, email, telefone e cnpj são obrigatórios.'}), 400

        nome = dados_json['nome']
        email = dados_json['email']
        telefone = dados_json['telefone']
        cnpj = dados_json['cnpj']

        # Inserção no banco
        sql = "INSERT INTO leads (nome, email, telefone, cnpj) VALUES (%s, %s, %s, %s)"
        valores = (nome, email, telefone, cnpj)
        cursor.execute(sql, valores)
        wordpress_bd.commit()

        return jsonify({'mensagem': 'Dados inseridos com sucesso!'}), 200

    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# Rodar localmente
if __name__ == '__main__':
    app.run(debug=True)
