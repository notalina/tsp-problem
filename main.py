import re
import math
import random 
from dataclasses import dataclass
from typing import *

@dataclass
class Point:
    x: int
    y: int
    def get_distance_to_point(self, destination):
        distance: int = math.sqrt((self.x - destination.x)**2 + (self.y - destination.y)**2)
        return distance

def get_points_coordinates():
    user_input_string = input()
    coordinates = re.findall(r"\d+", user_input_string)
    points: List[Point] = []
    for i in range(0, len(coordinates), 2):
        new_point: Point = Point(int(coordinates[i]), int(coordinates[i+1]))
        points.append(new_point)
    return points

def get_new_path(path: List[Point]):
    n: int = len(path)
    i = random.randint(0,n-1)
    j = random.randint(0,n-1)
    path[i], path[j] = path[j], path[i]
    return path

def get_path_length(path: List[Point]):
    distance: int = 0
    for i in range(len(path)):
        point_start: Point = path[i]
        point_end: Point = None
        if (i + 1 < len(path)):
            point_end = path[i+1]
        else:
            point_end = path[0]
        distance += point_start.get_distance_to_point(point_end)
    return distance

#Алгоритм отжига
def simulateAnnealing(starting_temperature: float, iterations: int, cooling_rate: int, path: List[Point]):
    temperature: float = starting_temperature
    best_distance: float = get_path_length(path)
    random.shuffle(path)
    current_solution = path
    for i in range(iterations):
        previous_solution = current_solution.copy()
        if temperature > 0.1:
            current_solution = get_new_path(current_solution)
            current_distance: float = get_path_length(current_solution)
            if current_distance < best_distance:
                best_distance = current_distance
            elif math.exp((best_distance - current_distance)/temperature) < random.random():                
                current_solution = previous_solution
        temperature *= cooling_rate
        print_result(current_solution)
    return current_solution
    
def print_result(path:List[Point]):
    distance = get_path_length(path)
    print("route: ", end="")
    for i in range(len(path)):
        if i < len(path)-1:
            print(f"{path[i].x}, {path[i].y} ->", end=" ")
        else:
            print(f"{path[i].x}, {path[i].y}")
    print(f"distance: {distance}")

if __name__ == "__main__":
    points: List[Point] = get_points_coordinates()
    temperature = 60.0
    iterations = 100
    cooling_rate = 0.6
    simulateAnnealing(temperature, iterations, cooling_rate, points)
    # Для небольших пространств и количества точек следует выставлять более низкую температуру
    # и более высокий коэффицент охлаждения.
    # Для больших пространств и количества точек – наоборот.




