import turtle


class Alvo:
    def __init__(self, grade, linha=None, coluna=None, no_alvo=None, size=12, cor="red"):
        self.grade = grade
        self.cor = cor
        
        if grade.usar_grafo:
            if not no_alvo:
                raise ValueError("no_alvo é obrigatório quando usar_grafo=True")
            self.no_alvo = no_alvo
            self.linha, self.coluna = grade.nos[no_alvo]
        else:
            if linha is None or coluna is None:
                raise ValueError("linha e coluna são obrigatórias quando usar_grafo=False")
            self.linha = linha
            self.coluna = coluna
            self.no_alvo = None
            
        self.grade.alvo = self
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.speed(0)
        self.t.penup()

    @property
    def posicao(self):
        return (self.linha, self.coluna)
    
    @property
    def nome_no(self):
        return self.no_alvo if self.grade.usar_grafo else None

    def recolore(self, size=16, cor=None):
        if cor is None:
            cor = self.cor
        self.t.goto(*self.grade(self.linha, self.coluna))
        self.t.dot(size, cor)

    def __repr__(self):
        if self.grade.usar_grafo:
            return f"Alvo({self.no_alvo})"
        else:
            return f"Alvo({self.linha}, {self.coluna})"

    def __eq__(self, other):
        if self.grade.usar_grafo:
            if hasattr(other, 'no_atual'):
                return self.no_alvo == other.no_atual
            elif hasattr(other, 'no_alvo'):
                return self.no_alvo == other.no_alvo
            return False
        else:
            return (self.linha, self.coluna) == (other.linha, other.coluna)
        