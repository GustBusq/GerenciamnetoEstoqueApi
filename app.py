from flask import Flask, jsonify, request
from flask_cors import CORS # Importe a extensão CORS

app = Flask(__name__)
CORS(app) # Habilite o CORS para todas as rotas da sua aplicação

# O resto do seu código permanece o mesmo
# ...
# Seu estoque (uma lista de dicionários)
estoque = []

# Funções de gestão de estoque
def cadastrar_produto(produto, preco, n_estoque):
    produto_estoque = {
        "Nome": produto,
        "Preço": preco,
        "Estoque": n_estoque
    }
    estoque.append(produto_estoque)
    return produto_estoque

def remover_produto(produto_nome):
    for item in estoque:
        if item['Nome'].lower() == produto_nome.lower():
            estoque.remove(item)
            return {"mensagem": f"Produto '{produto_nome}' foi removido."}
    return {"erro": f"Produto '{produto_nome}' não encontrado."}, 404

def atualizar_estoque(produto, estoque_novo):
    for item in estoque:
        if item["Nome"].lower() == produto.lower():
            item['Estoque'] = estoque_novo
            return {"mensagem": f"Quantidade do produto '{produto}' atualizada para {estoque_novo}"}
    return {"erro": f"Produto '{produto}' não encontrado."}, 404

def atualizar_preco(produto, preco_novo):
    for item in estoque:
        if item["Nome"].lower() == produto.lower():
            item['Preço'] = preco_novo
            return {"mensagem": f"O preço do produto '{produto}' atualizada para {preco_novo}"}
    return {"erro": f"Produto '{produto}' não encontrado."}, 404

# --- Rotas da API ---

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    if not estoque:
        return jsonify({"mensagem": "Adicione itens ao estoque primeiro!"})
    return jsonify(estoque)

@app.route('/produtos/cadastrar', methods=['POST'])
def adicionar_produto_api():
    dados = request.get_json()
    if not dados or 'nome' not in dados or 'preco' not in dados or 'estoque' not in dados:
        return jsonify({"erro": "Dados incompletos. 'nome', 'preco' e 'estoque' são obrigatórios."}), 400

    produto_cadastrado = cadastrar_produto(dados['nome'], dados['preco'], dados['estoque'])
    return jsonify(produto_cadastrado), 201

@app.route('/produtos/<nome_produto>', methods=['DELETE'])
def remover_produto_api(nome_produto):
    resultado = remover_produto(nome_produto)
    if isinstance(resultado, tuple):
        return jsonify(resultado[0]), resultado[1]
    return jsonify(resultado)

@app.route('/produtos/atualizar_estoque/<nome_produto>', methods=['PUT'])
def atualizar_estoque_api(nome_produto):
    dados = request.get_json()
    if 'estoque' not in dados:
        return jsonify({"erro": "O campo 'estoque' é obrigatório para a atualização."}), 400

    resultado = atualizar_estoque(nome_produto, dados['estoque'])
    if isinstance(resultado, tuple):
        return jsonify(resultado[0]), resultado[1]
    return jsonify(resultado)

@app.route('/produtos/atualizar_preco/<nome_produto>', methods=['PUT'])
def atualizar_preco_api(nome_produto):
    dados = request.get_json()
    if 'preco' not in dados:
        return jsonify({"erro": "O campo 'preco' é obrigatório para a atualização."}), 400

    resultado = atualizar_preco(nome_produto, dados['preco'])
    if isinstance(resultado, tuple):
        return jsonify(resultado[0]), resultado[1]
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)