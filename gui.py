import wx
import argparse
import re
import requests
import json
from BeautifulSoup import BeautifulSoup
import myConfigParser3_5


class Bot:
    def __init__(self):

        self.username = ''
        self.password = ''
        #self.modus = modus
        self.userid = '' # userid of logged in user
        self.communityid = '' # id of community from logged in user
        self.list_userids = [] # list of all userids in community of logged in user

        # HTTP Header parameters
        self.authToken = '' # authtoken to perform http request as a logged in user
        self.origin = 'http://www.comunio.de'
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36'
        self.accept_encoding = 'gzip, deflate, br'
        self.connection = 'keep-alive'

    def doLogin(self, username, password):
        self.session = requests.Session()
        headersLogin = {
            'Origin': self.origin,
            'Accept-Encoding': self.accept_encoding,
            'Accept-Language': 'de-DE,en-EN;q=0.9',
            'User-Agent': self.user_agent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/home',
            'Connection': self.connection,
        }

        dataLogin = [
            ('username', username),
            ('password', password),
        ]

        requestLogin = self.session.post(
            'https://api.comunio.de/login', headers=headersLogin, data=dataLogin)

        # extract authtoken to be able to do requests as a logged in user
        if(requestLogin.status_code < 400):
            jsonData = json.loads(requestLogin.text)
            self.authToken = str(jsonData['access_token'])
            if(self.authToken == ''): return 'Login Failed'
            else: return self.authToken
        else: return 'Login Failed'

    def getCommunityId(self, authToken):
        headersInfo = {
            'Origin': self.origin,
            'Accept-Encoding': self.accept_encoding,
            'Accept-Language': 'en-EN',
            'Authorization': 'Bearer ' + authToken,
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/dashboard',
            'User-Agent': self.user_agent,
            'Connection': self.connection,
        }

        requestInfo = requests.get('https://api.comunio.de/', headers=headersInfo)
        jsonData = json.loads(requestInfo.text)
        return jsonData['community']['id']

    def getUserId(self, authToken):
        headersInfo = {
            'Origin': self.origin,
            'Accept-Encoding': self.accept_encoding,
            'Accept-Language': 'en-EN',
            'Authorization': 'Bearer ' + authToken,
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/dashboard',
            'User-Agent': self.user_agent,
            'Connection': self.connection,
        }

        requestInfo = requests.get('https://api.comunio.de/', headers=headersInfo)
        jsonData = json.loads(requestInfo.text)
        return jsonData['user']['id']

    def standingsSeason(self, authToken):
        headersStandings = {
            'Origin': self.origin,
            'Accept-Encoding': self.accept_encoding,
            'Accept-Language': 'de-DE,en-EN;q=0.9',
            'Authorization': 'Bearer ' + authToken,
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/standings/total',
            'User-Agent': self.user_agent,
            'Connection': self.connection,
        }

        paramsStandings = (
            ('period', 'season'),
        )

#        requestStanding = requests.get('https://api.comunio.de/communities/' +self.communityid+ '/standings', headers=headersStandings, params=paramsStandings)
        requestStanding = requests.get('https://api.comunio.de/communities/' +self.getCommunityId(self.authToken)+ '/standings', headers=headersStandings, params=paramsStandings)

        # get IDs of all users
        jsonData = json.loads(requestStanding.text)
        tempid = ''
        for id in jsonData.get('items'):
            tempid = id
            counter = 0
        for id in jsonData.get('items').get(tempid).get('players'):
            counter = counter+1
            self.list_userids.append(str(id['id']))   
        return self.list_userids


    def getLatestStanding(self, authtoken, standing):
        headers = {
            'Origin': self.origin,
            'Accept-Encoding': self.accept_encoding,
            'Accept-Language': 'de-DE,en-EN;q=0.9',
            'Authorization': 'Bearer ' + self.authToken,
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/standings/total',
            'User-Agent': self.user_agent,
            'Connection': self.connection,
        }

        params = (
            ('period', 'matchday'),
            ('wpe', 'true'),
        )

        requestLatestStanding = requests.get('https://api.comunio.de/communities/' +self.getCommunityId(self.authToken)+ '/standings', headers=headers, params=params)
        jsonData = json.loads(requestLatestStanding.text)
        counter = 1
        for item in jsonData['items']:  
            if(counter == int(standing)):
                smResult = bot.sendMoney(self.authToken, str(item['_embedded']['user']['id']), '10000', 'Praemie fuer den ' +str(standing)+ '. Platz!')                
                return str(standing) + '. Platz: ' + str(item['_embedded']['user']['name']) + '(' + str(item['lastPoints']) + ')'
            else:
                counter = counter + 1 
        #return self.list_userids
        return -1

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
        dataText = '{"newsEntry":{"title":"' + title + \
            '","message":{"text":"<p>' + content + \
            '</p>"},"recipientId":null}}'
        requestNachricht = self.session.post('https://api.comunio.de/communities/' +
                                             self.communityid + '/users/12578395/news', headers=headersText, data=dataText)

    def sendMoney(self, communityid, userid, amount, reason):
        headersMoney = {
            'Authorization': 'Bearer ' + self.authToken,
            'Origin': self.origin,
            'Accept-Encoding': self.accept_encoding,
            'Accept-Language': 'de-DE,en-EN;q=0.9',
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/setup/clubs/rewardsAndDisciplinary',
            'Connection': self.connection,
        }

        dataMoney = '{"amount":' + amount + ',"reason":"' + reason + '"}'
        requestMoney = requests.post('https://api.comunio.de/communities/' + communityid +'/users/' + userid + '/penalties', headers=headersMoney, data=dataMoney)
        return requestMoney.status_code

class MouseEventFrame(wx.Frame):
    def __init__(self, parent, id):
        self.authTokenFromLogin = ''
        self.communityid = ''
        self.userid = ''

        wx.Frame.__init__(self, parent, id, 'program', size=(500, 500))
        self.panel = wx.Panel(self)

        self.welcomeLabel = wx.StaticText(self.panel, pos=(5,15), size=(100,20))
        self.welcomeLabel.Disable()
        # output console
        self.text = wx.TextCtrl(self.panel, pos=(5, 50), size=(285, 300), style=wx.TE_MULTILINE)
        self.text.SetEditable(False)

        #Login objects
        self.usernameText = wx.TextCtrl(self.panel, pos=(5, 15), size=(100, 10), value="darealmvp")
        self.passwordText = wx.TextCtrl(self.panel, pos=(105, 15), size=(100, 10), value="test7!", style=wx.TE_PASSWORD)
        self.buttonLogin = wx.Button(self.panel, label="Login", pos=(205, 5))

        # send money manually
        self.moneyAmount = wx.TextCtrl(self.panel, pos=(5, 370), size=(100, 10), value="1000")
        self.moneyReason = wx.TextCtrl(self.panel, pos=(115, 370), size=(100, 10), value="reason")
        self.moneyUserId = wx.ComboBox(self.panel, value="", pos=(5, 400), choices= bot.list_userids)        
        self.buttonSendMoney = wx.Button(self.panel, label="Send", pos=(130, 400), size=(100, 30))
        
        # Button events
        self.Bind(wx.EVT_BUTTON, self.myClick, self.buttonSendMoney) # send money manually event
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.buttonLogin) # login button event
    
    def myClick(self, event):
        result = bot.sendMoney(str(self.communityid), str(self.userid), str(self.moneyAmount.GetValue()), self.moneyReason.GetValue())
        if(result == 200):
            self.text.AppendText('\nSending money succesful!\nBenutzer: ' +str(self.userid)+ '\nSumme: ' +str(self.moneyAmount.GetValue())+ '\nBegruendung: ' +str(self.moneyReason.GetValue()))
        else: self.text.AppendText('\nSending money failed!')

    def OnButtonClick(self, event):
        self.authTokenFromLogin = bot.doLogin(self.usernameText.GetValue(), self.passwordText.GetValue()) # get authtoken
        if(self.authTokenFromLogin == 'Login Failed'): self.text.WriteText('Login failed!')
        else:
            # destroy login objects
            self.buttonLogin.Destroy()
            self.usernameText.Destroy()
            self.passwordText.Destroy()

            self.welcomeLabel.Enable()

            self.text.WriteText('\nLogin succesful!\nGathering information...')

            # get ids
            self.communityid = bot.getCommunityId(self.authTokenFromLogin)
            self.userid = bot.getUserId(self.authTokenFromLogin)


            self.text.AppendText('\nAuthToken: ' + self.authTokenFromLogin + '\nCommunity ID: ' + self.communityid + '\nUser ID: ' + self.userid)
            self.moneyUserId.SetItems(bot.standingsSeason(self.authTokenFromLogin)) # add userids to combobox

            self.welcomeLabel.SetLabelText('Welcome, number ' + str(self.userid))
        self.panel.Refresh()

if __name__ == '__main__':
    bot = Bot()
    app = wx.App()
    frame = MouseEventFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
