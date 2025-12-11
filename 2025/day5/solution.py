from dataclasses import dataclass

@dataclass
class Range:
    start: int
    end: int

def gauss(range: Range) -> int:
    n = range.end - range.start + 1
    a1 = range.start
    a2 = range.end
    return (n/2)*(a1 + a2)

def merge_ranges(range_a: Range, range_b: Range) -> list[Range]:
    new_range: Range = Range(start = 0, end= 0)
    # check if ranges can be merged
    if not (range_b.start <= range_a.start <= range_b.end) and not (range_b.start <= range_a.end <= range_b.end): 
        return [range_a, range_b]
    if range_a.end > range_b.end:
        new_range.end = range_a.end
    else:
        new_range.end = range_b.end
    
    if range_a.start < range_b.start:
        new_range.start = range_a.start
    else:
        new_range.start = range_b.start
    return [new_range]

class FileReader:
    def read_from_file(filepath: str) -> tuple[list[Range], list[int]]:
        ranges: list[Range] = []
        ids: list[int] = []
        try:
            with open(filepath, 'r') as file:
                line_index = 0
                isRangeSection = True
                for line in file:
                    line = line.strip() # Remove leading/trailing whitespace, including newline
                    if not line: # Skip empty lines
                        isRangeSection = False
                        continue
                    try:
                        if isRangeSection:
                            range = line.split("-")
                            ranges.append(Range(start=int(range[0]), end=int(range[1])))
                        else:
                            ids.append(int(line))
                                                   
                    except ValueError as e:
                        print(f"Warning: Could not parse line '{line}'. Skipping. Error: {e}")

        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found.")
        return (ranges, ids)

class Cafeteria:
    def __init__(self, file_path: str) -> None:
        self.ranges, self.ids = FileReader.read_from_file(file_path)
    def get_count_fresh_food(self) -> int:
        fresh_counter: int = 0
        for id in self.ids:
            for range in self.ranges:
                if id < range.start:
                    continue
                elif id > range.end:
                    continue
                fresh_counter = fresh_counter + 1
                break
        return fresh_counter
    def fresh_id_ranges(self) -> int:
        sum = 0
        for range in self.ranges:
            sum = sum + gauss(range)
        return sum
    def fresh_id_count(self) -> int:
        sum = 0
        for range in self.ranges:
            sum = sum + abs((range.end - range.start) + 1)
        return sum
    def merge_ranges(self):
        isMergedCompletely: bool = False
        new_ranges: list[Range] = self.ranges.copy()
        while(not isMergedCompletely):
            isMergedCompletely = True
            self.ranges = new_ranges.copy()

            for i in range(0, len(self.ranges)-1):
                new_range = merge_ranges(self.ranges[i], self.ranges[i + 1])
                if len(new_range) != 2:
                    isMergedCompletely = False
                new_ranges.remove(self.ranges[i])
                new_ranges.remove(self.ranges[i + 1])
                new_ranges = new_ranges + new_range
        return





myCafeteria = Cafeteria("example_input.txt")
print(myCafeteria.get_count_fresh_food())
myCafeteria.merge_ranges()
print(myCafeteria.fresh_id_count())