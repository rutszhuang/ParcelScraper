
import csv
import re
import os
from definitions import ROOT_DIR
from ScraperProcessClass import *
from collections import Counter





class SectionStatistics:
    validsection = []
    statistics_dict = []
    def __init__(self):
        None   
        
    def statistics(self):
        
        # Read section info from CSV file.

        with open(os.path.join(ROOT_DIR, "section.csv"), "r") as sectioncode_csv_file:
            sectioncode_csvr = csv.reader(sectioncode_csv_file, delimiter = ",")
            sect = [row[0] for row in sectioncode_csvr]
            # sect1 = re.split(' {9}', str(sec[0]))
            # sect2 = [(re.split('\s+', str(i))) for i in sec1]
            # sect1 + sect2 = sect
            sect = [(re.split('\s+', str(i))) for i in (re.split(' {9}', str(sect[0])))]
            sectioncode_dict = {str(sect[i][2]):sect[i][0] for i in range(len(sect))}
       
        for i in ScraperProcessClass.sectionname:
            if i in sectioncode_dict.keys():
                self.validsection.append(sectioncode_dict.get(i))     
            else: continue
        self.statistics_dict = Counter(self.validsection)

        '''
        Output scraper statistics to CSV file.
        '''
        with open(os.path.join(ROOT_DIR, "statistics.csv"), "w") as statistic_csv_file:
            statistics_csvw = csv.writer(statistic_csv_file, delimiter=",")
            statistics_csvw.writerow(["section_code", "count"])
            for key in self.statistics_dict:
                if self.statistics_dict[key] is None:
                    self.statistics_dict[key] = 0
                statistics_csvw.writerow([key, self.statistics_dict[key]])
