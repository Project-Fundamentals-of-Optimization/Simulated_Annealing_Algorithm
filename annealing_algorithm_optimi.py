import random
import math

N, K = map(int, input().split())  # Number of customers and technicians
d = list(map(int, input().split()))  # Maintenance times for each customer
t = []  # Travel time matrix
for i in range(N + 1):  # Includes depot at index 0
    sub_t = list(map(int, input().split()))
    t.append(sub_t)

# Simulated Annealing parameters
max_iter = 1000
init_temp = 100
alpha = 0.95

# Calculate working time
def calculate_working_time(routes):
    # Calculate the maximum working time across all technicians.
    max_time = 0
    for route in routes:
        time = 0  # Initial time
        prev = 0  # Start from depot
        for customer in route:
            time += t[prev][customer] + d[customer - 1]
            prev = customer
        time += t[prev][0]  # Return to depot
        max_time = max(max_time, time)
    return max_time

# Generate initial solution
def generate_initial_solution():
    customers = list(range(1, N + 1))  # Customers are indexed from 1 to N
    random.shuffle(customers)  # Shuffle customers randomly
    routes = [[] for _ in range(K)]  # K technicians, empty routes
    for i, customer in enumerate(customers):
        routes[i % K].append(customer)  # Distribute customers across technicians
    return routes

# Perturb solution
def perturb_solution(routes):
    new_routes = [route[:] for route in routes]  # Deep copy of routes
    tech1, tech2 = random.sample(range(K), 2)  # Pick two different technicians
    if new_routes[tech1] and new_routes[tech2]:  # Swap customers between two routes
        cust1 = random.choice(new_routes[tech1])
        cust2 = random.choice(new_routes[tech2])
        new_routes[tech1].remove(cust1)
        new_routes[tech2].remove(cust2)
        new_routes[tech1].append(cust2)
        new_routes[tech2].append(cust1)
    elif new_routes[tech1]:  # Move a customer from tech1 to tech2
        cust = random.choice(new_routes[tech1])
        new_routes[tech1].remove(cust)
        new_routes[tech2].append(cust)
    return new_routes

# Initialize
current_solution = generate_initial_solution()
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
