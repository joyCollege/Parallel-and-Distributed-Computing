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

# Worker function to process a sub-population:
def ga_worker(sub_population, distance_matrix, infeasible_penalty, num_tournaments, tournament_size, mutation_rate, num_nodes):
    """
    Perform genetic algorithm operations (selection, crossover, mutation) on a sub-population.
    
    Parameters:
        sub_population (list): A subset of the population.
        distance_matrix (numpy.ndarray): A matrix representing distances between nodes.
        infeasible_penalty (float): Penalty for infeasible routes.
        num_tournaments (int): Number of tournament selection rounds.
        tournament_size (int): Number of individuals per tournament.
        mutation_rate (float): Probability of mutation occurring.
        num_nodes (int): Number of nodes in the route.
    
    Returns:
        list: A list of new mutated offspring.
    """
    # Calculate fitness for each individual in the sub-population
    fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty) for route in sub_population])
    
    # Perform tournament selection on the sub-population
    selected = select_in_tournament(sub_population, fitness_values, num_tournaments, tournament_size)
    
    offspring = []
    # Pair off the selected individuals; if there's an odd number, ignore the last one
    for i in range(0, len(selected) - (len(selected) % 2), 2):
        parent1, parent2 = selected[i], selected[i+1]
        # Exclude the starting node (assumed to be 0) from crossover, then prepend it back to offspring
        route_child = order_crossover(parent1[1:], parent2[1:], num_nodes)
        offspring.append([0] + route_child)
    
    # Apply mutation to each offspring route
    mutated_offspring = [mutate(route, mutation_rate) for route in offspring]
    return mutated_offspring

def p2_starMapAsync_largerWorker(
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
    Runs a parallelized Genetic Algorithm (GA) using multiprocessing to evolve a 
    population of routes for a Traveling Salesman Problem (TSP) variant.

    The function utilizes tournament selection, order crossover, and mutation to 
    optimize the routes while ensuring diversity. If stagnation is detected, the 
    population is partially regenerated.

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
        - Uses multiprocessing to evaluate and evolve sub-populations in parallel.
        - Ensures population uniqueness after each generation.
        - Implements stagnation handling to avoid premature convergence.
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
    
    # Create an initial doneRoutes list and generate an enlarged initial population.
    doneRoutes = []
    np.random.seed(42)  # For reproducibility
    population = generate_unique_population(doneRoutes, population_size, num_nodes)
    
    best_calculate_fitness = 1e6
    stagnation_counter = 0
    num_workers = 6  

    # Create a multiprocessing Pool once for the entire GA run.
    with Pool(processes=num_workers) as pool:
        for generation in range(num_generations):
            # Global fitness evaluation for stagnation check
            fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty) for route in population], dtype=int)
            current_best = np.min(fitness_values)
            if current_best < best_calculate_fitness:
                best_calculate_fitness = current_best
                stagnation_counter = 0
            else:
                stagnation_counter += 1

            # Handle stagnation by regenerating part of the population if necessary.
            if stagnation_counter >= stagnation_limit:
                print(f"Regenerating population at generation {generation} due to stagnation")
                best_idx = np.argmin(fitness_values)
                best_route = [int(x) for x in population[best_idx]]  # Convert all elements to int
                best_distance = float(np.min(fitness_values))  
                
                print("Best route so far:", best_route, "with total distance:", best_distance)
                if use_default_stagnation:
                    best_individual = population[np.argmin(fitness_values)]
                    population = generate_unique_population(doneRoutes, population_size - 1, num_nodes)
                    population.append(best_individual)
                else:
                    elite_count = population_size // 10  # Keep top 10%
                    best_individuals = sorted(population, key=lambda ind: -calculate_fitness(ind, distance_matrix, infeasible_penalty))[:elite_count]
                    new_population = generate_unique_population(doneRoutes, population_size - len(best_individuals), num_nodes)
                    population = best_individuals + new_population
                stagnation_counter = 0
                continue  # Skip the rest of this generation

            # Split the current population into 6 sub-populations using the custom split function
            sub_pops = split_list(population, num_workers)

            # Run the GA worker in parallel on each sub-population
            async_results = pool.starmap_async(
                ga_worker,
                [(sub_pop, distance_matrix, infeasible_penalty, num_tournaments, tournament_size, mutation_rate, num_nodes)
                 for sub_pop in sub_pops]
            )
            # Wait for results and combine all mutated offspring from the workers
            results = async_results.get()
            all_mutated_offspring = [offspring for sublist in results for offspring in sublist]
            
            # Re-add the new routes to doneRoutes to track processed routes
            doneRoutes.extend(all_mutated_offspring)
            
            # Replacement: Replace the worst individuals in the population with new offspring
            fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty) for route in population], dtype=int)
            indices_to_replace = np.argsort(fitness_values)[::-1][:len(all_mutated_offspring)]
            for i, idx in enumerate(indices_to_replace):
                population[idx] = all_mutated_offspring[i]
                
            # Ensure population uniqueness non-parallelized
            unique_population = set(tuple(ind) for ind in population)
            while len(unique_population) < population_size:
                individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
                unique_population.add(tuple(individual))
            population = [list(ind) for ind in unique_population]
            
            print(f"Generation {generation}: Best fitness = {current_best:,}")

    # Final evaluation after all generations have completed.
    fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty) for route in population])
    best_idx = np.argmin(fitness_values)
    best_solution = [int(x) for x in population[best_idx]]
    print("Best Solution:", best_solution)
    print(f"Total Distance: {-calculate_fitness(best_solution, distance_matrix, infeasible_penalty):,}")

