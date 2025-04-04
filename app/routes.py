from flask import request, jsonify
from .database import db
from .models import Cliente, Funcionario, Loja, FormaPagamento, Venda, Produto, Categoria

def register_routes(app):
    
    # Rota de teste
    @app.route("/")
    def index():
        return jsonify({"mensagem": "API de vendas rodando!"})


    #### CLIENTES ####
    @app.route("/clientes", methods=["GET"])
    def listar_clientes():
        clientes = Cliente.query.all()
        return jsonify([{"id": c.id, "nome_completo": c.nome_completo, "email": c.email, "rg": c.rg} for c in clientes])

    @app.route("/clientes", methods=["POST"])
    def criar_cliente():
        dados = request.json
        novo_cliente = Cliente(
            nome_completo=dados["nome_completo"],
            email=dados["email"],
            rg=dados["rg"]
        )
        novo_cliente.set_senha(dados["senha"])  # Hash da senha
        db.session.add(novo_cliente)
        db.session.commit()
        return jsonify({"mensagem": "Cliente criado com sucesso!"}), 201


    #### FUNCIONÁRIOS ####
    @app.route("/funcionarios", methods=["GET"])
    def listar_funcionarios():
        funcionarios = Funcionario.query.all()
        return jsonify([{"id": f.id, "nome_completo": f.nome_completo, "cargo": f.cargo, "email": f.email, "rg": f.rg} for f in funcionarios])

    @app.route("/funcionarios", methods=["POST"])
    def criar_funcionario():
        dados = request.json
        novo_funcionario = Funcionario(
            nome_completo=dados["nome_completo"],
            cargo=dados["cargo"],
            email=dados["email"],
            rg=dados["rg"]
        )
        novo_funcionario.set_senha(dados["senha"])  # Hash da senha
        db.session.add(novo_funcionario)
        db.session.commit()
        return jsonify({"mensagem": "Funcionário criado com sucesso!"}), 201

    
    #### CATEGORIAS ####
    @app.route("/categorias", methods=["GET"])
    def listar_categoria():
        categorias =Categoria.query.all()
        return jsonify([{
            "id": c.id, "nome": c.nome} for c in categorias])

    @app.route("/categorias", methods=["POST"])
    def criar_categoria():
        dados = request.json
        nova_categoria =Categoria(
            nome=dados["nome"]
        )
        db.session.add(nova_categoria)
        db.session.commit()
        return jsonify({"mensagem": "Categoria criada com sucesso!"}), 201


    #### PRODUTOS ####
    @app.route("/produtos", methods=["GET"])
    def listar_produtos():
        produtos = Produto.query.all()
        return jsonify([{
            "id": p.id, "nome": p.nome, 
            "descricao": p.descricao, "preco": p.preco,
            "estoque": p.estoque} 
            for p in produtos])

    @app.route("/produtos", methods=["POST"])
    def criar_produto():
        dados = request.json
        novo_produto = Produto(
            nome=dados["nome"],
            descricao=dados["descricao"],
            preco=dados["preco"],
            estoque=dados["estoque"]
        )
        db.session.add(novo_produto)
        db.session.commit()
        return jsonify({"mensagem": "Funcionário criado com sucesso!"}), 201


    #### LOJAS ####
    @app.route("/lojas", methods=["GET"])
    def listar_lojas():
        lojas = Loja.query.all()
        return jsonify([{"id": l.id, "cidade": l.cidade, "estado": l.estado} for l in lojas])

    @app.route("/lojas", methods=["POST"])
    def criar_loja():
        dados = request.json
        nova_loja = Loja(
            cidade=dados["cidade"],
            estado=dados["estado"]
        )
        db.session.add(nova_loja)
        db.session.commit()
        return jsonify({"mensagem": "Loja criada com sucesso!"}), 201


    #### FORMAS DE PAGAMENTO ####
    @app.route("/formas_pagamento", methods=["GET"])
    def listar_formas_pagamento():
        formas = FormaPagamento.query.all()
        return jsonify([{"id": f.id, "tipo_pagamento": f.tipo_pagamento} for f in formas])

    @app.route("/formas_pagamento", methods=["POST"])
    def criar_forma_pagamento():
        dados = request.json
        nova_forma = FormaPagamento(tipo_pagamento=dados["tipo_pagamento"])
        db.session.add(nova_forma)
        db.session.commit()
        return jsonify({"mensagem": "Forma de pagamento criada com sucesso!"}), 201


    #### VENDAS ####
    @app.route("/vendas", methods=["GET"])
    def listar_vendas():
        vendas = Venda.query.all()
        return jsonify([
            {
                "id": v.id,
                "cliente_id": v.cliente_id,
                "funcionario_id": v.funcionario_id,
                "loja_id": v.loja_id,
                "forma_pagamento_id": v.forma_pagamento_id,
                "valor_total": v.valor_total,
                "data_venda": v.data_venda
            }
            for v in vendas
        ])

    @app.route("/vendas", methods=["POST"])
    def criar_venda():
        dados = request.json
        nova_venda = Venda(
            cliente_id=dados["cliente_id"],
            funcionario_id=dados["funcionario_id"],
            loja_id=dados["loja_id"],
            forma_pagamento_id=dados["forma_pagamento_id"],
            valor_total=dados["valor_total"]
        )
        db.session.add(nova_venda)
        db.session.commit()
        return jsonify({"mensagem": "Venda registrada com sucesso!"}), 201
