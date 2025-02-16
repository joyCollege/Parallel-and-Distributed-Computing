import time
from src.sequential_case import sequential_case
from src.threading_case import threading_case
from src.multiprocessing_case import multiprocessing_case
from src.print_analysis import print_analysis

def lab3_1():
    
    """
    Runs performance tests for different parallelization strategies (sequential, threading, and multiprocessing) 
    over a specified number of iterations (1 million).

    The function:
    1. Executes a sequential case to measure the baseline execution time.
    2. Iterates over a range of thread/process counts (2 to 5) to evaluate the performance of threading and multiprocessing.
    3. Measures and compares the execution times for the threaded and multiprocessing approaches.
    4. Prints analysis of the performance, showing the portion of parallelization achieved in each case.
    
    Args:
        None
    
    Prints:
        Performance analysis for each threading and multiprocessing case, comparing their parallelized portion 
        and execution time relative to the non-parallelized baseline.
    """

    n = 1000000
    print("*"*70)
    print("*"*20, 'Part 1: Adding {n} numbers', "*"*20)
    print("*"*70, "\n")

    ts = sequential_case(num_numbers=n)
    for i in [2, 3, 4, 5]:
        non_parallelized_time = time.time()

        threading_case_parallelized_time = time.time()
        threading_case_time= threading_case(num_threads=i, num_numbers=n)
        threading_case_parallelized_time = (time.time() - threading_case_parallelized_time) 

        
        multiprocessing_case_parallelized_time = time.time()
        multiprocessing_case_time= multiprocessing_case(num_processes=i, num_numbers=n)
        multiprocessing_case_parallelized_time = (time.time() - multiprocessing_case_parallelized_time) 

        non_parallelized_time = (time.time() - non_parallelized_time) 

        print_analysis(num_actions=i, serial_time=ts, 
                parallel_time=threading_case_time, 
                parallelized_portion=threading_case_parallelized_time/(non_parallelized_time-multiprocessing_case_parallelized_time), 
                title=f"Threading {i}")
        print_analysis(num_actions=i, 
                serial_time=ts, 
                parallel_time=multiprocessing_case_time, 
                parallelized_portion=multiprocessing_case_parallelized_time/(non_parallelized_time-threading_case_parallelized_time), 
                title=f"Multiprocessing {i}")

# lab3_1()
'''
Starting the sequential case...
>> Sum of random numbers: 500495857
>> Time taken: 338.0863666534424 milliseconds

**************** Threading 2 Performance Analysis ****************
Speadup              0.9923295903843112
Efficiency           0.16538826506405188
Amdhal’s speedup     5.99991603905863
Gustaffson’s speedup 5.999986006313951

**************** Multiprocessing 2 Performance Analysis ****************
Speadup              1.675926965528571
Efficiency           0.2793211609214285
Amdhal’s speedup     5.999865306713449
Gustaffson’s speedup 5.999977550614945

**************** Threading 3 Performance Analysis ****************
Speadup              0.9676560202260762
Efficiency           0.1612760033710127
Amdhal’s speedup     5.999918124617062
Gustaffson’s speedup 5.999986353916631

**************** Multiprocessing 3 Performance Analysis ****************
Speadup              2.3073382179938395
Efficiency           0.38455636966563994
Amdhal’s speedup     5.999815053133696
Gustaffson’s speedup 5.999969174572104

**************** Threading 4 Performance Analysis ****************
Speadup              1.0243918825201983
Efficiency           0.17073198042003304
Amdhal’s speedup     5.999913325922701
Gustaffson’s speedup 5.9999855541117695

**************** Multiprocessing 4 Performance Analysis ****************
Speadup              2.4702928039356418
Efficiency           0.41171546732260694
Amdhal’s speedup     5.999802780790848
Gustaffson’s speedup 5.9999671290513445

**************** Threading 5 Performance Analysis ****************
Speadup              1.016382832322711
Efficiency           0.16939713872045184
Amdhal’s speedup     5.999914001365943
Gustaffson’s speedup 5.999985666688883

**************** Multiprocessing 5 Performance Analysis ****************
Speadup              3.0726296082824494
Efficiency           0.5121049347137415
Amdhal’s speedup     5.999754383235837
Gustaffson’s speedup 5.999959062196805
'''


from src.data_preprocessing import data_preprocessing
from src.sequential_parameter_finder import sequential_parameter_finder
from src.multiprocessing_parameter_finder import multiprocessing_parameter_finder
from src.threading_parameter_finder import threading_parameter_finder

def lab3_2():
    """
    Part 2: Evaluates and compares different parallelization techniques (sequential, threading, and multiprocessing)
    for hyperparameter tuning of a Random Forest model.

    The function:
    1. Preprocesses the housing price data and splits it into training and validation sets.
    2. Defines the range of hyperparameters for the Random Forest model.
    3. Runs the sequential, threading, and multiprocessing grid search methods to find the best hyperparameters.
    4. Measures the execution times of each method and prints analysis comparing their performance.
    
    Args:
        None
    
    Prints:
        Performance analysis of each parallelization method in terms of execution time and parallelized portion.
    """
    print("\n"*5)
    print("*"*70)
    print("*"*20, 'Part 2: finding best parameters', "*"*20)
    print("*"*70, "\n")

    non_parallized_time = time.time()

    # Preprocess the data and split
    csv_path = './data/housing_prices_data/train.csv'
    data = dict()
    data['X_train_filled'], data['X_val_filled'], data['y_train'], data['y_val'] = data_preprocessing(csv_path)
    
    # Define the parameter ranges
    n_estimators_range = [10, 25, 50, 100, 200, 300, 400, 500, 600, 800]
    max_features_range = ['sqrt', 'log2', None, 0.2, 0.5]
    max_depth_range = [1, 2, 5, 10, 20, 30, 50, None]


    non_parallized_time =  time.time() - non_parallized_time
    
    # Run sequential, threading, and multiprocessing parameter finder
    # sequential_time =  sequential_parameter_finder(n_estimators_range, max_features_range, max_depth_range, data)
    # threading_time = threading_parameter_finder(n_estimators_range, max_features_range, max_depth_range, data)
    multiprocessing_time = multiprocessing_parameter_finder(n_estimators_range[::-1], max_features_range, max_depth_range, data)

    # print_analysis(num_actions = len(n_estimators_range) * len(max_features_range) * len(max_depth_range) ,
    #     serial_time = sequential_time,
    #     parallel_time = threading_time,
    #     parallelized_portion = threading_time / (non_parallized_time+threading_time) ,
    #     title = "threading_parameter_finder"
    #     )
    
    # print_analysis(num_actions = len(n_estimators_range) * len(max_features_range) * len(max_depth_range),
    #     serial_time = sequential_time,
    #     parallel_time = multiprocessing_time,
    #     parallelized_portion = multiprocessing_time / (non_parallized_time+multiprocessing_time),
    #     title = "multiprocessing_parameter_finder"
    #     )
    
lab3_2()

'''
The best parameters {'n_estimators': 100, 'max_features': None, 'max_depth': None} for RMSE = 26057.941851126383, MAPE: 9.868196740754167%
The sequential execution time is 63.36062264442444 

The best parameters {'n_estimators': 100, 'max_features': None, 'max_depth': None} for RMSE = 26057.941851126383, MAPE: 9.868196740754167%
The threading execution time is 25.058303117752075 

The best parameters {'n_estimators': 100, 'max_features': None, 'max_depth': None} for RMSE = 26057.941851126383, MAPE: 9.868196740754167%
The multiprocessing execution time is 12.762624979019165 

**************** threading_parameter_finder Performance Analysis ****************
Speadup              2.528528063001114
Efficiency           0.42142134383351904
Amdhal’s speedup     5.9480532782341395
Gustaffson’s speedup 5.99126660113218

**************** multiprocessing_parameter_finder Performance Analysis ****************
Speadup              4.9645447350043375
Efficiency           0.827424122500723
Amdhal’s speedup     5.8990178870252965
Gustaffson’s speedup 5.982881538095213



---- with transformation AND removing x outliers ----
The best parameters {'n_estimators': 25, 'max_features': 'sqrt', 'max_depth': 20} for RMSE = 0.0957066288065848, MAPE: 7.078892942298647%
The multiprocessing execution time is 3.4361608028411865 




----- with transformation ONLY ----
The best parameters {'n_estimators': 400, 'max_features': None, 'max_depth': 20} for RMSE = 0.13632892372048172, MAPE: 9.565758459583686%
The sequential execution time is 63.19388961791992 
The best parameters {'n_estimators': 400, 'max_features': None, 'max_depth': 20} for RMSE = 0.13632892372048172, MAPE: 9.565758459583686%
The threading execution time is 24.349693059921265 
The best parameters {'n_estimators': 400, 'max_features': None, 'max_depth': 20} for RMSE = 0.13632892372048172, MAPE: 9.565758459583686%
The multiprocessing execution time is 12.777265310287476 

>> threading_parameter_finder Performance Analysis >>
Speadup              2.5952643206798705
Efficiency           0.4325440534466451
Amdhal’s speedup     5.946629014493024
Gustaffson’s speedup 5.9910250016644895

>> multiprocessing_parameter_finder Performance Analysis >>
Speadup              4.945807109995599
Efficiency           0.8243011849992664
Amdhal’s speedup     5.8992645453760435
Gustaffson’s speedup 5.982924065559509




---- with transformation AND removing y outliers ----
The best parameters {'n_estimators': 400, 'max_features': 'log2', 'max_depth': 20} for RMSE = 0.12287539968239682, MAPE: 8.487969424865259%
The sequential execution time is 62.103671073913574 
The best parameters {'n_estimators': 400, 'max_features': 'log2', 'max_depth': 20} for RMSE = 0.12287539968239682, MAPE: 8.487969424865259%
The threading execution time is 21.89735746383667 
The best parameters {'n_estimators': 400, 'max_features': 'log2', 'max_depth': 20} for RMSE = 0.12287539968239682, MAPE: 8.487969424865259%
The multiprocessing execution time is 12.361319541931152 

**************** threading_parameter_finder Performance Analysis ****************
Speadup              2.836126284939968
Efficiency           0.4726877141566614
Amdhal’s speedup     5.93889428559979
Gustaffson’s speedup 5.989710927411458

**************** multiprocessing_parameter_finder Performance Analysis ****************
Speadup              5.024032496146557
Efficiency           0.8373387493577594
Amdhal’s speedup     5.892765780113264
Gustaffson’s speedup 5.981802395702095



---- with transformation AND removing y outliers with more parameters----
n_estimators_range = [10, 25, 50, 100, 200, 300, 400, 500, 600, 800]
max_features_range = ['sqrt', 'log2', None, 0.2, 0.5]
max_depth_range = [1, 2, 5, 10, 20, 30, 50, None]
The best parameters {'n_estimators': 500, 'max_features': 0.2, 'max_depth': 30} for RMSE = 0.12027586723667646, MAPE: 8.3359489677376%
The multiprocessing execution time is 77.59755396842957 

'''
