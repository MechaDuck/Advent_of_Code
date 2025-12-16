
from dataclasses import dataclass
import numpy as np
from scipy import spatial

@dataclass
class JunctionBox:
    coord: list[int, int, int]


class FileReader:
    def read_from_file(filepath: str) -> list[JunctionBox]:
        junction_boxes: list[JunctionBox] = []
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    line = line.strip() # Remove leading/trailing whitespace, including newline
                    if not line: # Skip empty lines
                        continue
                    try:
                        coords = line.split(",")
                        junction_boxes.append(JunctionBox([int(coords[0]), int(coords[1]), int(coords[2])]))              
                    except ValueError as e:
                        print(f"Warning: Could not parse line '{line}'. Skipping. Error: {e}")

        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found.")
        return junction_boxes

class Playground:
    def __init__(self, file_path: str) -> None:
        self.junction_boxes = FileReader.read_from_file(file_path)
        points =  []
        for junction_box in self.junction_boxes:
            points.append(junction_box.coord)
        self.points = np.array(points)




myPlayground = Playground("example_input.txt")
for i, point in enumerate(myPlayground.points):
    remaining_points =myPlayground.points[i+1:]
    print(remaining_points[spatial.KDTree(remaining_points).query(point)[1]])
print('')