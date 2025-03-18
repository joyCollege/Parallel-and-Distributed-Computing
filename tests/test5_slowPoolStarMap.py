import numpy as np
import pandas as pd
import multiprocessing as mp
from src.genetic_algorithms_functions import calculate_fitness, \
    select_in_tournament, order_crossover, mutate, \
    generate_unique_population
from time import time

def fitness_worker(route, distance_matrix, infeasible_penalty):
    return calculate_fitness(route, distance_matrix, infeasible_penalty)

def tournament_worker(_dummy, population, scores, tournament_size):
    return select_in_tournament(population, scores, 1, tournament_size)[0]

def crossover_worker(parent1, parent2):
    return [0] + order_crossover(parent1[1:], parent2[1:])

def mutation_worker(route, mutation_rate):
    return mutate(route, mutation_rate)

def p2_PoolStarMap():
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

    # ➤ Create a process pool
    with mp.Pool(mp.cpu_count()) as pool:
        for generation in range(num_generations):

            # ================ Parallelized Fitness Calculation ================ 
            calculate_fitness_values = pool.starmap(
                fitness_worker, [(route, distance_matrix, infeasible_penalty) for route in population]
            )
            calculate_fitness_values = np.array(calculate_fitness_values)

            # Check for stagnation
            current_best_calculate_fitness = np.min(calculate_fitness_values)
            if current_best_calculate_fitness < best_calculate_fitness:
                best_calculate_fitness = current_best_calculate_fitness
                stagnation_counter = 0
            else:
                stagnation_counter += 1

            # Regenerate population if stagnation limit is reached
            if stagnation_counter >= stagnation_limit:
                print(f"Regenerating population at generation {generation} due to stagnation")
                best_individual = population[np.argmin(calculate_fitness_values)]
                population = generate_unique_population(population_size - 1, num_nodes)
                population.append(best_individual)
                stagnation_counter = 0
                continue  

            # ================ Parallelized Tournament Selection ================ 
            selected = pool.starmap(
                tournament_worker, [(None, population, calculate_fitness_values, tournament_size)] * num_tournaments
            )

            # ================ Parallelized Crossover ================ 
            offspring = pool.starmap(
                crossover_worker, zip(selected[::2], selected[1::2])
            )

            # ================ Parallelized Mutation ================ 
            mutated_offspring = pool.starmap(
                mutation_worker, [(route, mutation_rate) for route in offspring]
            )

            # Replacement: Replace worst individuals
            for i, idx in enumerate(np.argsort(calculate_fitness_values)[::-1][:len(mutated_offspring)]):
                population[idx] = mutated_offspring[i]

            # Ensure population uniqueness
            unique_population = set(tuple(ind) for ind in population)
            while len(unique_population) < population_size:
                individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
                unique_population.add(tuple(individual))
            population = [list(individual) for individual in unique_population]

            # Print best fitness
            print(f"Generation {generation}: Best calculate_fitness = {current_best_calculate_fitness:,}")  

        # ================ Parallelized Final Fitness Calculation ================ 
        calculate_fitness_values = pool.starmap(
            fitness_worker, [(route, distance_matrix, infeasible_penalty) for route in population]
        )
        calculate_fitness_values = np.array(calculate_fitness_values)

    # Output the best solution
    best_idx = np.argmin(calculate_fitness_values)
    best_solution = population[best_idx]
    print("Best Solution:", best_solution)
    print(f"Total Distance: {calculate_fitness(best_solution, distance_matrix, infeasible_penalty):,}")  

    return time() - startTime
