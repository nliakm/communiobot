import wx
import argparse
import re
import requests
import json
from BeautifulSoup import BeautifulSoup
from requests_toolbelt.utils import dump


class Bot:
    def __init__(self):

        self.username = ''
        self.password = ''
        #self.modus = modus
        self.userid = ''
        self.communityid = ''
        self.authToken = ''

#   def run(self):
#     self.doLogin()
#     self.getInformation()
#     self.standingsCurrent()
#     self.postText()
#     self.sendMoney()

    def doLogin(self, username, password):
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
            ('username', username),
            ('password', password),
        ]

        requestLogin = self.session.post(
            'https://api.comunio.de/login', headers=headersLogin, data=dataLogin)

        # extract authtoken to be able to do requests as a logged in user
        if(requestLogin.status_code < 400):
            dataDump = dump.dump_all(requestLogin)
            decodedData = dataDump.decode('utf-8')
            m = re.search('(?<=access_token":")\w+', decodedData)
            self.authToken = m.group(0)
            if(self.authToken == ''): return 'Login Failed'
            else: return self.authToken
        else: return 'Login Failed'

    def getCommunityId(self, authToken):
        headersInfo = {
            'Origin': 'http://www.comunio.de',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-EN',
            'Authorization': 'Bearer ' + authToken,
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/dashboard',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36',
            'Connection': 'keep-alive',
        }

        requestInfo = requests.get('https://api.comunio.de/', headers=headersInfo)
        jsonData = json.loads(requestInfo.text)
        return jsonData['community']['id']

    def getUserId(self, authToken):
        headersInfo = {
            'Origin': 'http://www.comunio.de',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-EN',
            'Authorization': 'Bearer ' + authToken,
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/dashboard',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36',
            'Connection': 'keep-alive',
        }

        requestInfo = requests.get('https://api.comunio.de/', headers=headersInfo)
        jsonData = json.loads(requestInfo.text)
        return jsonData['user']['id']

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

    def sendMoney(self, authToken, communityid, userid, amount, reason):
        headersMoney = {
            'Authorization': 'Bearer ' + authToken,
            'Origin': 'http://www.comunio.de',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'de-DE,en-EN;q=0.9',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/setup/clubs/rewardsAndDisciplinary',
            'Connection': 'keep-alive',
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

        self.buttonLogin = wx.Button(self.panel, label="Login", pos=(205, 5))

        self.text = wx.TextCtrl(self.panel, pos=(5, 50), size=(285, 300), style=wx.TE_MULTILINE)
        self.text.SetEditable(False)
        #self.text.SetBackgroundColour((190,190,190))
        self.usernameText = wx.TextCtrl(self.panel, pos=(5, 15), size=(100, 10), value="darealmvp")
        self.passwordText = wx.TextCtrl(self.panel, pos=(105, 15), size=(100, 10), value="test7!", style=wx.TE_PASSWORD)

        self.moneyAmount = wx.TextCtrl(self.panel, pos=(300, 60), size=(100, 10), value="1000")
        self.moneyReason = wx.TextCtrl(self.panel, pos=(300, 90), size=(100, 10), value="reason")          
        self.buttonSendMoney = wx.Button(self.panel, label="Send", pos=(300, 120), size=(100, 30))
        
        self.Bind(wx.EVT_BUTTON, self.myClick, self.buttonSendMoney)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.buttonLogin) 
    
    def myClick(self, event):
        result = bot.sendMoney(self.authTokenFromLogin, str(self.communityid), str(self.userid), str(self.moneyAmount.GetValue()), self.moneyReason.GetValue())
        if(result == 200):
            self.text.AppendText('\nGutschrift erfolgreich!\nBenutzer: ' +str(self.userid)+ '\nSumme: ' +str(self.moneyAmount.GetValue())+ '\nBegruendung: ' +str(self.moneyReason.GetValue()))
        else: self.text.AppendText('\nGutschrift fehlgeschlagen!')

    def OnButtonClick(self, event):
        self.authTokenFromLogin = bot.doLogin(self.usernameText.GetValue(), self.passwordText.GetValue())
        if(self.authTokenFromLogin == 'Login Failed'): self.text.WriteText(self.authTokenFromLogin)
        else:
            self.buttonLogin.Disable()
            self.text.WriteText('\nLogin succesful!\nGathering information...')
            self.communityid = bot.getCommunityId(self.authTokenFromLogin)
            self.userid = bot.getUserId(self.authTokenFromLogin)
            self.text.AppendText('\nAuthToken: ' + self.authTokenFromLogin + '\nCommunity ID: ' + self.communityid + '\nUser ID: ' + self.userid)
        self.panel.Refresh()

if __name__ == '__main__':
    bot = Bot()
    app = wx.App()
    frame = MouseEventFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
