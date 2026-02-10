from config_parser import final_parse
try :
    test = final_parse("configs.txt")
except ConfigError as e:
    print(f"{ConfigError.__name__}: {e}")

# print(test.width, test.height, test.entry, test.exit, test.output_file, test.perfect)