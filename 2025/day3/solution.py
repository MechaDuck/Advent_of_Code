from dataclasses import dataclass

def list_of_ints_to_single_int(int_list: list[int]) -> int:

    if not int_list:
        return 0

    string_list = [str(num) for num in int_list]
    concatenated_string = "".join(string_list)
    single_integer = int(concatenated_string)
    return single_integer

@dataclass
class Battery:
    bank: list[int]


class BatteryFileReader:
    def read_batteries_from_file(filepath: str) -> list[Battery]:
        batteries = []
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    line = line.strip() # Remove leading/trailing whitespace, including newline
                    if not line: # Skip empty lines
                        continue
                    bank: list[int] = []
                    try:
                        for str in line:
                            bank.append(int(str))
                        batteries.append(Battery(bank))
     
                    except ValueError as e:
                        print(f"Warning: Could not parse line '{line}'. Skipping. Error: {e}")
        except FileNotFoundError:
            print(f"Error: The file '{filepath}' was not found.")
        return batteries

class JoltageCheck:

    def __init__(self, file_path: str) -> None:
        self.batteries: list[Battery] = BatteryFileReader.read_batteries_from_file(file_path)

    
    def findMaxJoltage(self) -> int:
        max_joltage: int = 0
        for battery in self.batteries:
            max_bank_val: int = 0
            pos_max_bank_val: int = 0
            for index, bank_val in enumerate(battery.bank[slice(0,len(battery.bank)-1)]):
                if bank_val > max_bank_val:
                    max_bank_val = bank_val
                    pos_max_bank_val = index
            second_largest_bank_val: int = 0
            for index, bank_val in enumerate(battery.bank[slice(pos_max_bank_val + 1,len(battery.bank))]):
                if bank_val > second_largest_bank_val:
                    second_largest_bank_val = bank_val
            max_joltage = max_joltage + max_bank_val * 10 + second_largest_bank_val
        return max_joltage

    def findMaxTwelveBankJoltage(self) -> int:
        max_joltage: int = 0
        for battery in self.batteries:
            max_bank_vals: list[int] = []
            index = 0
            #ignore last digits
            ignore_last_digits = len(battery.bank) - 12
            while index < len(battery.bank):
                new_bank = battery.bank[slice(index, len(battery.bank) - 12 + len(max_bank_vals) + 1)]
                max_index = new_bank.index(max(new_bank))
                max_bank_vals.append(max(new_bank))
                index = index + max_index + 1
                if len(max_bank_vals) == 12:
                    break
            #print(f"Intermediate result: {list_of_ints_to_single_int(max_bank_vals)}")
            max_joltage = max_joltage + list_of_ints_to_single_int(max_bank_vals)
        return max_joltage

myJoltageCheck = JoltageCheck("input.txt")
max_joltage = myJoltageCheck.findMaxJoltage()
print(f"Solution Part 1: {max_joltage}")

max_twelve_package_voltage = myJoltageCheck.findMaxTwelveBankJoltage()
print(f"Solution Part 2: {max_twelve_package_voltage}")