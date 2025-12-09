from dataclasses import dataclass

@dataclass
class Coordinates:
    x: int
    y: int

@dataclass
class Role:
    coordinates: Coordinates
    count_adjacent_roles: int = 0

@dataclass
class GridDimensions:
    x: int
    y: int

# Source - https://stackoverflow.com/a
# Posted by Lev Levitsky, modified by community. See post 'Timeline' for change history
# Retrieved 2025-12-09, License - CC BY-SA 3.0

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


class FileReader:
    def read_from_file(filepath: str) -> tuple[list[Role], GridDimensions]:
        paper_rolls_coord = []
        try:
            with open(filepath, 'r') as file:
                line_index = 0
                for line in file:
                    line = line.strip() # Remove leading/trailing whitespace, including newline
                    if not line: # Skip empty lines
                        continue
                    try:
                        index_of_rolls = find(line, "@")
                        for index_of_roll in index_of_rolls:
                            paper_rolls_coord.append(Role(Coordinates(x=index_of_roll, y=line_index)))
                    except ValueError as e:
                        print(f"Warning: Could not parse line '{line}'. Skipping. Error: {e}")
                    line_index = line_index + 1
        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found.")
        return (paper_rolls_coord,GridDimensions(y=line_index-1, x=len(line)))
    
class PrintingDepartment:
    def __init__(self, file_path: str) -> None:
        self.roles, self.grid_dimensions = FileReader.read_from_file(file_path)
        self.removed_roles: int = 0
    def check_if_role_exists_for_position(self, coord: Coordinates) -> bool:
        for role in self.roles:
            if role.coordinates == coord:
                return True
        return False
    
    def find_number_of_adjacent_rolls(self):
        for role in self.roles:
            adjacest_coord = Coordinates(x=role.coordinates.x - 1, y=role.coordinates.y - 1)
            if self.check_if_role_exists_for_position(adjacest_coord):
                role.count_adjacent_roles = role.count_adjacent_roles + 1
            adjacest_coord = Coordinates(x=role.coordinates.x, y=role.coordinates.y - 1)
            if self.check_if_role_exists_for_position(adjacest_coord):
                role.count_adjacent_roles = role.count_adjacent_roles + 1
            adjacest_coord = Coordinates(x=role.coordinates.x + 1, y=role.coordinates.y - 1)
            if self.check_if_role_exists_for_position(adjacest_coord):
                role.count_adjacent_roles = role.count_adjacent_roles + 1
            adjacest_coord = Coordinates(x=role.coordinates.x + 1, y=role.coordinates.y)
            if self.check_if_role_exists_for_position(adjacest_coord):
                role.count_adjacent_roles = role.count_adjacent_roles + 1
            adjacest_coord = Coordinates(x=role.coordinates.x + 1, y=role.coordinates.y + 1)
            if self.check_if_role_exists_for_position(adjacest_coord):
                role.count_adjacent_roles = role.count_adjacent_roles + 1
            adjacest_coord = Coordinates(x=role.coordinates.x, y=role.coordinates.y + 1)
            if self.check_if_role_exists_for_position(adjacest_coord):
                role.count_adjacent_roles = role.count_adjacent_roles + 1
            adjacest_coord = Coordinates(x=role.coordinates.x -1, y=role.coordinates.y + 1)
            if self.check_if_role_exists_for_position(adjacest_coord):
                role.count_adjacent_roles = role.count_adjacent_roles + 1            
            adjacest_coord = Coordinates(x=role.coordinates.x -1, y=role.coordinates.y)
            if self.check_if_role_exists_for_position(adjacest_coord):
                role.count_adjacent_roles = role.count_adjacent_roles + 1
    def remove_roles_by_forklift(self) -> bool:
        left_roles: list[Role] = []
        at_least_one_role_is_removed = False
        for role in self.roles:
            if role.count_adjacent_roles >= 4:
                role.count_adjacent_roles = 0
                left_roles.append(role)

            else:
                self.removed_roles = self.removed_roles + 1
                at_least_one_role_is_removed = True
        self.roles = left_roles
        return at_least_one_role_is_removed

    def count_roles_with_fewer_than_four_adjacents(self) -> int:
        count = 0
        for role in self.roles:
            if role.count_adjacent_roles < 4:
                count = count + 1
        return count


my_printing_department = PrintingDepartment("input.txt")
my_printing_department.find_number_of_adjacent_rolls()
print(my_printing_department.count_roles_with_fewer_than_four_adjacents())

while(True):
    if my_printing_department.remove_roles_by_forklift():
        my_printing_department.find_number_of_adjacent_rolls()
    else:
        break


print(my_printing_department.removed_roles)