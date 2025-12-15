from dataclasses import dataclass
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

def count_paths_dag(graph, start_node, end_nodes: list[any]) -> int:
    topo_sort = list(nx.topological_sort(graph))
    

    path_count = {node: 0 for node in graph.nodes}
    path_count[start_node] = 1 

    for node in topo_sort:
        if path_count[node] > 0: 
            for neighbor in graph.neighbors(node):
                path_count[neighbor] += path_count[node]
    sum = 0
    for end_node in end_nodes:
        sum = sum + path_count[end_node]
    return sum
    

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

class FileReader:
    def read_from_file(filepath: str):
        try:
            with open(filepath, 'r') as f:
                try:
                    grid = [list(line.rstrip("\n")) for line in f]                
                except ValueError as e:
                    print(f"Warning: Could not parse line '{line}'. Skipping. Error: {e}")

        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found.")
        return grid
    
class Laboratories:
    def __init__(self, file_path: str) -> None:
        self.grid = FileReader.read_from_file(file_path)
        self.simulation_line = 0
        self.counter_split = 0
        start_loc = findOccurrences(self.grid[0], "S")[0]
        self.node_dir = { f"0,{start_loc}": f"0,{start_loc}"}
        self.start_node = f"0,{start_loc}"
        self.graph = nx.DiGraph()

        self.graph.add_node(f"0,{start_loc}")

    def simulate_step(self) -> bool:
        if len(self.grid) == self.simulation_line + 1:
            return False

        beam_locs = findOccurrences(self.grid[self.simulation_line], "|") + findOccurrences(self.grid[self.simulation_line], "S")
        for beam_loc in beam_locs:
            parent_id = self.node_dir[f"{self.simulation_line},{beam_loc}"]
            object = self.grid[self.simulation_line + 1][beam_loc]
            if object == "^":

                child_id_left = f"{self.simulation_line + 1},{beam_loc - 1}"
                self.grid[self.simulation_line + 1][beam_loc - 1] = '|'

                self.graph.add_edge(parent_id,child_id_left)
                self.node_dir[child_id_left] = child_id_left

                child_id_right = f"{self.simulation_line + 1},{beam_loc + 1}"
                self.grid[self.simulation_line + 1][beam_loc + 1] = '|'

                self.graph.add_edge(parent_id,child_id_right)
                self.node_dir[child_id_right] = child_id_right

                self.counter_split = self.counter_split +1
            else:
                child_id = f"{self.simulation_line + 1},{beam_loc}"
                self.grid[self.simulation_line + 1][beam_loc] = '|'

                self.graph.add_edge(parent_id,child_id)
                self.node_dir[child_id]= child_id
        self.simulation_line = self.simulation_line + 1
        return True

myLaboratories = Laboratories("input.txt")
while(True):
    if not myLaboratories.simulate_step():
        break

print(f"Solution Part 1: {myLaboratories.counter_split}")

topo_sort = list(nx.topological_sort(myLaboratories.graph))
end_nodes = [node for node in myLaboratories.graph.nodes if myLaboratories.graph.out_degree(node) == 0]

count_paths = count_paths_dag(myLaboratories.graph, myLaboratories.start_node, end_nodes)
print(f"Solution Part 2: {count_paths}")
