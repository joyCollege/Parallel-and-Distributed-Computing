import numpy as np
import pandas as pd
from src.genetic_algorithms_functions import calculate_fitness, select_in_tournament, mutate
from src.updated_GA_functions import generate_unique_population, order_crossover
from multiprocessing import Manager, Pool

def split_list(lst, n):
    """Split a list into n nearly equal parts."""
    k, m = divmod(len(lst), n)
    return [lst[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n)]

def process_chunk(chunk, distance_matrix, infeasible_penalty, doneRoutes):
    """
    Process a chunk of the population: calculate fitness for each individual,
    and update the shared doneRoutes list (storing route tuples).
    """
    results = []
    for individual in chunk:
        fitness = -calculate_fitness(individual, distance_matrix, infeasible_penalty)
        route_tuple = tuple(individual)
        if route_tuple not in doneRoutes:
            doneRoutes.append(route_tuple)
        results.append((individual, fitness))
    return results

def p1_starMap_fitnessOnly(
                        population_size      = 10000,  # default = 10000
                        num_tournaments      = 500,    # default = 4 (but using 500 here)
                        tournament_size      = 1000,   # default = 3 (but using 1000 here)
                        mutation_rate        = 0.2,    # default = 0.1 (set to 0.2)
                        num_generations      = 200,    # default = 200
                        infeasible_penalty   = 1e6,    # default = 1e6
                        stagnation_limit     = 5,      # default = 5
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
    
    # Shared doneRoutes list (storing route tuples)
    doneRoutes = Manager().list()
    population = generate_unique_population(doneRoutes, population_size, num_nodes)
    
    # Initialize variables for tracking stagnation
    best_calculate_fitness = int(1e6)
    stagnation_counter = 0

    pool = Pool(processes=6)

    # Main GA loop
    for generation in range(num_generations):
        
        # Instead of np.array_split, use our custom split_list function.
        chunks = split_list(population, 6)
        chunk_results = pool.starmap(
            process_chunk,
            [(chunk, distance_matrix, infeasible_penalty, doneRoutes) for chunk in chunks]
        )
        # Flatten the results and extract fitness values.
        flat_results = [item for sublist in chunk_results for item in sublist]
        fitness_values = np.array([fitness for (_, fitness) in flat_results])
        current_best_calculate_fitness = np.min(fitness_values)

        # Check for stagnation
        if current_best_calculate_fitness <= best_calculate_fitness:
            best_calculate_fitness = current_best_calculate_fitness
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        # Regenerate population if stagnation limit is reached, keeping the best individual
        if stagnation_counter >= stagnation_limit:
            print(f"Regenerating population at generation {generation} due to stagnation")
            print("Best route so far:", population[np.argmin(fitness_values)], "with total distance:", np.min(fitness_values))

            if use_default_stagnation:
                best_individual = population[np.argmin(fitness_values)]
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
        selected = select_in_tournament(population, fitness_values, num_tournaments, tournament_size)
        offspring = []
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i + 1]
            route1 = order_crossover(parent1[1:], parent2[1:], num_nodes)
            offspring.append([0] + route1)
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

        # Replacement: Replace the individuals that lost in the tournaments with the new offspring
        for i, idx in enumerate(np.argsort(fitness_values)[::-1][:len(mutated_offspring)]):
            population[idx] = mutated_offspring[i]

        # Ensure population uniqueness
        unique_population = set(tuple(ind) for ind in population)
        while len(unique_population) < population_size:
            individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
            unique_population.add(tuple(individual))
        population = [list(individual) for individual in unique_population]

        print(f"Generation {generation}: Best calculate_fitness = {current_best_calculate_fitness:,}")

    # Update calculate_fitness_values for the final population
    fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty) for route in population])
    best_idx = np.argmin(fitness_values)
    best_solution = population[best_idx]
    print("Best Solution:", best_solution)
    print(f"Total Distance: {-calculate_fitness(best_solution, distance_matrix, infeasible_penalty):,}")

    pool.close()
    pool.join()