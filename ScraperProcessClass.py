# NB: Install webdriver with brew --- "brew install chromedriver"
from selenium import webdriver
from selenium.webdriver.common.by import By

class ScraperProcessClass:
    data = []
    v = []
    y = []
    w = []
    
    def __init__(self, urlslug, totalpages=25):
        self.totalpages = totalpages
        self.urlslug = urlslug

    def scrape(self): 
        driver = webdriver.Chrome()
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

    def process(self):
        p = str(self.data).split(",")
        q=[]
        exception=[]
        for i in range(len(p)):
            try:         
                q.append((p[i].split("\\n"))[3])
            except:
                exception.append(p[i].split("\\n"))

        r = str(q).replace("、", ",").replace("及", ",").replace(" ","").replace("'","").replace("[","").replace("]","")
        s = r.split(",")
        s1 = [] 
        for element in s:
            if "北市" in element: s1.append(element.split("北市")[1])
            else: s1.append(element)

        t = []
        for element in s1:
            if "地" in element:
                t.append(element.split("地")[0])
            elif "等" in element:
                t.append(element.split("等")[0])
            elif "（" in element:
                t.append(element.split("（")[0])
            elif "(" in element:
                t.append(element.split("(")[0]) 
            else: t.append(element)

        u = []
        for n in range(len(t)):
            if "段" not in t[n]:
                if "小段" in u[n-1]:
                    u.append(str(u[n-1]).split("小段")[0]+"小段"+t[n])
                else:
                    u.append(str(u[n-1]).split("段")[0]+"段"+t[n])
            else: u.append(t[n])

        # TODO: rewrite code to be easier to read and maintain = refactor
        self.v = []
        for n in range(len(u)):
            if "同區段" in u[n]: self.v.append(str(self.v[n-1]).split("段")[0]+"段"+str(u[n]).split("同區段")[1])
            elif "同小段" in u[n]: self.v.append(str(self.v[n-1]).split("段")[0]+"段"+str(u[n]).split("同小段")[1])
            elif "同段" in u[n]:
                if "大同段" not in u[n]: self.v.append(str(self.v[n-1]).split("段")[0]+"段"+str(u[n]).split("段")[1])
                else: self.v.append(u[n])
            elif "同區" in u[n]:
                if "大同區" not in u[n]: self.v.append(str(self.v[n-1]).split("區")[0]+"區"+str(u[n]).split("區")[1])
                else: self.v.append(u[n])
            else: self.v.append(u[n])

        self.w = [(self.v[i].index("段")) for i in range(len(self.v))]
        # x = [] # x 可以獲得完整 段小段地號
        # for i in range(len(v)):
        #     w3 = v[i].index("段")
        #     if "新洲美" in v[i]: x.append(v[i][w3-3:])
        #     else: x.append(v[i][w3-2:])

        self.y = [] #y僅獲得段小段 為了統計段代碼出現次數
        Z = ["金泰", "舊宗", "安康", "民生", "經貿", "向陽", "中洲", "三合", "新洲美", "軟橋"]
        for i in range(len(self.v)):
            w2 = self.v[i].index("段")
            if any(z in self.v[i] for z in Z): self.y.append(self.v[i][w2-2:w2+1])
            elif "新洲美" in self.v[i]: self.y.append(self.v[i][w2-3:w2+1])
            else: self.y.append(self.v[i][w2-2:w2+4])
