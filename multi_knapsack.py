from pyscipopt import Model, quicksum
"""
maximize value while staying below capacity

a simple constrained linear optimization using pyscipopt

"""
values = [34, 56, 34, 78, 467, 54, 36, 36, 4563, 46, 346, 34, 34, 63, 463, 6, 456, 45, 64, 7]

weights = [7, 86, 5, 76, 7, 56, 76, 76, 7, 67, 6, 76, 75, 6, 567, 56, 578, 58, 6, 465]

x = {}
n = len(values)
capacity = [200, 300]
m = 2
model = Model('knapsack')

# define variables as binaries
for i in range(n):
    for j in range(m):
        x[i, j] = model.addVar(name=f'x_{i}', vtype='B')

# add constraint so that the sum of weights is less than or equal to capacity
for j in range(m):
    model.addCons(quicksum(x[i, j] * weights[i] for i in range(n)) <= capacity[j])

for i in range(n):
    model.addCons(quicksum(x[i, j] for j in range(m)) <= 1)

# set the objective to the negative of sum of values to maximize value
model.setObjective(quicksum(-x[i, j] * values[i] for i in range(n) for j in range(m)))

# optimize
model.optimize()

sol = model.getBestSol()

# print results
for i in range(n):
    print(sol[x[i, 0]], sol[x[i, 1]])
