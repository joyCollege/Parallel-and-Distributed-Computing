from mpi4py import MPI
from src.explorer import Explorer
from src.maze import create_maze

if __name__ == "__main__":
    '''
    Runs the explorer from explorer.py on a static map on 4 machines using MPI4Py
    Uses different is_stuck definitions. 
    '''
    comm = MPI.COMM_WORLD
    rank =comm.Get_rank()
    size =comm.Get_size()

    maze = create_maze(0, 0, "static")
    explorer = Explorer(maze, visualize= False, stuck_def= rank % 4)
    time_taken, moves = explorer.solve()
    num_moves = len(moves)
    backtracks = explorer.backtrack_count

    # Others sends metrics to root
    result = (rank, time_taken, num_moves, backtracks )
    results= comm.gather(result, root = 0)

    # Root compares results
    if rank == 0:
        print("\n=== Summary of Results ===")
        best = None

        for r in results:
            if best is None:
                best = r
            else:
                # Prioritize time, then moves
                if r[1] <= best[1]:
                    best = r
        for this_rank, this_time, this_move, this_backtracks in results:
            print(f"Rank {this_rank}, is_stuck definition {this_rank % 4}, Time = {this_time:.10f}s, Moves = {this_move}, Backtracks = {this_backtracks}")
        
        print(f"\nFastest run: Rank {best[0]} Time =  {best[1]:.10f}s, Moves = {best[2]}, Backtracks = {best[3]}")

