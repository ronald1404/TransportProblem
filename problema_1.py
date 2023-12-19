from pulp import *

# Oferta dos aquartelamentos
a = [2,2,1]

# Demanda das frentes de batalha [2,1,1]
b = [2,1,1]

# Capacidade dos Transbordos
t = [4,5]

# Custo de transporte da origem i para o destino j
Cij = [[0,0,0],
       [0,0,0],
       [0,0,4]] # no grafo existe apenas uma aresta de a3 para b3

# custo de transportes das origens para os pontos de transbordo
Dik = [
  	[1,3],
  	[2,3],
  	[0,1],
  	[0,1]] # o transporte 4,2 é do transbordo 1 para o transbordo 2

# Custo de transporte dos transbordos para os destinos
Ekj = [[2,4,0],
       [3,5,2]]
 

model = pulp.LpProblem('linear_programming', LpMinimize)

# get solver
solver = pulp.PULP_CBC_CMD()

# declaração das variaveis de decisão
# quantidades de i para j
X33 = LpVariable('X33', lowBound=0, upBound=None, cat='Continuous')
# quantidades de i para k
Y11 = LpVariable('Y11', lowBound=0, upBound=None, cat='Continuous')
Y12 = LpVariable('Y12', lowBound=0, upBound=None, cat='Continuous')
Y21 = LpVariable('Y21', lowBound=0, upBound=None, cat='Continuous')
Y22 = LpVariable('Y22', lowBound=0, upBound=None, cat='Continuous')
Y32 = LpVariable('Y32', lowBound=0, upBound=None, cat='Continuous')
Y42 = LpVariable('Y42', lowBound=0, upBound=None, cat='Continuous')
# quantidades de k para j
Z11 = LpVariable('Z11', lowBound=0, upBound=None, cat='Continuous')
Z12 = LpVariable('Z12', lowBound=0, upBound=None, cat='Continuous')
Z21 = LpVariable('Z21', lowBound=0, upBound=None, cat='Continuous')
Z22 = LpVariable('Z22', lowBound=0, upBound=None, cat='Continuous')
Z23 = LpVariable('Z23', lowBound=0, upBound=None, cat='Continuous')


# Função Objetivo
model += Cij[2][2]*X33 \
+ Dik[0][0]*Y11 + Dik[0][1]*Y12 + Dik[1][0]*Y21 + Dik[1][1]*Y22 + Dik[2][1]*Y32 + Dik[3][1]*Y42 \
+ Ekj[0][0]*Z11 + Ekj[0][1]*Z12 + Ekj[1][0]*Z21 + Ekj[1][1]*Z22 + Ekj[1][2]*Z23


# Restrições (Tudo o que sai deve ser igual a oferta)
model += Y11 + Y12 <= a[0]
model += Y21 + Y22 <= a[1]
model += X33 + Y32 <= a[2]

model += Z11 + Z21 == b[0]
model += Z12 + Z22 == b[1]
model += X33 + Z23 == b[2]

model += Y11 + Y21  <= t[0]
model += Y12 + Y22 + Y32 + Y42 <= t[0]
model += Z11 + Z12 ==  Y11 + Y21
model += Z21 + Z22 + Z23 == Y12 + Y22 + Y32 + Y42

# solver
results = model.solve(solver=solver)

# print results
if LpStatus[results] == 1: print('A solução é ótima')
print(f'Função Objetiva: z* = {value(model.objective)}')

variaves = [X33,Y11,Y12,Y21,Y22,Y32,Y42,Z11,Z12,Z21,Z22,Z23]

for var in variaves:
    if value(var) != 0.0:
        print(f'Solução: {var.name}* = {value(var)}')
