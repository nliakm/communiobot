import configparser

def createConfig():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'firstplacement': '2000', 'secondplacement': '1500', 'thirdplacement': '1000', 'fourthplacement': '500' }
    with open('config3.ini', 'w') as configfile:
        config.write(configfile)

def updateConfig(filename):
    config = configparser.ConfigParser()
    config.sections()

    config.read(filename)
    for key in config['DEFAULT']: print(key)