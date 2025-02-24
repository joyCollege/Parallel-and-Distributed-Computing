def process_temperature(queue):
    global counter
    global latest_temperatures_lock
    global average_temperatures

    while True:
        sensor_id, temperature = queue.get() 

        with latest_temperatures_lock:
            counter[sensor_id] += 1
            if average_temperatures[sensor_id] is None:
                average_temperatures[sensor_id] = temperature
            else:
                total = (average_temperatures[sensor_id] * (counter[sensor_id] - 1)) + temperature
                average_temperatures[sensor_id] = total / counter[sensor_id]

        queue.task_done()