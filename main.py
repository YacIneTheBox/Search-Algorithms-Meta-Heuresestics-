import csv
import random
import math
import copy
import sys
from collections import deque


class City:
    def __init__(self, name, lat, lon, x, y):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.x = x
        self.y = y

def load_cities(path):
    cities = []
    sCity = "Algiers"
    try:
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                name, lat, lon, x, y = row
                city = City(name, float(lat), float(lon), float(x), float(y))
                cities.append(city)



    except FileNotFoundError:
        print(f"File not found: {path}")
        sys.exit(1)

    finally:
        random.shuffle(cities)
        index = next(i for i, city in enumerate(cities) if city.name == sCity)
        cities[0],cities[index] = cities[index],cities[0] 
    return cities

def distance(city1, city2):
    x1, y1 = city1.x, city1.y
    x2, y2 = city2.x, city2.y
    return math.hypot(x2 - x1, y2 - y1)

def total_distance(route):
    if not route:
        return 0.0
    dist = 0.0
    for i in range(len(route) - 1):
        dist += distance(route[i], route[i + 1])
    # return to start
    dist += distance(route[-1], route[0])
    return dist

# Random search
def random_search(cities, iterations=10000, start_city_name="Algiers"):
    clon = copy.deepcopy(cities)
    best_path = list(clon)
    shortest = float('inf')

    for _ in range(iterations):
        random.shuffle(clon)
        # ensure start city is first
        try:
            idx = next(i for i, c in enumerate(clon) if c.name == start_city_name)
            clon[0], clon[idx] = clon[idx], clon[0]
        except StopIteration:
            pass
        d = total_distance(clon)
        if d < shortest:
            shortest = d
            best_path = list(clon)
    return shortest, best_path

# 2-OPT local search
def local_2opt_search(cities, start_city_name="Algiers"):
    best = copy.deepcopy(cities)
    try:
        idx = next(i for i, c in enumerate(best) if c.name == start_city_name)
        best[0], best[idx] = best[idx], best[0]
    except StopIteration:
        pass

    improved = True
    best_distance = total_distance(best)
    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best)):
                if j - i == 1:
                    continue
                new_route = best[:i] + best[i:j][::-1] + best[j:]
                new_distance = total_distance(new_route)
                if new_distance < best_distance:
                    best = new_route
                    best_distance = new_distance
                    improved = True
        # loop until no improvement
    return best_distance, best

# Hill climbing (using 2-opt neighbors)
def hill_climbing(cities, start_city_name="Algiers"):
    clon = copy.deepcopy(cities)
    try:
        idx = next(i for i, c in enumerate(clon) if c.name == start_city_name)
        clon[0], clon[idx] = clon[idx], clon[0]
    except StopIteration:
        pass

    best_distance = total_distance(clon)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(clon) - 2):
            for j in range(i + 1, len(clon)):
                if j - i == 1:
                    continue
                neighbor = clon[:i] + clon[i:j][::-1] + clon[j:]
                dist_neighbor = total_distance(neighbor)
                if dist_neighbor < best_distance:
                    clon = neighbor
                    best_distance = dist_neighbor
                    improved = True
                    break
            if improved:
                break
    return best_distance, clon

# Nearest neighbor (Plus Proche Voisin) starting from start_city_name
def nearest_neighbor(cities, start_city_name="Algiers"):
    if not cities:
        return 0.0, []
    remaining = copy.deepcopy(cities)
    try:
        idx = next(i for i, c in enumerate(remaining) if c.name == start_city_name)
    except StopIteration:
        idx = 0
    current = remaining.pop(idx)
    tour = [current]

    while remaining:
        # find closest city to current
        closest_idx = min(range(len(remaining)), key=lambda k: distance(current, remaining[k]))
        current = remaining.pop(closest_idx)
        tour.append(current)

    return total_distance(tour), tour




def Simulated_Annealing(cities,inital_temp = 10000,
                        min_temp = 1,cooling_rate = 0.95,
                        iteration_per_temp=100):
    if not cities:
        return 0.0,[]
    
    cpCities = copy.deepcopy(cities)
    
    current_distance = total_distance(cpCities)
    best = list(cpCities)
    best_distance = current_distance

    temp = inital_temp

    while temp >= min_temp:
        # Appliquer le 2opt pour perturbation
        for _ in range (iteration_per_temp):
            i = random.randint(1, len(cpCities)-2)
            j = random.randint(i + 1, len(cpCities))

            neighbor = cpCities[:i] + cpCities[i:j][::-1] + cpCities[j:]
            neighbor_distance = total_distance(neighbor)

            delta = neighbor_distance - current_distance

            # si accepted proceed sinon une test une chance de se faire accepter 
            if delta < 0:
                cpCities = neighbor
                current_distance = neighbor_distance

                if current_distance < best_distance:
                    best = list(cpCities)
                    best_distance = current_distance

            else:
                acceptation_proba = math.exp(-delta / temp)
                if random.random() < acceptation_proba:
                    cpCities = neighbor
                    current_distance = neighbor_distance

        temp *= cooling_rate
    
    return best_distance,best


def Tabu_Search(cities,max_iterations=1000,tabu_tenure=10,
                neighborhood_size=50):
    current = copy.deepcopy(cities)

    current_distance = total_distance(current)
    best = list(current)
    best_distance = current_distance
    
    # list des movements interdits
    tabu_list = deque(maxlen=tabu_tenure)

    #Compteur iterations whithout upgrades
    no_improve = 0
    max_no_improve = 100

    for iteration in range(max_iterations):

        candidates = []

        for _ in range (neighborhood_size):
            i = random.randint(1,len(current)-2)
            j = random.randint(i + 1,len(current))
            
            # verif si tabu
            move = (i,j)
            is_tabu = move in tabu_list or (j, i) in tabu_list

            # generate Voisin
            neighbor = current[:i] + current[i:j][::-1] + current[j:]
            neighbor_distance = total_distance(neighbor)

            # critere d'aspiration , accept si meilleurs que best global
            aspiration = neighbor_distance < best_distance

            # Ajouter le candidat si non tabou ou aspiration
            if not is_tabu or aspiration:
                candidates.append((neighbor_distance,neighbor,move))

        if not candidates:
            break

        # choisisr le meilleurs boisin (meme si moins bon que currecnt)
        candidates.sort(key=lambda x: x[0])
        next_distance, next_solution,best_move  = candidates[0]

        # Mettre a jour la soluc
        current = next_solution
        current_distance = next_distance

        # ajouter le mov a la list taboue
        tabu_list.append(best_move)

        # Mettre a jour le meilleurs global
        if current_distance < best_distance:
            best = list(current)
            best_distance = current_distance
            no_improve = 0

        else:
            no_improve += 1

        if no_improve >= max_no_improve:
            break

    return best_distance,best


def print_tour_info(dist, tour):
    print(f"Total distance: {dist:.3f} #######################################")
    print("Tour order:")
    for c in tour:
        print(c.name, end=" . ")
    print("\n")

def main_loop(cities):
    iterations = 10000 # pour random search
    menu = (
        "\nChoose algorithm (enter number) or 'q' to quit:\n"
        "1 - Random search\n"
        "2 - Local 2-OPT search\n"
        "3 - Hill Climbing\n"
        "4 - Nearest Neighbor (Plus Proche Voisin)\n"
        "5 - Simulated_Annealing\n"
        "6 - Tabu_Search\n"
        "s - Show total distance of the original order\n"
        "q - Quit\n"
    )
    # comment 
    while True:
        print(menu)
        choice = input("Your choice: ").strip().lower()
        if choice == 'q':
            print("Quitting...")
            break
        if choice == 's':
            print(f"Original order total distance: {total_distance(cities):.3f}")
            continue

        if choice not in ('1', '2', '3', '4','5','6'):
            print("Invalid choice, please enter 1,2,3,4,5,s or q.")
            continue

        if choice == '1':
            dist, tour = random_search(cities, iterations)
            print(f"Random search (best of {iterations}):")
            print_tour_info(dist, tour)
        elif choice == '2':
            dist, tour = local_2opt_search(cities)
            print("Local 2-OPT result:")
            print_tour_info(dist, tour)
        elif choice == '3':
            dist, tour = hill_climbing(cities)
            print("Hill Climbing result:")
            print_tour_info(dist, tour)
        elif choice == '4':
            dist, tour = nearest_neighbor(cities)
            print("Nearest Neighbor result:")
            print_tour_info(dist, tour)
        elif choice == '5':
            dist,tour = Simulated_Annealing(cities)
            print("Simulated_Annealing results:")
            print_tour_info(dist,tour)
        elif choice == "6":
            dist,tour = Tabu_Search(cities)
            print("Tabu Search results:")
            print_tour_info(dist,tour)


if __name__ == "__main__":
    # change path if needed
    CSV_PATH = "algeria_20_cities_xy.csv"
    cities = load_cities(CSV_PATH)
    if not cities:
        print("No cities loaded.")
        sys.exit(1)

    main_loop(cities)
