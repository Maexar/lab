import turtle
from time import sleep, perf_counter

from lab.busca import Alvo


class Grade:
    alvo: Alvo

    def __init__(self, nlinhas=15, ncolunas=15, tamanho_do_no=30, fps=10):
        self.tamanho_do_no, self.nlinhas, self.ncolunas = tamanho_do_no, nlinhas, ncolunas
        width = ncolunas * tamanho_do_no + 100
        height = nlinhas * tamanho_do_no + 100
        self.screen = turtle.Screen()
        self.screen.setup(width, height)
        self.screen.tracer(0, 0)
        self.fps = fps
        self.grid = turtle.Turtle()
        self.grid.hideturtle()
        self.grid.speed(0)
        self.grid.color("lightgray")
        self.inicio = perf_counter()

        self.xi = - (ncolunas * tamanho_do_no) // 2
        self.yi = - (nlinhas * tamanho_do_no) // 2
        xf = self.xi + ncolunas * tamanho_do_no
        yf = self.yi + nlinhas * tamanho_do_no

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

        self.pincel = turtle.Turtle()
        self.pincel.hideturtle()
        self.pincel.speed(0)
        self.screen.update()

    def desenha(self):
        if hasattr(self, 'alvo'):
            self.alvo.recolore()
        self.screen.update()
        
        # Usar perf_counter para timing mais preciso em FPS alto
        agora = perf_counter()
        if not hasattr(self, 'ultimo_frame'):
            self.ultimo_frame = agora
        
        tempo_decorrido = agora - self.ultimo_frame
        tempo_target = 1.0 / self.fps
        
        if tempo_decorrido < tempo_target:
            sleep(tempo_target - tempo_decorrido)
        
        self.ultimo_frame = perf_counter()

    def pinta(self, l, c, cor):
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
