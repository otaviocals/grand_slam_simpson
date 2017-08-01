#Required external modules: Selenium, BeautifoulSoup4,

from csv import writer, reader
from contextlib import closing
from selenium.webdriver import PhantomJS
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
from os.path import isdir
from os import makedirs, getcwd, remove
from sys import platform
from datetime import datetime, timedelta
from dateutil.parser import parse
from urllib.request import urlretrieve
from glob import glob
from zipfile import ZipFile
import sys

######################
# Webscrapping Stage #
######################

def GrandSlamScraper(folder,  phantom_path = ""):

    #Australian Open Results URLs

    url="http://www.espn.com/tennis/scoreboard/_/year/2017/tournamentId/154/matchType/1"

    rows = []
    row = []
    append_to_csv = False
    current_os = platform

    if current_os.startswith("linux"):
        slash = "/"
    elif current_os.startswith("win32") or current_os.startswith("cygwin"):
        slash = "\\"
    elif current_os.startswith("darwin"):
        slash = "/"
    else:
        slash = "/"

    folder_data = folder+slash+"data"
    folder_logs = folder+slash+"logs"


#Checking Folders Existence

    if(not isdir(folder)):
        makedirs(folder)
    if(not isdir(folder_data)):
        makedirs(folder_data)
    if(not isdir(folder_logs)):
        makedirs(folder_logs)

#Getting Raw Data

    with closing(PhantomJS(phantom_path)) as browser:

        browser.implicitly_wait(2)
        tries = 0

    #Getting Newest Data Date

        print(url)
        browser.get(url)
        while tries <= 20:

            #Getting Data
            data_source = browser.find_element_by_xpath(
                    "//div[@id=\"content\"]/div[@class=\"span-4\"]")

            #Getting Matches Titles
            titles_source = data_source.find_elements_by_xpath(
                    "//div[@class=\"matchTitle\"]")

            #Getting Matches Columns
            matches_clear_source = data_source.find_elements_by_xpath(
                    "//div[@class=\"span-4\"]/div[@class=\"span-2 clear\"]")

            matches_last_source = data_source.find_elements_by_xpath(
                    "//div[@class=\"span-4\"]/div[@class=\"span-2 last\"]")

            for i in range(len(titles_source)):
                title = titles_source[i].text

                matches_clear = matches_clear_source[i].find_elements_by_xpath(
                        "./div[@class=\"matchContainer\"]")
                matches_last = matches_last_source[i].find_elements_by_xpath(
                    "./div[@class=\"matchContainer\"]")

                matches = matches_clear + matches_last
#add for here
                name1 = matches[
                        0].find_elements_by_xpath(
                        "./div[@class=\"matchInfo\"]//td[@class=\"teamLine\"]/a")[
                                0].text
                win1 = len(matches[
                        0].find_elements_by_xpath(
                        "./div[@class=\"matchInfo\"]//td[@class=\"teamLine\"]"+
                        "/div[@class=\"arrowWrapper\"]"))

                name2 = matches[
                        0].find_elements_by_xpath(
                        "./div[@class=\"matchInfo\"]//td[@class=\"teamLine2\"]/a")[
                                0].text

                win2 = len(matches[
                        0].find_elements_by_xpath(
                        "./div[@class=\"matchInfo\"]//td[@class=\"teamLine2\"]"+
                        "/div[@class=\"arrowWrapper\"]"))
                print(name1)
                print(win1)
                print(name2)
                print(win2)
                #print(len(matches_last))

            data_string = data_source.text.encode('utf8')

            if len(data_string) > 0:
                break

            tries += 1
        #print(data_string)
        #print(len(titles_source))
        #print(len(matches_clear_source))
        #print(len(matches_last_source))




######################
#        Main        #
######################

if __name__ == "__main__":
    from sys import argv

    url = input("Enter url to scrap from:\n")
    folder = input("Enter folder to download to:\n")
    driver_path = input("Enter driver path:\n")

    print("Starting...")

    Webscraper(url,folder,phantom_path = driver_path)
