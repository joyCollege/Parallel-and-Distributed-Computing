from random import randint
from time import sleep


def simulate_sensor(sensor_id, queue):
    global latest_temperatures_lock
    global latest_temperatures
    
    while True:
        temperature_reading = randint(15, 40)
        queue.put((sensor_id, temperature_reading))  

        with latest_temperatures_lock:
            latest_temperatures[sensor_id] = temperature_reading

        sleep(1)  