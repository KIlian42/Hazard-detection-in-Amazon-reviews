import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver

if __name__ == '__main__':
    # predfined list
    list = ['ASPHYXIATION', 'BURNS', 'CHEMICAL', 'CHOKING', 'CUTS', 'DAMAGE TO HEARING', 'DAMAGE TO SIGHT', 'DROWNING', 'ELECTRIC SHOCK', 'ELECTROMAGNETIC DISTURBANCE', 'ENERGY CONSUMPTION', 'ENTRAPMENT', 'ENVIRONMENT', 'FIRE', 'HEALTH RISK', 'INJURIES', 'MEASUREMENT INCORRECT', 'MICROBIOLOGICAL', 'SECURITY', 'STRANGULATION', 'SUFFOCATION']
    bag_of_synonyms = []
    '''
    try:
        os.mkdir('hazards/')
    except OSError:
        print('Path already exists')
    # scrape synonyms from synonyms.com
    driver = webdriver.Safari()
    for element in list:
        splitted = element.split()
        url = 'https://www.synonyms.com/synonym/'
        for i in splitted:
            url += str(i.lower()) + '+'
        url = url[:-1]
        data = driver.get(url)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        file_name = element.lower().replace(' ', '_')
        completeName = os.path.join('hazards/', file_name+'.html')
        file = open(completeName, 'w')
        file.write(str(soup))
        file.close()
    '''
    for element in list:
        file_name = element.lower().replace(' ', '_')
        completeName = os.path.join('hazards/', file_name+'.html')
        file = open(completeName)
        soup = BeautifulSoup(file, features='html.parser')
        box = soup.find('p', {'class': 'syns'})
        synonyms = [str(element.lower())]
        if box != None:
            for synonym in box.find_all(href=True):
                synonyms.append(synonym.string)
        bag_of_synonyms.append(synonyms)
        file.close()
    for i in bag_of_synonyms:
        print(i)


