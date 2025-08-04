import os
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Conexão com o banco
wordpress_bd = mysql.connector.connect(
    host='SEU_HOST',
    user='SEU_USUARIO',
    password='SUA_SENHA',
    port=3306,
    database='SEU_BANCO'
)
cursor = wordpress_bd.cursor()

@app.route('/inserir_dados', methods=['POST'])
def inserir_dados():
    try:
        dados_json = request.get_json()
        if not all(k in dados_json for k in ['nome', 'email', 'telefone', 'cnpj']):
            return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

        sql = "INSERT INTO leads (nome, email, telefone, cnpj) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (
            dados_json['nome'],
            dados_json['email'],
            dados_json['telefone'],
            dados_json['cnpj']
        ))
        wordpress_bd.commit()
        return jsonify({'mensagem': 'Dados inseridos com sucesso!'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # 👈 usa a porta definida pelo Render
    app.run(host='0.0.0.0', port=port)
