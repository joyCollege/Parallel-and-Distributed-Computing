if __name__ == "__main__":
    from src.p3_parallel_fitness import p3_parallel_fitness
    p3_parallel_fitness_time = p3_parallel_fitness()
    print("*"*50,"\n","p3_parallel_fitness time:", p3_parallel_fitness_time, "\n" + "*"*50)

    # from src.p0_sequential import p0_sequential
    # p0_sequential_time = p0_sequential()
    # print("*"*50,"\n","p0_sequential time:", p0_sequential_time, "\n" + "*"*50)
    # 7.81717586517334
    
    # from src.p1_ThreadPoolExecutor import p1_ThreadPoolExecutor
    # p1_ThreadPoolExecutor_time = p1_ThreadPoolExecutor()
    # print("*"*50,"\n","p1_ThreadPoolExecutor_time time:", p1_ThreadPoolExecutor_time, "\n" + "*"*50)
    # # 31.0927996635437

    # from src.p2_PoolStarMap import p2_PoolStarMap
    # p2_PoolStarMap_time = p2_PoolStarMap()
    # print("*"*50,"\n","p2_PoolStarMap_time time:", p2_PoolStarMap_time, "\n" + "*"*50)
    # # 32.868497133255005



    