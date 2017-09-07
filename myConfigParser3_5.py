import configparser
import os

def createConfig():
    if (not checkIfFileExists('config.ini')):
        config = configparser.ConfigParser()
        config['Feste Praemien'] = {'1': '2000', '2': '1500', '3': '1000', '4': '500' }
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