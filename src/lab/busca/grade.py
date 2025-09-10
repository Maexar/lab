import turtle
from time import sleep, time

from lab.busca import Alvo


class Grade:
    alvo: Alvo

    def __init__(self, nlinhas=15, ncolunas=15, tamanho_do_no=30, fps=10, usar_grafo=False):
        self.tamanho_do_no, self.nlinhas, self.ncolunas = tamanho_do_no, nlinhas, ncolunas
        self.usar_grafo = usar_grafo
        
        self.nos = {}
        self.arestas = {}
        
        if usar_grafo:
            self._criar_grafo_exemplo()
        
        width = ncolunas * tamanho_do_no + 100
        height = nlinhas * tamanho_do_no + 100
        self.screen = turtle.Screen()
        
        # Configurar tela cheia
        self.screen.setup(1.0, 1.0)  # Ocupar 100% da largura e altura da tela
        
        try:
            # Acesso ao tkinter root window para maximizar
            root = self.screen.getcanvas().winfo_toplevel()
            root.state('zoomed')  # Windows/Linux
        except:
            try:
                root.attributes('-zoomed', True)  # Linux alternativo
            except:
                pass  # Se falhar, mantém o setup(1.0, 1.0)
        
        self.screen.tracer(0, 0)
        self.fps = fps
        self.grid = turtle.Turtle()
        self.grid.hideturtle()
        self.grid.speed(0)
        self.grid.color("lightgray")
        self.inicio = time()

        self.xi = - (ncolunas * tamanho_do_no) // 2
        self.yi = - (nlinhas * tamanho_do_no) // 2
        xf = self.xi + ncolunas * tamanho_do_no
        yf = self.yi + nlinhas * tamanho_do_no

        if not usar_grafo:
            for x in range(self.xi, xf + 1, tamanho_do_no):
                self.grid.penup()
                self.grid.goto(x, self.yi)
                self.grid.pendown()
                self.grid.goto(x, yf)

            for y in range(self.yi, yf + 1, tamanho_do_no):
                self.grid.penup()
                self.grid.goto(self.xi, y)
                self.grid.pendown()
                self.grid.goto(xf, y)
        else:
            self._desenhar_grafo()

        self.pincel = turtle.Turtle()
        self.pincel.hideturtle()
        self.pincel.speed(0)
        self.screen.update()
        
    def _criar_grafo_exemplo(self):
        self.nos = {
            'A': (3, 3),
            'B': (3, 12), 
            'C': (12, 3),
            'D': (12, 12),
            'E': (7, 7)
        }
        
        arestas_com_pesos = [
            ('A', 'B', 2.0),
            ('A', 'C', 1.5), 
            ('A', 'E', 1.0),
            ('B', 'D', 1.5),
            ('B', 'E', 2.5),
            ('C', 'D', 1.0),
            ('C', 'E', 1.2),
            ('D', 'E', 1.8),
        ]
        
        for origem, destino, peso in arestas_com_pesos:
            self.arestas[(origem, destino)] = peso
            self.arestas[(destino, origem)] = peso
    
    def _desenhar_grafo(self):
        self.grid.color("gray")
        for (origem, destino), peso in self.arestas.items():
            if origem < destino:
                pos_origem = self.nos[origem]
                pos_destino = self.nos[destino]
                
                x1, y1 = self(*pos_origem)
                x2, y2 = self(*pos_destino)
                
                self.grid.penup()
                self.grid.goto(x1, y1)
                self.grid.pendown()
                self.grid.goto(x2, y2)
                
                meio_x, meio_y = (x1 + x2) / 2, (y1 + y2) / 2
                self.grid.penup()
                self.grid.goto(meio_x, meio_y)
                self.grid.write(f"{peso}", align="center", font=("Arial", 8, "normal"))
        
        for nome, (linha, coluna) in self.nos.items():
            x, y = self(linha, coluna)
            self.grid.penup()
            self.grid.goto(x, y)
            self.grid.dot(20, "lightblue")
            self.grid.goto(x, y - 5)
            self.grid.write(nome, align="center", font=("Arial", 12, "bold"))
    
    def obter_vizinhos(self, no_nome):
        vizinhos = []
        for (origem, destino), peso in self.arestas.items():
            if origem == no_nome:
                vizinhos.append((destino, peso))
        return vizinhos
    
    def obter_peso_aresta(self, origem, destino):
        return self.arestas.get((origem, destino), float('inf'))

    def redesenhar_no(self, nome_no, cor):
        if self.usar_grafo and nome_no in self.nos:
            if hasattr(self, 'alvo') and self.alvo and nome_no == self.alvo.nome_no:
                if cor in ["blue", "lightgreen"]:
                    pass
                else:
                    return  
                
            linha, coluna = self.nos[nome_no]
            x, y = self(linha, coluna)
            self.pincel.penup()
            self.pincel.goto(x, y)
            self.pincel.dot(25, cor)
            self.pincel.goto(x, y - 5)
            self.pincel.color("black")
            self.pincel.write(nome_no, align="center", font=("Arial", 12, "bold"))

    def desenha(self):
        espera = 1 / self.fps - (time() - self.inicio)
        if espera > 0:
            sleep(espera)
        self.inicio = time()
        if hasattr(self, 'alvo') and self.alvo is not None:
            self.alvo.recolore()
        self.screen.update()

    def pinta(self, l, c, cor):
        if self.usar_grafo:
            x, y = self(l, c)
            self.pincel.penup()
            self.pincel.goto(x, y)
            self.pincel.dot(25, cor)
        else:
            self.pincel.penup()
            self.pincel.goto(self(l + 0.5, c - 0.5))
            self.pincel.pendown()
            self.pincel.fillcolor(cor)
            self.pincel.begin_fill()
            for _ in range(4):
                self.pincel.forward(self.tamanho_do_no)
                self.pincel.left(90)
            self.pincel.end_fill()

    def __call__(self, linha, coluna):
        x = self.xi + (coluna - 0.5) * self.tamanho_do_no
        y = self.yi + (self.nlinhas - linha + 0.5) * self.tamanho_do_no
        return x, y