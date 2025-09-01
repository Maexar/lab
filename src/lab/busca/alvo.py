import turtle


class Alvo:
    def __init__(self, grade, linha, coluna, size=12, cor="red"):
        self.linha = linha
        self.coluna = coluna
        self.grade = grade
        self.cor = cor
        self.grade.alvo = self

    def recolore(self, size=16, cor=None):
        if cor is None:
            cor = self.cor
        x, y = self.grade(self.linha, self.coluna)
        self.grade.pincel.penup()
        self.grade.pincel.goto(x, y)
        self.grade.pincel.dot(size, cor)

    @property
    def posicao(self):
        return self.linha, self.coluna

    def __repr__(self):
        return f"Alvo({self.linha}, {self.coluna})"

    def __eq__(self, other):
        return (self.linha, self.coluna) == (other.linha, other.coluna)
