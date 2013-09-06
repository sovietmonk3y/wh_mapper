import os
import sys
sys.path.append('/'.join(os.path.abspath(__file__).split('scripts')[0].split('/')[:-2]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wh_mapper.settings")

import re
import urllib

from BeautifulSoup import BeautifulSoup

from wh_mapper.constants import SYSTEM_TYPE_CHOICES, SYSTEM_WSPACE_EFFECT_CHOICES
from wh_mapper.models import System

file = open('system_db_inserts.sql', 'w')

url = 'http://evemaps.dotlan.net/region'

region_list_soup = BeautifulSoup(urllib.urlopen(url))

igb_re_pattern = re.compile('igb')
empire_region_list = [anchor.text for anchor in region_list_soup.find(id='inner').find('table').findAll(name='a', attrs={'class' : igb_re_pattern})]
null_region_list = [anchor.text for anchor in region_list_soup.find(id='inner').findAll('table')[1].findAll(name='a', attrs={'class' : igb_re_pattern})]
wspace_region_list = [anchor.text for anchor in region_list_soup.find(id='inner').findAll('table')[3].findAll(name='a', attrs={'class' : igb_re_pattern})]

SYSTEM_TYPE_MAPPING = {'0.1' : SYSTEM_TYPE_CHOICES[1][0],
                       '0.2' : SYSTEM_TYPE_CHOICES[1][0],
                       '0.3' : SYSTEM_TYPE_CHOICES[1][0],
                       '0.4' : SYSTEM_TYPE_CHOICES[1][0],
                       '0.5' : SYSTEM_TYPE_CHOICES[0][0],
                       '0.6' : SYSTEM_TYPE_CHOICES[0][0],
                       '0.7' : SYSTEM_TYPE_CHOICES[0][0],
                       '0.8' : SYSTEM_TYPE_CHOICES[0][0],
                       '0.9' : SYSTEM_TYPE_CHOICES[0][0],
                       '1.0' : SYSTEM_TYPE_CHOICES[0][0]}

for empire_region in empire_region_list:
    region_soup = BeautifulSoup(urllib.urlopen(url + '/' + empire_region))
    region_tr_list = region_soup.find(id='inner').find('table').findAll('tr')[1:]
    for system_tr in region_tr_list:
        system_td_list = system_tr.findAll('td')
        print "Entering " + system_td_list[1].findAll('a')[-1].text +\
              " with a sec status of " + system_td_list[2].findChild('span').text +\
              " as a " +\
              SYSTEM_TYPE_MAPPING[system_td_list[2].findChild('span').text] +\
              " system in the region " + empire_region
        file.write("INSERT INTO wh_mapper_system VALUES('" +
                   system_td_list[1].findAll('a')[-1].text +
                   "', '" +
                   SYSTEM_TYPE_MAPPING[system_td_list[2].findChild('span').text] +
                   "', '" + empire_region + "', '');")

for null_region in null_region_list:
    region_soup = BeautifulSoup(urllib.urlopen(url + '/' + null_region))
    region_tr_list = region_soup.findAll(name='a', attrs={'name' : 'sys'})[-1].parent.findNextSibling('table').findAll('tr')[1:]
    for system_tr in region_tr_list:
        system_td_list = system_tr.findAll('td')
        print "Entering " + system_td_list[1].findAll('a')[-1].text +\
              " with a sec status of " + system_td_list[2].findChild('span').text +\
              " as a " + SYSTEM_TYPE_CHOICES[2][0] + " system in the region " +\
              null_region
        file.write("INSERT INTO wh_mapper_system VALUES('" +
                   system_td_list[1].findAll('a')[-1].text +
                   "', '" + SYSTEM_TYPE_CHOICES[2][0] + "', '" + null_region + "', '');")

SYSTEM_TYPE_MAPPING = {'1' : SYSTEM_TYPE_CHOICES[3][0],
                       '2' : SYSTEM_TYPE_CHOICES[4][0],
                       '3' : SYSTEM_TYPE_CHOICES[5][0],
                       '4' : SYSTEM_TYPE_CHOICES[6][0],
                       '5' : SYSTEM_TYPE_CHOICES[7][0],
                       '6' : SYSTEM_TYPE_CHOICES[8][0]}

WSPACE_EFFECT_MAPPING = dict([(effect[1], effect[0]) for effect in SYSTEM_WSPACE_EFFECT_CHOICES])
WSPACE_EFFECT_MAPPING['Wolf-Rayet Star'] = WSPACE_EFFECT_MAPPING['Wolf-Rayet']

for wspace_region in wspace_region_list:
    region_soup = BeautifulSoup(urllib.urlopen(url + '/' + wspace_region))
    region_tr_list = region_soup.find(id='inner').find('table').findAll('tr')[1:]
    for system_tr in region_tr_list:
        system_td_list = system_tr.findAll('td')
        output =  "Entering " + system_td_list[1].findAll('a')[-1].text +\
                  " with a class of " + system_td_list[2].text
        if system_td_list[3].text:
            output += " and with the wspace effect " + system_td_list[3].text
        print output
        output = "INSERT INTO wh_mapper_system VALUES('" +\
                 system_td_list[1].findAll('a')[-1].text + "', '" +\
                 SYSTEM_TYPE_MAPPING[system_td_list[2].text] + "', '', '"
        if system_td_list[3].text:
            output += WSPACE_EFFECT_MAPPING[system_td_list[3].text]
        output += "');"
        file.write(output)

file.close()
