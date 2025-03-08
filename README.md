# 4.1 Temperature Sensor Simulation Program

This program simulates temperature sensors that periodically generate random temperature readings. The readings are then processed to calculate and update the average temperature for each sensor in real time using multithreading.

## Features
- Simulates multiple temperature sensors.
- Each sensor generates random temperature readings at regular intervals.
- The latest temperature readings from each sensor are displayed and updated in real-time.
- The program calculates and updates the average temperature for each sensor.
- Thread-safe data handling using locks to ensure consistency.

## Components

1. **`simulate_sensor`**: 
   - Simulates the behavior of a temperature sensor.
   - Generates random temperature readings between 15 and 40 degrees Celsius.
   - Puts the sensor ID and temperature reading into a queue.
   - Updates the latest temperature for each sensor in a shared dictionary.
   
2. **`process_temperature`**: 
   - Processes temperature readings from the queue.
   - Updates the average temperature for each sensor based on the received readings.
   - Uses a lock to ensure thread-safe updates to the shared data.
   
3. **Main Program**:
   - Initializes multiple sensor threads that simulate the sensors.
   - Starts a separate processing thread that updates the average temperature for each sensor.
   - Prints the latest and average temperatures every second.

## Requirements

- Python 3.x
- `threading` module (built-in)
- `queue` module (built-in)

## Usage

1. Clone the repository or copy the code files to your project folder.
2. Run the program by executing the Python file.

```bash
python main.py
```

3. The program will output the latest and average temperatures for each sensor every second.

## Example Output

```
The latest temperatures: {'sensor 0': 25, 'sensor 1': 30, 'sensor 2': 22}
The average temperatures: {'sensor 0': 24.5, 'sensor 1': 30.0, 'sensor 2': 22.0}
```

## How It Works

1. **Sensors**: 
   - The program initializes 3 sensors. Each sensor generates a random temperature between 15 and 40 degrees Celsius every second.
   
2. **Data Sharing and Locking**:
   - The `latest_temperatures` dictionary holds the most recent temperature reading for each sensor.
   - The `latest_temperatures_lock` ensures that updates to this dictionary are thread-safe.
   
3. **Processing Temperature**:
   - The `process_temperature` function retrieves the temperature data from the queue and updates the average temperature for each sensor in the `average_temperatures` dictionary. It also uses a lock to ensure thread-safe updates.

## Concurrency

- The program uses multithreading to simulate multiple sensors and process temperature data concurrently.
- Each sensor runs in its own thread, and the data processing happens in a separate thread to maintain performance.

## License

This project is open-source and available under the MIT License.

Here's the updated README.md with the requested changes to the image processing sections:

---

# 4.2 Image Processing and Model Optimization

## Overview
This project focuses on image processing techniques for feature extraction and hyperparameter optimization using sequential, threading, and multiprocessing approaches. The dataset used contains brain tumor images labeled as 'yes' and 'no'.

## Features
- **Image Preprocessing**: Applies filters like Entropy, Gaussian, Sobel, Gabor, Hessian, and Prewitt for feature extraction.
- **Parallel Processing**: Uses multiprocessing and threading to speed up image processing and model training.
- **Hyperparameter Tuning**: Implements strategies for optimizing model parameters with sequential, threading, and multiprocessing methods.
- **Data Storage**: Saves and loads processed images using pickle for efficient storage and retrieval.

## Installation
Make sure you have Python installed along with the required dependencies. You can install the dependencies by running:

```sh
pip install -r requirements.txt
```

## Usage

### 1. Load and Process Images
```python
from src.read_path import read_path
yes_images, no_images = read_path()
```

### 2. Sequential Image Processing (Original Run)
The sequential run serves as the baseline to compare the speedup and efficiency of other methods. It processes the images one by one without parallelization.
```python
from src.sequential_processing import sequential_run
execution_time, yes_processed, no_processed = sequential_run(yes_images, no_images)
```

### 3. Parallel Image Processing with Pooling (Multiprocessing Pool)
This approach places everything into a `multiprocessing.Pool` for parallel processing. It splits the task and processes multiple filters concurrently.
```python
from src.pooling_processing import pooling_run
execution_time, yes_processed, no_processed = pooling_run(yes_images, no_images)
```

### 4. Hessian Filter Processing (Concurrent Futures ProcessPoolExecutor)
The `hessian_run` method uses `concurrent.futures.ProcessPoolExecutor` to divide the image processing task into smaller chunks, each processed by a different process. This approach optimizes the Hessian filter computation.
```python
from src.hessian_processing import hessian_run
execution_time, yes_processed, no_processed = hessian_run(yes_images, no_images)
```

### 5. Thread-Based Image Processing (Using ProcessPoolExecutor and ThreadPoolExecutor)
For shorter runtime filters (like Gaussian, Sobel, Prewitt, and Gabor), threading is used with `ThreadPoolExecutor`. Since these filters are more I/O-bound and quick to execute, threading helps improve efficiency by parallelizing the task.
```python
from src.thread_processing import thread_run
execution_time, yes_processed, no_processed = thread_run(yes_images, no_images)
```

### 6. Split-Based Processing (One Filter per Process)
In the split attempt, each filter is assigned to a separate process to maximize parallelism. This method divides the workload into individual filters, with each one processed independently.
```python
from src.split_processing import split_run
execution_time, yes_processed, no_processed = split_run(yes_images, no_images)
```

### 7. Hybrid Image Processing (Thread and Process Combination)
The hybrid approach combines both threading and multiprocessing. Some filters are processed using threads (for I/O-bound tasks), while others are handled by processes (for CPU-bound tasks).
```python
from src.hybrid_processing import hybrid_run
execution_time, yes_processed, no_processed = hybrid_run(yes_images, no_images)
```

### 8. Save and Load Processed Images
```python
from src.file_handling import save_processed_images, load_processed_images

save_processed_images(yes_processed, "yes_processed.pkl")
loaded_images = load_processed_images("yes_processed.pkl")
```

### 9. Model Training with Hyperparameter Optimization
```python
from src.parameter_optimization import multiprocessing_parameter_finder

best_params = multiprocessing_parameter_finder(n_estimators_range, max_features_range, max_depth_range, data)
```

## Performance Comparison
The execution times of different processing methods are compared:
- **Sequential Processing** (baseline run)
- **Threading Processing** (ThreadPoolExecutor)
- **Multiprocessing Processing** (Multiprocessing Pool)
- **Hessian Filter with ProcessPoolExecutor**
- **Split-Based Processing**
- **Hybrid Processing** (Thread and Process Combination)

## License
This project is open-source and available for modification and distribution.

---

Let me know if you need further adjustments!