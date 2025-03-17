# Parallel and Distributed Computing Repository
## By: Dela Cruz, Joy Anne P. [60301959]

This repository contains coursework, assignments, and lab materials for the DSAI3202 Parallel and Distributed Computing course. Below is an overview of the structure and contents of the repository.

## Table of Contents

### 1. Assignments 
- **Assignment 1.1:** Parallel Processing Techniques and Performance Analysis
- **Assignment 1.2:** Optimization of travelling salesman Problem (in progress...)

### 2. Labs
- **Lab 1:** Machine Learning Pipeline with Parallel Processing
- **Lab 2:** Performance Analysis of Parallel Processing Techniques
- **Lab 3:** Parallel Summation and Hyperparameter Tuning
- **Lab 4:** Temperature Sensor Simulation & Image Processing Optimization
- **Lab 5:** Distributed Computation using MPI

### 3. Lab tutorials
- **Celery Task Queue Implementation**: Distributed task processing using Celery.
- **Distributed Lab**: Various experiments related to distributed computing.
- **Experimental Branch**: Contains additional testing and advanced optimizations.

## 1. Assignments 

### Assignment 1 part1.1: Parallel Processing Techniques and Performance Analysis
This assignment explores different parallel processing methods for computational tasks, including:
- Sequential Processing
- Threading
- Multiprocessing (Direct Processes, Pools, and Async Processing)
- Performance Metrics Analysis (Speedup, Efficiency, Amdahl’s and Gustafson’s Laws)

### Assignment 1 part1.2: Advanced Parallel Computing Implementations
This section contains optimizations and more complex implementations, including:
- Database Connection Pools using Semaphores
- Load Balancing Techniques
- Advanced Task Scheduling for Parallel Execution

### Assignment 1 part2 (in progress...)

## 2. Labs

### Lab 1: Machine Learning Pipeline
- Implements a pipeline using the Iris dataset with training and evaluation in a parallelized manner.
- Key functions:
  - `load_data()`, `split_data()`, `train_model()`, `evaluate_model()`.

### Lab 2: Performance Analysis of Parallel Processing Techniques
- Comparison of different parallel computing models:
  - Sequential Execution
  - Threading
  - Multiprocessing
  - Advanced Threading & Multiprocessing Techniques
- Performance evaluation using Amdahl’s and Gustafson’s laws.

### Lab 3: Parallel Summation and Hyperparameter Tuning
#### **3.1 Summation of Random Numbers**
- Parallelized summation using threading and multiprocessing.
- Performance analysis and scalability metrics.

#### **3.2 Hyperparameter Tuning for Random Forest**
- Uses different parallelization strategies for model training and optimization.
- Methods include:
  - Sequential Execution
  - Thread-Based Grid Search
  - Multiprocessing Grid Search
  - Queue-Based Execution

### Lab 4: Temperature Sensor Simulation & Image Processing Optimization
#### **4.1 Temperature Sensor Simulation**
- Simulates temperature readings with multithreading.
- Uses real-time data updates and thread-safe data handling.

#### **4.2 Image Processing and Model Optimization**
- Implements parallel processing techniques for feature extraction.
- Filters include Entropy, Gaussian, Sobel, Gabor, Hessian, and Prewitt.
- Compares threading, multiprocessing, and hybrid approaches.
- Hyperparameter tuning with parallelized execution.

### Lab 5: Distributed Computation using MPI
- Uses **Message Passing Interface (MPI)** to distribute computation across multiple machines.
- Includes a **distributed square computation** example using MPI.Scatter(), MPI.isend(), and MPI.irecv().
- Implements an `scp_and_run.sh` script for file distribution and execution across clusters.

## 3. Lab tutorials

### Celery Task Queue Implementation (in progress...)
- Implements Celery for distributed task processing.
- Uses RabbitMQ or Redis as a message broker.
- Optimizes asynchronous execution of tasks.

### Distributed Lab
- Various experiments and benchmarks for distributed computing.
- Includes different task scheduling techniques.

### Experimental Branch
- Contains additional optimizations, advanced parallel execution models, and new experiments.

## Installation
Ensure Python and dependencies are installed:
```bash
pip install -r requirements.txt
```

## Summary
This repository provides an in-depth study of **parallel and distributed computing**, covering theoretical concepts, implementation strategies, and performance analysis. The coursework explores different computing paradigms, real-world applications, and scalability challenges.