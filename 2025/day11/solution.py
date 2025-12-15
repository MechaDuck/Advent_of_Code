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