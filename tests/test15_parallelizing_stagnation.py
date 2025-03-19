import numpy as np
import pandas as pd
from multiprocessing import Pool
from src.genetic_algorithms_functions import calculate_fitness, select_in_tournament, mutate
from src.updated_GA_functions import generate_unique_population, order_crossover

def split_list(lst, n):
    """Splits a list into n nearly-equal parts."""
    k, m = divmod(len(lst), n)
    return [lst[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n)]

def generate_population_worker(chunk_size, doneRoutes, num_nodes):
    """Worker to generate a chunk of unique individuals."""
    return generate_unique_population(doneRoutes, chunk_size, num_nodes)

def parallel_generate_population(doneRoutes, target_size, num_nodes, pool, num_workers):
    """
    Uses the pool to generate a new population in parallel.
    Splits the target size across workers and then combines the results.
    """
    # Determine how many individuals each worker should generate.
    chunks = [target_size // num_workers + (1 if i < target_size % num_workers else 0) for i in range(num_workers)]
    results = pool.starmap(generate_population_worker, [(chunk, doneRoutes, num_nodes) for chunk in chunks])
    new_population = [ind for sublist in results for ind in sublist]
    return new_population[:target_size]

def ga_worker(sub_population, distance_matrix, infeasible_penalty, num_tournaments, tournament_size, mutation_rate):
    """
    Processes a sub-population:
      - Calculates fitness values
      - Performs tournament selection
      - Applies order crossover and mutation.
    """
    fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty)
                               for route in sub_population])
    
    selected = select_in_tournament(sub_population, fitness_values, num_tournaments, tournament_size)
    
    offspring = []
    # Pair off the selected individuals (ignoring an extra individual if present)
    for i in range(0, len(selected) - (len(selected) % 2), 2):
        parent1, parent2 = selected[i], selected[i+1]
        # Exclude the starting node (assumed to be 0) for crossover and then add it back.
        route_child = order_crossover(parent1[1:], parent2[1:])
        offspring.append([0] + route_child)
    
    mutated_offspring = [mutate(route, mutation_rate) for route in offspring]
    return mutated_offspring

def test15_parallelizing_stagnation(
                        population_size         = 10000,  # Main population size
                        num_tournaments         = 500,
                        tournament_size         = 1000,
                        mutation_rate           = 0.2,
                        num_generations         = 200,
                        infeasible_penalty      = 1e6,
                        stagnation_limit        = 5,
                        use_extended_datset     = False,
                        use_default_stagnation  = True
                    ):
    # Load the distance matrix.
    FILEPATH = './data/city_distances_extended.csv' if use_extended_datset else './data/city_distances.csv'
    distance_matrix = pd.read_csv(FILEPATH).to_numpy()
    num_nodes = distance_matrix.shape[0]
    
    # Prepare doneRoutes and generate an enlarged initial population.
    doneRoutes = []
    np.random.seed(42)  # For reproducibility
    population = generate_unique_population(doneRoutes, population_size, num_nodes)
    
    best_fitness = 1e6
    stagnation_counter = 0
    num_workers = 6  # Based on your six-core design

    # Create one Pool for the entire run.
    with Pool(processes=num_workers) as pool:
        for generation in range(num_generations):
            # First, compute fitness values globally.
            fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty)
                                         for route in population])
            current_best = np.min(fitness_values)
            
            if current_best < best_fitness:
                best_fitness = current_best
                stagnation_counter = 0
            else:
                stagnation_counter += 1
            
            # Check for stagnation BEFORE running the normal GA worker.
            if stagnation_counter >= stagnation_limit:
                print(f"Regenerating population at generation {generation} due to stagnation")
                print("Best route so far:", population[np.argmin(fitness_values)], "with total distance:", np.min(fitness_values))
                
                if use_default_stagnation:
                    best_individual = population[np.argmin(fitness_values)]
                    # Generate a new population (all but the best) in parallel.
                    new_population = parallel_generate_population(doneRoutes, population_size - 1, num_nodes, pool, num_workers)
                    new_population.append(best_individual)
                else:
                    elite_count = population_size // 10
                    best_individuals = sorted(population,
                                              key=lambda ind: -calculate_fitness(ind, distance_matrix, infeasible_penalty)
                                             )[:elite_count]
                    new_population_part = parallel_generate_population(doneRoutes, population_size - len(best_individuals),
                                                                       num_nodes, pool, num_workers)
                    new_population = best_individuals + new_population_part
                
                stagnation_counter = 0
                population = new_population
                # Skip the rest of the generation so that next iteration continues with the new population.
                continue
            
            # If no stagnation, proceed with the normal parallel GA worker.
            sub_pops = split_list(population, num_workers)
            async_results = pool.starmap_async(
                ga_worker,
                [(sub_pop, distance_matrix, infeasible_penalty, num_tournaments, tournament_size, mutation_rate)
                 for sub_pop in sub_pops]
            )
            results = async_results.get()
            # Flatten the list of offspring from all workers.
            all_mutated_offspring = [offspring for sublist in results for offspring in sublist]
            doneRoutes.extend(all_mutated_offspring)
            
            # Replacement: Replace the worst individuals in the current population.
            fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty)
                                         for route in population])
            indices_to_replace = np.argsort(fitness_values)[::-1][:len(all_mutated_offspring)]
            for i, idx in enumerate(indices_to_replace):
                population[idx] = all_mutated_offspring[i]
            
            # Ensure population uniqueness.
            unique_population = set(tuple(ind) for ind in population)
            while len(unique_population) < population_size:
                individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
                unique_population.add(tuple(individual))
            population = [list(ind) for ind in unique_population]
            
            print(f"Generation {generation}: Best fitness = {current_best:,}")
        
        # Final evaluation.
        fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty)
                                     for route in population])
        best_idx = np.argmin(fitness_values)
        best_solution = population[best_idx]
        print("Best Solution:", best_solution)
        print(f"Total Distance: {-calculate_fitness(best_solution, distance_matrix, infeasible_penalty):,}")

# Example call:
# updated_GA_trial_parallel()
