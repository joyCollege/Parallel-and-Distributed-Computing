import numpy as np
import pandas as pd
from src.genetic_algorithms_functions import calculate_fitness, \
    select_in_tournament, order_crossover, mutate, \
    generate_unique_population
from time import time 

def test8_firstExtendedRun():
    startTime = time()

    # Load the distance matrix
    distance_matrix = pd.read_csv('./data/city_distances_extended.csv').to_numpy()

    use_default_parameters = False
    use_default_stagnation = True

    if use_default_parameters:
        # Default Parameters 
        num_nodes = distance_matrix.shape[0]
        population_size     = 10000
        num_tournaments     = 4     # Number of tournaments to run
        tournament_size     = 3     # Added this
        mutation_rate       = 0.1
        num_generations     = 200
        infeasible_penalty  = 1e6   # Penalty for infeasible routes
        stagnation_limit    = 5     # Number of generations without improvement before regeneration
    else: 
        # Experimental Parameters 
        num_nodes = distance_matrix.shape[0]
        population_size     = 50000 # default = 10000
        num_tournaments     = 2500   # default = 4  
        tournament_size     = 10000  # default = 3 
        mutation_rate       = .8     # default = 0.1
        num_generations     = 2000   # default = 200
        infeasible_penalty  = 1e6   # default = 1e6  
        stagnation_limit    = 3     # default = 5  

    # Generate initial population: each individual is a route starting at node 0
    np.random.seed(42)  # For reproducibility
    population = generate_unique_population(population_size, num_nodes)

    # Initialize variables for tracking stagnation
    best_calculate_fitness = int(1e6)
    stagnation_counter = 0

    # Main GA loop
    for generation in range(num_generations):
        # Evaluate calculate_fitness
        calculate_fitness_values = np.array([calculate_fitness(route, distance_matrix, infeasible_penalty) for route in population])

        # Check for stagnation
        current_best_calculate_fitness = np.min(calculate_fitness_values)
        if current_best_calculate_fitness < best_calculate_fitness:
            best_calculate_fitness = current_best_calculate_fitness
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        # Regenerate population if stagnation limit is reached, keeping the best individual
        if stagnation_counter >= stagnation_limit:
            if use_default_stagnation:
                print(f"Regenerating population at generation {generation} due to stagnation")
                best_individual = population[np.argmin(calculate_fitness_values)]
                population = generate_unique_population(population_size - 1, num_nodes)
                population.append(best_individual)
                stagnation_counter = 0
                continue  # Skip the rest of the loop for this generation
            else:
                print(f"Regenerating population at generation {generation} due to stagnation")
                
                # Keep the top 10% best individuals
                elite_count = population_size // 10  # 10% of population
                best_individuals = sorted(population, key=lambda ind: calculate_fitness(ind, distance_matrix, infeasible_penalty))[:elite_count]
                
                new_population = generate_unique_population(population_size - len(best_individuals), num_nodes)
                population = best_individuals + new_population
                stagnation_counter = 0
                continue  # Skip rest of loop for this generation


        # Selection, crossover, and mutation
        selected = select_in_tournament(population,
                                        calculate_fitness_values,
                                        num_tournaments,
                                        tournament_size)
        offspring = []
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i + 1]
            route1 = order_crossover(parent1[1:], parent2[1:])
            offspring.append([0] + route1)
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

        # Replacement: Replace the individuals that lost in the tournaments with the new offspring
        for i, idx in enumerate(np.argsort(calculate_fitness_values)[::-1][:len(mutated_offspring)]):
            population[idx] = mutated_offspring[i]

        # Ensure population uniqueness
        unique_population = set(tuple(ind) for ind in population)
        while len(unique_population) < population_size:
            individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
            unique_population.add(tuple(individual))
        population = [list(individual) for individual in unique_population]

        # Print best calculate_fitness
        print(f"Generation {generation}: Best calculate_fitness = {current_best_calculate_fitness:,}")  # Changed to add commas 

    # Update calculate_fitness_values for the final population
    calculate_fitness_values = np.array([calculate_fitness(route, distance_matrix, infeasible_penalty) for route in population])

    # Output the best solution
    best_idx = np.argmin(calculate_fitness_values)
    best_solution = population[best_idx]
    print("Best Solution:", best_solution)
    print(f"Total Distance: {calculate_fitness(best_solution, distance_matrix, infeasible_penalty):,}") # Changed to add commas 
    
    return time() - startTime

