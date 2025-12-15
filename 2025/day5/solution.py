from dataclasses import dataclass, field

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
    if not (range_a.start <= range_b.end and range_b.start <= range_a.end):
        return [range_a, range_b]
    merged = Range(
        start=min(range_a.start, range_b.start),
        end=max(range_a.end, range_b.end)
    )
    return [merged]

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

        while(not isMergedCompletely):
            new_ranges: list[Range] = []
            isMergedCompletely = True
            for i, range_1 in enumerate(self.ranges):
                for j in range(i +1, len(self.ranges)):
                    new_range = merge_ranges(range_1, self.ranges[j])
                    if len(new_range) != 2:
                        isMergedCompletely = False
                        self.ranges.remove(self.ranges[j])
                        self.ranges.remove(range_1)
                        self.ranges = self.ranges + new_range
                        break
                if isMergedCompletely == False:
                    break

        return


myCafeteria = Cafeteria("input.txt")
print(myCafeteria.get_count_fresh_food())
myCafeteria.merge_ranges()
print(myCafeteria.fresh_id_count())