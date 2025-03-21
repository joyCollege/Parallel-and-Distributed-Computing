import numpy as np
import pandas as pd
from multiprocessing import Pool
from src.genetic_algorithms_functions import calculate_fitness, select_in_tournament, mutate
from src.updated_GA_functions import generate_unique_population, order_crossover

def split_list(lst, n):
    """
    Split a list into `n` nearly equal parts.

    Args:
        lst (list): The list to split.
        n (int): Number of parts to divide the list into.

    Returns:
        list: A list of sublists.
    """
    k, m = divmod(len(lst), n)
    return [lst[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n)]

def generate_population_worker(chunk_size, doneRoutes, num_nodes):
    """
    Worker function to generate a chunk of unique individuals for the population.

    Args:
        chunk_size (int): Number of individuals to generate.
        doneRoutes (list): List of already processed routes to ensure uniqueness.
        num_nodes (int): Number of cities (nodes) in the problem.

    Returns:
        list: A list of unique routes (individuals) generated for the population.
    """
    return generate_unique_population(doneRoutes, chunk_size, num_nodes)

def parallel_generate_population(doneRoutes, target_size, num_nodes, pool, num_workers):
    """
    Generates a new population in parallel using multiple worker processes.

    The population is split into chunks, each processed by a separate worker to 
    ensure efficient and unique population generation.

    Args:
        doneRoutes (list): List of routes already processed (to avoid duplicates).
        target_size (int): Total number of individuals to generate.
        num_nodes (int): Number of cities (nodes) in the problem.
        pool (multiprocessing.Pool): Pool of worker processes for parallel execution.
        num_workers (int): Number of worker processes to use.

    Returns:
        list: A list of newly generated unique routes, with a total size of `target_size`.
    """
    # Determine how many individuals each worker should generate.
    chunks = [target_size // num_workers + (1 if i < target_size % num_workers else 0) for i in range(num_workers)]
    results = pool.starmap(generate_population_worker, [(chunk, doneRoutes, num_nodes) for chunk in chunks])
    new_population = [ind for sublist in results for ind in sublist]
    return new_population[:target_size]

def ga_worker(sub_population, distance_matrix, infeasible_penalty, 
     num_tournaments, tournament_size, mutation_rate, num_nodes):
    """
    Processes a sub-population in the Genetic Algorithm (GA) by performing:
      - Fitness evaluation
      - Tournament selection
      - Order crossover
      - Mutation

    Args:
        sub_population (list): A list of routes (individuals) representing a sub-population.
        distance_matrix (np.ndarray): Matrix of distances between nodes.
        infeasible_penalty (float): Penalty applied to infeasible solutions.
        num_tournaments (int): Number of tournaments for selection.
        tournament_size (int): Number of individuals per tournament.
        mutation_rate (float): Probability of mutation per individual.
        num_nodes (int): Number of cities (nodes) in the problem.

    Returns:
        list: A list of mutated offspring routes after crossover and mutation.
    """
    fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty)
                               for route in sub_population], dtype=int)
    
    selected = select_in_tournament(sub_population, fitness_values, num_tournaments, tournament_size)
    
    offspring = []
    # Pair off the selected individuals (ignoring an extra individual if present)
    for i in range(0, len(selected) - (len(selected) % 2), 2):
        parent1, parent2 = selected[i], selected[i+1]
        # Exclude the starting node (assumed to be 0) for crossover and then add it back.
        route_child = order_crossover(parent1[1:], parent2[1:], num_nodes)
        offspring.append([0] + route_child)
    
    mutated_offspring = [mutate(route, mutation_rate) for route in offspring]
    return mutated_offspring

def p3_starMapAsync_stagnation(
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
    """
    Runs a parallelized Genetic Algorithm (GA) for the Traveling Salesman Problem (TSP) with 
    enhanced stagnation handling using multiprocessing.

    This function divides the population into sub-populations and processes them in parallel 
    using tournament selection, order crossover, and mutation. If stagnation is detected, 
    it regenerates part or all of the population to escape local optima.

    Args:
        population_size (int, optional): Total number of individuals in the population. Default is 10000.
        num_tournaments (int, optional): Number of tournaments for selection. Default is 500.
        tournament_size (int, optional): Number of individuals per tournament. Default is 1000.
        mutation_rate (float, optional): Probability of mutation per individual. Default is 0.2.
        num_generations (int, optional): Number of generations to evolve. Default is 200.
        infeasible_penalty (float, optional): Penalty for infeasible solutions. Default is 1e6.
        stagnation_limit (int, optional): Maximum consecutive generations without improvement before population reset. Default is 5.
        use_extended_datset (bool, optional): Whether to use an extended dataset (100 cities instead of 32). Default is False.
        use_default_stagnation (bool, optional): Whether to use full population reset or elite preservation upon stagnation. Default is True.

    Returns:
        None. The function prints the best solution found and its total distance.

    Notes:
        - Uses multiprocessing to process sub-populations in parallel for efficiency.
        - Implements stagnation detection and population regeneration when needed.
        - Maintains population uniqueness after each generation.
    """

    # Load the distance matrix
    if use_extended_datset: 
        FILEPATH = './data/city_distances_extended.csv'
        num_nodes=100
    else: 
        FILEPATH = './data/city_distances.csv'
        num_nodes=32

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
                best_idx = np.argmin(fitness_values)
                best_route = [int(x) for x in population[best_idx]]  # Convert all elements to int
                best_distance = float(np.min(fitness_values))  
            
                print("Best route so far:", best_route, "with total distance:", best_distance)

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
                [(sub_pop, distance_matrix, infeasible_penalty, num_tournaments, tournament_size, mutation_rate, num_nodes)
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
        best_solution = [int(x) for x in population[best_idx]]
        print("Best Solution:", best_solution)
        print(f"Total Distance: {-calculate_fitness(best_solution, distance_matrix, infeasible_penalty):,}")
