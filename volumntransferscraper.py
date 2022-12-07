# TODO: Rename to TallySectionCounts.py
'''
problems i met: paging, \\n, split, replace, description to formating, import scrtname and dbf encoding,
'''

from definitions import ROOT_DIR
import os
import csv
from ScraperProcessClass import * 
import time
import re
from collections import Counter

# import shapefile
start = time.time()
print(start)

urlslug = "https://www.udd.gov.taipei/volumn-transfer/avdwckf?page="

#initialize Sections CSV Reader
sections_csv_file = open(os.path.join(ROOT_DIR, 'section.csv'), "r")
csvr = csv.reader(sections_csv_file, delimiter=",")


#######################################################
# Scrape URLS and process results
#######################################################
scraper = ScraperProcessClass(urlslug, 25)
scraper.scrape()
scraper.process()


#######################################################
# Read section info from CSV and read into section dictonary
#######################################################
sect = [row[0] for row in csvr]
# sect1 = re.split(' {9}', str(sec[0]))
# sect2 = [(re.split('\s+', str(i))) for i in sec1]
# sect1 + sect2 = sect
sect = [(re.split('\s+', str(i))) for i in (re.split(' {9}', str(sect[0])))]
sectdict = {str(sect[i][2]):sect[i][0] for i in range(len(sect))}
# print(sectdict)

# WHATS HAPPENING HERE?
n = []
for i in scraper.y:
    if i in sectdict.keys():
        n.append(sectdict.get(i))
    else: continue
print(Counter(n))

#######################################################
# Output section #s and section counts to CSV files.
#######################################################

# Initialize CSV debug info Writer
results_csv_file = open(os.path.join(ROOT_DIR, 'results.csv'), "w")
results_csvw = csv.writer(results_csv_file, delimiter=",")
results_csvw.writerow(["Address", "Road", "Section"])

# For reference, output addresses, streets, and city section #s and section counts to a CSV file.
for i in range(len(scraper.v)):
    print(scraper.v[i], "#", scraper.y[i], "##", scraper.w[i])
    results_csvw.writerow([scraper.v[i], scraper.y[i], scraper.w[i]])

#initialize CSV Section Counts Writer
sectioncounts_csv_file = open(os.path.join(ROOT_DIR, 'section_counts.csv'), "w")
sectioncounts_csvw = csv.writer(sectioncounts_csv_file, delimiter=",")
sectioncounts_csvw.writerow(["Section", "Count"])

# Tally record counts by section
sectioncounts_dict = Counter(n)
for key in sectioncounts_dict:
    value = sectioncounts_dict[key]
    if sectioncounts_dict[key] is None:
        sectioncounts_dict[key] = 0
    sectioncounts_csvw.writerow([key, sectioncounts_dict[key]])


#######################################################
# Output time taken
#######################################################
end = time.time()
timepassed = end - start
print("計時：%f 秒鐘" %timepassed)


