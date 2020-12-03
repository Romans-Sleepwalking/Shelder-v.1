from datetime import datetime
from datedelta import datedelta
from bs4 import BeautifulSoup as Soup
import requests
import re
import json


class LabasMajasShelter:
    """
    "Labās Mājas" shelter has dogs and cats...
    I will be calling them 'cutties' because they are cute
    """
    segments = {'doggies': 'https://patversme.lv/suni/', 'kitties': 'https://patversme.lv/kaki/'}
    cuttieList = []  # this array will be full of all shelter's registered animals as Cuttie objects
    profile_count = 0

    def __init__(self):
        pass

    def getCutties(self):
        # ______________________________________________________________________________________________________________
        #   STEP No.1: Fetches animal IDs and page URLs; Classifies them by segments: cats/dogs

        for segment in self.segments:
            Ramen = Soup(requests.get(self.segments[segment]).text, 'lxml')  # Fetches segments webpages
            content = Ramen.find('div', {"class": "entry-content full-animal-list"})  # finds the right container

            for a in content.find_all('a', href=True):  # for every url in the animal profiles' list of urls
                cuttieURL = a['href']
                cuttieID = cuttieURL.split('/')[-2]  # extracts animal's unique_id from a url
                if cuttieID not in ['musejie-pavisam', 'kakeni-2']:  # filters non-standard profiles
                    self.cuttieList.append(Cuttie(cuttieID, cuttieURL, segment))

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

            cuttie.registerProfile(  # method registers cutties' profiles
                content.h1.text,  # cuttie's name is the title of a body paragraphs
                clean_paragraphs[:-2],  # cuttie's description is the main body paragraphs
                clean_paragraphs[-1]  # cuttie's age data is the last paragraph
            )
            self.profile_count += 1

        print(str(self.profile_count) + ' profiles fetched!')  # check

        # ______________________________________________________________________________________________________________
        #   STEP No.3: Returns cuttie profiles as JSON

        cuttiesData = {'doggies': [], 'kitties': []}

        for cuttie in self.cuttieList:
            cuttieProfile = {cuttie.id: {'name': cuttie.name, 'description': cuttie.description, 'age': cuttie.age}}
            cuttiesData[cuttie.segment].append(cuttieProfile)
        return json.dumps(cuttiesData)


class Cuttie(LabasMajasShelter):
    def __init__(self, unique_id=str, url=str, animal_segment=str):
        self.id = unique_id
        self.url = url
        self.segment = animal_segment

    def registerProfile(self, name=str, description=str, ageData=str):
        self.name = name
        self.description = description

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
        year_regex = re.search(year_pattern, ageData)  # .

        if year_regex is not None:
            year = int(year_regex.group(2))

            if year not in (2019, 2020):
                ageStamp = datetime.now() - datedelta(years=year, months=month)
                return ageStamp.year
            else:
                return 0
        else:
            return ' '
