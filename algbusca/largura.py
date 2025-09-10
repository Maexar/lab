import turtle
from collections import deque
import heapq

import numpy as np


from lab.busca.agente import Agente
from lab.busca.alvo import Alvo
from lab.busca.grade import Grade

rnd = np.random.default_rng(23)
grade = Grade(fps=1, usar_grafo=True)
agente = Agente(grade, no_inicial='A')  
alvo = Alvo(grade, no_alvo='D')
visitados = set()
fronteira = [(0.0, agente.nome_no)]
custos = {agente.nome_no: 0.0}

grade.redesenhar_no(agente.nome_no, "blue")
grade.screen.update()

# Marcar todos os outros nós como não visitados (verde)
for nome_no in grade.nos.keys():
    if nome_no != agente.nome_no:
        grade.redesenhar_no(nome_no, "lightgreen")

# Garantir que o alvo apareça vermelho por cima
grade.alvo.recolore()
grade.screen.update()

while agente.nome_no != alvo.nome_no and fronteira:
    custo_atual, no_atual = heapq.heappop(fronteira)
    
    if no_atual in visitados:
        continue
        
    if no_atual != agente.nome_no:
        print(f"Movendo de {agente.nome_no} para {no_atual}")
        custo_movimento = custo_atual - agente.custo_total
        agente.move(no_atual, custo_movimento)
        print(f"Tartaruga agora em: {agente.turtle.pos()}")
    else:
        print(f"Já no nó {no_atual}")
        grade.redesenhar_no(no_atual, "blue")
    
    visitados.add(no_atual)
    
    print(f"Agente no nó {agente.nome_no}")
    
    for vizinho, peso_aresta in agente.sucessores:
        if vizinho not in visitados:
            novo_custo = agente.custo_total + peso_aresta
            if vizinho not in custos or novo_custo < custos[vizinho]:
                custos[vizinho] = novo_custo
                heapq.heappush(fronteira, (novo_custo, vizinho))
                grade.redesenhar_no(vizinho, "lightgreen")
    
    grade.screen.update()
    
    grade.alvo.recolore()
    grade.screen.update()
    
    grade.desenha()

# Final simples
print(f"Algoritmo terminou no nó {agente.nome_no}")
if agente.nome_no == alvo.nome_no:
    print("🎉 SUCESSO! Agente chegou ao alvo!")
    grade.redesenhar_no(agente.nome_no, "gold")
    grade.screen.update()

turtle.done()