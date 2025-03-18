import numpy as np
import pandas as pd
import multiprocessing as mp
from src.genetic_algorithms_functions import calculate_fitness, \
    select_in_tournament, order_crossover, mutate, \
    generate_unique_population
from time import time

# ➤ Define function for parallel fitness calculation
def fitness_worker(route, distance_matrix, infeasible_penalty):
    return calculate_fitness(route, distance_matrix, infeasible_penalty)

def p3_parallel_fitness():
    startTime = time()

    # Load the distance matrix
    distance_matrix = pd.read_csv('./data/city_distances.csv').to_numpy()

    # Default Parameters 
    num_nodes = distance_matrix.shape[0]
    population_size     = 10000
    num_tournaments     = 4     
    tournament_size     = 3    
    mutation_rate       = 0.1
    num_generations     = 200
    infeasible_penalty  = 1e6  
    stagnation_limit    = 5    

    # Generate initial population
    np.random.seed(42)  
    population = generate_unique_population(population_size, num_nodes)

    # Initialize variables for tracking stagnation
    best_calculate_fitness = int(1e6)
    stagnation_counter = 0

    total_fitness_time = 0
    total_selection_time = 0
    total_crossover_time = 0
    total_mutation_time = 0
    total_replacement_time = 0

    # 🚀 **Open the Pool for the Entire Execution**
    pool = mp.Pool(mp.cpu_count()) 

    for generation in range(num_generations):

        # 🚀 **Parallelized Fitness Calculation**
        start = time()
        calculate_fitness_values = pool.starmap(
            fitness_worker, [(route, distance_matrix, infeasible_penalty) for route in population]
        )
        calculate_fitness_values = np.array(calculate_fitness_values)
        total_fitness_time += time() - start

        # Stagnation Check (Sequential, Fast)
        current_best_calculate_fitness = np.min(calculate_fitness_values)
        if current_best_calculate_fitness < best_calculate_fitness:
            best_calculate_fitness = current_best_calculate_fitness
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        # Regenerate population if stagnation limit is reached
        if stagnation_counter >= stagnation_limit:
            best_individual = population[np.argmin(calculate_fitness_values)]
            population = generate_unique_population(population_size - 1, num_nodes)
            population.append(best_individual)
            stagnation_counter = 0
            continue  

        # 🚀 **Selection (Sequential, Fast)**
        start = time()
        selected = select_in_tournament(population, calculate_fitness_values, num_tournaments, tournament_size)
        total_selection_time += time() - start

        # 🚀 **Crossover (Sequential, Fast)**
        start = time()
        offspring = []
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i + 1]
            route1 = order_crossover(parent1[1:], parent2[1:])
            offspring.append([0] + route1)
        total_crossover_time += time() - start

        # 🚀 **Mutation (Sequential, Fast)**
        start = time()
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]
        total_mutation_time += time() - start

        # 🚀 **Optimized Replacement & Uniqueness Check (No `set()`)**
        start = time()
        for i, idx in enumerate(np.argsort(calculate_fitness_values)[::-1][:len(mutated_offspring)]):
            population[idx] = mutated_offspring[i]

        # 🚀 **Better Uniqueness Check Using NumPy**
        population = np.unique(np.array(population), axis=0).tolist()
        while len(population) < population_size:
            individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
            population.append(individual)
        total_replacement_time += time() - start

    # 🚀 **Parallelized Final Fitness Calculation**
    start = time()
    calculate_fitness_values = pool.starmap(
        fitness_worker, [(route, distance_matrix, infeasible_penalty) for route in population]
    )
    calculate_fitness_values = np.array(calculate_fitness_values)
    total_fitness_time += time() - start

    # ✅ **Close the Pool**
    pool.close()
    pool.join()

    # Output the best solution
    best_idx = np.argmin(calculate_fitness_values)
    best_solution = population[best_idx]

    total_time = time() - startTime

    # 🚀 **Print Timing Summary**
    print("\n=== Timing Breakdown ===")
    print(f"Total Execution Time: {total_time:.2f} seconds")
    print(f"Fitness Evaluation Time: {total_fitness_time:.2f} seconds ({(total_fitness_time / total_time) * 100:.2f}%)")
    print(f"Selection Time: {total_selection_time:.2f} seconds ({(total_selection_time / total_time) * 100:.2f}%)")
    print(f"Crossover Time: {total_crossover_time:.2f} seconds ({(total_crossover_time / total_time) * 100:.2f}%)")
    print(f"Mutation Time: {total_mutation_time:.2f} seconds ({(total_mutation_time / total_time) * 100:.2f}%)")
    print(f"Replacement & Uniqueness Time: {total_replacement_time:.2f} seconds ({(total_replacement_time / total_time) * 100:.2f}%)")

    return total_time

# === Timing Breakdown ===
# Total Execution Time: 26.36 seconds
# Fitness Evaluation Time: 18.47 seconds (70.06%)
# Selection Time: 0.11 seconds (0.42%)
# Crossover Time: 0.01 seconds (0.05%)
# Mutation Time: 0.00 seconds (0.01%)
# Replacement & Uniqueness Time: 5.43 seconds (20.61%)
# ************************************************** 
#  p3_parallel_fitness time: 26.361685037612915 
# **************************************************