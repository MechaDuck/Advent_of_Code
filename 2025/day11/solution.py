from dataclasses import dataclass
import networkx as nx

@dataclass
class Node:
    device_name: str
    outputs: list[str]

def count_paths_dag(graph, start_node, end_node: any) -> int:
    topo_sort = list(nx.topological_sort(graph))
    

    path_count = {node: 0 for node in graph.nodes}
    path_count[start_node] = 1 

    for node in topo_sort:
        if path_count[node] > 0: 
            for neighbor in graph.neighbors(node):
                path_count[neighbor] += path_count[node]
    return path_count[end_node]

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
topo_sort = list(nx.topological_sort(myReactor.graph))

svr_fft_path_count = count_paths_dag(myReactor.graph, 'svr', 'fft')
fft_dac_path_count = count_paths_dag(myReactor.graph, 'fft', 'dac')
dac_fft_path_count = count_paths_dag(myReactor.graph, 'dac', 'out')

print(f"Solution Part 2: {svr_fft_path_count * fft_dac_path_count * dac_fft_path_count}")
