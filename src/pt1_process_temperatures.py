
import time
from queue import Queue
from pt1_global_vars import latest_temperatures, temperature_averages

def process_temperatures():
    temperature_queue = Queue()
    
    while True:
        if "temperature" in latest_temperatures:
            # Add the latest temperature to the queue
            temperature_queue.put(latest_temperatures["temperature"])
            
            # Ensure we only keep a certain number of recent readings in the queue (e.g., 10)
            if temperature_queue.qsize() > 10:
                temperature_queue.get()
            
            # Calculate the average temperature
            avg_temp = sum(list(temperature_queue.queue)) / temperature_queue.qsize()
            
            # Update the global dictionary with the average temperature
            temperature_averages["average_temperature"] = avg_temp
        
        time.sleep(1)  # Check every second