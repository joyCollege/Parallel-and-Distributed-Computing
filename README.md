# Lab 3: Performance Analysis of Parallel Processing Techniques
## DSAI3202: Parallel and Distributed Computing
## By: Dela Cruz, Joy Anne P. [60301959]

## Overview
This project evaluates the performance of different parallel computing methods (sequential, threading, and multiprocessing) for two computational tasks:

1. **Summation of Random Numbers** (Lab 3.1)
2. **Hyperparameter Tuning for Random Forest** (Lab 3.2)

The performance analysis includes speedup calculations and efficiency comparisons.

---

## Lab 3.1: Summation of Random Numbers

### Description
In this task, we analyze how different parallelization techniques affect the performance of summing a large number of random numbers. We compare:
- **Sequential Execution**
- **Threading** (Multiple threads running in parallel)
- **Multiprocessing** (Multiple processes running in parallel)

### Execution Flow
1. **Sequential Execution:** The baseline execution time is measured by summing 1,000,000 random numbers.
2. **Threading & Multiprocessing:** The task is divided into 2 to 5 parallel executions.
3. **Performance Metrics:**
   - Execution time for each method.
   - Speedup and efficiency analysis.

### Key Functions
- `sequential_case(num_numbers)`: Runs the sequential execution.
- `threading_case(num_threads, num_numbers)`: Executes the summation using multiple threads.
- `multiprocessing_case(num_processes, num_numbers)`: Executes the summation using multiple processes.
- `print_analysis(num_actions, serial_time, parallel_time, parallelized_portion, title)`: Prints performance metrics.

### Output of adding 1000000 numbers
```bash
**********************************************************************
******************** Part 1: Adding 1000000 numbers ********************
********************************************************************** 


Starting the sequential case...
>> Sum of random numbers: 500407908
>> Time taken: 331.5882682800293 milliseconds

Starting all 2 threads...
>> Range 1-500001 finished with sum 249887823
>> Range 500001-1000001 finished with sum 250139532
>> Range 1-500001 finished with sum 250168820
>> Range 500001-1000001 finished with sum 250260232
>> Final sum: 1000456407
>> Time taken: 657.4714183807373 milliseconds

Starting all 2 processes...
>> Range 1-500001 finished with sum 249895902
>> Range 500001-1000001 finished with sum 250288597
>> Range 1-500001 finished with sum 250102691
>> Range 500001-1000001 finished with sum 250430119
>> Final sum: 1000717309
>> Time taken: 469.0127372741699 milliseconds

**************** Threading 2 Performance Analysis ****************
Speadup              0.5043386815151388
Efficiency           0.0840564469191898
Amdhal’s speedup     5.999945610080845
Gustaffson’s speedup 5.999990934931299

**************** Multiprocessing 2 Performance Analysis ****************
Speadup              0.7069920322573102
Efficiency           0.11783200537621837
Amdhal’s speedup     5.999925218772482
Gustaffson’s speedup 5.9999875363067385

Starting all 3 threads...
>> Range 1-333334 finished with sum 166827239
>> Range 333334-666667 finished with sum 166800404
>> Range 1-333334 finished with sum 166687314
>> Range 666667-1000001 finished with sum 167174383
>> Range 333334-666667 finished with sum 166629257
>> Range 666667-1000001 finished with sum 166884032
>> Final sum: 1001002629
>> Time taken: 744.4407939910889 milliseconds

Starting all 3 processes...
>> Range 1-333334 finished with sum 167255421
>> Range 333334-666667 finished with sum 166745469
>> Range 666667-1000001 finished with sum 166806555
>> Range 333334-666667 finished with sum 166866809
>> Range 666667-1000001 finished with sum 166391040
>> Range 1-333334 finished with sum 166708913
>> Final sum: 1000774207
>> Time taken: 341.9511318206787 milliseconds

**************** Threading 3 Performance Analysis ****************
Speadup              0.4454192609493113
Efficiency           0.07423654349155188
Amdhal’s speedup     5.9999519636922365
Gustaffson’s speedup 5.999991993884609

**************** Multiprocessing 3 Performance Analysis ****************
Speadup              0.9696948991352257
Efficiency           0.16161581652253762
Amdhal’s speedup     5.999898288810955
Gustaffson’s speedup 5.999983047847788

Starting all 4 threads...
>> Range 250001-500001 finished with sum 124967670
>> Range 750001-1000001 finished with sum 124980914
>> Range 250001-500001 finished with sum 124922749
>> Range 1-250001 finished with sum 125334740
>> Range 750001-1000001 finished with sum 125116192
>> Range 500001-750001 finished with sum 124992528
>> Range 1-250001 finished with sum 125306375
>> Range 500001-750001 finished with sum 125198422
>> Final sum: 1000819590
>> Time taken: 676.3811111450195 milliseconds

Starting all 4 processes...
>> Range 250001-500001 finished with sum 125182371
>> Range 1-250001 finished with sum 125408561
>> Range 500001-750001 finished with sum 125160868
>> Range 750001-1000001 finished with sum 124942489
>> Range 250001-500001 finished with sum 125331454
>> Range 1-250001 finished with sum 125166554
>> Range 750001-1000001 finished with sum 125053262
>> Range 500001-750001 finished with sum 125204817
>> Final sum: 1001450376
>> Time taken: 208.8003158569336 milliseconds

**************** Threading 4 Performance Analysis ****************
Speadup              0.49023880592806074
Efficiency           0.08170646765467679
Amdhal’s speedup     5.999968278450353
Gustaffson’s speedup 5.999994713047108

**************** Multiprocessing 4 Performance Analysis ****************
Speadup              1.588064016661871
Efficiency           0.2646773361103118
Amdhal’s speedup     5.999903368675347
Gustaffson’s speedup 5.9999838945198425

Starting all 5 threads...
>> Range 800001-1000001 finished with sum 100376682
>> Range 200001-400001 finished with sum 100152422
>> Range 800001-1000001 finished with sum 100206111
>> Range 1-200001 finished with sum 100151963
>> Range 200001-400001 finished with sum 100190296
>> Range 600001-800001 finished with sum 100153746
>> Range 1-200001 finished with sum 100184321
>> Range 400001-600001 finished with sum 100012952
>> Range 600001-800001 finished with sum 99963572
>> Range 400001-600001 finished with sum 100408749
>> Final sum: 1001800814
>> Time taken: 717.9560661315918 milliseconds

Starting all 5 processes...
>> Range 1-200001 finished with sum 100333804
>> Range 200001-400001 finished with sum 100001238
>> Range 600001-800001 finished with sum 100053228
>> Range 800001-1000001 finished with sum 99970775
>> Range 400001-600001 finished with sum 99981579
>> Range 1-200001 finished with sum 100007301
>> Range 600001-800001 finished with sum 100272747
>> Range 800001-1000001 finished with sum 100224910
>> Range 200001-400001 finished with sum 100205848
>> Range 400001-600001 finished with sum 99988218
>> Final sum: 1001039648
>> Time taken: 192.10457801818848 milliseconds

**************** Threading 5 Performance Analysis ****************
Speadup              0.4618503609373412
Efficiency           0.07697506015622353
Amdhal’s speedup     5.999960153343219
Gustaffson’s speedup 5.999993358846432

**************** Multiprocessing 5 Performance Analysis ****************
Speadup              1.726082073112461
Efficiency           0.2876803455187435
Amdhal’s speedup     5.999856782084395
Gustaffson’s speedup 5.999976129777625

```

## Lab 3.2: Hyperparameter Tuning for Random Forest

### Description
This task evaluates different parallelization strategies for hyperparameter tuning of a Random Forest model using a housing price dataset. The comparison includes:
- **Sequential Execution**
- **Threading-Based Grid Search**
- **Multiprocessing-Based Grid Search**
- **Queue-Based Parallel Execution**

### Execution Flow
1. **Data Preprocessing:** The dataset is preprocessed and split into training and validation sets.
2. **Hyperparameter Search:**
   - `n_estimators`: Number of trees in the forest.
   - `max_features`: Number of features to consider at each split.
   - `max_depth`: Maximum depth of the tree.
3. **Performance Metrics:**
   - Execution time for each method.
   - Parallelized portion analysis.

### Key Functions
- `data_preprocessing(csv_path)`: Loads and preprocesses the dataset.
- `sequential_parameter_finder(n_estimators_range, max_features_range, max_depth_range, data)`: Performs sequential hyperparameter search.
- `threading_parameter_finder(n_estimators_range, max_features_range, max_depth_range, data)`: Uses threading for parallel search.
- `multiprocessing_parameter_finder(n_estimators_range, max_features_range, max_depth_range, data)`: Uses multiprocessing for parallel search.
- `queue_parameter_finder(n_estimators_range, max_features_range, max_depth_range, data)`: Uses a queue-based approach for parallel search.
- `print_analysis(num_actions, serial_time, parallel_time, parallelized_portion, title)`: Prints performance metrics.

### Selected run notes
```bash
===================================================================================================
---- the first run ----
===================================================================================================
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


===================================================================================================
---- with transformation AND removing x outliers ----
===================================================================================================
The best parameters {'n_estimators': 25, 'max_features': 'sqrt', 'max_depth': 20} for RMSE = 0.0957066288065848, MAPE: 7.078892942298647%
The multiprocessing execution time is 3.4361608028411865 

===================================================================================================
⭐ ---- with transformation AND removing y outliers WITH more parameters----
===================================================================================================
n_estimators_range = [10, 25, 50, 100, 200, 300, 400, 500, 600, 800]
max_features_range = ['sqrt', 'log2', None, 0.2, 0.5]
max_depth_range = [1, 2, 5, 10, 20, 30, 50, None]
The best parameters {'n_estimators': 500, 'max_features': 0.2, 'max_depth': 30} for RMSE = 0.12027586723667646, MAPE: 8.3359489677376%
The multiprocessing execution time is 77.59755396842957 

===================================================================================================
⭐ ---- with transformation AND removing y outliers WIHTOUT more parameters----
===================================================================================================
The best parameters {'n_estimators': 400, 'max_features': 'log2', 'max_depth': 20} for RMSE = 0.12287539968239682, MAPE: 8.487969424865259%
The sequential execution time is 63.702088356018066 
The best parameters {'n_estimators': 400, 'max_features': 'log2', 'max_depth': 20} for RMSE = 0.12287539968239682, MAPE: 8.487969424865259%
The threading execution time is 24.746341705322266 
The best parameters {'n_estimators': 400, 'max_features': 'log2', 'max_depth': 20} for RMSE = 0.12287539968239682, MAPE: 8.487969424865259%
The multiprocessing execution time is 12.724173784255981 
The best parameters (100, 'sqrt', None) for RMSE = 0.12220846771275232, MAPE: 8.664785338976484%
The queue multiprocessing execution time is 12.652228593826294 

**************** threading_parameter_finder Performance Analysis ****************
Speadup              2.5742022442984966
Efficiency           0.4290337073830828
Amdhal’s speedup     5.948394541994672
Gustaffson’s speedup 5.991324472907605

**************** multiprocessing_parameter_finder Performance Analysis ****************
Speadup              5.006383081221246
Efficiency           0.834397180203541
Amdhal’s speedup     5.900605472882478
Gustaffson’s speedup 5.983155198636087

**************** queue_parameter_finder Performance Analysis ****************
Speadup              5.03485120298109
Efficiency           0.839141867163515
Amdhal’s speedup     5.900051577358773
Gustaffson’s speedup 5.983059737473351
```

## Results and Insights
- **Threading vs. Multiprocessing:**
  - Threading is affected by Python's Global Interpreter Lock (GIL) but can improve performance when tasks involve I/O operations.
  - Multiprocessing bypasses the GIL, providing significant speedup for CPU-bound tasks.
- **Performance Trade-offs:**
  - As the number of parallel processes increases, the efficiency may decrease due to overhead costs.
  - The choice of parallelization technique depends on the nature of the workload.

---

## Installation
```bash
pip install -r requirements.txt
```

---
## Usage
To execute the summation analysis and hyperparameter tuning analysis:
```bash
python3 main.py
```
---


