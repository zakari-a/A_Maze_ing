from errors import *

class Config:
    def __init__(self, width, height, entry, exit, output_file, perfect):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect


def get_config(file_path) -> dict:
    data: dict = {}

    try:
        line_num = 0
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                line_num += 1
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ConfigSyntaxError(f"Line {line_num}: Missing '=' in line")
                
                if line.count("=") != 1:
                    raise ConfigSyntaxError(f"Line {line_num}: there is more than 1 '=' in line")
                
                key, value = line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()
                if key in ["WIDTH", "HEIGHT"]:
                    try:
                        value = int(value)
                        if value <= 0 or value > 64:
                            raise ConfigSyntaxError
    
                    except ConfigSyntaxError:
                        if value > 64:
                            raise ConfigValueError(f"Line {line_num}: Value for {key} should < 64")
                        raise ConfigValueError(f"Line {line_num}: Value for {key} should be a positive number")
                    except ValueError:
                        raise ConfigValueError(f"Line {line_num}: Value for {key} should be a valid number")
                if key not in data:
                    data[key] = value
                else:
                    raise ConfigSyntaxError(f"Line {line_num}: {key} is duplicated in the file!")
                
    except FileNotFoundError:
        raise ConfigFileError(f"Can't find {file_path} file!")
    
    except PermissionError:
        raise ConfigFileError(f"Permission denied from {file_path}")
    
    except OSError:
        raise ConfigFileError("Something went wrong at the OS level while opening the file")
    
    missing: set[str]
    keys: set[str] = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}

    missing = keys - set(data.keys())     
    if missing:
        raise ConfigMissingKeyError(f"These configs are missing {missing}")

    return data

def parse_coords(coord: str) -> tuple:
    x : int
    y : int

    try:
        coord = coord.strip()
        if coord.count(",") != 1:
            raise ConfigSyntaxError("Invalid Coordinates")
        x, y = coord.split(",", 1)
        x = int(x.strip())
        y = int(y.strip())
    except ValueError:
        raise ConfigValueError("Invalid Coordinates")
    
    return (x, y)

def final_parse(file) -> Config:

    data = get_config(file)

    entry_ = parse_coords(data["ENTRY"])
    exit_ = parse_coords(data["EXIT"])
    if entry_[0] < 0 or entry_[0] >= data["WIDTH"]:
        raise ConfigValueError(f"ENTRY x-coordinate out of bounds: x={entry_[0]} for WIDTH={data['WIDTH']}")
    if entry_[1] < 0 or entry_[1] >= data["HEIGHT"]:
        raise ConfigValueError(f"ENTRY y-coordinate out of bounds: y={entry_[1]} for HEIGHT={data['HEIGHT']}")
    
    if exit_[0] < 0 or exit_[0] >= data["WIDTH"]:
        raise ConfigValueError(f"EXIT x-coordinate out of bounds: x={exit_[0]} for WIDTH={data['WIDTH']}")
    if exit_[1] < 0 or exit_[1] >= data["HEIGHT"]:
        raise ConfigValueError(f"EXIT y-coordinate out of bounds: y={exit_[1]} for HEIGHT={data['HEIGHT']}")
    
    if data["OUTPUT_FILE"] != "maze.txt":
        raise ConfigValueError("Output file should be named 'maze.txt'")
    
    if data["PERFECT"] in {'false', 0, 'False'}:
        data["PERFECT"] = False
    elif data["PERFECT"] in {'true', 1, 'TRUE'}:
        data["PERFECT"] = True

    return Config(
        width=data["WIDTH"], 
        height=data["HEIGHT"],
        entry=entry_,
        exit=exit_,
        output_file=data["OUTPUT_FILE"],
        perfect=data["PERFECT"]
    )
