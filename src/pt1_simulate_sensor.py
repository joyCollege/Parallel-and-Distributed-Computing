from random import randint
from time import time
from pt1_global_vars import latest_temperatures

def simulate_sensor():
    while True:
        # Generate a random temperature
        temp = random.randint(15, 40)
        # Update the global dictionary with the new temperature reading
        latest_temperatures["temperature"] = temp
        time.sleep(1)  # Wait for 1 second before next reading