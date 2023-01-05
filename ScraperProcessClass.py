
# To install pip modules:
# Ex. /Applications/QGIS-LTR.app/Contents/MacOS/bin/python3 -m pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
from definitions import ROOT_DIR
import os

class ScraperProcessClass:
    data = []
    fulladdress = []
    sectionname = []

    def __init__(self, urlslug, totalpages=25):
        self.totalpages = totalpages
        self.urlslug = urlslug

    def scrape(self):
        PATH = "Documents/github/webscraper/chromedriver"
        driver = webdriver.Chrome(PATH)
        def udddata():
            driver.get(urls) 
            contents = driver.find_elements(By.CLASS_NAME, "col-md-6")
            data = [[content.text] for content in contents]        
            return data

        for i in range(1, self.totalpages+1):
            urls = self.urlslug + str(i)
            self.data.append(udddata())
            i += 1
        driver.close()

### processing steps ###
# step1_rawdata
# step2_givenparcel
# step3_splitnumber
# step4_cutheads
# step5_cuttails
# step6_giveheads
# step7_correctname
# step8_sectionname
###

    def process(self):
        rawdata = str(self.data).split(",")
        givenparcel=[]
        exception=[]
        for i in range(len(rawdata)):
            try:         
                givenparcel.append((rawdata[i].split("\\n"))[3])
            except:
                exception.append(rawdata[i].split("\\n"))

        splitnumber = str(givenparcel).replace("、", ",").replace("及", ",").replace(" ","").replace("'","").replace("[","").replace("]","").split(",")

        cutheads = [] 
        for element in splitnumber:
            if "北市" in element: cutheads.append(element.split("北市")[1])
            else: cutheads.append(element)


        cuttails = []
        for element in cutheads:
            if "地" in element:
                cuttails.append(element.split("地")[0])
            elif "等" in element:
                cuttails.append(element.split("等")[0])
            elif "（" in element:
                cuttails.append(element.split("（")[0])
            elif "(" in element:
                cuttails.append(element.split("(")[0]) 
            else: cuttails.append(element)

        giveheads = []
        for n in range(len(cuttails)):
            if "段" not in cuttails[n]:
                if "小段" in giveheads[n-1]:
                    giveheads.append(str(giveheads[n-1]).split("小段")[0]+"小段"+cuttails[n])
                else:
                    giveheads.append(str(giveheads[n-1]).split("段")[0]+"段"+cuttails[n])
            else: giveheads.append(cuttails[n])

        correctname = []
        for n in range(len(giveheads)):
            if "同區段" in giveheads[n]: correctname.append(str(correctname[n-1]).split("段")[0]+"段"+str(giveheads[n]).split("同區段")[1])
            elif "同小段" in giveheads[n]: correctname.append(str(correctname[n-1]).split("段")[0]+"段"+str(giveheads[n]).split("同小段")[1])
            elif "同段" in giveheads[n]:
                if "大同段" not in giveheads[n]: correctname.append(str(correctname[n-1]).split("段")[0]+"段"+str(giveheads[n]).split("段")[1])
                else: correctname.append(giveheads[n])
            elif "同區" in giveheads[n]:
                if "大同區" not in giveheads[n]: correctname.append(str(correctname[n-1]).split("區")[0]+"區"+str(giveheads[n]).split("區")[1])
                else: correctname.append(giveheads[n])
            else: correctname.append(giveheads[n])

        KeywordIndex = correctname[i].index("段")
        for i in range(len(correctname)):    
            if "新洲美" in correctname[i]: self.fulladdress.append(correctname[i][KeywordIndex-3:])
            else: self.fulladdress.append(correctname[i][KeywordIndex-2:])

        SectionWithoutBranches = ["金泰", "舊宗", "安康", "民生", "經貿", "向陽", "中洲", "三合", "新洲美", "軟橋"]
        for i in range(len(correctname)):
            if any(z in correctname[i] for z in SectionWithoutBranches): self.sectionname.append(correctname[i][KeywordIndex-2:KeywordIndex+1])
            elif "新洲美" in correctname[i]: self.sectionname.append(correctname[i][KeywordIndex-3:KeywordIndex+1])
            else: self.sectionname.append(correctname[i][KeywordIndex-2:KeywordIndex+4])

# Output parcel complete address to CSV file.

        with open(os.path.join(ROOT_DIR, "parcellist.csv"), "w") as parcel_csv_file:
            csvw = csv.writer(parcel_csv_file, delimiter=",")
            csvw.writerow(["no.", "volumn out parcel"])
            for i in range(len(self.fulladdress)):
                csvw.writerow([str(i), self.fulladdress[i]])