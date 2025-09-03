import turtle
from collections import deque

import numpy as np

from lab.busca import sorteia_coords, embaralha
from lab.busca.agente import Agente
from lab.busca.alvo import Alvo
from lab.busca.grade import Grade

try:
    rnd = np.random.default_rng()  # Seed aleatória a cada execução
    grade = Grade(fps=10)
    agente = Agente(grade, linha=10, coluna=10)
    alvo = Alvo(grade, *sorteia_coords(grade, rnd))
    visitados = set()
    sucessores = deque([agente.posicao])

    while agente != alvo and sucessores:
        embaralha(sucessores, rnd)
        proximo = sucessores.pop()
        sucessores.clear()
        agente.move(*proximo)
        visitados.add(proximo)
        for sucessor in agente.sucessores:
            if sucessor not in visitados:
                grade.pinta(*sucessor, cor="lightgreen")
                sucessores.append(sucessor)
        grade.pinta(*agente.posicao, cor="blue")
        grade.desenha()

    grade.pinta(*agente.posicao, cor="green" if agente == alvo else "red")
    grade.desenha()

    turtle.exitonclick()
    
except Exception as e:
    print(f"Erro durante a execução: {e}")
    import traceback
    traceback.print_exc()
finally:
    try:
        turtle.Screen()._root.quit()
        turtle.Screen()._root.destroy()
    except:
        pass
    try:
        turtle.bye()
    except:
        pass
