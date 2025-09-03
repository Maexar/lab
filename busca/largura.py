import turtle
from collections import deque

import numpy as np

from lab.busca import sorteia_coords
from lab.busca.agente import Agente
from lab.busca.alvo import Alvo
from lab.busca.grade import Grade

try:
    rnd = np.random.default_rng()  # Seed aleatória a cada execução
    grade = Grade(fps=10)
    agente = Agente(grade, 8, 8)
    alvo = Alvo(grade, *sorteia_coords(grade, rnd))
    visitados = set()
    fronteira = deque([agente.posicao])

    while agente != alvo and fronteira:
        proximo = fronteira.pop()  # Retira da lista o elemento mais à direita (FIFO)
        
        # Só processa se ainda não foi visitado
        if proximo not in visitados:
            agente.move(*proximo)
            visitados.add(proximo)
            grade.pinta(*proximo, cor="blue")
            
            # Adiciona sucessores não visitados à fronteira
            for sucessor in agente.sucessores:
                if sucessor not in visitados and sucessor not in fronteira:
                    grade.pinta(*sucessor, cor="lightgreen")
                    fronteira.appendleft(sucessor)  # Insere elemento à esquerda da fila
            
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