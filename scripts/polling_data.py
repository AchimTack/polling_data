# -*- coding: utf-8 -*-
__author__ = 'achimtack'

from urllib2 import urlopen
from bs4 import BeautifulSoup
import time
import csv
import unicodedata

def clean_string(instring):
    outstring = instring.replace('\n',' ').replace('\r',' ')
    return outstring

def clean_string_safe(instring):
    outstring = instring.replace('Ü','ue').replace('Ä','ae').replace('Ö','oe').replace('ü','ue').replace('ä','ae').replace('ö','oe')
    outstring = outstring.replace('.','').replace('-','').replace('*','').strip().replace(':','').replace(',','_').replace(' ','').replace('(','').replace(')','').replace('?','').lower()
    return outstring

file = r"..\data\polls.csv"
ofile  = open(file, "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, lineterminator = '\n')
writer.writerow(["state", "year", "month", "date", "pollster", "pollster_safe", "purchaser", "purchaser_safe"])
ofile.close()

laenderList = ['baden-wuerttemberg',
               'bayern',
               'berlin',
               'brandenburg',
               'bremen',
               'hamburg',
               'hessen',
               'mecklenburg-vorpommern',
               'niedersachsen',
               'nrw',
               'rheinland-pfalz',
               'saarland',
               'sachsen',
               'sachsen-anhalt',
               'schleswig-holstein',
               'thueringen'
                ]

for land in laenderList:
    url = 'http://www.wahlrecht.de/umfragen/landtage/'+land+'.htm'
    print url

    ofile  = open(file, "a")
    writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')

    html = urlopen(url)
    soup = BeautifulSoup(html)
    data_rows = soup.findAll('tr')
    poll_data = [[td.getText() for td in data_rows[i].findAll('td')] for i in range(len(data_rows))]

    for poll in poll_data:
        if len(poll) >10:
            try:
                institut = clean_string(poll[0].encode('utf-8'))
                #I know...
                institut_safe = institut.replace('Forsch’gr.Wahlen', 'forschungsgruppewahlen')
                institut_safe = institut_safe.replace('quelle', '').replace('Quelle', '')
                institut_safe = clean_string_safe(institut_safe)

                auftraggeber = clean_string(poll[1].encode('utf-8'))
                auftraggeber_safe = auftraggeber.replace('quelle', '').replace('Quelle', '')
                auftraggeber_safe = clean_string_safe(auftraggeber_safe)
                date = clean_string(poll[3])
                year = str(int(date[-4:]))
                month = str(int(date[3:5]))

                if institut_safe[:8] != "landtags":
                    values = (land, year, month, date, institut, institut_safe, auftraggeber, auftraggeber_safe)
                    print values
                    writer.writerow(values)

            except Exception as r:
                print r

    ofile.close()
    time.sleep(1)
