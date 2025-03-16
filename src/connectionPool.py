from multiprocessing import Semaphore, current_process, Manager
from time import sleep
import random

class ConnectionPool:
    def __init__(self, max_connections):
        self.semaphore = Semaphore(max_connections)
        self.connections = Manager().list(range(1, max_connections + 1))

    def get_connection(self):
        self.semaphore.acquire()
        return self.connections.pop(0)

    def release_connection(self, conn):
        self.connections.append(conn)
        self.semaphore.release()

def access_database(connectionPool):
    """Simulate a process performing a database operation."""
    process_name = current_process().name
    print(f"{process_name} waiting for a connection")
    
    # Acquire a connection 
    conn = connectionPool.get_connection()
    print(f"{process_name} has acquired connection-{conn}.")
    
    # Sleep for a random duration to simulate work
    work_duration = random.randint(1, 10+1)
    sleep(work_duration)
    
    # Release the connection
    connectionPool.release_connection(conn)
    print(f"{process_name} released connection {conn}. Worked for {work_duration}s.")

