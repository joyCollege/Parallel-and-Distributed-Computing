"""
Main entry point for the maze runner game.
"""

import argparse
from src.game import run_game
from src.explorer import Explorer


def main():
    parser = argparse.ArgumentParser(description="Maze Runner Game")
    parser.add_argument("--type", choices=["random", "static"], default="random",
                        help="Type of maze to generate (random or static)")
    parser.add_argument("--width", type=int, default=30,
                        help="Width of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--height", type=int, default=30,
                        help="Height of the maze (default: 30, ignored for static mazes)")
    parser.add_argument("--auto", action="store_true",
                        help="Run automated maze exploration")
    parser.add_argument("--visualize", action="store_true",
                        help="Visualize the automated exploration in real-time")
    
    args = parser.parse_args()
    
    if args.auto:
        # Create maze and run automated exploration
        from src.maze import create_maze
        maze = create_maze(args.width, args.height, args.type)
        explorer = Explorer(maze, visualize=args.visualize)
        time_taken, moves = explorer.solve()
        print(f"Maze solved in {time_taken:.2f} seconds")
        print(f"Number of moves: {len(moves)}")
        if args.type == "static":
            print("Note: Width and height arguments were ignored for the static maze")
    else:
        # Run the interactive game
        run_game(maze_type=args.type, width=args.width, height=args.height)

def basic_static():
    '''
    Runs the explorer from explorer.py on a static map 

    Result of the run:
        === Maze Exploration Statistics ===
        Total time taken: 0.0018935204 seconds
        Total moves made: 1279
        Number of backtrack operations: 0
        Average moves per second: 675461.45
        ==================================

        Maze solved in 0.00 seconds
        Number of moves: 1279
    '''
    from src.explorer import Explorer
    from src.maze import create_maze

    # Create maze and explorer
    maze = create_maze(0, 0, "static")
    explorer = Explorer(maze, visualize=False)

    # Run the explorer
    time_taken, moves = explorer.solve()
    print(f"Maze solved in {time_taken:.2f} seconds")
    print(f"Number of moves: {len(moves)}")

if __name__ == "__main__":
    # main()
    basic_static()