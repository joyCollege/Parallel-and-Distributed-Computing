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

# 4.2 Working on it...