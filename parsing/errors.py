class MazeError(Exception):
    """Base class for all Maze-related exceptions."""
    pass


class ConfigError(MazeError):
    """Base class for configuration-related exceptions."""
    pass


class ConfigFileError(ConfigError):
    """Raised when there is an error reading the configuration file."""
    pass


class ConfigSyntaxError(ConfigError):
    """Raised when there is a syntax error in the configuration."""
    pass


class ConfigMissingKeyError(ConfigError):
    """Raised when a required key is missing in the configuration."""
    pass


class ConfigValueError(ConfigError):
    """Raised when a configuration value is invalid."""
    pass


class MazeValidationError(MazeError):
    """Raised when the maze validation fails."""
    pass


class Pattern42Error(MazeError):
    """Raised for errors related to Pattern 42."""
    pass
