from dataclasses import dataclass
import networkx as nx

@dataclass
class Node:
    device_name: str
    outputs: list[str]


class FileReader:
    def read_from_file(filepath: str) -> list[Node]:
        try:
            with open(filepath, 'r') as f:
                nodes: list[Node] = []
                for line in f:
                    line = line.strip() # Remove leading/trailing whitespace, including newline
                    if not line: # Skip empty lines
                        continue
                    try:
                        device_name, outputs = line.split(':')
                        outputs= outputs.split(' ')[1:]
                        nodes.append(Node(device_name,outputs))
                    except ValueError as e:
                        print(f"Warning: Could not parse line '{line}'. Skipping. Error: {e}")
        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found.")
        return nodes

class Reactor:
    def __init__(self, file_path: str) -> None:
        self.nodes = FileReader.read_from_file(file_path)
        self.graph = nx.DiGraph()
        self.counter = 0
    def create_graph(self, forbidden_node:list[str] = [])->None:
        for node in self.nodes:
            for output in node.outputs:
                edge_1 = node.device_name
                edge_2 = output
                if node.device_name in forbidden_node:
                    continue
                if output in forbidden_node:
                    continue
                self.graph.add_edge(edge_1, edge_2)
            



myReactor = Reactor("input.txt")
myReactor.create_graph()
paths = nx.all_simple_paths(myReactor.graph, source='you', target='out')
print(f"Solution Part 1: {len(list(paths))}")

myReactor = Reactor("input.txt")
myReactor.create_graph()

# dac to fft is zero, meaning paths are only interesting, if the search does not hit dac before fft
# paths = nx.all_simple_paths(myReactor.graph, source='dac', target='fft')
# print(f"{len(list(paths))}")

# dac to out has 16647 paths
# paths = nx.all_simple_paths(myReactor.graph, source='dac', target='out')
# print(f"{len(list(paths))}")

myReactor = Reactor("input.txt")
myReactor.create_graph(['dac'])

paths = nx.all_simple_paths(myReactor.graph, source='svr', target='fft', cutoff=14)
print(f"{len(list(paths))}")
paths = list(nx.dfs_edges(myReactor.graph, source='svr'))

c = 0
for path in paths:
    if 'fft' in path:
        c = c + 1

myReactor = Reactor("input.txt")
myReactor.create_graph(['fft'])

paths = nx.all_simple_paths(myReactor.graph, source='svr', target='dac')
print(f"{len(list(paths))}")

paths = list(nx.dfs_edges(myReactor.graph, source='svr'))

paths = nx.all_simple_paths(myReactor.graph, source='fft', target='svr')
print(f"{len(list(paths))}")

filtered_paths = [path for path in paths if 'dac' not in path]


paths = nx.all_simple_paths(myReactor.graph, source='dac', target='out')
print(f"{len(list(paths))}")



paths = nx.all_simple_paths(myReactor.graph, source='svr', target='ddc')
print(f"{len(list(paths))}")












paths = list(paths)
counter = 0
for path in paths:
    if 'dac' in path and 'fft' in path:
        counter = counter + 1


print(f"Solution Part 2: {counter}")