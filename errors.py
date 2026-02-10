class MazeError(Exception):
    pass

class ConfigError(MazeError):
    pass

class ConfigFileError(ConfigError):
    pass

class ConfigSyntaxError(ConfigError):
    pass

class ConfigMissingKeyError(ConfigError):
    pass

class ConfigValueError(ConfigError):
    pass

class MazeValidationError(MazeError):
    pass

class Pattern42Error(MazeError):
    pass