import turtle
from collections import deque

import numpy as np

from lab.busca import sorteia_coords
from lab.busca.agente import Agente
from lab.busca.alvo import Alvo
from lab.busca.grade import Grade

try:
    rnd = np.random.default_rng(5)
    grade = Grade(fps=10)
    agente = Agente(grade, linha=10, coluna=10)
    alvo = Alvo(grade, *sorteia_coords(grade, rnd))
    visitados = set()
    pilha = deque([agente.posicao])

    while agente != alvo and pilha:
        proximo = pilha.pop()  # Remove do topo da pilha (LIFO)
        
        # Só processa se ainda não foi visitado
        if proximo not in visitados:
            agente.move(*proximo)
            visitados.add(proximo)
            grade.pinta(*proximo, cor="blue")
            
            # Adiciona sucessores não visitados à pilha
            for sucessor in agente.sucessores:
                if sucessor not in visitados:
                    grade.pinta(*sucessor, cor="lightgreen")
                    pilha.append(sucessor)  # Adiciona no topo da pilha
            
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
