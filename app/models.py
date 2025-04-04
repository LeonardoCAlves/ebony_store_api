from .database import db
from werkzeug.security import generate_password_hash, check_password_hash

# Modelo de Cliente
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    rg = db.Column(db.String(20), unique=True, nullable=False)

    vendas = db.relationship("Venda", backref="cliente", lazy=True)

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

# Modelo de Funcionário
class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(150), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    rg = db.Column(db.String(20), unique=True, nullable=False)

    vendas = db.relationship("Venda", backref="funcionario", lazy=True)

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

# Modelo de Loja
class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)  # Exemplo: "RJ", "SP"

    vendas = db.relationship("Venda", backref="loja", lazy=True)

# Modelo de Forma de Pagamento
class FormaPagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_pagamento = db.Column(db.String(50), unique=True, nullable=False)

    vendas = db.relationship("Venda", backref="forma_pagamento", lazy=True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)

    produtos = db.relationship('Produto', backref='categoria', lazy=True)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

    vendas_associadas = db.relationship("VendaProduto", backref="produto", lazy=True)

class VendaProduto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionario.id"), nullable=False)
    loja_id = db.Column(db.Integer, db.ForeignKey("loja.id"), nullable=False)
    forma_pagamento_id = db.Column(db.Integer, db.ForeignKey("forma_pagamento.id"), nullable=False)

    valor_total = db.Column(db.Float, nullable=False)
    data_venda = db.Column(db.DateTime, server_default=db.func.now())

    venda_produtos = db.relationship("VendaProduto", backref="venda", lazy=True)
