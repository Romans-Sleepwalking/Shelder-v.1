import ImageEditor
from datetime import datetime
from datedelta import datedelta
from bs4 import BeautifulSoup as Soup
import requests
import re
import wx
import webbrowser
# _____________________________________________________________________________________________________________________
"""
SHELDER
version 1.0
@ Romāns Prokopjevs 2020 | Project-2 BITL2 Riga Business School

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
    Framework's documentation is ancient (mostly ~Python 2.6 examples). Numerous design improvement tryouts failed
        as 'loading bar' widget or buttonIcons
        
Maybe a second app version is coming soon.
"""
# _____________________________________________________________________________________________________________________
#   Frame1:  Landing with segment choice


class Landing(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Landing, self).__init__(*args, **kwargs)
        appIcon = wx.Icon('app_icon.ico', wx.BITMAP_TYPE_ANY)
        self.SetIcon(appIcon)
        self.InitUI()

    def InitUI(self):
        self.InitMenus()
        self.InitMainPanel()

        self.SetSize((600, 800))
        self.SetTitle('Shelder App - Just Pick Your Love')
        self.Center()
        self.Show(True)

    def InitMainPanel(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#FFF5E8')

        # title
        titleFont = wx.Font(50, family=wx.FONTFAMILY_MODERN, style=0, weight=90, underline=False, faceName="",
                            encoding=wx.FONTENCODING_DEFAULT)
        titleWidget = wx.StaticText(parent=panel, pos=((150, 180)), label="Shelder")
        titleWidget.SetFont(titleFont)

        # moto
        motoFont = wx.Font(18, family=wx.FONTFAMILY_MODERN, style=0, weight=90, underline=False, faceName="",
                           encoding=wx.FONTENCODING_DEFAULT)
        motoWidget = wx.StaticText(parent=panel, pos=((90,280)), label="Your love is waiting for you!")
        motoWidget.SetFont(motoFont)

        # then create the widget
        # dogIcon = wx.Image(r"C:\Users\37120\OneDrive\Desktop\Computer Science\Shelder\dog_icon.bmp", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        # catIcon = wx.Image("cat_icon.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.dogButton = wx.Button(panel, -1, label='Dogs', pos=(50, 400))
        self.catButton = wx.Button(panel, -1, label='Cats', pos=(320, 400))
        self.dogButton.SetSize(200, 170)
        self.catButton.SetSize(200, 170)
        self.Bind(wx.EVT_BUTTON, self.chosenDoggies, self.dogButton)
        self.Bind(wx.EVT_BUTTON, self.chosenKitties, self.catButton)
        self.dogButton.SetDefault()
        self.catButton.SetDefault()

    def chosenDoggies(self, e):
        global db
        db = LabasMajasShelter('doggies')
        self.Close()
        game.firstRound()

    def chosenKitties(self, e):
        global db
        db = LabasMajasShelter('kitties')
        self.Close()
        game.firstRound()

    def FirstRound(self, event):
        pass

    def InitMenus(self):
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

    def ShowShelter(self, e):
        shelter_info = "More about the shelter at https://patversme.lv/"
        dlg = wx.MessageDialog(self, shelter_info, 'About "Lābas Mājas"', wx.OK)
        result = dlg.ShowModal()
        dlg.Destroy()

    def ShowCredits(self, e):
        credits_text = 'Shelter App @ Romāns Prokopjevs 2020 | Project-2 BITL2 Riga Business School'
        dlg = wx.MessageDialog(self, credits_text, 'Credits', wx.OK)
        result = dlg.ShowModal()
        dlg.Destroy()


def main():
    app_1 = wx.App()
    Landing(None)
    app_1.MainLoop()


# _____________________________________________________________________________________________________________________
#   Frame2:  First Round


class YesOrNo(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(YesOrNo, self).__init__(*args, **kwargs)
        appIcon = wx.Icon('app_icon.ico', wx.BITMAP_TYPE_ANY)
        self.SetIcon(appIcon)
        self.InitUI()

    def InitUI(self):
        self.InitMenus()
        self.InitMainPanel()

        self.SetSize((600, 800))
        self.SetTitle('Shelder App - Just Pick Your Love')
        self.Center()
        self.Show(True)

    def InitMainPanel(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#FEFFE8')

        cuttie = db.cursor1

        self.img1 = wx.StaticBitmap(panel, -1, wx.Bitmap(db.cursor1.img))
        self.img1.SetPosition((40, 40))

        ProfileFont = wx.Font(24, family=wx.FONTFAMILY_MODERN, style=0, weight=90, underline=False, faceName="",
                              encoding=wx.FONTENCODING_DEFAULT)
        ProfileWidget = wx.StaticText(parent=panel, pos=((40, 450)), label=cuttie.name + cuttie.age)
        ProfileWidget.SetFont(ProfileFont)

        self.noButton = wx.Button(panel, -1, label='Skip cuttie', pos=(40, 535))
        self.yesButton = wx.Button(panel, -1, label='Like! <3', pos=(330, 535))

        self.noButton.SetSize(200, 150)
        self.yesButton.SetSize(200, 150)
        self.Bind(wx.EVT_BUTTON, self.No, self.noButton)
        self.Bind(wx.EVT_BUTTON, self.Yes, self.yesButton)
        self.noButton.SetDefault()
        self.yesButton.SetDefault()

    def No(self, e):
        print('no')
        db.cuttieList.remove(db.cursor1)
        self.Close()

    def Yes(self, e):
        print('yes')
        self.Close()

    def InitMenus(self):
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

    def ShowShelter(self, e):
        shelter_info = "More about the shelter at https://patversme.lv/"
        dlg = wx.MessageDialog(self, shelter_info, 'About "Lābas Mājas"', wx.OK)
        result = dlg.ShowModal()
        dlg.Destroy()

    def ShowCredits(self, e):
        credits_text = 'Shelter App @ Romāns Prokopjevs 2020 | Project-2 BITL2 Riga Business School'
        dlg = wx.MessageDialog(self, credits_text, 'Credits', wx.OK)
        result = dlg.ShowModal()
        dlg.Destroy()


# _____________________________________________________________________________________________________________________
#   Frame3:  Second Round


class LeftOrRight(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(LeftOrRight, self).__init__(*args, **kwargs)
        appIcon = wx.Icon('app_icon.ico', wx.BITMAP_TYPE_ANY)
        self.SetIcon(appIcon)
        self.InitUI()

    def InitUI(self):
        self.InitMenus()
        self.InitMainPanel()

        self.SetSize((1200, 800))
        self.SetTitle('Shelder App - Just Pick Your Love')
        self.Center()
        self.Show(True)

    def InitMainPanel(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#FFF5E8')

        self.img1 = wx.StaticBitmap(panel, -1, wx.Bitmap(db.cursor1.img))
        self.img2 = wx.StaticBitmap(panel, -1, wx.Bitmap(db.cursor2.img))
        self.img1.SetPosition((56, 80))
        self.img2.SetPosition((630, 80))

        self.leftButton = wx.Button(panel, -1, label='Left One!', pos=(90, 535))
        self.rightButton = wx.Button(panel, -1, label='Right One!', pos=(692, 535))

        self.leftButton.SetSize(400, 150)
        self.rightButton.SetSize(400, 150)
        self.Bind(wx.EVT_BUTTON, self.Left, self.leftButton)
        self.Bind(wx.EVT_BUTTON, self.Right, self.rightButton)
        self.leftButton.SetDefault()
        self.rightButton.SetDefault()

    def Left(self, e):
        print('left')
        db.cuttieList.remove(db.cursor2)
        self.Close()

    def Right(self, e):
        print('right')
        db.cuttieList.remove(db.cursor1)
        self.Close()

    def InitMenus(self):
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

    def ShowShelter(self, e):
        shelter_info = "More about the shelter at https://patversme.lv/"
        dlg = wx.MessageDialog(self, shelter_info, 'About "Lābas Mājas"', wx.OK)
        result = dlg.ShowModal()
        dlg.Destroy()

    def ShowCredits(self, e):
        credits_text = 'Shelter App @ Romāns Prokopjevs 2020 | Project-2 BITL2 Riga Business School'
        dlg = wx.MessageDialog(self, credits_text, 'Credits', wx.OK)
        result = dlg.ShowModal()
        dlg.Destroy()


# _____________________________________________________________________________________________________________________
#   Frame4:  The Winner Showcase


class ShowTheWinner(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(ShowTheWinner, self).__init__(*args, **kwargs)
        appIcon = wx.Icon('app_icon.ico', wx.BITMAP_TYPE_ANY)
        self.SetIcon(appIcon)
        self.InitUI()

    def InitUI(self):
        self.InitMenus()
        self.InitMainPanel()

        self.SetSize((1200, 800))
        self.SetTitle('Shelder App - Just Pick Your Love')
        self.Center()
        self.Show(True)

    def InitMainPanel(self):
        cuttie = db.cursor1

        panel = wx.Panel(self)
        panel.SetBackgroundColour('#E8FCE6')

        self.img = wx.StaticBitmap(panel, -1, wx.Bitmap(cuttie.img))
        self.img.SetPosition((56, 80))

        NameFont = wx.Font(30, family=wx.FONTFAMILY_MODERN, style=0, weight=90, underline=False, faceName="",
                             encoding=wx.FONTENCODING_DEFAULT)
        EndingFont = wx.Font(25, family=wx.FONTFAMILY_MODERN, style=0, weight=90, underline=False, faceName="",
                             encoding=wx.FONTENCODING_DEFAULT)
        NameWidget = wx.StaticText(parent=panel, pos=((700, 240)), label=cuttie.name + cuttie.age)
        EndingWidget = wx.StaticText(parent=panel, pos=((700, 300)), label="Is Waiting For You!")
        NameWidget.SetFont(NameFont)
        EndingWidget.SetFont(EndingFont)

        self.linkButton = wx.Button(panel, -1, label='Get', pos=(692, 450))
        self.linkButton.SetSize(400, 150)
        self.Bind(wx.EVT_BUTTON, self.UseLink, self.linkButton)
        self.linkButton.SetDefault()

    @staticmethod
    def UseLink(e):
        print('Link Used!')
        webbrowser.open(db.cursor1.url, new=2)

    def InitMenus(self):
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

    def ShowShelter(self, e):
        shelter_info = "More about the shelter at https://patversme.lv/"
        dlg = wx.MessageDialog(self, shelter_info, 'About "Lābas Mājas"', wx.OK)
        result = dlg.ShowModal()
        dlg.Destroy()

    def ShowCredits(self, e):
        credits_text = 'Shelter App @ Romāns Prokopjevs 2020 | Project-2 BITL2 Riga Business School'
        dlg = wx.MessageDialog(self, credits_text, 'Credits', wx.OK)
        result = dlg.ShowModal()
        dlg.Destroy()


# ______________________________________________________________________________________________________________
#   Data fetching and processing


class LabasMajasShelter:
    """
    "Labās Mājas" shelter has dogs and cats...
    I will be calling them 'cutties' because they are cute
    """
    segmentURLs = {'doggies': 'https://patversme.lv/suni/', 'kitties': 'https://patversme.lv/kaki/'}
    cuttieList = []  # this array will be full of all shelter's registered animals as Cuttie objects
    fetchCounter = 0
    cursor1 = None
    cursor2 = None

    def __init__(self, segment):
        # ______________________________________________________________________________________________________________
        #   STEP No.1: Fetches animal IDs and page URLs; Classifies them by segments: cats/dogs

        Ramen = Soup(requests.get(self.segmentURLs[segment]).text, 'lxml')  # Fetches segments webpages
        content = Ramen.find('div', {"class": "entry-content full-animal-list"})  # finds the right container

        for a in content.find_all('a', href=True):  # for every url in the animal profiles' list of urls
            cuttieURL = a['href']
            cuttieID = cuttieURL.split('/')[-2]  # extracts animal's unique_id from a url
            if cuttieID not in ['musejie-pavisam', 'kakeni-2', 'carlijs', 'kadrija']:  # filters non-standard profiles
                self.cuttieList.append(Cuttie(cuttieID, cuttieURL))

        print('Latest profile URLs have been fetched!')  # check

        # ______________________________________________________________________________________________________________
        #   STEP No.2: Fetches and registers profiles using URLs

        for cuttie in self.cuttieList:
            TomYum = Soup(requests.get(cuttie.url).text, 'lxml')  # fetches a full particulars animal's profile page
            content = TomYum.find('div', {"class": "card-body"})  # finds the right container
            html_paragraphs = content.findAll('p')  # finds the body paragraphs

            # Cures the paragraphs from HTML
            html_paragraphs.pop(0)
            clean_paragraphs = []
            for p in html_paragraphs:
                p = str(p).replace('<p>', "")
                p = p.replace('</p>', "")
                clean_paragraphs.append(p)

            # Deletes unnecessary data
            for p in clean_paragraphs:
                bad_pattern = '(Foto)(.*)'
                if re.search(bad_pattern, p) is not None:
                    clean_paragraphs.remove(p)

            # In case if Labās Mājas didn't add the age data
            if len(clean_paragraphs) == 1:
                clean_paragraphs.extend([' ', ' '])
            elif len(clean_paragraphs) == 2:
                clean_paragraphs.append(' ')

            imgHTML = TomYum.find('img', {"class": "card-img-left wp-post-image"})  # finds the right container
            imgHTML_pattern = '(.*)(src=")(.*)(" srcset=")(.*)'
            imgHTML_regex = re.search(imgHTML_pattern, str(imgHTML))

            if imgHTML_regex is None:
                imgHTML_pattern = '(.*)(src=")(.*)(" width=)(.*)'
                imgHTML_regex = re.search(imgHTML_pattern, str(imgHTML))

            cuttie.registerProfile(     # method registers cutties' profiles
                content.h1.text,        # cuttie's name is the title of a body paragraphs
                clean_paragraphs[:-2],  # cuttie's description is the main body paragraphs
                clean_paragraphs[-1],   # cuttie's age data is the last paragraph
                imgHTML_regex.group(3)  # profile image URL
            )
            self.fetchCounter += 1

        print(str(self.fetchCounter) + ' profiles fetched!')  # check


class Cuttie(LabasMajasShelter):
    def __init__(self, unique_id=str, url=str):
        self.id = unique_id
        self.url = url

    def registerProfile(self, name=str, description=str, ageData=str, imgURL=str):
        self.name = name
        self.description = description
        self.img = ImageEditor.getImage(imgURL)

        if ageData != ' ':
            self.age = self.calcAge(ageData)
        else:
            self.age = ageData

        print('+' + self.name + ' (' + str(self.age) + ' y.o.)')

    @staticmethod
    def calcAge(ageData):
        monthDict = {'janvār': 1, 'februār': 2, 'mart': 3, 'aprīl': 4, 'maij': 5, 'jūnij': 6, 'jūlij': 7,
                     'august': 8, 'septembr': 9, 'oktobr': 10, 'novembr': 11, 'decembr': 12}
        month = 6  # the approximate medium

        for mm in monthDict:
            if re.search(mm, ageData) is not None:
                month = monthDict[mm]

        year_pattern = '(.*)(20\d\d)(.*)'
        year_regex = re.search(year_pattern, ageData)

        if year_regex is not None:
            year = int(year_regex.group(2))

            if year not in (2019, 2020):
                ageStamp = datetime.now() - datedelta(years=year, months=month)
                return ', ' + str(ageStamp.year)
            else:
                return ', <1'
        else:
            return ' '


# _____________________________________________________________________________________________________________________
#   Game

class Game:
    def __init__(self):
        pass

    def firstRound(self):
        for cuttie in db.cuttieList:
            db.cursor1 = cuttie
            app_2 = wx.App()
            YesOrNo(None)
            app_2.MainLoop()
            del app_2

        self.secondRound()

    def secondRound(self):
        while len(db.cuttieList) != 1:
            active_cuttie_count = len(db.cuttieList)

            for i in db.cuttieList:
                index = db.cuttieList.index(i)

                if index != active_cuttie_count // 2:
                    db.cursor1 = db.cuttieList[index]
                    db.cursor2 = db.cuttieList[index + 1]
                    app_3 = wx.App()
                    LeftOrRight(None)
                    app_3.MainLoop()
                    del app_3

        self.showTheWinner()

    @staticmethod
    def showTheWinner():
        db.cursor1 = db.cuttieList[0]
        print(db.cursor1.name + ' is the ultimate winner!!!')
        app_4 = wx.App()
        ShowTheWinner(None)
        app_4.MainLoop()


# _____________________________________________________________________________________________________________________
#   Launch

if __name__ == '__main__':
    SHOW_SHELTER = 1
    SHOW_CREDITS = 2
    game = Game()
    gameRoom = []
    main()
