def process_temperature(queue, latest_temperatures_lock, average_temperatures, counter):
    """
    Continuously processes temperature data from the queue and updates the average temperature for each sensor.

    The function:
    1. Retrieves sensor ID and temperature from the queue.
    2. Uses a lock to ensure thread-safe updates to shared data.
    3. Maintains a count of readings per sensor.
    4. Updates the running average temperature for each sensor.
    5. Marks the queue task as done.

    Args:
        queue (Queue): A queue containing tuples of (sensor_id, temperature).
        latest_temperatures_lock (RLock): A lock to ensure thread-safe access to shared temperature data.
        average_temperatures (dict): Dictionary storing the average temperature for each sensor.
        counter (dict): Dictionary storing the number of readings received per sensor.

    Returns:
        None
    """
    while True:
        sensor_id, temperature = queue.get()

        with latest_temperatures_lock:
            if sensor_id not in counter:
                counter[sensor_id] = 0
            if sensor_id not in average_temperatures:
                average_temperatures[f"sensor {sensor_id}"] = 0

            counter[sensor_id] += 1
            total = (average_temperatures[f"sensor {sensor_id}"] * (counter[sensor_id] - 1)) + temperature
            average_temperatures[f"sensor {sensor_id}"] =  round(total / counter[sensor_id],2)

        queue.task_done()
