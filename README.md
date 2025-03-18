# Assignment 1 - Part 2
## DSAI3202 - Parallel and Distributed Computing
## By: Dela Cruz, Joy Anne 60301959

in the calculate_fitness i did not put negative since we are trying to find the min in the genetic_algorithm_trial

at this point i changed the total distance to print  add commas and to give non negative

Running with normal parameter lead to stagnation and increasing to , number_tournaments=7,tournament_size=20 did not do much to fix the stagnation the Total Distance: is still 1,224.0

i changed the parameters as an attempt to top stagnation but the total distance is the same and theres stil stagnation
        # Experimental Parameters 
        num_nodes = distance_matrix.shape[0]
        population_size     = 10000 # default = 10000
        num_tournaments     = 20    # default = 4  
        tournament_size     = 7     # default = 3 
        mutation_rate       = 0.5   # default = 0.1
        num_generations     = 200   # default = 200
        infeasible_penalty  = 1e6   # default = 1e6  
        stagnation_limit    = 5     # default = 5  
  
i changed the stagnation but it actually got worst with a distance of 2,416 to imreturning ti back but this was the attempt
                print(f"Regenerating population at generation {generation} due to stagnation")
                
                # Keep the top 10% best individuals
                elite_count = population_size // 10  # 10% of population
                best_individuals = sorted(population, key=lambda ind: calculate_fitness(ind, distance_matrix, infeasible_penalty))[:elite_count]
                
                new_population = generate_unique_population(population_size - len(best_individuals), num_nodes)
                population = best_individuals + new_population
                stagnation_counter = 0
                continue  # Skip rest of loop for this generation

 i experimented with using the new stagnant function and and a very high num_tournaments 500 and there are still stagnation and the total distance improved now being 1,211.0, adding more tournament_size 1000 did not improve the results. since theres still so much stagnation, i make the stgantion and mutation extreme giving a Total Distance: 1,074.0 which is the best one so far
        num_nodes = distance_matrix.shape[0]
        population_size     = 10000 # default = 10000
        num_tournaments     = 500   # default = 4  
        tournament_size     = 1000  # default = 3 
        mutation_rate       = 1   # default = 0.1
        num_generations     = 200   # default = 200
        infeasible_penalty  = 1e6   # default = 1e6  
        stagnation_limit    = 2     # default = 5  