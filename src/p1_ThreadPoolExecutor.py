import numpy as np
import pandas as pd
import concurrent.futures
from src.genetic_algorithms_functions import calculate_fitness, \
    select_in_tournament, order_crossover, mutate, \
    generate_unique_population
from time import time 

def p1_ThreadPoolExecutor():
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

    # Main GA loop
    for generation in range(num_generations):

        #  ======= Parallelized Fitness Evaluation ======= 
        with concurrent.futures.ThreadPoolExecutor() as executor:
            calculate_fitness_values = list(executor.map(
                lambda route: calculate_fitness(route, distance_matrix, infeasible_penalty), 
                population
            ))
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

        #  ======= Parallelized Tournament Selection ======= 
        with concurrent.futures.ThreadPoolExecutor() as executor:
            selected = list(executor.map(
                lambda _: select_in_tournament(population, calculate_fitness_values, 1, tournament_size)[0], 
                range(num_tournaments)
            ))

        #  ======= Parallelized Crossover ======= 
        offspring = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            offspring = list(executor.map(
                lambda parents: [0] + order_crossover(parents[0][1:], parents[1][1:]),
                zip(selected[::2], selected[1::2])
            ))

        #  ======= Parallelized Mutation ======= 
        with concurrent.futures.ThreadPoolExecutor() as executor:
            mutated_offspring = list(executor.map(
                lambda route: mutate(route, mutation_rate), 
                offspring
            ))

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

    #  ======= Parallelized Final Fitness Calculation ======= 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        calculate_fitness_values = list(executor.map(
            lambda route: calculate_fitness(route, distance_matrix, infeasible_penalty), 
            population
        ))
    calculate_fitness_values = np.array(calculate_fitness_values)

    # Output the best solution
    best_idx = np.argmin(calculate_fitness_values)
    best_solution = population[best_idx]
    print("Best Solution:", best_solution)
    print(f"Total Distance: {calculate_fitness(best_solution, distance_matrix, infeasible_penalty):,}")  

    return time() - startTime
