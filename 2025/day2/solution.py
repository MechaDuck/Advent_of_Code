from dataclasses import dataclass

@dataclass
class IDRange:
    start: int
    end: int

class IDFileReader:
    def read_ids_from_file(filepath: str) -> list[IDRange]:
        """
        Reads id instructions from a file and stores them as a list of ID objects.

        Args:
            filepath (str): The path to the input file.

        Returns:
            list[ID]: A list of ID objects
        """
        ids = []
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    line = line.strip() # Remove leading/trailing whitespace, including newline
                    if not line: # Skip empty lines
                        continue
                    range_strings = line.split(',')
                    for range_str in range_strings:
                        range_str = range_str.strip()
                        if not range_str:
                            continue

                        try:
                            start_str, end_str = range_str.split('-')
                            start = int(start_str)
                            end = int(end_str)
                            ids.append(IDRange(start=start, end=end))
                        except ValueError as e:
                            print(f"Warning: Could not parse line '{line}'. Skipping. Error: {e}")
        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found.")
        return ids
    
class IDValidator:
    def __init__(self, file_path: str) -> None:
        self.ids: list[IDRange] = IDFileReader.read_ids_from_file(file_path)
        self.invalid_id_sum: int = 0

    def slice_string_into_k_parts(self, input_string: str, k: int) -> list[str]:
        """
        Slices a given string into k parts. If the string length is not
        perfectly divisible by k, the extra characters are distributed to the
        first parts (e.g., if length is 7 and k=3, parts might be 3, 2, 2).

        Args:
            input_string (str): The string to be sliced.
            k (int): The desired number of parts. Must be a positive integer.

        Returns:
            list[str]: A list containing the k sliced parts.
                    Returns an empty list if k is non-positive.
                    If k > len(input_string), some parts at the end will be empty.
        """
        n = len(input_string)

        if k <= 0:
            return []
        if k == 1:
            return [input_string]
        
        # Calculate the base length for each part using integer division
        base_length = n // k
        
        # Calculate the number of remaining characters that need to be distributed
        remainder = n % k
        
        parts = []
        current_start_index = 0
        
        for i in range(k):
            # Determine the length of the current part
            # The first 'remainder' parts will get an extra character
            part_length = base_length + (1 if i < remainder else 0)
            
            # Slice the string to get the current part
            part = input_string[current_start_index : current_start_index + part_length]
            parts.append(part)
            
            # Update the starting index for the next part
            current_start_index += part_length
            
        return parts

    def validate(self, max_k_to_check: int = len(str(id))) -> None:
        for id_range in self.ids:
            for id in range(id_range.start, id_range.end + 1):
                for k in range(2, max_k_to_check + 1):
                    parts = self.slice_string_into_k_parts(str(id), k)
                    if len(parts) > 0 and all(part == parts[0] for part in parts):
                        self.invalid_id_sum = self.invalid_id_sum + id
                        break
    def reset(self):
        self.invalid_id_sum = 0

                    

myIDValidator = IDValidator("input.txt")
myIDValidator.validate(2)
print(f"Solution Part 1: {myIDValidator.invalid_id_sum}")
myIDValidator.reset()
myIDValidator.validate()
print(f"Solution Part 2: {myIDValidator.invalid_id_sum}")