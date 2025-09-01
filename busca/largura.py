import turtle
from collections import deque

import numpy as np

from lab.busca import sorteia_coords
from lab.busca.agente import Agente
from lab.busca.alvo import Alvo
from lab.busca.grade import Grade

rnd = np.random.default_rng(23)
grade = Grade(fps=20)
agente = Agente(grade, 8, 8)
alvo = Alvo(grade, *sorteia_coords(grade, rnd))
visitados = set()
fronteira = deque([agente.posicao])

while agente != alvo and fronteira:
    proximo = fronteira.popleft()  
    agente.move(*proximo)
    grade.pinta(*proximo, cor="blue")  
    visitados.add(proximo)
    
    for sucessor in agente.sucessores:
        if sucessor not in visitados and sucessor not in fronteira:
            grade.pinta(*sucessor, cor="lightgreen")  
            fronteira.append(sucessor)  
            grade.desenha()

    grade.pinta(*agente.posicao, cor="green" if agente == alvo else "blue")
    grade.desenha()

turtle.done()