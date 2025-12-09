
import enum
from dataclasses import dataclass

class Direction(enum.Enum):
    LEFT = 'L'
    RIGHT = 'R'

@dataclass
class Movement:
    direction: Direction
    steps: int

class MovementsFileReader:
    def read_movements_from_file(filepath: str) -> list[Movement]:
        """
        Reads movement instructions from a file and stores them as a list of Movement objects.

        Args:
            filepath (str): The path to the input file.

        Returns:
            list[Movement]: A list of Movement objects, each containing a Direction enum
                            and an integer for steps.
        """
        movements = []
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    line = line.strip() # Remove leading/trailing whitespace, including newline
                    if not line: # Skip empty lines
                        continue

                    # Extract the direction character and the number
                    direction_char = line[0]
                    steps_str = line[1:]

                    try:
                        steps = int(steps_str)
                        # Convert the character to the corresponding Enum member
                        direction = Direction(direction_char)
                        movements.append(Movement(direction=direction, steps=steps))
                    except ValueError as e:
                        print(f"Warning: Could not parse line '{line}'. Skipping. Error: {e}")
        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found.")
        return movements

class Dial:
    MAX_NUMBER = 99
    MIN_NUMBER = 0
    START_NUMBER = 50

    def __init__(self, file_path: str) -> None:
        self.movements: list[Movement] = MovementsFileReader.read_movements_from_file(file_path)
        self.current_number: int = self.START_NUMBER
        self.hit_zero_counter: int = 0
        self.landing_on_zero_counter: int = 0
    
    def subtract(self,steps: int)-> int:
        for i in range(steps):
            self.current_number = self.current_number - 1
            if self.current_number == 0:
                self.hit_zero_counter = self.hit_zero_counter + 1
            if self.current_number < 0:
                self.current_number = 99

    
    def add(self, steps: int)->int:
        for i in range(steps):
            self.current_number = self.current_number + 1
            if self.current_number > self.MAX_NUMBER:
                self.current_number = 0
            if self.current_number == 0:
                self.hit_zero_counter = self.hit_zero_counter + 1
    



    def doMovements(self) -> None:
        for movement in self.movements:
            if movement.direction == Direction.LEFT:
                self.subtract(movement.steps)
            else:
                self.add( movement.steps)
            if self.current_number == 0:
                self.landing_on_zero_counter = self.landing_on_zero_counter + 1
        
        print(f"Solution Part 1: {self.landing_on_zero_counter}")
        print(f"Solution Part 2: {self.hit_zero_counter}")

myDial = Dial("example_input.txt")
myDial.doMovements()
