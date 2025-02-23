# main.py
import threading
from src.pt1_sensor_simulation import simulate_sensor
from src.pt1_process_temperatures import process_temperatures

if __name__ == "__main__":
    # Create two threads to run both functions simultaneously
    sensor_thread = threading.Thread(target=simulate_sensor)
    processing_thread = threading.Thread(target=process_temperatures)
    
    sensor_thread.start()
    processing_thread.start()
    
    sensor_thread.join()
    processing_thread.join()
