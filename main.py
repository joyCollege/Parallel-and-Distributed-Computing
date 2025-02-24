import random
import time
from queue import Queue
from threading import Thread, RLock
from src.pt1_process_temperature import process_temperature
from src.pt1_simulate_sensor import simulate_sensor

if __name__ == "__main__":
    queue = Queue()  
    latest_temperatures = {}
    average_temperatures = {}
    counter = 0

    latest_temperatures_lock = RLock()

    sensors = []
    for i in range(3):
        sensor = Thread(target=simulate_sensor, args=(i, queue))
        sensors.append(sensor)

    # Start the sensor threads
    for sensor in sensors:
        sensor.daemon = True  # Daemon threads terminate when main program exits
        sensor.start()

    # Start the processing thread
    processing_thread = Thread(target=process_temperature, args=(queue,), daemon=True)
    processing_thread.start()

    # Continuously print the temperatures
    while True:
        with latest_temperatures_lock:
            print(f"The latest temperatures: {latest_temperatures}")
            print(f"The average temperatures: {average_temperatures}\n")
        time.sleep(1)
