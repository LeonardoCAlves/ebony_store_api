import random
from faker import Faker
from app.database import db
from app import create_app
from app.models import Cliente, Funcionario, Loja, FormaPagamento, Categoria, Produto, Venda, VendaProduto

fake = Faker("pt_BR")

app = create_app()

def seed():
    with app.app_context():
        print("🧹 Limpando tabelas...")
        db.drop_all()
        db.create_all()

        # Criando lojas
        print("🏬 Criando lojas...")
        lojas = []
        for _ in range(5):
            loja = Loja(cidade=fake.city(), estado=fake.estado_sigla())
            lojas.append(loja)
            db.session.add(loja)
        db.session.commit()

        # Criando clientes
        print("👥 Criando clientes...")
        clientes = []
        for _ in range(20):
            cliente = Cliente(
                nome_completo=fake.name(),
                email=fake.unique.email(),
                rg=fake.unique.numerify("########")
            )
            cliente.set_senha("senha123")  # Definir senha corretamente
            clientes.append(cliente)
            db.session.add(cliente)
        db.session.commit()

        # Criando funcionários
        print("👔 Criando funcionários...")
        cargos = ["vendedor", "vendedor", "vendedor", "gerente", "estoquista"]
        funcionarios = []
        for cargo in cargos:
            funcionario = Funcionario(
                nome_completo=fake.name(),
                cargo=cargo,
                email=fake.unique.email(),
                rg=fake.unique.numerify("########")
            )
            funcionario.set_senha("senha123")
            funcionarios.append(funcionario)
            db.session.add(funcionario)
        db.session.commit()

        # Criando formas de pagamento
        print("💳 Criando formas de pagamento...")
        tipos_pagamento = ["Crédito", "Débito", "Dinheiro", "PIX"]
        formas_pagamento = []
        for tipo in tipos_pagamento:
            fp = FormaPagamento(tipo_pagamento=tipo)
            formas_pagamento.append(fp)
            db.session.add(fp)
        db.session.commit()

        # Criando categorias
        print("📂 Criando categorias...")
        categorias_nomes = ["Vestimenta", "Eletrônicos", "Celulares", "Calçados", "Acessórios"]
        categorias = []
        for nome in categorias_nomes:
            categoria = Categoria(nome=nome)
            categorias.append(categoria)
            db.session.add(categoria)
        db.session.commit()

        # Mapear descrições por categoria
        descricoes_por_categoria = {
            "Vestimenta": "Camisa polo de algodão macio, ideal para qualquer ocasião.",
            "Eletrônicos": "Fone de ouvido Bluetooth com cancelamento de ruído e bateria de longa duração.",
            "Celulares": "Smartphone com tela AMOLED de 6.5' e câmera tripla de 64MP.",
            "Calçados": "Tênis de corrida ultraleve com amortecimento para máximo conforto.",
            "Acessórios": "Óculos de sol com proteção UV e armação resistente."
        }

        # Criando produtos
        print("📦 Criando produtos...")
        produtos = []
        for categoria in categorias:
            for _ in range(10):  # Criar 10 produtos por categoria
                produto = Produto(
                    nome=fake.unique.word().capitalize(),
                    descricao=descricoes_por_categoria.get(categoria.nome, "Produto de alta qualidade."),
                    preco=round(random.uniform(10, 1000), 2),
                    estoque=random.randint(10, 100),
                    categoria_id=categoria.id
                )
                produtos.append(produto)
                db.session.add(produto)
        db.session.commit()

        # Criando vendas
        print("🧾 Criando vendas com produtos...")
        clientes = Cliente.query.all()
        funcionarios = Funcionario.query.filter(Funcionario.cargo == "vendedor").all()
        lojas = Loja.query.all()
        formas_pagamento = FormaPagamento.query.all()
        produtos = Produto.query.all()

        for _ in range(100):
            cliente = random.choice(clientes)
            funcionario = random.choice(funcionarios)
            loja = random.choice(lojas)
            forma_pagamento = random.choice(formas_pagamento)

            venda = Venda(
                cliente_id=cliente.id,
                funcionario_id=funcionario.id,
                loja_id=loja.id,
                forma_pagamento_id=forma_pagamento.id,
                valor_total=0.0  # atualizado depois
            )
            db.session.add(venda)
            db.session.flush()  # gera venda.id

            total = 0.0
            num_itens = random.randint(1, 5)
            produtos_venda = random.sample(produtos, num_itens)

            for produto in produtos_venda:
                quantidade = random.randint(1, 3)
                venda_produto = VendaProduto(
                    venda_id=venda.id,
                    produto_id=produto.id,
                    quantidade=quantidade
                )
                db.session.add(venda_produto)
                total += produto.preco * quantidade

            venda.valor_total = round(total, 2)

        db.session.commit()
        print("✅ Dados gerados com sucesso.")

if __name__ == "__main__":
    seed()
