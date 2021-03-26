from .entradatabelasimbolos import EntradaTabelaDeSimbolos


class TabelaDeSimbolos:
    def __init__(self):
        self.tabela_simbolos = {}

    # Método de inserção
    def inserir(self, nome, valor, tipo_dado):
        entrada = EntradaTabelaDeSimbolos(nome, valor, tipo_dado)

        # Inserindo no dict do Python (inserção parecida com tabela Hash)
        self.tabela_simbolos[nome] = entrada

    # Método de busca
    def existe(self, nome) -> EntradaTabelaDeSimbolos:
        return self.tabela_simbolos.get(nome)

    # Retorna o tipo da variável
    def verificar(self, nome):
        return self.tabela_simbolos.get(nome).tipo_dado
