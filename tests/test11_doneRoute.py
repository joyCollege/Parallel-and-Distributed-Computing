import numpy as np
import pandas as pd
from src.genetic_algorithms_functions import calculate_fitness, \
    select_in_tournament, mutate

def generate_unique_population(doneRoutes, population_size, num_nodes):
    """
    Generate a unique population of individuals for a genetic algorithm.

    Each individual in the population represents a route in a graph, where the first node is fixed (0) and the 
    remaining nodes are a permutation of the other nodes in the graph. This function ensures that all individuals
    in the population are unique.

    Parameters:
        - population_size (int): The desired size of the population.
        - num_nodes (int): The number of nodes in the graph, including the starting node.

    Returns:
        - list of lists: A list of unique individuals, where each individual is represented as a list of node indices.
    """
    population = set()
    while len(population) < population_size:
        individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
        if individual not in doneRoutes:
            population.add(tuple(individual))
            doneRoutes.append(individual)
    return [list(ind) for ind in population]

def order_crossover(parent1, parent2, num_nodes=32):
    """
    Order crossover (OX) for permutations using circular filling.
    This function assumes that the fixed starting node (0) should not appear in the variable parts.
    It removes any 0's and then fills in any missing genes from the full set (1 to num_nodes-1).

    Parameters:
        - parent1 (list): The first parent's variable part.
        - parent2 (list): The second parent's variable part.
        - num_nodes (int): Total number of nodes (including the fixed starting node).

    Returns:
        - list: The offspring's variable part.
    """
    # Expected genes: 1 to num_nodes-1
    expected_genes = set(range(1, num_nodes))
    
    # Filter out any 0's if present
    parent1 = [gene for gene in parent1 if gene != 0]
    parent2 = [gene for gene in parent2 if gene != 0]
    
    # Ensure parent's variable parts contain all expected genes (if not, add missing ones)
    missing_from_p1 = list(expected_genes - set(parent1))
    missing_from_p2 = list(expected_genes - set(parent2))
    if missing_from_p1:
        parent1.extend(missing_from_p1)
    if missing_from_p2:
        parent2.extend(missing_from_p2)
    
    size = len(expected_genes)  # This should be num_nodes-1
    start, end = sorted(np.random.choice(range(size), 2, replace=False))
    offspring = [None] * size
    # Copy segment from parent1
    offspring[start:end+1] = parent1[start:end+1]
    
    pos = (end + 1) % size
    for gene in parent2:
        if gene not in offspring:
            offspring[pos] = gene
            pos = (pos + 1) % size

    # Fill any remaining positions with any missing genes
    missing = list(expected_genes - set(offspring))
    for i in range(size):
        if offspring[i] is None:
            if missing:
                offspring[i] = missing.pop(0)
            else:
                raise ValueError("Offspring not fully filled even after correction: " + str(offspring))
    
    if None in offspring:
        raise ValueError("Offspring not fully filled: " + str(offspring))
    
    return offspring


def test11_doneRoute():
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
        population_size     = 10000 # default = 10000
        num_tournaments     = 500   # default = 4  
        tournament_size     = 1000  # default = 3 
        mutation_rate       = .2    # default = 0.1
        num_generations     = 200   # default = 200
        infeasible_penalty  = 1e6   # default = 1e6  
        stagnation_limit    = 5     # default = 5  

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
                population = generate_unique_population(doneRoutes, population_size - 1, num_nodes)
                population.append(best_individual)
                stagnation_counter = 0
                continue  # Skip the rest of the loop for this generation
            else:
                print(f"Regenerating population at generation {generation} due to stagnation")
                
                # Keep the top 10% best individuals
                elite_count = population_size // 10  # 10% of population
                best_individuals = sorted(population, key=lambda ind: calculate_fitness(ind, distance_matrix, infeasible_penalty))[:elite_count]
                
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

