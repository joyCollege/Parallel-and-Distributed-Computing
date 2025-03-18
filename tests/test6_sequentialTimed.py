import numpy as np
import pandas as pd
from src.genetic_algorithms_functions import calculate_fitness, \
    select_in_tournament, order_crossover, mutate, \
    generate_unique_population
from time import time 

def test6_sequentialTimed():
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
    total_stagnation_time = 0
    total_selection_time = 0
    total_crossover_time = 0
    total_mutation_time = 0
    total_replacement_time = 0

    # Main GA loop
    for generation in range(num_generations):

        # 🚀 **Time Fitness Evaluation**
        start = time()
        calculate_fitness_values = np.array([calculate_fitness(route, distance_matrix, infeasible_penalty) for route in population])
        total_fitness_time += time() - start

        # 🚀 **Time Stagnation Check**
        start = time()
        current_best_calculate_fitness = np.min(calculate_fitness_values)
        if current_best_calculate_fitness < best_calculate_fitness:
            best_calculate_fitness = current_best_calculate_fitness
            stagnation_counter = 0
        else:
            stagnation_counter += 1
        total_stagnation_time += time() - start

        # Regenerate population if stagnation limit is reached
        if stagnation_counter >= stagnation_limit:
            # print(f"Regenerating population at generation {generation} due to stagnation")  # Commented for performance tracking
            best_individual = population[np.argmin(calculate_fitness_values)]
            population = generate_unique_population(population_size - 1, num_nodes)
            population.append(best_individual)
            stagnation_counter = 0
            continue  

        # 🚀 **Time Selection**
        start = time()
        selected = select_in_tournament(population, calculate_fitness_values, num_tournaments, tournament_size)
        total_selection_time += time() - start

        # 🚀 **Time Crossover**
        start = time()
        offspring = []
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i + 1]
            route1 = order_crossover(parent1[1:], parent2[1:])
            offspring.append([0] + route1)
        total_crossover_time += time() - start

        # 🚀 **Time Mutation**
        start = time()
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]
        total_mutation_time += time() - start

        # 🚀 **Time Replacement & Uniqueness Check**
        start = time()
        for i, idx in enumerate(np.argsort(calculate_fitness_values)[::-1][:len(mutated_offspring)]):
            population[idx] = mutated_offspring[i]

        unique_population = set(tuple(ind) for ind in population)
        while len(unique_population) < population_size:
            individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
            unique_population.add(tuple(individual))
        population = [list(individual) for individual in unique_population]
        total_replacement_time += time() - start

        # print(f"Generation {generation}: Best calculate_fitness = {current_best_calculate_fitness:,}")  # Commented for performance tracking

    # 🚀 **Time Final Fitness Calculation**
    start = time()
    calculate_fitness_values = np.array([calculate_fitness(route, distance_matrix, infeasible_penalty) for route in population])
    total_fitness_time += time() - start

    # Output the best solution
    best_idx = np.argmin(calculate_fitness_values)
    best_solution = population[best_idx]
    # print("Best Solution:", best_solution)  # Commented for performance tracking
    # print(f"Total Distance: {calculate_fitness(best_solution, distance_matrix, infeasible_penalty):,}")  # Commented for performance tracking

    total_time = time() - startTime

    # 🚀 **Print Timing Summary**
    print("\n=== Timing Breakdown ===")
    print(f"Total Execution Time: {total_time:.2f} seconds")
    print(f"Fitness Evaluation Time: {total_fitness_time:.2f} seconds ({(total_fitness_time / total_time) * 100:.2f}%)")
    print(f"Stagnation Check Time: {total_stagnation_time:.2f} seconds ({(total_stagnation_time / total_time) * 100:.2f}%)")
    print(f"Selection Time: {total_selection_time:.2f} seconds ({(total_selection_time / total_time) * 100:.2f}%)")
    print(f"Crossover Time: {total_crossover_time:.2f} seconds ({(total_crossover_time / total_time) * 100:.2f}%)")
    print(f"Mutation Time: {total_mutation_time:.2f} seconds ({(total_mutation_time / total_time) * 100:.2f}%)")
    print(f"Replacement & Uniqueness Time: {total_replacement_time:.2f} seconds ({(total_replacement_time / total_time) * 100:.2f}%)")

    return total_time
