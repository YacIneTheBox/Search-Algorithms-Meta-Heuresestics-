# 🛠️Project Overview

This project is a command-line tool for solving a Traveling Salesman–type problem on a set of Algerian cities loaded from a CSV file. It implements several metaheuristic and heuristic algorithms: random search, local 2‑OPT search, hill climbing, nearest neighbor, simulated annealing, and tabu search, Genetic Search ,all evaluated with a cyclic tour distance function. The program prints the best tour distance found and the visiting order of cities for the selected algorithm.

​
## Features 

  ⚪ Load cities (name, latitude, longitude, and projected coordinates) from a CSV file, with “Algiers” forced as the starting city when present.

  ⚪ Compute Euclidean distances and total tour length, including the return to the starting city.

  ⚪ Compare multiple algorithms for route optimization:     
  ```
      👾 Random Search
      👾 2‑OPT Local Search
      👾 Hill Climbing
      👾 Nearest Neighbor
      👾 Simulated Annealing (with 2‑OPT perturbations)
      👾 Tabu Search (with tabu tenure and aspiration criteria).
      👾 Genetic Search
  ```

## CLI Menu Usage

When the script runs, an interactive CLI menu is displayed in the terminal.

​
Available options are:
```
    1 – Random search (best of N iterations).

    2 – Local 2‑OPT search.

    3 – Hill Climbing (2‑OPT neighbors).

    4 – Nearest Neighbor (Plus Proche Voisin).

    5 – Simulated Annealing.

    6 – Tabu Search.

    7 - Genetic Search

    s – Show total distance of the original city order.

    q – Quit the program.
```
    
After choosing an option, the program runs the selected algorithm and prints the total distance and the city order on a single tour line.

​
Requirements
```
  Python 3.x
  Standard library modules: csv, random, math, copy, sys, collections.deque (all already included with Python).

  A CSV file with city data in the format: name,lat,lon,x,y and a header line (default filename in the code is algeria_20_cities_xy.csv).
```
How to Run (Linux / macOS)

    Ensure Python 3 is installed (python3 --version).

    Place main.py and the CSV file (e.g., algeria_20_cities_xy.csv) in the same directory.

In a terminal, move into the project directory:

    cd path/to/project

Run the script:

    python3 main.py

How to Run (Windows)

    Make sure Python 3 is installed and added to your PATH (python --version).

    Put main.py and the CSV file (e.g., algeria_20_cities_xy.csv) in the same folder.

Open Command Prompt or PowerShell and navigate to that folder:

    cd path\to\project

Execute the script:

    python main.py

Use the CLI menu to choose an algorithm and inspect the printed tour and distance.
