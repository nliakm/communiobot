import ConfigParser

def createConfig():
    config = ConfigParser.ConfigParser()
    config.add_section('TEST')
    config.set('TEST', 'firstplacement', '2000')
    config.set('TEST', 'secondplacement', '1500')
    config.set('TEST', 'thirdplacement', '1000')
    config.set('TESTreq', 'fourthplacement', '500')    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def updateConfig(filename):
    config = ConfigParser.ConfigParser()
    config.add_section('TEST')
    config.set('TEST', 'firstplacement', '2000')
    config.set('TEST', 'secondplacement', '1500')
    config.set('TEST', 'thirdplacement', '1000')
    config.set('TESTreq', 'fourthplacement', '500')    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)