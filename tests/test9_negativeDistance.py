import numpy as np
import pandas as pd
from src.genetic_algorithms_functions import order_crossover, mutate, \
    generate_unique_population
from time import time 

def calculate_fitness(route, distance_matrix, infeasible_penalty=1e6):
    """
    Calculates fitness as the negative total route distance.
    Returns a negative penalty for infeasible routes.
    
    Parameters:
        - route (list): Order of nodes visited.
        - distance_matrix (numpy.ndarray): Matrix where [i, j] gives the distance from node i to node j.
        - infeasible_penalty (int): Penalty for infeasible segments.
    
    Returns:
        - float: Negative total distance for feasible routes or -infeasible_penalty if any segment is infeasible.
    """
    total_distance = 0
    for i in range(len(route) - 1):
        d = distance_matrix[route[i], route[i + 1]]
        if d == 100000:  # Infeasible route indicator
            return -infeasible_penalty  # Return negative penalty
        total_distance += d

    d_return = distance_matrix[route[-1], route[0]]
    if d_return == 100000:
        return -infeasible_penalty

    return -(total_distance + d_return)

def select_in_tournament(population, scores, number_tournaments=4, tournament_size=3):
    """
    Tournament selection for the GA, selecting the individual with the lowest fitness value.
    
    Parameters:
        - population (list): The current population of routes.
        - scores (np.array): Fitness scores (positive after adjustment) for each individual.
        - number_tournaments (int): Number of tournaments.
        - tournament_size (int): Number of individuals per tournament.
    
    Returns:
        - list: Selected individuals for crossover.
    """
    selected = []
    for _ in range(number_tournaments):
        tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
        best_idx = tournament_indices[np.argmin(scores[tournament_indices])]
        selected.append(population[best_idx])
    return selected


def test9_negativeDistance():
    distance_matrix = pd.read_csv('./data/city_distances.csv').to_numpy()

    # Parameters
    num_nodes = distance_matrix.shape[0]
    population_size = 10000
    num_tournaments = 4   # Number of tournaments to run
    mutation_rate = 0.1
    num_generations = 200
    infeasible_penalty = 1e6   # Penalty for infeasible routes
    stagnation_limit = 5       # Generations without improvement before regeneration

    # Generate initial population: each individual is a route starting at node 0
    np.random.seed(42)  # For reproducibility
    population = generate_unique_population(population_size, num_nodes)

    # Initialize variables for tracking stagnation and best fitness.
    best_fitness = 1e6  # Using positive fitness values (actual distances) for comparison
    stagnation_counter = 0

    # Main GA loop
    for generation in range(num_generations):
        # Evaluate raw fitness values (which are negative distances)
        raw_fitness_values = np.array([calculate_fitness(route, distance_matrix, infeasible_penalty)
                                    for route in population])
        # Flip the sign: now feasible routes get their actual (positive) total distance,
        # and infeasible routes become infeasible_penalty.
        fitness_values = -raw_fitness_values

        # Stagnation check using np.min (lowest distance is best)
        current_best_fitness = np.min(fitness_values)
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        # Regenerate population if stagnation limit is reached, keeping the best individual.
        if stagnation_counter >= stagnation_limit:
            print(f"Regenerating population at generation {generation} due to stagnation")
            best_individual = population[np.argmin(fitness_values)]
            population = generate_unique_population(population_size - 1, num_nodes)
            population.append(best_individual)
            stagnation_counter = 0
            continue  # Skip the rest of the loop for this generation

        # Selection, crossover, and mutation
        selected = select_in_tournament(population, fitness_values)
        offspring = []
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i + 1]
            # Keep node 0 fixed
            route1 = order_crossover(parent1[1:], parent2[1:])
            offspring.append([0] + route1)
        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

        # Replacement: Replace the individuals with worst fitness with new offspring.
        for i, idx in enumerate(np.argsort(fitness_values)[::-1][:len(mutated_offspring)]):
            population[idx] = mutated_offspring[i]

        # Ensure population uniqueness
        unique_population = set(tuple(ind) for ind in population)
        while len(unique_population) < population_size:
            individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
            unique_population.add(tuple(individual))
        population = [list(ind) for ind in unique_population]

        print(f"Generation {generation}: Best fitness = {current_best_fitness}")

    # Final evaluation of fitness for the final population
    raw_fitness_values = np.array([calculate_fitness(route, distance_matrix, infeasible_penalty)
                                    for route in population])
    fitness_values = -raw_fitness_values
    best_idx = np.argmin(fitness_values)
    best_solution = population[best_idx]
    print("Best Solution:", best_solution)
    print("Total Distance:", np.min(fitness_values))