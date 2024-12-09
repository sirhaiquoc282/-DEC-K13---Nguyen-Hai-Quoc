from configparser import ConfigParser


def load_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    config = {}
    try:
        parser.read(filename)
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    except:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )
    return config
