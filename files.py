import configparser
def read_config(section,item):
    configParser = configparser.ConfigParser()
    configParser.read('config.ini')

    target = configParser[section][item]
    return target