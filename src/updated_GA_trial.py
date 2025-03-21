import numpy as np
import pandas as pd
from src.genetic_algorithms_functions import calculate_fitness, select_in_tournament, mutate
from src.updated_GA_functions import generate_unique_population, order_crossover

def updated_GA_trial(
                        population_size      = 10000,  # default = 10000
                        num_tournaments      = 500,   # default = 4
                        tournament_size      = 1000,  # default = 3
                        mutation_rate        = .2,    # default = 0.1
                        num_generations      = 200,   # default = 200
                        infeasible_penalty   = 1e6,   # default = 1e6
                        stagnation_limit     = 5,     # default = 5
                        use_extended_datset  = False,
                        use_default_stagnation = True
                    ):
    
    # Load the distance matrix
    if use_extended_datset: 
        FILEPATH = './data/city_distances_extended.csv'
        num_nodes=100
    else: 
        FILEPATH = './data/city_distances.csv'
        num_nodes=32

    distance_matrix = pd.read_csv(FILEPATH).to_numpy()
    num_nodes = distance_matrix.shape[0]

    # Generate initial population: each individual is a route starting at node 0
    np.random.seed(42)  # For reproducibility
    doneRoutes = []
    population = generate_unique_population(doneRoutes, population_size, num_nodes)

    # Initialize variables for tracking stagnation
    best_calculate_fitness = int(1e6)
    stagnation_counter = 0

    # Main GA loop
    for generation in range(num_generations):
        # Evaluate calculate_fitness
        calculate_fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty) for route in population], dtype=int)

        # Check for stagnation
        current_best_calculate_fitness = np.min(calculate_fitness_values)
        if current_best_calculate_fitness < best_calculate_fitness:
            best_calculate_fitness = current_best_calculate_fitness
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        # Regenerate population if stagnation limit is reached, keeping the best individual
        if stagnation_counter >= stagnation_limit:
            print(f"Regenerating population at generation {generation} due to stagnation")
            best_idx = np.argmin(calculate_fitness_values)
            best_route = [int(x) for x in population[best_idx]]  # Convert all elements to int
            best_distance = float(np.min(calculate_fitness_values))  
            
            print("Best route so far:", best_route, "with total distance:", best_distance)
            if use_default_stagnation:
                best_individual = population[np.argmin(calculate_fitness_values)]
                population = generate_unique_population(doneRoutes, population_size - 1, num_nodes)
                population.append(best_individual)
                stagnation_counter = 0
                continue  # Skip the rest of the loop for this generation
            else:
                # Keep the top 10% best individuals
                elite_count = population_size // 10  # 10% of population
                best_individuals = sorted(population, key=lambda ind: -calculate_fitness(ind, distance_matrix, infeasible_penalty))[:elite_count]
                
                new_population = generate_unique_population(doneRoutes, population_size - len(best_individuals), num_nodes)
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
            route1 = order_crossover(parent1[1:], parent2[1:], num_nodes)
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
    calculate_fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty) for route in population])

    # Output the best solution
    best_idx = np.argmin(calculate_fitness_values)
    best_solution = [int(x) for x in population[best_idx]]
    print("Best Solution:", best_solution)
    print(f"Total Distance: {-calculate_fitness(best_solution, distance_matrix, infeasible_penalty):,}") # Changed to add commas 

