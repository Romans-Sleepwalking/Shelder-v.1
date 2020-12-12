import ImageHandler
from datetime import datetime
from datedelta import datedelta
from bs4 import BeautifulSoup as Soup
import re
import wx
import webbrowser
import requests
# _____________________________________________________________________________________________________________________
"""
SHELDER
version 1.1 DEV
@ Romāns Prokopjevs 2020 | Project-2 BITL2 Riga Business School
https://github.com/Romans-Sleepwalking/Shelder

Shelder is a pet speed-dating application
This app has been made to find homes for abandoned darlings using gamification and a modern dating app format

This app use:
    Beautiful Soup library to web scrape data from the "Lābas Mājas" shelter located at Riga, Latvia
    wxPython as a framework library 
    
Executed code:
    1    initializes global class variables and launches the' Landing' frame
    
    2.1  loads the chosen animal segment from the shelter's website and initialize animals as Cuttie class objects
    2.2  analyzes first fetched HTML code: deduces animals profile URLs
    2.3  loads the deduced animal profiles appending data of the Cuttie class objects
    2.4  analyzes second fetched HTML code: figures animals names, age, profile image URLs
    2.5  loads and reformats the profile images to wxPython preferred .bmp at ImageEditor.py (takes much time)
    
    3    starts game; launches FirstRound cycle of frames where a user must choose if the animal is preferable or not
         like Tinder: if the user 'likes' a pet, it won't be deleted from memory.
         
    4    launches SecondRound cycle of frames where the user must choose between two animals which one is preferable:
         the chosen animal won't be deleted from memory.
    
    5    showcases the winner - most preferable animal with the button leading to browser - to the official profile page
    
Problems:
    App rejected all the tryouts of DataClass-FrameworkClass-GameClass separation so that the main.py may be too long
    Framework's documentation is ancient (mostly ~Python 2.6 examples). Numerous design improvement tryouts failed:
        'loading bar' widget
        imageButton widgets
        
Maybe a second app version is coming soon.
"""
# _____________________________________________________________________________________________________________________
#   Frame1:  Landing with segment choice


class Landing(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Landing, self).__init__(*args, **kwargs)

        # sets up app window's icon
        appIcon = wx.Icon('app_icon.ico', wx.BITMAP_TYPE_ANY)
        self.SetIcon(appIcon)

        self.InitMainPanel()  # calls function which sets app main content

        self.InitMenus()  # calls function which sets up app menubar

        # window's size, naming, appearance
        self.SetSize((600, 800))
        self.SetTitle('Shelder App - Just Pick Your Love')
        self.Center()
        self.Show(True)

    def InitMainPanel(self):  # sets app main content
        panel = wx.Panel(self)

        panel.SetBackgroundColour('#FFF5E8')  # bg color

        # title text widget
        titleFont = wx.Font(50, family=wx.FONTFAMILY_MODERN, style=0, weight=90)
        titleWidget = wx.StaticText(parent=panel, pos=((150, 180)), label="Shelder")
        titleWidget.SetFont(titleFont)

        # moto text widget
        motoFont = wx.Font(18, family=wx.FONTFAMILY_MODERN, style=0, weight=90)
        motoWidget = wx.StaticText(parent=panel, pos=((90, 280)), label="Your love is waiting for you!")
        motoWidget.SetFont(motoFont)

        # dogs/cats button widgets
        self.dogButton = wx.Button(panel, -1, label='Dogs', pos=(50, 400))
        self.catButton = wx.Button(panel, -1, label='Cats', pos=(320, 400))
        self.dogButton.SetSize(200, 170)
        self.catButton.SetSize(200, 170)
        self.Bind(wx.EVT_BUTTON, self.chosenDoggies, self.dogButton)
        self.Bind(wx.EVT_BUTTON, self.chosenKitties, self.catButton)
        self.dogButton.SetDefault()
        self.catButton.SetDefault()

    def chosenDoggies(self, e):  # pressed 'Dogs' button
        global db
        db = LabasMajasShelter('doggies')  # initializes data-list for doggo kitty segment
        self.Close()  # closes frame
        game.firstRound()  # calls the first game-round

    def chosenKitties(self, e):  # pressed 'Cats' button
        global db
        db = LabasMajasShelter('kitties')  # initializes data-list for chosen kitty segment
        self.Close()  # closes frame
        game.firstRound()  # calls the first game-round

    def InitMenus(self):  # sets up app menubar
        menubar = wx.MenuBar()
        aboutMenu = wx.Menu()
        shelterMenuItem = wx.MenuItem(aboutMenu, SHOW_SHELTER, 'More About "Labās Mājas"')
        creditsMenuItem = wx.MenuItem(aboutMenu, SHOW_CREDITS, 'Credits')
        aboutMenu.AppendItem(shelterMenuItem)
        aboutMenu.AppendItem(creditsMenuItem)
        menubar.Append(aboutMenu, 'More')
        self.Bind(wx.EVT_MENU, self.ShowShelter, id=SHOW_SHELTER)
        self.Bind(wx.EVT_MENU, self.ShowCredits, id=SHOW_CREDITS)
        self.SetMenuBar(menubar)

    @staticmethod
    def ShowShelter(e):  # pressed 'More About Labās Mājas' button
        webbrowser.open('https://patversme.lv/', new=2)  # opens 'Labās Mājas' shelter's webpage in a new tab

    def ShowCredits(self, e):  # pressed 'Credits' button
        credits_text = 'Shelter App @ Romāns Prokopjevs 2020 | Project-2 BITL2 Riga Business School'  # displays this
        dlg = wx.MessageDialog(self, credits_text, 'Credits', wx.OK)
        result = dlg.ShowModal()
        dlg.Destroy()


# _____________________________________________________________________________________________________________________
#   Frame2:  First Round


class YesOrNo(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(YesOrNo, self).__init__(*args, **kwargs)

        # sets up app window's icon
        appIcon = wx.Icon('app_icon.ico', wx.BITMAP_TYPE_ANY)
        self.SetIcon(appIcon)

        self.InitMainPanel()  # calls function which sets app main content

        # window's size, naming, appearance
        self.SetSize((600, 800))
        self.SetTitle('Shelder App - Just Pick Your Love')
        self.Center()
        self.Show(True)

    def InitMainPanel(self):  # sets app main content
        panel = wx.Panel(self)

        panel.SetBackgroundColour('#FEFFE8')  # bg color

        # profile image widget
        self.img1 = wx.StaticBitmap(panel, -1, wx.Bitmap(db.cursor1.img))
        self.img1.SetPosition((40, 40))

        # cuttie's name+age text widget
        ProfileFont = wx.Font(24, family=wx.FONTFAMILY_MODERN, style=0, weight=90)
        ProfileWidget = wx.StaticText(parent=panel, pos=((40, 450)), label=db.cursor1.name + db.cursor1.age)
        ProfileWidget.SetFont(ProfileFont)

        # no/yes button widgets
        self.noButton = wx.Button(panel, -1, label='Skip cuttie', pos=(40, 535))
        self.noButton.SetSize(200, 150)
        self.Bind(wx.EVT_BUTTON, self.No, self.noButton)
        self.noButton.SetDefault()

        self.yesButton = wx.Button(panel, -1, label='Like! <3', pos=(330, 535))
        self.yesButton.SetSize(200, 150)
        self.Bind(wx.EVT_BUTTON, self.Yes, self.yesButton)
        self.yesButton.SetDefault()

    def No(self, e):  # pressed 'No' button
        db.cursor1.status = False  # removes the cuttie obj from the data-list
        self.Close()  # closes frame

    def Yes(self, e):  # pressed 'Yes' button
        self.Close()  # just closes frame


# _____________________________________________________________________________________________________________________
#   Frame3:  Second Round


class LeftOrRight(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(LeftOrRight, self).__init__(*args, **kwargs)

        # sets up app window's icon
        appIcon = wx.Icon('app_icon.ico', wx.BITMAP_TYPE_ANY)
        self.SetIcon(appIcon)

        self.InitMainPanel()  # calls function which sets app main content

        # window's size, naming, appearance
        self.SetSize((1200, 800))
        self.SetTitle('Shelder App - Just Pick Your Love')
        self.Center()
        self.Show(True)

    def InitMainPanel(self):  # sets app main content
        panel = wx.Panel(self)

        panel.SetBackgroundColour('#FFF5E8')  # bg color

        # two profile image widgets
        self.img1 = wx.StaticBitmap(panel, -1, wx.Bitmap(db.cursor1.img))
        self.img2 = wx.StaticBitmap(panel, -1, wx.Bitmap(db.cursor2.img))
        self.img1.SetPosition((56, 80))
        self.img2.SetPosition((630, 80))

        # left/right button widgets
        self.leftButton = wx.Button(panel, -1, label='Left One!', pos=(90, 535))
        self.rightButton = wx.Button(panel, -1, label='Right One!', pos=(692, 535))
        self.leftButton.SetSize(400, 150)
        self.rightButton.SetSize(400, 150)
        self.Bind(wx.EVT_BUTTON, self.Left, self.leftButton)
        self.Bind(wx.EVT_BUTTON, self.Right, self.rightButton)
        self.leftButton.SetDefault()
        self.rightButton.SetDefault()

    def Left(self, e):  # pressed 'Left' button
        db.cursor2.status = False  # removes the other, unchosen obj from the data list
        self.Close()  # closes frame

    def Right(self, e):  # pressed 'Right' button
        db.cursor1.status = False  # removes the other, unchosen obj from the data list
        self.Close()  # closes frame


# _____________________________________________________________________________________________________________________
#   Frame4:  The Winner Showcase


class ShowTheWinner(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(ShowTheWinner, self).__init__(*args, **kwargs)

        # sets up app window's icon
        appIcon = wx.Icon('app_icon.ico', wx.BITMAP_TYPE_ANY)
        self.SetIcon(appIcon)

        self.InitMainPanel()  # calls function which sets app main content

        self.InitMenus()  # calls function which sets up app menubar

        # window's size, naming, appearance
        self.SetSize((1200, 800))
        self.SetTitle('Shelder App - Just Pick Your Love')
        self.Center()
        self.Show(True)

    def InitMainPanel(self):  # sets app main content
        panel = wx.Panel(self)

        panel.SetBackgroundColour('#E8FCE6')  # bg color

        # profile image widget
        self.img = wx.StaticBitmap(panel, -1, wx.Bitmap(db.cursor1.img))
        self.img.SetPosition((56, 80))

        # cuttie's name+age and ending text widgets
        NameFont = wx.Font(30, family=wx.FONTFAMILY_MODERN, style=0, weight=90)
        EndingFont = wx.Font(25, family=wx.FONTFAMILY_MODERN, style=0, weight=90)
        NameWidget = wx.StaticText(parent=panel, pos=((700, 240)), label=db.cursor1.name + db.cursor1.age)
        EndingWidget = wx.StaticText(parent=panel, pos=((700, 300)), label="Is Waiting For You!")
        NameWidget.SetFont(NameFont)
        EndingWidget.SetFont(EndingFont)

        # 'Get' button widget
        self.linkButton = wx.Button(panel, -1, label='Get', pos=(692, 450))
        self.linkButton.SetSize(400, 150)
        self.Bind(wx.EVT_BUTTON, self.UseLink, self.linkButton)
        self.linkButton.SetDefault()

        # 'More Cutties' button widget
        self.moreCuttiesButton = wx.Button(panel, -1, label='More Kitties :3', pos=(200, 500))
        self.moreCuttiesButton.SetSize(200, 80)
        self.Bind(wx.EVT_BUTTON, self.MoreCutties, self.moreCuttiesButton)
        self.moreCuttiesButton.SetDefault()

    @staticmethod
    def UseLink(e):  # pressed 'Get' button
        webbrowser.open(db.cursor1.url, new=2)  # opens 'Labās Mājas' shelter game winner's profile webpage in a new tab

    @staticmethod
    def MoreCutties(e):
        ImageHandler.MorePictures(db.segment)

    def InitMenus(self):  # calls function which sets up app menubar
        menubar = wx.MenuBar()
        aboutMenu = wx.Menu()
        shelterMenuItem = wx.MenuItem(aboutMenu, SHOW_SHELTER, 'More About "Labās Mājas"')
        creditsMenuItem = wx.MenuItem(aboutMenu, SHOW_CREDITS, 'Credits')
        aboutMenu.AppendItem(shelterMenuItem)
        aboutMenu.AppendItem(creditsMenuItem)
        menubar.Append(aboutMenu, 'More')
        self.Bind(wx.EVT_MENU, self.ShowShelter, id=SHOW_SHELTER)
        self.Bind(wx.EVT_MENU, self.ShowCredits, id=SHOW_CREDITS)
        self.SetMenuBar(menubar)

    @staticmethod
    def ShowShelter(e):  # pressed 'More About Labās Mājas' button
        webbrowser.open('https://patversme.lv/', new=2)  # opens 'Labās Mājas' shelter's webpage in a new tab

    def ShowCredits(self, e):  # pressed 'Credits' button
        credits_text = 'Shelter App @ Romāns Prokopjevs 2020 | Project-2 BITL2 Riga Business School'  # displays this
        dlg = wx.MessageDialog(self, credits_text, 'Credits', wx.OK)
        result = dlg.ShowModal()
        dlg.Destroy()

# ______________________________________________________________________________________________________________
#   Data fetching and processing


class LabasMajasShelter:
    """
    The "Labās Mājas" shelter has dogs and cats separated in two segments on the official website
    The shelter animals has been called 'cutties' because they are cute
    The core of the cycling data is the 'cuttieList' data-list which contains Active Game Participants
    During subjective choices between cutties the unchosen animals will be erased from 'cuttieList'
    The old framework did not support 2nd party arguments, so author came up with 'cursors' for marking cuttie objects
    Beware of potential EXTREME IMAGE CACHE quantity at the main folder!
    """
    segmentURLs = {'doggies': 'https://patversme.lv/suni/', 'kitties': 'https://patversme.lv/kaki/'}
    cuttieList = []
    activeCutties = []
    fetchCounter = 0
    cursor1 = None
    cursor2 = None

    def __init__(self, segment):  # called from the 'Landing' frame with chosen dogs/cats segment
        self.segment = segment
        # fetches the chosen animal segment and finds the right HTML-container
        Ramen = Soup(requests.get(self.segmentURLs[self.segment]).text, 'lxml')
        content = Ramen.find('div', {"class": "entry-content full-animal-list"})

        blackList = ['musejie-pavisam', 'kakeni-2', 'carlijs', 'kadrija']  # some known collective/unreadable profiles

        # initialize all whitelist cuties' by finding the profile page URLs from the right container
        for a in content.find_all('a', href=True):
            cuttieURL = a['href']
            cuttieID = cuttieURL.split('/')[-2]  # extracts unique ID from URL
            if cuttieID not in blackList:
                self.cuttieList.append(Cuttie(cuttieURL))

        print('Latest profile URLs have been fetched!')

        # cutties' data collection from the every saved URL
        for cuttie in self.cuttieList:

            # fetches the cuttie's profile page and finds the right HTML-container
            TomYum = Soup(requests.get(cuttie.url).text, 'lxml')
            content = TomYum.find('div', {"class": "card-body"})

            # finds cuttie description paragraphs; remove HTML and other junk from the paragraphs
            HTML_paragraphs = content.findAll('p')
            HTML_paragraphs.pop(0)
            clean_paragraphs = []
            for p in HTML_paragraphs:
                HTML_pattern = '(<p>)(.*)(</p>)'
                HTML_regex = re.search(HTML_pattern, str(p))
                bad_pattern = '(Foto)(.*)'
                if re.search(bad_pattern, HTML_regex[2]) is None:
                    clean_paragraphs.append(str(HTML_regex[2]))

            # This fixes some problems with the age data
            if len(clean_paragraphs) in (1, 2):
                clean_paragraphs.append(' ')

            # finds the profile image URL; removes all the junk around the link
            HTML_img = TomYum.find('img', {"class": "card-img-left wp-post-image"})
            HTML_pattern = '(.*)(src=")(.*)(" srcset=")(.*)'
            HTML_regex = re.search(HTML_pattern, str(HTML_img))

            if HTML_regex is None:  # one known pattern exception
                HTML_pattern = '(.*)(src=")(.*)(" width=)(.*)'
                HTML_regex = re.search(HTML_pattern, str(HTML_img))

            # calls the data registration method for cuttie object
            cuttie.registerProfile(
                content.h1.text,  # cuttie's name is the title of a body paragraphs
                clean_paragraphs[-1],  # cuttie's age data is probably in the last paragraph
                HTML_regex.group(3)  # profile image URL
            )
            self.fetchCounter += 1  # updates counter

        print(str(self.fetchCounter) + ' profiles fetched!')


class Cuttie(LabasMajasShelter):
    def __init__(self, url=str):  # called from the LabasMajasShelter.__init__ method
        self.url = url  # initialize cuttie's profile using URL

    def registerProfile(self, name=str, ageData=str, imgURL=str):  # called from the LabasMajasShelter.__init__ method
        self.name = name
        self.img = ImageHandler.getImage(imgURL)  # calls the supported ImageHandler.py; returns profile image location
        self.status = True  # if True - status is active

        # check for age data: if exist -> calls the decoding method
        if ageData != ' ':
            self.age = self.calcAge(ageData)
        else:
            self.age = ageData

        print('+' + self.name + ' (' + str(self.age) + ' y.o.)')

    @staticmethod
    def calcAge(ageData):  # called from the registerProfile method

        # the Latvian language key-month-word-part dictionary
        monthDict = {'janvār': 1, 'februār': 2, 'mart': 3, 'aprīl': 4, 'maij': 5, 'jūnij': 6, 'jūlij': 7,
                     'august': 8, 'septembr': 9, 'oktobr': 10, 'novembr': 11, 'decembr': 12}
        month = 6  # the approximate medium for the cases where is no month

        # searches for the month using regex and month dictionary
        for mm in monthDict:
            if re.search(mm, ageData) is not None:
                month = monthDict[mm]

        # searches for the year using regex
        year_pattern = '(.*)(20\d\d)(.*)'
        year_regex = re.search(year_pattern, ageData)

        if year_regex is not None:  # if year information exist
            year = int(year_regex.group(2))

            # if cuttie is younger than one year, he/she will get: <1
            if year not in (2019, 2020):
                ageStamp = datetime.now() - datedelta(years=year, months=month)
                return ', ' + str(ageStamp.year)  # non-baby cutties will get calculated age
            else:
                return ', <1'  # if cuttie is younger than one year, he/she will get: <1
        else:
            return ' '  # if year information does not exist


# _____________________________________________________________________________________________________________________
#   Game

class Game:
    def __init__(self):  # called from the launch
        pass

    def firstRound(self):  # called from the chosen doggies/kitties

        for cuttie in db.cuttieList:  # for every active cuttie
            db.cursor1 = cuttie  # pointer
            app_2 = wx.App()
            YesOrNo(None)  # launches the 'FirstRound' frame
            app_2.MainLoop()
            del app_2  # deletes the frame to recall it more than once

        self.secondRound()  # calls the second round

    def secondRound(self):  # called from the firstRound method

        # refreshes the list of active participants
        for cuttie in db.cuttieList:
            if cuttie.status is True:
                db.activeCutties.append(cuttie)

        while len(db.activeCutties) != 1:  # while winner is not defined -> first/next iteration

            for cuttie in db.activeCutties:  # TEST
                print(cuttie.name)

            for cuttie in db.activeCutties:  # for every active cuttie

                index = db.activeCutties.index(cuttie)  # remember index

                if index % 2 == 1:  # if index was not the last -> duel partner exist (first index is 0)

                    # sets cursors for a duel
                    db.cursor1 = db.activeCutties[index]
                    db.cursor2 = db.activeCutties[index - 1]

                    app_3 = wx.App()
                    LeftOrRight(None)  # launches the 'SecondRound' frame
                    app_3.MainLoop()
                    del app_3  # deletes the frame to recall it more than once

            # refreshes the list of active participants
            db.activeCutties = []
            for cuttie in db.cuttieList:
                if cuttie.status is True:
                    db.activeCutties.append(cuttie)

        self.showTheWinner()  # If one active participant left, the cuttie wins

    @staticmethod
    def showTheWinner():  # called from the secondRound method
        db.cursor1 = db.activeCutties[0]  # reads the last stand cuttie
        app_4 = wx.App()
        ShowTheWinner(None)  # launches the 'WinnerShowcase' frame
        app_4.MainLoop()


# _____________________________________________________________________________________________________________________
#   Launch

if __name__ == '__main__':
    SHOW_SHELTER = 1  # required for proper menu panel
    SHOW_CREDITS = 2

    game = Game()  # global game class variable

    app_1 = wx.App()
    Landing(None)  # launches the first 'Landing' frame
    app_1.MainLoop()

input()
