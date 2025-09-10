import turtle


class Agente:
    def __init__(self, grade, linha=None, coluna=None, no_inicial=None, cor="black", forma="turtle"):
        self.grade = grade
        self.custo_total = 0.0
        
        if grade.usar_grafo:
            # modo grafo
            if not no_inicial:
                raise ValueError("no_inicial é obrigatório quando usar_grafo=True")
            self.no_atual = no_inicial
            self.linha, self.coluna = grade.nos[no_inicial]
        else:
            # modo grade tradicional
            if linha is None or coluna is None:
                raise ValueError("linha e coluna são obrigatórias quando usar_grafo=False")
            self.linha = linha
            self.coluna = coluna
            self.no_atual = None
            self.direcoes_possiveis = {"norte": (1, 0), "sul": (-1, 0), "oeste": (0, 1), "leste": (0, -1)}
        
        self.turtle = turtle.Turtle(shape=forma)
        self.turtle.color(cor)
        self.turtle.penup()
        self.turtle.speed(3)
        
        x, y = self.grade(self.linha, self.coluna)
        self.turtle.goto(x, y)

    def move(self, destino, custo=None):
        """Move o agente. Em modo grafo, destino é nome do nó. Em modo grade, é (linha, coluna)"""
        if self.grade.usar_grafo:
            if custo is None:
                custo = self.grade.obter_peso_aresta(self.no_atual, destino)
            
            self.grade.redesenhar_no(self.no_atual, "blue")
            
            self.no_atual = destino
            self.linha, self.coluna = self.grade.nos[destino]
            self.custo_total += custo
        else:
            if isinstance(destino, tuple):
                self.linha, self.coluna = destino
            else:
                self.linha, self.coluna = destino, custo
            self.custo_total += 1.0
        
        x, y = self.grade(self.linha, self.coluna)
        self.grade.screen.tracer(1, 0)
        self.turtle.goto(x, y)
        self.grade.screen.tracer(0, 0)
        
        if self.grade.usar_grafo:
            self.grade.redesenhar_no(self.no_atual, "blue")

    @property
    def posicao(self):
        return self.linha, self.coluna

    @property
    def sucessores(self):
        if self.grade.usar_grafo:
            return self.grade.obter_vizinhos(self.no_atual)
        else:
            lst = []
            for _, (l, c) in self.direcoes_possiveis.items():
                linha = self.linha + l
                coluna = self.coluna + c
                if 1 <= linha <= self.grade.nlinhas and 1 <= coluna <= self.grade.ncolunas:
                    lst.append((linha, coluna))
            return lst

    @property 
    def nome_no(self):
        return self.no_atual if self.grade.usar_grafo else None

    def __repr__(self):
        if self.grade.usar_grafo:
            return f"Agente({self.no_atual}, custo={self.custo_total:.1f})"
        else:
            return f"Agente({self.linha}, {self.coluna})"

    def __eq__(self, other):
        if self.grade.usar_grafo:
            return hasattr(other, 'no_atual') and self.no_atual == other.no_atual
        else:
            return (self.linha, self.coluna) == (other.linha, other.coluna)