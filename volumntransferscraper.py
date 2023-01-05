'''
problems i met: paging, \\n, split, replace, description to formating, import scrtname and dbf encoding,
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

start = time.time()
print(start)
PATH = "Documents/github/webscraper/chromedriver"
driver = webdriver.Chrome(PATH)
totalpages = 25
data = []
def udddata():
    driver.get(urls) 
    contents = driver.find_elements(By.CLASS_NAME, "col-md-6")
    data = [[content.text] for content in contents]        
    return data

for i in range(1, totalpages+1):
    urls = "https://www.udd.gov.taipei/volumn-transfer/avdwckf?page=" + str(i)
    data.append(udddata())
    i += 1
driver.close()

rawdata = str(data).split(",")
givenparcel=[]
exception=[]
for i in range(len(rawdata)):
    try:         
        givenparcel.append((rawdata[i].split("\\n"))[3])
    except:
        exception.append(rawdata[i].split("\\n"))


splitnumber = str(givenparcel).replace("、", ",").replace("及", ",").replace(" ","").replace("'","").replace("[","").replace("]","").split(",")

step4_cuthead = [] 
for element in splitnumber:
    if "北市" in element: step4_cuthead.append(element.split("北市")[1])
    else: step4_cuthead.append(element)

step5_cuttail = []
for element in step4_cuthead:
    if "地" in element:
        step5_cuttail.append(element.split("地")[0])
    elif "等" in element:
        step5_cuttail.append(element.split("等")[0])
    elif "（" in element:
        step5_cuttail.append(element.split("（")[0])
    elif "(" in element:
        step5_cuttail.append(element.split("(")[0]) 
    else: step5_cuttail.append(element)

u = []
for n in range(len(step5_cuttail)):
    if "段" not in step5_cuttail[n]:
        if "小段" in u[n-1]:
            u.append(str(u[n-1]).split("小段")[0]+"小段"+step5_cuttail[n])
        else:
            u.append(str(u[n-1]).split("段")[0]+"段"+step5_cuttail[n])
    else: u.append(step5_cuttail[n])

v = []
for n in range(len(u)):
    if "同區段" in u[n]: v.append(str(v[n-1]).split("段")[0]+"段"+str(u[n]).split("同區段")[1])
    elif "同小段" in u[n]: v.append(str(v[n-1]).split("段")[0]+"段"+str(u[n]).split("同小段")[1])
    elif "同段" in u[n]:
        if "大同段" not in u[n]: v.append(str(v[n-1]).split("段")[0]+"段"+str(u[n]).split("段")[1])
        else: v.append(u[n])
    elif "同區" in u[n]:
        if "大同區" not in u[n]: v.append(str(v[n-1]).split("區")[0]+"區"+str(u[n]).split("區")[1])
        else: v.append(u[n])
    else: v.append(u[n])

w = [(v[i].index("段")) for i in range(len(v))]
# x = [] # x 可以獲得完整 段小段地號
# for i in range(len(v)):
#     w3 = v[i].index("段")
#     if "新洲美" in v[i]: x.append(v[i][w3-3:])
#     else: x.append(v[i][w3-2:])

y = [] #y僅獲得段小段 為了統計段代碼出現次數
Z = ["金泰", "舊宗", "安康", "民生", "經貿", "向陽", "中洲", "三合", "新洲美", "軟橋"]
for i in range(len(v)):
    w2 = v[i].index("段")
    if any(z in v[i] for z in Z): y.append(v[i][w2-2:w2+1])
    elif "新洲美" in v[i]: y.append(v[i][w2-3:w2+1])
    else: y.append(v[i][w2-2:w2+4])

# 導入段代碼
import csv
import re
d = open("documents/github/Project_volumntransfer/section.csv", "r")
csvr = csv.reader(d, delimiter = ",")
sect = [row[0] for row in csvr]
# sect1 = re.split(' {9}', str(sec[0]))
# sect2 = [(re.split('\s+', str(i))) for i in sec1]
# sect1 + sect2 = sect
sect = [(re.split('\s+', str(i))) for i in (re.split(' {9}', str(sect[0])))]
sectdict = {str(sect[i][2]):sect[i][0] for i in range(len(sect))}
# print(sectdict)

n = []
for i in y:
    if i in sectdict.keys():
        n.append(sectdict.get(i))
    else: continue
from collections import Counter
result = Counter(n)

with open("documents/github/Project_volumntransfer/count.csv", "w") as d:
    csvw = csv.writer(d, delimiter=",")
    csvw.writerow(["section_code", "count"])
    for key in result:
        if result[key] is None:
            result[key] = 0
        csvw.writerow([key, result[key]])


end = time.time()
timepassed = end - start
print("計時：%f 秒鐘" %timepassed)

