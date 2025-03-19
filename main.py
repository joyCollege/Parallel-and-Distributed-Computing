from time import time
from src.calc_print_analysis import calc_print_analysis

if __name__ == "__main__":
    from src.updated_GA_trial import updated_GA_trial
    updated_GA_trial_time = time()
    updated_GA_trial(num_generations=100)
    updated_GA_trial_time = time() - updated_GA_trial_time
    print("*"*200,"\n","updated_GA_trial time:", updated_GA_trial_time, "\n" + "*"*200)
    
    # from src.p1_starMap_fitnessOnly import p1_starMap_fitnessOnly
    # p1_starMap_fitnessOnly_time = time()
    # p1_starMap_fitnessOnly(num_generations=100)
    # p1_starMap_fitnessOnly_time = time() - p1_starMap_fitnessOnly_time
    # print("*"*200,"\n","p1_starMap_fitnessOnly time:", p1_starMap_fitnessOnly_time, "\n" + "*"*200)
    # calc_print_analysis(updated_GA_trial_time, p1_starMap_fitnessOnly_time, "p1_starMap_fitnessOnly")

    from src.p2_starMapAsync_largerWorker import p2_starMapAsync_largerWorker
    p2_starMapAsync_largerWorker_time = time()
    p2_starMapAsync_largerWorker(num_generations=100)
    p2_starMapAsync_largerWorker_time = time() - p2_starMapAsync_largerWorker_time
    print("*"*200,"\n","p2_starMapAsync_largerWorker time:", p2_starMapAsync_largerWorker_time, "\n" + "*"*200)
    # calc_print_analysis(updated_GA_trial_time, p2_starMapAsync_largerWorker_time, "p2_starMapAsync_largerWorker")

    from src.p3_starMapAsync_stagnation import p3_starMapAsync_stagnation
    p3_starMapAsync_stagnation_time = time()
    p3_starMapAsync_stagnation(num_generations=100)
    p3_starMapAsync_stagnation_time = time() - p3_starMapAsync_stagnation_time
    print("*"*200,"\n","p3_starMapAsync_stagnation time:", p3_starMapAsync_stagnation_time, "\n" + "*"*200)
    # calc_print_analysis(updated_GA_trial_time, p3_starMapAsync_stagnation_time, "p2_starMapAsync_largerWorker")


    print("*"*200,"\n","updated_GA_trial time:", updated_GA_trial_time)
    # print("p1_starMap_fitnessOnly time:", p1_starMap_fitnessOnly_time)
    print("p2_starMapAsync_largerWorker time:", p2_starMapAsync_largerWorker_time)
    print("p3_starMapAsync_stagnation time:", p3_starMapAsync_stagnation_time, "\n" + "*"*200)

    # calc_print_analysis(updated_GA_trial_time, p1_starMap_fitnessOnly_time, "p1_starMap_fitnessOnly")
    calc_print_analysis(updated_GA_trial_time, p2_starMapAsync_largerWorker_time, "p2_starMapAsync_largerWorker")
    calc_print_analysis(updated_GA_trial_time, p3_starMapAsync_stagnation_time, "p2_starMapAsync_largerWorker")
