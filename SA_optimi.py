import random
import math
import numpy as np

N, K = map(int, input().split())
d = list(map(int, input().split()))
t = [list(map(int, input().split())) for _ in range(N + 1)]

# Simulated Annealing parameters
max_iter = 2000
init_temp = 200
alpha = 0.99

# Calculate working time
def calculate_working_time(routes):
    max_time = 0
    for route in routes:
        time = 0
        prev = 0
        for customer in route:
            time += t[prev][customer] + d[customer - 1]
            prev = customer
        time += t[prev][0]  # Return to depot
        max_time = max(max_time, time)
    return max_time

# Savings heuristic for better initialization
def savings_initial_solution():
    customers = list(range(1, N + 1))
    savings = []
    for i in customers:
        for j in customers:
            if i != j:
                savings.append((t[0][i] + t[j][0] - t[i][j], i, j))
    savings.sort(reverse=True)

    routes = {i: [i] for i in customers}
    for _, i, j in savings:
        if i in routes and j in routes and routes[i] != routes[j]:
            if len(routes[i]) + len(routes[j]) <= N // K:
                routes[i].extend(routes[j])
                del routes[j]

    return list(routes.values())[:K] + [[] for _ in range(K - len(routes))]

# Perturb solution
def perturb_solution(routes):
    new_routes = [route[:] for route in routes]  # Deep copy
    if random.random() < 0.5:  # Swap within a route
        route = random.choice(new_routes)
        if len(route) > 1:
            i, j = random.sample(range(len(route)), 2)
            route[i], route[j] = route[j], route[i]
    else:  # Move between routes
        tech1, tech2 = random.sample(range(K), 2)
        if new_routes[tech1]:
            cust = random.choice(new_routes[tech1])
            new_routes[tech1].remove(cust)
            new_routes[tech2].append(cust)
    return new_routes

# Initialize
current_solution = savings_initial_solution()
current_cost = calculate_working_time(current_solution)
best_solution = current_solution
best_cost = current_cost
temp = init_temp

# Simulated Annealing
for _ in range(max_iter):
    new_solution = perturb_solution(current_solution)
    new_cost = calculate_working_time(new_solution)

    # Acceptance criteria
    if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / temp):
        current_solution = new_solution
        current_cost = new_cost

    # Update best solution
    if current_cost < best_cost:
        best_solution = current_solution
        best_cost = current_cost

    # Cool down
    temp *= alpha

# Output the result
def print_solution(K, best_solution):
    print(K)
    for route in best_solution:
        route.insert(0, 0)
        route.append(0)
        print(len(route))
        print(" ".join(map(str, route)))

print_solution(K, best_solution)
