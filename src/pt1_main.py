import random
import time
from queue import Queue
from threading import Thread, RLock
from .pt1_process_temperature import process_temperature
from .pt1_simulate_sensor import simulate_sensor

def lab4_1():
    """
    Main function to simulate temperature sensors and process the temperature data in real time using multithreading.

    The function:
    1. Initializes a queue for temperature data and shared dictionaries for storing the latest and average temperatures.
    2. Uses an RLock to ensure thread-safe access to shared data.
    3. Starts multiple sensor threads that simulate temperature readings and push them into the queue.
    4. Starts a processing thread to calculate and update average temperatures based on the incoming data.
    5. Continuously prints the latest and average temperatures with a 1-second delay.

    Args:
        None

    Prints:
        The latest temperature readings and their corresponding average values every second.
    """
    queue = Queue()
    latest_temperatures = {}
    average_temperatures = {}
    counter = {}

    latest_temperatures_lock = RLock()

    sensors = []
    for i in range(3):
        sensor = Thread(target=simulate_sensor, args=(i, queue, latest_temperatures, latest_temperatures_lock))
        sensors.append(sensor)

    for sensor in sensors:
        sensor.daemon = True
        sensor.start()

    processing_thread = Thread(target=process_temperature, args=(queue, latest_temperatures_lock, average_temperatures, counter), daemon=True)
    processing_thread.start()

    while True:
        with latest_temperatures_lock:
            print(f"The latest temperatures: {latest_temperatures}")
            print(f"The average temperatures: {average_temperatures}\n")
        time.sleep(1)
