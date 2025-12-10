from dataclasses import dataclass

@dataclass
class Range:
    start: int
    end: int


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

myCafeteria = Cafeteria("input.txt")
print(myCafeteria.get_count_fresh_food())