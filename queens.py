from pyscipopt import Model, quicksum
import numpy as np
import matplotlib.pyplot as plt
from itertools import product


x = {}
model = Model()
n = 8
m = 8

for i in range(n):
    for j in range(n):
        x[i, j] = model.addVar(name=f'x_{i+1}_{j+1}', vtype='B')

for i in range(n):
    model.addCons(quicksum(x[i, j] for j in range(n)) <= 1)

for j in range(n):
    model.addCons(quicksum(x[i, j] for i in range(n)) <= 1)

for k in range(-n + 1, n):
    if k >= 0:
        model.addCons(quicksum(x[i, i+k] for i in range(n - k)) <= 1)
    else:
        model.addCons(quicksum(x[i, i+k] for i in range(-k, n)) <= 1)

for k in range(-n + 1, n):
    if k >= 0:
        model.addCons(quicksum(x[i, n - i - k - 1] for i in range(n - k)) <= 1)
    else:
        model.addCons(quicksum(x[i, n - i - k - 1] for i in range(-k, n)) <= 1)

model.addCons(sum(x[i, j] for i in range(n) for j in range(n)) == m)
model.setObjective(1)
model.writeProblem('queens.lp')
model.optimize()
sol = model.getBestSol()

chessboard = np.zeros((n, n))
chessboard[1::2, 0::2] = 1
chessboard[0::2, 1::2] = 1

plt.imshow(chessboard, cmap='binary')

for i, j in product(range(n), repeat=2):
    if int(sol[x[i, j]]):
        plt.text(i, j, '♕', fontsize=20, ha='center', va='center', color='black' if (i - j) % 2 == 0 else 'white')

plt.show()