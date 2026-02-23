from typing import Dict, Tuple
from parsing.errors import (
    ConfigValueError, ConfigSyntaxError,
    ConfigMissingKeyError, ConfigFileError)


class Config:
    """A class to hold the configuration data for the maze generator."""
    def __init__(
            self, width: int, height: int, entry: Tuple[int, int],
            exit: Tuple[int, int], output_file: str, perfect: bool):
        """Initialize the Config object with the provided parameters."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect


def get_config(file_name: str) -> Dict[str, str]:
    """
    Reads the configuration file and returns
    a dictionary of key-value pairs.
    """
    data: Dict[str, str] = {}

    try:
        line_num = 0
        with open(file_name, "r") as file:
            lines = file.readlines()
            for line in lines:
                line_num += 1
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ConfigSyntaxError(
                        f"Line {line_num}: Missing '=' in line")

                if line.count("=") != 1:
                    raise ConfigSyntaxError(
                        f"Line {line_num}: there is more than 1 '=' in line")

                key, value = line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()
                if key in ["WIDTH", "HEIGHT"]:
                    try:
                        int_value = int(value)
                    except ValueError:
                        raise ConfigValueError(
                            f"Line {line_num}: Value for "
                            f"{key} should be a valid number"
                        )
                    if int_value <= 0 or int_value > 64:
                        if int_value > 64:
                            raise ConfigValueError(
                                f"Line {line_num}: Value "
                                f"for {key} should < 64")
                        raise ConfigValueError(
                            f"Line {line_num}: Value for "
                            f"{key} should be a positive number"
                        )
                    value = str(int_value)
                if key not in data:
                    data[key] = value
                else:
                    raise ConfigSyntaxError(f"Line {line_num}: {key} "
                                            f"is duplicated in the file!")

    except FileNotFoundError:
        raise ConfigFileError(f"Can't find {file_name} file!")

    except PermissionError:
        raise ConfigFileError(f"Permission denied from {file_name}")

    except OSError:
        raise ConfigFileError("Something went wrong at the OS level "
                              "while opening the file")

    missing: set[str]
    keys: set[str] = {"WIDTH", "HEIGHT", "ENTRY", "EXIT",
                      "OUTPUT_FILE", "PERFECT"}

    missing = keys - set(data.keys())
    if missing:
        raise ConfigMissingKeyError(f"These configs are missing {missing}")

    return data


def parse_coords(coord: str) -> Tuple[int, int]:
    """
    Parse a coordinate string in the format 'x,y'
    and return a tuple (x, y).
    """
    x: int
    y: int

    try:
        coord = coord.strip()
        if coord.count(",") != 1:
            raise ConfigSyntaxError("Invalid Coordinates")
        x_str, y_str = coord.split(",", 1)
        x = int(x_str.strip())
        y = int(y_str.strip())
    except ValueError:
        raise ConfigValueError("Invalid Coordinates")

    return (x, y)


def final_parse(file: str) -> Config:
    """Performs the final parsing of the configuration file."""
    data = get_config(file)

    width = int(data["WIDTH"])
    height = int(data["HEIGHT"])

    entry_ = parse_coords(data["ENTRY"])
    exit_ = parse_coords(data["EXIT"])
    if entry_[0] < 0 or entry_[0] >= width:
        raise ConfigValueError(f"ENTRY x-coordinate out of bounds: "
                               f"x={entry_[0]} for WIDTH={width}")
    if entry_[1] < 0 or entry_[1] >= height:
        raise ConfigValueError(f"ENTRY y-coordinate out of bounds: "
                               f"y={entry_[1]} for HEIGHT={height}")

    if exit_[0] < 0 or exit_[0] >= width:
        raise ConfigValueError(f"EXIT x-coordinate out of bounds: "
                               f"x={exit_[0]} for WIDTH={width}")

    if exit_[1] < 0 or exit_[1] >= height:
        raise ConfigValueError(f"EXIT y-coordinate out of bounds: "
                               f"y={exit_[1]} for HEIGHT={height}")

    if data["OUTPUT_FILE"] != "maze.txt":
        raise ConfigValueError("Output file should be named 'maze.txt'")

    if exit_ == entry_:
        raise ConfigValueError("Entry and Exit should have different coords")

    perfect_raw = data["PERFECT"].strip().lower()
    if perfect_raw in {"false", "0", "False", "FALSE"}:
        perfect = False

    elif perfect_raw in {"true", "1", "True", "TRUE"}:
        perfect = True

    else:
        raise ConfigValueError("Value for PERFECT must be "
                               "(true/false) or (0/1)")

    return Config(
        width=width,
        height=height,
        entry=entry_,
        exit=exit_,
        output_file=data["OUTPUT_FILE"],
        perfect=perfect
    )
