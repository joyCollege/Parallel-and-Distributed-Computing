from random import randint
from time import sleep

def simulate_sensor(sensor_id, queue, latest_temperatures, latest_temperatures_lock):
    """
    Simulates a temperature sensor that generates random temperature readings and updates the shared data.

    The function:
    1. Continuously generates a random temperature reading between 15 and 40 degrees.
    2. Puts the sensor ID and temperature reading into the queue.
    3. Uses a lock to safely update the latest temperature for the sensor in a shared dictionary.
    4. Sleeps for 1 second before generating the next reading.

    Args:
        sensor_id (int): The ID of the sensor generating temperature readings.
        queue (Queue): A queue used for storing temperature data.
        latest_temperatures (dict): Dictionary storing the latest temperature readings for each sensor.
        latest_temperatures_lock (RLock): A lock to ensure thread-safe updates to the latest temperatures.

    Returns:
        None
    """
    while True:
        temperature_reading = randint(15, 40)
        queue.put((sensor_id, temperature_reading))

        with latest_temperatures_lock:
            latest_temperatures[f"sensor {sensor_id}"] = temperature_reading

        sleep(1)
