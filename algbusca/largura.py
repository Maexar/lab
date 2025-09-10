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


grade.alvo.recolore()  
grade.screen.update()


while fronteira:
    custo_atual, no_atual = heapq.heappop(fronteira)
    
    if no_atual in visitados:
        continue
        
    visitados.add(no_atual)
    grade.redesenhar_no(no_atual, "lightgreen")
  
    
    if no_atual == alvo.nome_no:
        grade.screen.update()
        grade.desenha()
        break
    
    vizinhos = grade.obter_vizinhos(no_atual)
    for vizinho, peso_aresta in vizinhos:
        if vizinho not in visitados:
            novo_custo = custo_atual + peso_aresta
            
            if vizinho not in custos or novo_custo < custos[vizinho]:
                custos[vizinho] = novo_custo
                heapq.heappush(fronteira, (novo_custo, vizinho))
    
    grade.screen.update()
    grade.desenha()

grade.alvo.recolore()
grade.screen.update()

caminho = []
if alvo.nome_no in custos:
    atual = alvo.nome_no
    while atual != agente.nome_no:
        caminho.append(atual)
        
        melhor_pred = None
        menor_custo_pred = float('inf')
        
        for vizinho, peso in grade.obter_vizinhos(atual):
            if vizinho in custos:
                custo_total_via_vizinho = custos[vizinho] + peso
                if abs(custo_total_via_vizinho - custos[atual]) < 0.001:  
                    if custos[vizinho] < menor_custo_pred:
                        menor_custo_pred = custos[vizinho]
                        melhor_pred = vizinho
        
        atual = melhor_pred
        if atual is None:
            break
    
    caminho.append(agente.nome_no)
    caminho.reverse()
    
  
    grade.redesenhar_no(agente.nome_no, "blue")
    grade.screen.update()
    grade.alvo.recolore()
    grade.screen.update()
    grade.desenha()
    
    for i in range(1, len(caminho)):
        destino = caminho[i]
        
        peso_aresta = grade.obter_peso_aresta(agente.nome_no, destino)
        agente.move(destino, peso_aresta)
        
        grade.redesenhar_no(agente.nome_no, "blue")
        
        grade.screen.update()
        grade.alvo.recolore()
        grade.screen.update()
        grade.desenha()
else:
    print(" Alvo inalcançável")

if agente.nome_no == alvo.nome_no:
    grade.redesenhar_no(agente.nome_no, "blue")
    grade.screen.update()

turtle.done()