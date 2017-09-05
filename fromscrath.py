import argparse
import re
import requests
import json
from addict import Dict
from BeautifulSoup import BeautifulSoup
from requests_toolbelt.utils import dump


class Bot:
  def __init__(self, username, password, modus):
    self.username = username
    self.password = password
    self.modus = modus
    self.userid = ''
    self.communityid = ''
    self.authToken = ''
    self.list_userids = []

  def run(self):
    self.login()
    self.getInformation()    
    self.standingsSeason()
    self.postText()
    self.sendMoney()

  def login(self):
    self.session = requests.Session()
    headersLogin = {
      'Origin': 'http://www.comunio.de',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'de-DE,en-EN;q=0.9',
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json, text/plain, */*',
      'Referer': 'http://www.comunio.de/home',
      'Connection': 'keep-alive',
    }

    dataLogin = [
      ('username', self.username),
      ('password', self.password),
    ]

    requestLogin = self.session.post('https://api.comunio.de/login', headers=headersLogin, data=dataLogin)

    # extract authtoken to be able to do requests as a logged in user
    dataDump = dump.dump_all(requestLogin)
    decodedData = dataDump.decode('utf-8')
    m = re.search('(?<=access_token":")\w+', decodedData)
    self.authToken = m.group(0)
    print 'Gathering information...\nAuthToken for current session: ' + m.group(0)

    #simple get request

  def getInformation(self):
    headersInfo = {
        'Origin': 'http://www.comunio.de',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-EN',
        'Authorization': 'Bearer ' + self.authToken,
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'http://www.comunio.de/dashboard',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36',
        'Connection': 'keep-alive',
    }

    requestInfo = self.session.get('https://api.comunio.de/', headers=headersInfo)
    jsonData = json.loads(requestInfo.text)
    #print jsonData
    self.communityid = jsonData['community']['id']
    self.userid = jsonData['user']['id']
    print 'Community ID = ' + self.communityid + '\nUser ID = ' + self.userid

  def standingsSeason(self):
    headersStandings = {
        'Origin': 'http://www.comunio.de',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'de-DE,en-EN;q=0.9',
        'Authorization': 'Bearer ' + self.authToken,
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'http://www.comunio.de/standings/total',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36',
        'Connection': 'keep-alive',
    }

    paramsStandings = (
        ('period', 'season'),
    )

    requestStanding = requests.get('https://api.comunio.de/communities/2152667/standings', headers=headersStandings, params=paramsStandings)

    # get IDs of all users
    jsonData = json.loads(requestStanding.text)
    tempid = ''
    for id in jsonData.get('items'):
      tempid = id
    counter = 0
    for id in jsonData.get('items').get(tempid).get('players'):
      counter = counter+1
      print str(counter) + ". Platz: (" + str(id['name']) + "), Punkte: " + str(id['points'])
      self.list_userids.append(id['id'])

    # for item in self.list_userids:
    #   print item
  def postText(self):
    headersText = {
        'Authorization': 'Bearer ' + self.authToken,
        'Origin': 'http://www.comunio.de',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'de-DE,en-EN;q=0.9',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'http://www.comunio.de/newsEntry/',
        'Connection': 'keep-alive',
    }
    title = "Das ist ein Titel"
    content = "Das ist der Inhalt</p>\\n<p>1. Zeile</p>\\n<p>2. Zeile"
    dataText = '{"newsEntry":{"title":"' +title+ '","message":{"text":"<p>' +content+ '</p>"},"recipientId":null}}'
    requestNachricht = self.session.post('https://api.comunio.de/communities/' +self.communityid+ '/users/12578395/news', headers=headersText, data=dataText)

  def sendMoney(self):
    headersMoney = {
        'Authorization': 'Bearer ' + self.authToken,
        'Origin': 'http://www.comunio.de',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'de-DE,en-EN;q=0.9',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'http://www.comunio.de/setup/clubs/rewardsAndDisciplinary',
        'Connection': 'keep-alive',
    }

    userid = self.userid
    amount = '10000'
    reason = '1. Platz am letzten Spieltag'
    dataMoney = '{"amount":' +amount+ ',"reason":"' +reason+ '"}'
    sendMoney = self.session.post('https://api.comunio.de/communities/' +self.communityid+ '/users/' +userid+ '/penalties', headers=headersMoney, data=dataMoney)

def main():
    # parse commandline arguments
    parser = argparse.ArgumentParser(description='Do stuff in communio automatically')
    parser.add_argument("username", help='username used for login')
    parser.add_argument("password", help='password used for login')
    parser.add_argument('modus', help='set modus: login, send_money, post_text or all')
    args = parser.parse_args()

    bot = Bot(args.username, args.password, args.modus)
    if(bot.modus == 'login'):
      bot.login()
      bot.getInformation()
      bot.standingsSeason()
    elif(bot.modus == 'send_money'):
      bot.login()
      bot.getInformation()
      bot.sendMoney()
    elif(bot.modus == 'post_text'):
      bot.login()
      bot.getInformation()
      bot.postText()
    elif(bot.modus == 'all'):
      bot.login()
      bot.getInformation()
      bot.postText()
      bot.sendMoney()
    else:
      print 'unkown modus. aborted'  

main()