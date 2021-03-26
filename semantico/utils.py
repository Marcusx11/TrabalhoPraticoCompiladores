from lexico.token import Token
from .tabelasimbolos import TabelaDeSimbolos


class SemanticoUtils:
    erros_semanticos = list()

    def adicionar_erros_semanticos(self, token: Token, mensagem: str):
        # TODO Token para pegar a linha e a coluna onde ocorreu o erro
        self.erros_semanticos.append("Erro: {}".format(mensagem))

    def verificar_tipo(self, tabela: TabelaDeSimbolos):
        # TODO expressão aritémtica
        print("A fazer")
