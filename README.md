# Lab 2: Performance Analysis of Parallel Processing Techniques
## DSAI3202: Parallel and Distributed Computing
## By: Dela Cruz, Joy Anne P. [60301959]

## Overview
This project compares the execution performance of different computing techniques:
- **Sequential execution**
- **Threading**
- **Advanced threading**
- **Multiprocessing**
- **Advanced multiprocessing**

The script runs a computational task multiple times (`n = 1,000,000`) and measures execution time, speedup, efficiency, and scalability using Amdahl’s and Gustafson’s laws.

## Features
- Runs a computation-intensive task using different execution models.
- Measures performance in terms of speedup and efficiency.
- Uses Amdahl’s and Gustafson’s laws to analyze scalability.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
Run the script using:
```bash
python3 main.py
```

## Performance Metrics
1. **Speedup:** Measures performance improvement of parallel execution vs. sequential execution.
2. **Efficiency:** Computes how effectively parallel processing utilizes resources.
3. **Amdahl’s Law:** Predicts theoretical speedup based on the parallelizable portion of a task.
4. **Gustafson’s Law:** Analyzes how performance scales with additional processors.

## Modules
| Module | Description |
|---------|-------------|
| `sequential_case.py` | Runs the task sequentially. |
| `threading_case.py` | Runs the task using threading. |
| `advanced_threading_case.py` | Uses optimized threading techniques. |
| `multiprocessing_case.py` | Runs the task using multiprocessing. |
| `advanced_multiprocessing_case.py` | Uses optimized multiprocessing techniques. |
| `calc_speadup.py` | Computes speedup factor. |
| `calc_efficiency.py` | Calculates parallel efficiency. |
| `calc_amdahl.py` | Computes theoretical speedup using Amdahl’s law. |
| `calc_gustafson.py` | Computes theoretical speedup using Gustafson’s law. |

## Output
```bash
**************** Running 1000000 times ****************
Serial case taken: 576.592206954956 milliseconds
Threading case taken: 577.9819488525391 milliseconds
Advanced Threading case taken: 592.4191474914551 milliseconds
Multiprocessing case taken: 365.28849601745605 milliseconds
Advanced Multiprocessing case taken: 180.54986000061035 milliseconds

**************** Threading Performance Analysis ****************
Speadup              0.9975955271607668
Efficiency           0.4987977635803834
Amdhal’s speedup     -0.0020805089382344624
Gustaffson’s speedup 1.0120223641961656

**************** Advanced Threading Performance Analysis ****************
Speadup              0.9732842184397369
Efficiency           0.24332105460993422
Amdhal’s speedup     2.25
Gustaffson’s speedup 2.666666666666667

**************** Multiprocessing Performance Analysis ****************
Speadup              1.5784570640500062
Efficiency           0.7892285320250031
Amdhal’s speedup     1.7142857142857142
Gustaffson’s speedup 3.5

**************** Advanced Multiprocessing Performance Analysis ****************
Speadup              3.193534500403417
Efficiency           0.7983836251008543
Amdhal’s speedup     2.25
```
