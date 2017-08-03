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

def GrandSlamScraper(folder,  phantom_path = "",year="",tourn="",mode=""):


    tourn_names = ["AUS","FRE","WIM","USO"]
    tourn_codes = ["154","172","188","189"]
    tourn_name = tourn_names[tourn]
    tourn_code = tourn_codes[tourn]

    mode_names = ["MEN_SING","WOM_SING","MEN_DOUB","WOM_DOUB","TEAM_CUP","MIX_DOUB"]
    mode_name = mode_names[mode]
    mode += 1

    url="http://www.espn.com/tennis/scoreboard/_/year/"+str(year)+"/tournamentId/"+tourn_code+"/matchType/"+str(mode)


    rows = []
    row = []
    append_to_csv = False
    current_os = platform

    lines = list()

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

        browser.get(url)
        while tries <= 20:

            #Getting Data
            data_source = browser.find_elements_by_xpath(
                    "//div[@id=\"content\"]/div[@class=\"span-4\"]")
            if len(data_source)==0:
                return []

            #Getting Matches Titles
            titles_source = data_source[0].find_elements_by_xpath(
                    "//div[@class=\"matchTitle\"]")

            #Getting Matches Columns
            matches_clear_source = data_source[0].find_elements_by_xpath(
                    "//div[@class=\"span-4\"]/div[@class=\"span-2 clear\"]")

            matches_last_source = data_source[0].find_elements_by_xpath(
                    "//div[@class=\"span-4\"]/div[@class=\"span-2 last\"]")

            for i in range(len(titles_source)):
                title = titles_source[i].text[2:].split(":")[0].upper().replace(" ","_")

                if mode < 3:
                    match_container = "matchContainer"
                else:
                    match_container = "matchContainerDoubles"

                matches_clear = matches_clear_source[i].find_elements_by_xpath(
                        "./div[@class=\""+match_container+"\"]")
                matches_last = matches_last_source[i].find_elements_by_xpath(
                    "./div[@class=\""+match_container+"\"]")

                matches = matches_clear + matches_last
#add for here
                for j in range(len(matches)):
                #for j in range(1):
                        if len(matches[j].find_elements_by_xpath("./div[@class=\"matchInfo\"]//div[@class=\"arrowWrapper\"]"))!=1:
                            continue
                        name1 = matches[
                                j].find_elements_by_xpath(
                                "./div[@class=\"matchInfo\"]//td[@class=\"teamLine\"]"+
                                "/a")[0].text
                        name12 = "NA"
                        win1 = len(matches[
                                j].find_elements_by_xpath(
                                "./div[@class=\"matchInfo\"]//td[@class=\"teamLine\"]"+
                                "/div[@class=\"arrowWrapper\"]"))==1
                        points1 = matches[
                                j].find_elements_by_xpath(
                                "./div[@class=\"linescore\"]//td[@class=\"lsLine2\"]")
                        for k in range(len(points1)):
                            points1[k] = points1[k].text
                        points1 = points1 + ["NA"]*(5-len(points1))

                        if mode >= 3:
                            name12 =  matches[
                                        j].find_elements_by_xpath(
                                        "./div[@class=\"matchInfo\"]/table/tbody/"+
                                        "tr[3]/td/a")[0].text
                            win1 = len(matches[
                                    j].find_elements_by_xpath(
                                    "./div[@class=\"matchInfo\"]/table/tbody/tr[3]/td"+
                                    "/div[@class=\"arrowWrapper\"]"))==1

                        line1 = [str(year)] + [tourn_name] + [mode_name] + [title] + [name1] + [name12] + [str(win1)] + points1
                        line1 = [",".join(line1)]

                        name2 = matches[
                                j].find_elements_by_xpath(
                                "./div[@class=\"matchInfo\"]//td[@class=\"teamLine2\"]"
                                +"/a")[0].text
                        name22 = "NA"
                        win2 = len(matches[
                                j].find_elements_by_xpath(
                                "./div[@class=\"matchInfo\"]//td[@class=\"teamLine2\"]"+
                                "/div[@class=\"arrowWrapper\"]"))==1
                        points2 = matches[
                                j].find_elements_by_xpath(
                                "./div[@class=\"linescore\"]//td[@class=\"lsLine3\"]")
                        for k in range(len(points2)):
                            points2[k] = points2[k].text
                        points2 = points2 + ["NA"]*(5-len(points2))
                        if mode >= 3:
                            name22 =  matches[
                                        j].find_elements_by_xpath(
                                        "./div[@class=\"matchInfo\"]/table/tbody/"+
                                        "tr[5]/td/a")[0].text
                            win2 = len(matches[
                                    j].find_elements_by_xpath(
                                    "./div[@class=\"matchInfo\"]/table/tbody/tr[5]/td"+
                                    "/div[@class=\"arrowWrapper\"]"))==1


                        line2 = [str(year)] + [tourn_name] + [mode_name] + [title] + [name2] + [name22] + [str(win2)] + points2
                        line2 = [",".join(line2)]

                        lines = lines + line1 + line2

                        #print(j)
                        print(line1)
                        print(line2)
                #print(type(list(name1)))
                #print(type(list(str(win1))))
                #print(type(points1))
                #print(len(matches_last))

            data_string = data_source[0].text.encode('utf8')

            if len(data_string) > 0:
                break

            tries += 1
        #print(data_string)
        #print(len(titles_source))
        #print(len(matches_clear_source))
        #print(len(matches_last_source))

    return lines



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
