import configparser
import os

def createConfig():
    if (not checkIfFileExists('config.ini')):
        config = configparser.ConfigParser()
        config['Feste Praemien'] = {'1': '10000', '2': '9000', '3': '8000', '4': '7000', '5': '6000', '6': '5000', '7': '4000', '8': '3000', '9': '2000', '10': '1000'}
        config['Punkte basiert'] = {'Multiplikator': '1000'}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        return True
    return False

def checkIfFileExists(filename):
    return os.path.isfile(filename)

def updateConfig(filename, section_name, valuelist):
    if (checkIfFileExists(filename)):
        config = configparser.ConfigParser()
        config.sections()
        config.read(filename)
        if(section_name == 'Punkte basiert'):
            config['Punkte basiert']['Multiplikator'] = valuelist
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        return True
    return False

def updateConfigStaticRewards(filename, placement, value):
    if (checkIfFileExists(filename)):
        config = configparser.ConfigParser()
        config.sections()
        config.read(filename)
        config['Feste Praemien'][str(placement)] = str(value)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        return True
    return False

def readConfig(filename, placement, modus):
    if (checkIfFileExists(filename)):
        config = configparser.ConfigParser()
        config.sections()
        config.read(filename)
        if(str(modus) == 'static'):   
            return config['Feste Praemien'][str(placement)]
        elif(str(modus) == 'pointbased'):
            return config['Punkte basiert']['Multiplikator']
    return -1  