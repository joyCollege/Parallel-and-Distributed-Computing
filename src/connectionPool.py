from multiprocessing import Semaphore, current_process, Manager
from time import sleep
import random

class ConnectionPool:
    """
    Manages a pool of database connections using a semaphore.

    Attributes:
    max_connections (int): Maximum number of connections available.
    semaphore (Semaphore): Controls access to available connections.
    connections (list): A managed list of available connections.
    """
    def __init__(self, max_connections):
        """
        Initializes the connection pool.

        Parameters:
        max_connections (int): Maximum number of concurrent connections allowed.
        """
        self.semaphore = Semaphore(max_connections)
        self.connections = Manager().list(range(1, max_connections + 1))

    def get_connection(self):
        """
        Acquires a connection from the pool.

        Returns:
        int: The acquired connection ID.
        """
        self.semaphore.acquire()
        return self.connections.pop(0)

    def release_connection(self, conn):
        """
        Releases a connection back to the pool.

        Parameters:
        conn (int): The connection ID to be released.
        """
        self.connections.append(conn)
        self.semaphore.release()

def access_database(connectionPool):
    """
    Simulates a process accessing a database using a connection from the pool.

    Parameters:
    connectionPool (ConnectionPool): The pool managing database connections.

    Behavior:
    - The process waits for a connection.
    - Once acquired, it simulates work by sleeping for a random time.
    - After work is done, the connection is released back to the pool.
    """
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

