from .tabelasimbolos import TabelaDeSimbolos


# Forma de armazenar os escopos diferentes conforme forem aparecendo em pilha
# Regra dos escopos mais aninhados
class Escopos:
    def __init__(self):
        self.pilha_de_tabelas = list()  # Lista que funcionará como pilha
        self.criar_novo_escopo()  # Escopo global (escopo inicial)


    # Método para criar novo escopo (basicamente, "empilha" um escopo novo)
    def criar_novo_escopo(self):
        escopo = TabelaDeSimbolos()
        self.pilha_de_tabelas.append(escopo)

    # Método para obter escopo atual
    def obter_escopo_atual(self) -> TabelaDeSimbolos:
        return self.pilha_de_tabelas[-1]  # Índices negativos em Python faz a leitura do array do final p/ o começo

    # Método para percorrer os escopos
    def percorrer_escopos_aninhados(self):
        return self.pilha_de_tabelas

    def abandonar_escopo(self):
        # Tira o escopo do topo da pilha (saiu do escopo)
        self.pilha_de_tabelas.pop()

