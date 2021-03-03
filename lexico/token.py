
# Referencia da construção desta classe: https://www.youtube.com/watch?v=36MOhcBz7p0&t=2312s

class Token:
    def __init__(self, tipo_token, lexema: str):
        self.tipo_token = tipo_token
        self.lexema = lexema

    def to_string(self):
        string = "< " + str(self.tipo_token) + " , '" + self.lexema + "' >"
        return string
