from mpi4py import MPI
import numpy as np
import pandas as pd
from src.genetic_algorithms_functions import calculate_fitness, select_in_tournament, mutate
from src.updated_GA_functions import generate_unique_population, order_crossover
from time import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def split_list(lst, n):
    """Splits a list into n nearly-equal parts."""
    k, m = divmod(len(lst), n)
    return [lst[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n)]

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
        child = order_crossover(parent1[1:], parent2[1:], num_nodes)
        offspring.append([0] + child)
    mutated_offspring = [mutate(route, mutation_rate) for route in offspring]
    return mutated_offspring

if __name__ == '__main__':
    # === Master loads data and initial population ===
    startTime = time()
    use_extended_datset = False
    
    # Load the distance matrix
    if use_extended_datset: 
        FILEPATH = './data/city_distances_extended.csv'
        num_nodes=100
    else: 
        FILEPATH = './data/city_distances.csv'
        num_nodes=32

    if rank == 0:
        distance_matrix = pd.read_csv(FILEPATH).to_numpy()
    else:
        distance_matrix = None
    # Broadcast the distance matrix to all processes
    distance_matrix = comm.bcast(distance_matrix, root=0)
    num_nodes = distance_matrix.shape[0]
    
    # GA parameters
    population_size = 10000
    num_generations = 200
    num_tournaments = 500
    tournament_size = 1000
    mutation_rate = 0.2
    infeasible_penalty = 1e6
    stagnation_limit = 5
    use_default_stagnation = True
    
    # Generate initial population on the master and broadcast it
    if rank == 0:
        np.random.seed(42)
        doneRoutes = []
        population = generate_unique_population(doneRoutes, population_size, num_nodes)
    else:
        population = None
    population = comm.bcast(population, root=0)
    
    best_fitness = 1e6
    stagnation_counter = 0

    for generation in range(num_generations):
        # === Global fitness evaluation on the master ===
        if rank == 0:
            fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty)
                                         for route in population])
            current_best = np.min(fitness_values)
            if current_best < best_fitness:
                best_fitness = current_best
                stagnation_counter = 0
            else:
                stagnation_counter += 1
        else:
            current_best = None

        # === If stagnation is detected, regenerate the population ===
        if rank == 0 and stagnation_counter >= stagnation_limit:
            print(f"Regenerating population at generation {generation} due to stagnation")
            best_route = population[np.argmin(fitness_values)]
            best_route_native = [int(x) for x in best_route]
            print("Best route so far:", best_route_native, "with total distance:", np.min(fitness_values))
            if use_default_stagnation:
                new_population = generate_unique_population([], population_size - 1, num_nodes)
                new_population.append(best_route)
            else:
                elite_count = population_size // 10
                sorted_pop = sorted(population,
                                      key=lambda ind: -calculate_fitness(ind, distance_matrix, infeasible_penalty))
                best_individuals = sorted_pop[:elite_count]
                new_population_part = generate_unique_population([], population_size - elite_count, num_nodes)
                new_population = best_individuals + new_population_part
            population = new_population
            stagnation_counter = 0
        
        # Broadcast the (possibly updated) population to all processes.
        population = comm.bcast(population, root=0)
        
        # === Distribute the population among processes for GA worker computation ===
        if rank == 0:
            sub_pops = split_list(population, size)
        else:
            sub_pops = None
        local_sub_pop = comm.scatter(sub_pops, root=0)
        
        # Each process works on its chunk:
        local_offspring = ga_worker(local_sub_pop, distance_matrix, infeasible_penalty,
                                    num_tournaments, tournament_size, mutation_rate)
        
        # Gather offspring from all processes at the master.
        offspring_list = comm.gather(local_offspring, root=0)
        
        # === Replacement step on the master ===
        if rank == 0:
            # Flatten the offspring list.
            all_mutated_offspring = [ind for sublist in offspring_list for ind in sublist]
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
        
        # Broadcast the updated population for the next generation.
        population = comm.bcast(population, root=0)
    
    # === Final evaluation on the master ===
    if rank == 0:
        fitness_values = np.array([-calculate_fitness(route, distance_matrix, infeasible_penalty)
                                     for route in population])
        best_idx = np.argmin(fitness_values)
        best_solution = population[best_idx]
        best_solution_native = [int(x) for x in best_solution]
        print("Best Solution:", best_solution_native)
        print(f"Total Distance: {-calculate_fitness(best_solution, distance_matrix, infeasible_penalty):,}")
        print(f"Distributed execution time with {size}n:", time() - startTime)