import wx
import argparse
import configparser
import re
import requests
import json
from myConfigParser3_5 import createConfig
from myConfigParser3_5 import updateConfig
from myConfigParser3_5 import readConfig
from myConfigParser3_5 import updateConfigStaticRewards

########################################################################


class Bot:
    """"""
    #----------------------------------------------------------------------

    def __init__(self):
        """Constructor"""
        self.username = ''
        self.password = ''
        self.userid = ''  # userid of logged in user
        self.communityid = ''  # id of community from logged in user
        self.list_userids = []  # list of all userids in community of logged in user
        self.placement_and_userids = []  # dict with userid as key and placement as value
        self.leaguename = ''  # name of community
        # number of players that will get a reward (descending)
        self.nrOfRewardedPlayers = 4

        # HTTP Header parameters
        self.authToken = ''  # authtoken to perform http request as a logged in user
        self.origin = 'http://www.comunio.de'
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36'
        self.accept_encoding = 'gzip, deflate, br'
        self.connection = 'keep-alive'

    #----------------------------------------------------------------------
    def doLogin(self, username, password):
        """"""
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

        try:
            requestLogin = self.session.post(
                'https://api.comunio.de/login', headers=headersLogin, data=dataLogin)
            requestLogin.encoding = 'utf-8'

            if not requestLogin.status_code // 100 == 2:
                errorData = json.loads(requestLogin.text)
                frame.text.AppendText(
                    'Login fehlgeschlagen!\nError: Unexpected response {}'.format(requestLogin))
                # errorText = errorData['error_description'].decode('latin-1').encode('utf-8')
                # try: frame.text.AppendText(str(errorText))
                # except KeyError:
                #     frame.text.AppendText('Login fehlgeschlagen!\nError: Unexpected response {}'.format(requestLogin))
                return 'Error: Unexpected response {}'.format(requestLogin)

            jsonData = json.loads(requestLogin.text)
            frame.text.AppendText(
                '\nLogin erfolgleich!\nZiehe Informationen...')
            self.authToken = str(jsonData['access_token'])
            self.getUserAndLeagueInfo()  # get username, userid, communityid and leaguename
            frame.getInformationsAfterLogin()  # update gui after login
            createConfig()  # if no config.ini exists, default config will be created
            return self.authToken

        except requests.exceptions.RequestException as e:
            frame.text.AppendText(
                'Login fehlgeschlagen!\nError: Unexpected response {}'.format(e))
            return 'Error: {}'.format(e)

    #----------------------------------------------------------------------
    def getAuthToken(self):
        """"""
        return self.authToken

    #----------------------------------------------------------------------
    def getPlacementAndUserIds(self):
        """"""
        # jsonData = json.dumps(self.placement_and_userids)
        # return jsonData
        return self.placement_and_userids

    #----------------------------------------------------------------------
    def getUserName(self):
        """"""
        return self.username

    #----------------------------------------------------------------------
    def getUserId(self):
        """"""
        return self.userid

    #----------------------------------------------------------------------
    def getCommunityId(self):
        """"""
        return self.communityid

    #----------------------------------------------------------------------
    def getUserAndLeagueInfo(self):
        """"""
        headersInfo = {
            'Origin': self.origin,
            'Accept-Encoding': self.accept_encoding,
            'Accept-Language': 'en-EN',
            'Authorization': 'Bearer ' + self.authToken,
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/dashboard',
            'User-Agent': self.user_agent,
            'Connection': self.connection,
        }

        requestInfo = requests.get(
            'https://api.comunio.de/', headers=headersInfo)

        jsonData = json.loads(requestInfo.text)
        self.username = jsonData['user']['name']
        self.userid = jsonData['user']['id']
        self.leaguename = jsonData['community']['name']
        self.communityid = jsonData['community']['id']

        return requestInfo.status_code

    #----------------------------------------------------------------------
    def getAllUserIds(self):
        """"""
        headersStandings = {
            'Origin': self.origin,
            'Accept-Encoding': self.accept_encoding,
            'Accept-Language': 'de-DE,en-EN;q=0.9',
            'Authorization': 'Bearer ' + self.authToken,
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/standings/total',
            'User-Agent': self.user_agent,
            'Connection': self.connection,
        }

        paramsStandings = (
            ('period', 'season'),
        )

        requestStanding = requests.get('https://api.comunio.de/communities/' + self.communityid +
                                       '/standings', headers=headersStandings, params=paramsStandings)

        # get IDs of all users
        jsonData = json.loads(requestStanding.text)
        tempid = ''
        # workaround to get id of object that stores all user ids
        for id in jsonData.get('items'):
            tempid = id
            counter = 0
        for id in jsonData['items'][tempid]['players']:
            counter = counter + 1
            self.list_userids.append(str(id['id']))
        return self.list_userids

    #----------------------------------------------------------------------
    def getLatestPoints(self):
        """"""
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

        requestLatestStanding = requests.get(
            'https://api.comunio.de/communities/' + self.communityid + '/standings', headers=headers, params=params)

        jsonData = json.loads(requestLatestStanding.text) # print jsonData

        # save user with points into dict
        for item in jsonData['items']:
            data = {'userid': str(item['_embedded']['user']['id'])} # create json object with attribute userid
            data['totalPoints'] = int(item['totalPoints']) # add attribute totalPoints with value
            self.placement_and_userids.append(
                data)  # append json object to json
            self.placement_and_userids = sorted(self.placement_and_userids, reverse=True) # sort by points
        
        # output standings in output console
        counter = 0
        for entry in self.placement_and_userids:
            counter = counter + 1
            frame.text.AppendText('\n' + str(counter) + '. Platz mit ' + str(entry['totalPoints']) + ' Punkten: ' + str(entry['userid']))
        #return -1

    #----------------------------------------------------------------------
    def postText(self):
        """"""
        headersText = {
            'Authorization': 'Bearer ' + self.authToken,
            'Origin': self.origin,
            'Accept-Encoding': self.accept_encoding,
            'Accept-Language': 'de-DE,en-EN;q=0.9',
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/newsEntry/',
            'Connection': self.connection,
        }
        title = "Das ist ein Titel"
        content = "Das ist der Inhalt</p>\\n<p>1. Zeile</p>\\n<p>2. Zeile"
        dataText = '{"newsEntry":{"title":"' + title + \
            '","message":{"text":"<p>' + content + \
            '</p>"},"recipientId":null}}'
        requestNachricht = self.session.post('https://api.comunio.de/communities/' +
                                             self.communityid + '/users/12578395/news', headers=headersText, data=dataText)

    #----------------------------------------------------------------------
    def sendMoney(self, communityid, userid, amount, reason):
        """"""
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
        requestMoney = requests.post('https://api.comunio.de/communities/' + self.communityid +
                                     '/users/' + userid + '/penalties', headers=headersMoney, data=dataMoney)
        return requestMoney.status_code

    #----------------------------------------------------------------------
    def executeTransaction(self, configfile):
        """"""
        counter = 1
        for entry in self.placement_and_userids:
            #tempPlacement = str(entry['standing'])
            tempUserid = str(entry['userid'])
            # if radiobutton 'feste pramien' is checked
            if(frame.GetMenuBar().FindItemById(frame.staticReward.GetId()).IsChecked()):
                temp = readConfig('config.ini', counter, 'static')
                if(int(temp) > 0):  # ignoring values lower 1
                    if(self.sendMoney(self.communityid, tempUserid, temp, str(counter) + '. Platz.') == 200):
                        frame.text.AppendText(
                            '\nTransaktion fuer ' + str(counter) + '. Platz erfolgreich!')
                    else:
                        frame.text.AppendText(
                            '\nTransaktion fuer ' + str(counter) + '. Platz fehlgeschlagen!')
            # if radiobutton 'punkte basiert' is checked
            elif(frame.GetMenuBar().FindItemById(frame.multiplierReward.GetId()).IsChecked()):
                temp = readConfig('config.ini', counter, 'static')
                if(int(temp) > 0):  # ignoring values lower 1
                    if(self.sendMoney(self.communityid, tempUserid, str(int(entry['totalPoints']) * int(readConfig('config.ini', 1, 'pointbased'))), str(counter) + '. Platz.') == 200):
                        frame.text.AppendText(
                            '\nTransaktion fuer ' + str(counter) + '. Platz erfolgreich!')
                    else:
                        frame.text.AppendText(
                            '\nTransaktion fuer ' + str(counter) + '. Platz fehlgeschlagen!')
            counter = counter + 1

########################################################################


class MouseEventFrame(wx.Frame):
    """Constructor"""

    def __init__(self, parent, id):

        self.authTokenFromLogin = ''
        self.communityid = ''
        self.userid = ''
        self.username = ''
        self.userlist = []

        wx.Frame.__init__(self, parent, id, 'comuniobot', size=(300, 405))
        self.panel = wx.Panel(self)

        # menu bar
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        maxPlayerGetRewardMenuItem = menu.Append(wx.NewId(
        ), 'Letzte Platzierung fuer Praemie', 'Letzte Platzierung, die eine Praemie erhaelt')
        staticRewardsMenuItem = menu.Append(
            wx.NewId(), 'Feste Praemien setzen', 'Setze die festen Praemien')
        multiplierMenuItem = menu.Append(
            wx.NewId(), 'Multiplikator anpassen', 'Den Multiplikator anpassen')
        exitMenuItem = menu.Append(wx.NewId(), "Beenden",
                                   "Programm beenden")
        menuBar.Append(menu, "&Datei")

        self.radioMenu = wx.Menu()
        self.staticReward = self.radioMenu.Append(wx.NewId(), "Feste Praemien",
                                                  "Die Spieler bekommen je nach Platzierung feste Betraege",
                                                  wx.ITEM_RADIO)
        self.multiplierReward = self.radioMenu.Append(wx.NewId(), "Punkte basiert",
                                                      "Punkte als Multiplikator eines festen Betrags",
                                                      wx.ITEM_RADIO)
        # psiItem = radioMenu.Append(wx.NewId(), "psi",
        #                           "a simple Python shell using wxPython as GUI",
        #                           wx.ITEM_RADIO)
        menuBar.Append(self.radioMenu, "&Modus")

        self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)
        self.Bind(wx.EVT_MENU, self.onMaxPlayGetRewardDialog,
                  maxPlayerGetRewardMenuItem)
        self.Bind(wx.EVT_MENU, self.onStaticRewardsDialog,
                  staticRewardsMenuItem)
        self.Bind(wx.EVT_MENU, self.onMultiplierDialog, multiplierMenuItem)
        self.SetMenuBar(menuBar)

        self.welcomeLabel = wx.StaticText(
            self.panel, pos=(5, 15), size=(100, 20))
        self.welcomeLabel.Disable()
        # output console
        self.text = wx.TextCtrl(self.panel, pos=(
            5, 50), size=(285, 300), style=wx.TE_MULTILINE)
        self.text.SetEditable(False)

        # Login objects
        self.usernameText = wx.TextCtrl(self.panel, pos=(
            5, 15), size=(100, 10), value="username")
        self.passwordText = wx.TextCtrl(self.panel, pos=(105, 15), size=(
            100, 10), value="password", style=wx.TE_PASSWORD)
        self.buttonLogin = wx.Button(self.panel, label="Login", pos=(205, 5))

        self.buttonTransaction = wx.Button(
            self.panel, label="Absenden", pos=(205, 5))
        self.buttonTransaction.Show(False)
        self.buttonTransaction.Disable()

        # send money manually
        # self.moneyAmount = wx.TextCtrl(self.panel, pos=(
        #     5, 370), size=(100, 10), value="1000")
        # self.moneyReason = wx.TextCtrl(self.panel, pos=(
        #     115, 370), size=(100, 10), value="begruendung")
        # self.moneyUserId = wx.ComboBox(
        #     self.panel, value="", pos=(5, 400), choices=bot.list_userids)
        # self.buttonSendMoney = wx.Button(
        #     self.panel, label="Senden", pos=(130, 400), size=(100, 30))

        # Button events
        #self.Bind(wx.EVT_BUTTON, self.myClick, self.buttonSendMoney)
        self.Bind(wx.EVT_BUTTON, self.clickTransaction, self.buttonTransaction)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.buttonLogin)

    #----------------------------------------------------------------------
    def onMultiplierDialog(self, event):
        """"""
        dlg = SetMultiplierDialog()
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            updateConfig('config.ini', 'Punkte basiert',
                         dlg.multiplierValue.GetValue())
        dlg.Destroy()

    #----------------------------------------------------------------------
    def onMaxPlayGetRewardDialog(self, event):
        """"""
        dlg = MyDialog()
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            updateConfig('config.ini', 'maxPlayerReward',
                         dlg.comboBox1.GetValue())
        dlg.Destroy()
    #----------------------------------------------------------------------

    def onStaticRewardsDialog(self, event):
        """"""
        dlg = SetStaticRewardsDialog()
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            for i in range(10):
                updateConfigStaticRewards(
                    'config.ini', i + 1, dlg.ticker_ctrls[i].GetValue())
        dlg.Destroy()

    #----------------------------------------------------------------------
    def onExit(self, event):
        """"""
        self.Close()

    #----------------------------------------------------------------------
    def clickTransaction(self, event):
        """"""
        bot.executeTransaction('config.ini')

    #----------------------------------------------------------------------
    def myClick(self, event):
        """"""
        if(str(self.moneyUserId.GetSelection()) != '-1'):
            result = bot.sendMoney(str(self.communityid), str(self.moneyUserId.GetValue()), str(
                self.moneyAmount.GetValue()), self.moneyReason.GetValue())
            if(result == 200):
                self.text.AppendText('\nTransaktion erfolgeich!\nBenutzer: ' + str(self.moneyUserId.GetValue()) +
                                     '\nSumme: ' + str(self.moneyAmount.GetValue()) + '\nBegruendung: ' + str(self.moneyReason.GetValue()))
            else:
                self.text.AppendText('\nTransaktion fehlgeschlagen!')
        else:
            wx.MessageBox('Keine User ID ausgewaehlt!', 'Fehler!',
                          wx.OK | wx.ICON_ERROR, self.panel)

    #----------------------------------------------------------------------
    def printPlacement(self):
        """"""
        self.text.AppendText('\nPlatzierungen letzter Spieltag:')
        bot.getLatestPoints()
        # for i in range(len(self.userlist)):
        #     temp = bot.getLatestPoints()
        #     if(str(temp) != '-1'):
        #         self.text.AppendText('\n' + str(temp))

        with open('standings.json', 'w') as outfile:
            json.dump(bot.getPlacementAndUserIds(), outfile)

    #----------------------------------------------------------------------
    def getInformationsAfterLogin(self):
        """"""
        # destroy login objects
        self.buttonLogin.Destroy()
        self.usernameText.Destroy()
        self.passwordText.Destroy()

        # get ids
        self.communityid = bot.getCommunityId()
        self.userid = bot.getUserId()
        self.userlist = bot.getAllUserIds()

        # show welcome information
        self.welcomeLabel.Enable()
        self.buttonTransaction.Enable()
        self.buttonTransaction.Show(True)
        self.text.AppendText(
            '\nCommunity ID: ' + self.communityid + '\nEigene User ID: ' + self.userid)
        self.welcomeLabel.SetLabelText(
            'Willkommen, ' + str(bot.getUserName() + '!'))
        # self.moneyUserId.SetItems(self.userlist)  # add userids to combobox
        self.printPlacement()  # print placement of last matchday in output console

    #----------------------------------------------------------------------
    def OnButtonClick(self, event):
        """"""
        bot.doLogin(self.usernameText.GetValue(),
                    self.passwordText.GetValue())  # execute login
        self.authTokenFromLogin = bot.getAuthToken()  # get authtoken

        self.panel.Refresh()

########################################################################


class SetMultiplierDialog(wx.Dialog):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Multiplikator", size=(200, 100))
        self.value = readConfig('config.ini', '1', 'pointbased')
        self.multiplierValue = wx.TextCtrl(self, value=self.value)

        okBtn = wx.Button(self, wx.ID_OK)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.multiplierValue, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(okBtn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(sizer)

########################################################################


class SetStaticRewardsDialog(wx.Dialog):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(
            self, None, title="Praemien setzen", size=(230, 470))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.ticker_ctrls = {}
        ticker_items = []
        for i in range(10):
            ticker_items.append(readConfig('config.ini', i + 1, 'static'))
        counter = 0
        for item in ticker_items:
            ctrl = wx.TextCtrl(self, value=item, name=item)
            sizer.Add(ctrl, 0, wx.ALL | wx.CENTER, 5)
            self.ticker_ctrls[counter] = ctrl
            counter = counter + 1
        okBtn = wx.Button(self, wx.ID_OK)
        sizer.Add(okBtn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(sizer)

########################################################################


class MyDialog(wx.Dialog):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Platzierung", size=(100, 100))
        self.value = readConfig('config.ini', '1', 'maxPlayerReward')
        self.comboBox1 = wx.ComboBox(self,
                                     choices=['1', '2', '3', '4', '5',
                                              '6', '7', '8', '9', '10'],
                                     value=self.value)
        self.comboBox1.SetEditable(False)
        okBtn = wx.Button(self, wx.ID_OK)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.comboBox1, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(okBtn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(sizer)


#----------------------------------------------------------------------
if __name__ == '__main__':
    bot = Bot()
    app = wx.App()
    frame = MouseEventFrame(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
