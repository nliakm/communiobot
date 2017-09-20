import wx
import argparse
import configparser
import re
import requests
import json
from ConfigHandler import createConfig
from ConfigHandler import updateConfig
from ConfigHandler import readConfig
from ConfigHandler import updateConfigStaticRewards
import sys
########################################################################

reload(sys)
sys.setdefaultencoding('utf8')

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
        self.leader = False
        self.lastMatchday = ''

        # HTTP Header parameters
        self.authToken = ''  # authtoken to perform http request as a logged in user
        self.origin = 'http://www.comunio.de'
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36'
        self.accept_encoding = 'gzip, deflate, br'
        self.connection = 'keep-alive'

    #----------------------------------------------------------------------
    def doLogin(self, username, password):
        """Login to comunio.de.

        username -- the username entered into username textbox
        password -- the password entered into password textbox

        Gets the authtoken needed for further requests as the user.
        Create default config.ini if not present.
        Runs getUserAndLeagueInfo to get username, userid, communityid and communityname
        Updates the gui after login with call of function getInformationsAfterLogin
        """
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
            #requestLogin.encoding = 'iso-8859-15'

            if not requestLogin.status_code // 100 == 2:
                errorData = json.loads(requestLogin.text)
                errorText = errorData['error_description']
                try: frame.text.AppendText(str(errorText))
                except KeyError:
                    frame.text.AppendText('Login fehlgeschlagen!\nError: Unexpected response {}'.format(requestLogin))
                return errorText

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

    #----------------------------------------------------------------------
    def getAuthToken(self):
        """Getter for authtoken."""
        return self.authToken

    #----------------------------------------------------------------------
    def getLeaderStatus(self):
        """Getter for leader."""
        return self.leader

    #----------------------------------------------------------------------
    def getLastMatchDay(self):
        """Getter for last matchday."""
        return self.lastMatchday

    #----------------------------------------------------------------------
    def getPlacementAndUserIds(self):
        """"""
        return self.placement_and_userids

    #----------------------------------------------------------------------
    def getUserName(self):
        """Getter for username of logged in user."""
        return self.username

    #----------------------------------------------------------------------
    def getUserId(self):
        """Getter for userid of logged in user."""
        return self.userid

    #----------------------------------------------------------------------
    def getCommunityId(self):
        """Getter for community id of logged in user."""
        return self.communityid

    #----------------------------------------------------------------------
    def getWealth(self, userid):
        """Get budget of user from last matchday.

        userid -- userid of user
        """
        headersInfo = {
            'Origin': self.origin,
            'Accept-Encoding': self.accept_encoding,
            'Accept-Language': 'en-EN',
            'Authorization': 'Bearer ' + self.authToken,
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/standings/total',
            'User-Agent': self.user_agent,
            'Connection': self.connection,
        }

        requestInfo = requests.get(
            'https://api.comunio.de/users/' + str(userid) + '/squad-latest', headers=headersInfo)
        jsonData = json.loads(requestInfo.text)
        wealth = int(jsonData['matchday']['budget'])
        return wealth

    #----------------------------------------------------------------------
    def getUserAndLeagueInfo(self):
        """Gets username, userid, communityid and communityname of logged in user."""
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
        self.leader = jsonData['user']['isLeader']
        self.leaguename = jsonData['community']['name']
        self.communityid = jsonData['community']['id']

        return requestInfo.status_code

    def getUserInfo(self, userid):
        """Gets username, userid, communityid and communityname of logged in user."""
        headersInfo = {
            'Origin': self.origin,
            'Accept-Encoding': self.accept_encoding,
            'Accept-Language': 'en-EN',
            'Authorization': 'Bearer ' + self.authToken,
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'http://www.comunio.de/standings/total',
            'User-Agent': self.user_agent,
            'Connection': self.connection,
        }
        requestInfo = requests.get(
            'https://api.comunio.de/users/' + str(userid) + '/squad', headers=headersInfo)

        marktwert = 0
        jsonData = json.loads(requestInfo.text)
        for item in jsonData['items']:
            item['quotedprice']
            marktwert = marktwert + int(item['quotedprice'])

        return marktwert


    #----------------------------------------------------------------------
    def getAllUserIds(self):
        """Gets all userids from community and store them into a list."""
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
        jsonData = json.loads(requestStanding.text)
        tempid = ''
        # workaround to get id of object that stores all user ids
        for id in jsonData.get('items'):
            tempid = id
        for id in jsonData['items'][tempid]['players']:
            self.list_userids.append(str(id['id']))
        return self.list_userids

    #----------------------------------------------------------------------
    def getLatestPoints(self):
        """Gets points of all users and store them into a json object."""
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
        jsonData = json.loads(requestLatestStanding.text)  # print jsonData
        self.lastMatchday = jsonData['_embedded']['formerEventsWithPoints']['events'][0]['event']
        # function to be able to sort by points
        def myFn(s):
            return s['totalPoints']

        # save user with points, name and id into dict obj
        for item in jsonData['items']:
            # create json object with attribute userid
            data = {'userid': str(item['_embedded']['user']['id'])}
            # add attribute totalPoints with value
            data['totalPoints'] = int(item['totalPoints'])
            # add attribute name
            data['name'] = str(item['_embedded']['user']['name'])
            self.placement_and_userids.append(
                data)  # append json object to json
            self.placement_and_userids = sorted(
                self.placement_and_userids, key=myFn, reverse=True)  # sort by points

    #----------------------------------------------------------------------
    def sendMoney(self, communityid, userid, amount, reason):
        """Send Money to a user.

        communityid -- communityid of logged in user
        userid -- userid of user who will recieve the money
        amount -- amount of money to send
        reason -- text that will appear on dashboard
        """
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
    def executeTransaction(self, configfile='config.ini'):
        """Execeutes transaction based on configfile.

        configfile -- configfile that is used (default config.ini) 
        """
        counter = 1  # needed for display placement number in output console
        for entry in self.placement_and_userids:
            # check last placement for reward
            if counter <= int(readConfig('config.ini', '1', 'maxPlayerReward')):
                tempUserid = str(entry['userid'])  # userid in loop
                # if radiobutton 'feste pramien' is checked
                if(frame.GetMenuBar().FindItemById(frame.staticReward.GetId()).IsChecked()):
                    temp = readConfig('config.ini', counter, 'static')
                    if(int(temp) > 0):  # ignoring values lower 1
                        if(self.sendMoney(self.communityid, tempUserid, temp, str(counter) + '. Platz.') == 200):
                            frame.text.AppendText(
                                '\nTransaktion fuer ' + str(entry['name']) + '(' + str(counter) + '. Platz) erfolgreich!')
                        else:
                            frame.text.AppendText(
                                '\nTransaktion fuer ' + str(entry['name']) + '(' + str(counter) + '. Platz) fehlgeschlagen!')
                # if radiobutton 'punkte basiert' is checked
                elif(frame.GetMenuBar().FindItemById(frame.multiplierReward.GetId()).IsChecked()):
                    temp = readConfig('config.ini', counter, 'static')
                    if(int(temp) > 0):  # ignoring values lower 1
                        if(self.sendMoney(self.communityid, tempUserid, str(int(entry['totalPoints']) * int(readConfig('config.ini', 1, 'pointbased'))), str(counter) + '. Platz.') == 200):
                            frame.text.AppendText(
                                '\nTransaktion fuer ' + str(entry['name']) + '(' + str(counter) + '. Platz) erfolgreich!')
                        else:
                            frame.text.AppendText(
                                '\nTransaktion fuer ' + str(entry['name']) + '(' + str(counter) + '. Platz) fehlgeschlagen!')
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

        wx.Frame.__init__(self, parent, id, 'comuniobot v0.2', size=(
            700, 405), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
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
        menuBar.Append(self.radioMenu, "&Modus")

        self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)
        self.Bind(wx.EVT_MENU, self.onMaxPlayGetRewardDialog,
                  maxPlayerGetRewardMenuItem)
        self.Bind(wx.EVT_MENU, self.onStaticRewardsDialog,
                  staticRewardsMenuItem)
        self.Bind(wx.EVT_MENU, self.onMultiplierDialog, multiplierMenuItem)
        self.SetMenuBar(menuBar)

        # Sizer implementation
        topSizer = wx.BoxSizer(wx.VERTICAL) # parent sizer
        loginSizer = wx.BoxSizer(wx.HORIZONTAL) # sizer of login objects
        praemienSizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5) # sizer for transaction button
        self.outputSizer = wx.StaticBox(self.panel, -1, 'Ausgabe:', size=(695, 305)) # static sizer around output console
        outputSizer = wx.StaticBoxSizer(self.outputSizer, wx.VERTICAL) # sizer for output console

        # welcome text       
        self.welcomeLabel = wx.StaticText(self.panel)
        self.welcomeLabel.Disable()
        loginSizer.Add(self.welcomeLabel, 0, wx.CENTER, 5)

        # output console
        self.text = wx.TextCtrl(self.panel, size=(690, 300), style=wx.TE_MULTILINE)        
        self.text.SetEditable(False)
        outputSizer.Add(self.text, 0, wx.ALL, 5)

        # Login objects
        self.usernameText = wx.TextCtrl(self.panel, value="username")
        self.passwordText = wx.TextCtrl(self.panel, value="password", style=wx.TE_PASSWORD)
        self.buttonLogin = wx.Button(self.panel, label="Login")
        loginSizer.Add(self.usernameText, 0, wx.ALL, 5)
        loginSizer.Add(self.passwordText, 0, wx.ALL, 5)
        loginSizer.Add(self.buttonLogin, 0, wx.ALL, 5)

        # transaction button and text
        self.buttonTransaction = wx.Button(self.panel, label="Absenden", size=(70,50))
        self.buttonTransaction.Disable()
        myFont = wx.Font(
            15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Default')        
        self.transactionLabel = wx.StaticText(self.panel, label='Praemien verteilen: ')
        self.transactionLabel.SetFont(myFont)
        self.transactionLabel.Disable()
        praemienSizer.Add(self.transactionLabel, 0, wx.ALIGN_CENTER)
        praemienSizer.Add(self.buttonTransaction, 0, wx.EXPAND)


        topSizer.Add(loginSizer, 0, wx.CENTER)
        topSizer.Add(outputSizer, 0, wx.CENTER, 5)
        topSizer.Add(praemienSizer, 0, wx.ALL | wx. EXPAND, 5)
        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)

        self.Bind(wx.EVT_BUTTON, self.clickTransaction, self.buttonTransaction)
        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.buttonLogin)

    #----------------------------------------------------------------------
    def onMultiplierDialog(self, event):
        """Dialog to change multiplier value."""
        createConfig()  # if config not existent create it to be able to edit settings
        dlg = SetMultiplierDialog()
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            updateConfig('config.ini', 'Punkte basiert',
                         dlg.multiplierValue.GetValue())
        dlg.Destroy()

    #----------------------------------------------------------------------
    def onMaxPlayGetRewardDialog(self, event):
        """Dialog to change number of players who will get a reward."""
        createConfig()  # if config not existent create it to be able to edit settings
        dlg = MyDialog()
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            updateConfig('config.ini', 'maxPlayerReward',
                         dlg.comboBox1.GetValue())
        dlg.Destroy()
    #----------------------------------------------------------------------

    def onStaticRewardsDialog(self, event):
        """Dialog to change the values of rewards."""
        createConfig()  # if config not existent create it to be able to edit settings
        dlg = SetStaticRewardsDialog()
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            for i in range(int(readConfig('config.ini', '1', 'maxPlayerReward'))):
                updateConfigStaticRewards(
                    'config.ini', i + 1, dlg.ticker_ctrls[i].GetValue())
        dlg.Destroy()

    #----------------------------------------------------------------------
    def onExit(self, event):
        """Event that terminates app Datei > Beenden"""
        self.Close()

    #----------------------------------------------------------------------
    def clickTransaction(self, event):
        """Call the executeTransaction method"""
        if(bot.getLeaderStatus()):
            bot.executeTransaction('config.ini')
        else:
             wx.MessageBox('Du bist kein Communityleader!', 'Fehler!',wx.OK | wx.ICON_ERROR, self.panel)            

    # #----------------------------------------------------------------------
    # def myClick(self, event):
    #     """Event for button which manually sends money to a specific user."""
    #     if(str(self.moneyUserId.GetSelection()) != '-1'):
    #         result = bot.sendMoney(str(self.communityid), str(self.moneyUserId.GetValue()), str(
    #             self.moneyAmount.GetValue()), self.moneyReason.GetValue())
    #         if(result == 200):
    #             self.text.AppendText('\nTransaktion erfolgeich!\nBenutzer: ' + str(self.moneyUserId.GetValue()) +
    #                                  '\nSumme: ' + str(self.moneyAmount.GetValue()) + '\nBegruendung: ' + str(self.moneyReason.GetValue()))
    #         else:
    #             self.text.AppendText('\nTransaktion fehlgeschlagen!')
    #     else:
    #         wx.MessageBox('Keine User ID ausgewaehlt!', 'Fehler!',
    #                       wx.OK | wx.ICON_ERROR, self.panel)

    #----------------------------------------------------------------------
    def printPlacement(self):
        """Print placements of players into output console."""
        bot.getLatestPoints()
        self.text.AppendText('\n-----------------------------------\nPlatzierungen vom ' + str(bot.getLastMatchDay()) + ':')
        counter = 0
        for entry in bot.getPlacementAndUserIds():
            counter = counter + 1
            frame.text.AppendText('\n' + str(counter) + '. Platz mit ' + str(
                entry['totalPoints']) + ' Punkten: ' + str(entry['name']) + '(User ID: ' + str(entry['userid'])
                + ') - Kontostand am Spieltag: ' + str(bot.getWealth(entry['userid'])) + ' Euro')        
        self.text.AppendText('\n-----------------------------------\nVermoegenswerte der Spieler:')
        with open('standings.json', 'w') as outfile:  # save standings into .json file
            json.dump(bot.getPlacementAndUserIds(), outfile)
        for item in self.userlist:
            self.text.AppendText('\nuserid: ' + str(item) +
                                 ', Vermoegen(aktueller MW + Kontostand vom letzten Spieltag): '
                                 + str(int(bot.getWealth(item)) + int(bot.getUserInfo(item))) + ' Euro')

    #----------------------------------------------------------------------
    def getInformationsAfterLogin(self):
        """Updates the gui after login is sucessful."""
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
        labelFont = wx.Font(
            15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Default')
        self.welcomeLabel.SetFont(labelFont)
        self.welcomeLabel.SetLabelText(
            'Willkommen, ' + str(bot.getUserName() + '!'))
        self.text.AppendText(
            '\nCommunity ID: ' + self.communityid + '\nEigene User ID: ' + self.userid)            
        self.printPlacement()  # print placement of last matchday in output console

    #----------------------------------------------------------------------
    def OnButtonClick(self, event):
        """Starts the login."""
        bot.doLogin(self.usernameText.GetValue(),
                    self.passwordText.GetValue())  # execute login
        self.authTokenFromLogin = bot.getAuthToken()  # get authtoken
        #bot.getUserInfo()
        self.panel.Refresh()

########################################################################


class SetMultiplierDialog(wx.Dialog):
    """Class for multiplier dialog."""

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
    """Class for static reward dialog."""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(
            self, None, title="Praemien setzen", size=(230, 770))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.ticker_ctrls = {}
        ticker_items = []
        # for i in range(int(readConfig('config.ini', '1', 'maxPlayerReward'))):
        #     ticker_items.append(readConfig('config.ini', i + 1, 'static'))
        for i in range(18):
            ticker_items.append(readConfig('config.ini', i + 1, 'static'))        

        counter = 0
        for item in ticker_items:
            ctrl = wx.TextCtrl(self, value=item, name=item)
            sizer.Add(ctrl, 0, wx.ALL | wx.CENTER, 5)
            self.ticker_ctrls[counter] = ctrl
            if counter >= int(readConfig('config.ini', '1', 'maxPlayerReward')):
                self.ticker_ctrls[counter].Disable()
            counter = counter + 1
        okBtn = wx.Button(self, wx.ID_OK)
        sizer.Add(okBtn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(sizer)

########################################################################


class MyDialog(wx.Dialog):
    """Class for max player reward dialog."""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Platzierung", size=(100, 100))
        self.value = readConfig('config.ini', '1', 'maxPlayerReward')
        self.comboBox1 = wx.ComboBox(self,
                                     choices=['1', '2', '3', '4', '5', '6',
                                            '7', '8', '9', '10', '11', '12',
                                            '13', '14', '15', '16', '17', '18'],
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
