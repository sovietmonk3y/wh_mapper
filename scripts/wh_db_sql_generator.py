import os
import sys
sys.path.append('/'.join(os.path.abspath(__file__).split('scripts')[0].split('/')[:-2]))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wh_mapper.settings")

import urllib

from BeautifulSoup import BeautifulSoup

from wh_mapper.constants import SYSTEM_TYPE_CHOICES
from wh_mapper.models import Wormhole

url = 'http://evemaps.dotlan.net/wormholes'

wormholes_soup = BeautifulSoup(urllib.urlopen(url))

wormhole_tables = wormholes_soup.find(id='inner').findAll('table')

WORMHOLE_CLASS_MAPPING = {1 : SYSTEM_TYPE_CHOICES[3][0],
                          2 : SYSTEM_TYPE_CHOICES[4][0],
                          3 : SYSTEM_TYPE_CHOICES[5][0],
                          4 : SYSTEM_TYPE_CHOICES[6][0],
                          5 : SYSTEM_TYPE_CHOICES[7][0],
                          6 : SYSTEM_TYPE_CHOICES[8][0],
                          7 : SYSTEM_TYPE_CHOICES[0][0],
                          8 : SYSTEM_TYPE_CHOICES[1][0],
                          9 : SYSTEM_TYPE_CHOICES[2][0]}

class_count = 1
wormholes = {}
for table in wormhole_tables:
    wormhole_tr_list = table.findAll('tr')[1:]

    for wormhole_tr in wormhole_tr_list:
        wormhole_td_list = wormhole_tr.findAll('td')
        wormhole_dict = {
            'type' : WORMHOLE_CLASS_MAPPING[class_count],
            'life' : int(wormhole_td_list[1].text.split(' ')[0]),
            'total_mass' : int(wormhole_td_list[2].text.split(' ')[0].replace('.', '')),
            'jump_mass' : int(wormhole_td_list[4].text.split(' ')[0].replace('.', ''))}
        if wormhole_td_list[3].text != '-':
            wormhole_dict['mass_regen'] = int(wormhole_td_list[3].text.split(' ')[0]
                                                                 .replace('.', ''))
        else:
            wormhole_dict['mass_regen'] = None
        wormholes[wormhole_td_list[0].findChild('b').text.split(' ')[1]] = wormhole_dict

    class_count += 1

url = 'http://wiki.eveonline.com/en/wiki/Wormholes'

wormholes_soup = BeautifulSoup(urllib.urlopen(url))

wormhole_tr_list = wormholes_soup.findAll('tr', attrs={'style' : "background:#4D4D57"})

for wormhole_tr in wormhole_tr_list:
    wormhole_td_list = wormhole_tr.findAll('td')
    wormhole_static = wormhole_td_list[1].findChild('a') or wormhole_td_list[1]
    wormholes[wormhole_td_list[0].findChild('a').text]['static'] = int(
        wormhole_static.text.strip() == 'static')

file = open('wh_db_inserts.sql', 'w')

for sig in wormholes:
    sql_query = ("INSERT INTO wh_mapper_wormhole (sig, type, life, " +
                 "total_mass, mass_regen, jump_mass, static) VALUES ('" +
                 sig + "', '" + wormholes[sig]['type'] + "', " +
                 str(wormholes[sig]['life']) + ", " +
                 str(wormholes[sig]['total_mass']) + ", " +
                 str(wormholes[sig]['mass_regen'] or 0) + ", " +
                 str(wormholes[sig]['jump_mass']) + ", " +
                 str(wormholes[sig]['static']) + ");\n")
    file.write(sql_query)

file.close()
