import requests as req
import json
import os
import re
import xlwt
from selenium import webdriver
from selenium.webdriver.common.by import By
import bs4
import time


'''
实现参考：https://www.cnblogs.com/kangz/p/10011348.html
第一步，下载出所有车型的网页。
'''
def get_html():
    '''
    解析汽车之家所有车型数据保存到D盘
    '''
    li = [chr(i) for i in range(ord("A"),ord("Z")+1)]
    firstSite="https://www.autohome.com.cn/grade/carhtml/"
    firstSiteSurfixe=".html"
    secondSite = "https://car.autohome.com.cn/config/series/"
    secondSiteSurfixe = ".html"

    for a in li:
        if a is not None:
            requestUrl = firstSite+a+firstSiteSurfixe
            print(requestUrl)
            #开始获取每个品牌的车型
            resp = req.get(requestUrl)
            # print(str(resp.content,"gbk"))
            bs = bs4.BeautifulSoup(resp.content, "html.parser")
            # bs = bs4.BeautifulSoup(str(resp.content,"utf-8"),"html.parser")
            bss = bs.find_all("li")
            con = 0
            for b in bss:
                d = b.h4
                if d is not None:
                    her = str(d.a.attrs['href'])
                    her = her.split("#")[0]
                    her = her[her.index(".cn")+3:].replace("/", '')

                    # 检查her是否为有效文件名
                    if her:
                        secSite = secondSite + her + secondSiteSurfixe
                        print("secSite = " + secSite)

                        resp = req.get(secSite)
                        text = str(resp.content, encoding="utf-8")

                        # 确保目录存在
                        directory = "D:\\sensetime2\\scraper\\python\\autoparamater\\html"
                        if not os.path.exists(directory):
                            os.makedirs(directory)

                        # 创建文件并写入内容
                        with open(os.path.join(directory, str(her)), "a", encoding="utf-8") as fil:
                            fil.write(text)

                    con = (con + 1)
                    # if con > 5:
                    #     break
            else:
                print(con)

'''
将原始 HTML 文件中的 JavaScript 函数提取出来，然后嵌入到新的 HTML 内容中，并将生成的新 HTML 文件保存到指定目录
'''
def get_newhtml():
    print("Start...")
    rootPath = "D:\\sensetime2\\scraper\\python\\autoparamater\\html\\"
    files = os.listdir(rootPath)
    for file in files:
        print("fileName=="+file.title())
        text = ""
        for fi in open(rootPath+file,'r',encoding="utf-8"):
            text = text+fi
        else:
            print("fileName=="+file.title())
        #解析数据的json
        alljs = ("var rules = '2';"
                 "var document = {};"
                 "function getRules(){return rules}"
                 "document.createElement = function() {"
                 "      return {"
                 "              sheet: {"
                 "                      insertRule: function(rule, i) {"
                 "                              if (rules.length == 0) {"
                 "                                      rules = rule;"
                 "                              } else {"
                 "                                      rules = rules + '#' + rule;"
                 "                              }"
                 "                      }"
                 "              }"
                 "      }"
                 "};"
                 "document.querySelectorAll = function() {"
                 "      return {};"
                 "};"
                 "document.head = {};"
                 "document.head.appendChild = function() {};"

                 "var window = {};"
                 "window.decodeURIComponent = decodeURIComponent;")
        try:
            js = re.findall('(\(function\([a-zA-Z]{2}.*?_\).*?\(document\);)', text)
            for item in js:
                alljs = alljs + item
        except Exception as e:
            print('makejs function exception')


        newHtml = "<html><meta http-equiv='Content-Type' content='text/html; charset=utf-8' /><head></head><body>    <script type='text/javascript'>"
        alljs = newHtml + alljs+" document.write(rules)</script></body></html>"
        directory = "D:\\sensetime2\\scraper\\python\\autoparamater\\newhtml"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, file + ".html")

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(alljs)
        f.close()



'''
.解析出每个车型的数据json，比如var config  ,var option , var bag等
'''
def get_json():
    print("Start...")
    rootPath = "D:\\sensetime2\\scraper\\python\\autoparamater\\html\\"
    files = os.listdir(rootPath)
    for file in files:
        print("fileName=="+file.title())
        text = ""
        for fi in open(rootPath+file,'r',encoding="utf-8"):
            text = text+fi
        else:
            print("fileName=="+file.title())
        #解析数据的json
        jsonData = ""
        config = re.search('var config = (.*?){1,};',text)
        if config!= None:
            # print(config.group(0))
            jsonData = jsonData+ config.group(0)
        option = re.search('var option = (.*?)};',text)
        if option != None:
            # print(option.group(0))
            jsonData = jsonData+ option.group(0)
        bag = re.search('var bag = (.*?);',text)
        if bag != None:
            # print(bag.group(0))
            jsonData = jsonData+ bag.group(0)
        # print(jsonData)
        directory = "D:\\sensetime2\\scraper\\python\\autoparamater\\json"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, file + ".html")

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(jsonData)
        f.close()

'''
生成样式文件，保存到本地。这一步很重要，网站经过混淆处理，部分显示的文字是通过css样式拼出来的
chromedriver获取参考：https://blog.csdn.net/sdzhr/article/details/82660860
使用参考：https://www.cnblogs.com/hellosecretgarden/p/9206648.html
'''
class Crack():
    def __init__(self,keyword,username,passod):
        self.url = 'https://www.baidu.com'
        self.browser = webdriver.Chrome()
        time.sleep(1)

def get_content():
    lists = os.listdir("D:/sensetime2/scraper/python/autoparamater/newHtml/")
    crack = Crack('测试公司','17610177519','17610177519')
    for fil in lists:
        file = os.path.exists("D:\\sensetime2\\scraper\\python\\autoparamater\\content\\"+fil)
        time.sleep(1)
        if file :
            print('文件已经解析。。。'+str(file))
            continue
        print(fil)
        crack.browser.get("file:///D:/sensetime2/scraper/python/autoparamater/newHtml/"+fil+"")
        text = crack.browser.find_element(By.TAG_NAME,'body')
        print(text.text)
        file_path = "D:\\sensetime2\\scraper\\python\\autoparamater\\content\\" + fil

        # 确保目录存在
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # 打开文件并写入内容
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(text.text)
    else:
        f.close()
        crack.browser.close()


'''
读取样式文件，匹配数据文件，生成正常数据文件
'''
def search_json():
    rootPath = "D:\\sensetime2\\scraper\\python\\autoparamater\\json\\"
    listdir = os.listdir(rootPath)
    for json_s in listdir:
        # print(json_s.title())
        jso = ""
        #读取json数据文件
        for fi in open(rootPath+json_s,'r',encoding="utf-8"):
            jso = jso+fi
        content = ""
        #读取样式文件
        spansPath = "D:\\sensetime2\\scraper\\python\\autoparamater\\content\\"+json_s.title().split(".")[0]+".html"
        # print(spansPath)
        for spans in  open(spansPath,"r",encoding="utf-8"):
            content = content+ spans
        # print(content)
        #获取所有span对象
        jsos = re.findall("<span(.*?)></span>",jso)
        num = 0
        for js in jsos:
            # print("匹配到的span=>>"+js)
            num = num +1
            #获取class属性值
            sea = re.search("'(.*?)'",js)
            # print("匹配到的class==>"+sea.group(1))
            spanContent = str(sea.group(1))+"::before { content:(.*?)}"
            #匹配样式值
            spanContentRe = re.search(spanContent,content)
            if spanContentRe != None:
                if sea.group(1) != None:
                    # print("匹配到的样式值="+spanContentRe.group(1))
                    jso = jso.replace(str("<span class='"+sea.group(1)+"'></span>"),re.search("\"(.*?)\"",spanContentRe.group(1)).group(1))
        # print(jso)
        file_path = "D:\\sensetime2\\scraper\\python\\autoparamater\\newJson\\" + json_s.title()

        # 确保目录存在
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # 打开文件并写入内容
        with open(file_path, "a", encoding="utf-8") as fi:
            fi.write(jso)
        fi.close()

'''
指定需要的字段，从数据文件中提取出来保存到excel中
'''
def excel_generation():
    rootPath = "D:\\sensetime2\\scraper\\python\\autoparamater\\newJson\\"
    workbook = xlwt.Workbook(encoding = 'ascii')#创建一个文件
    worksheet = workbook.add_sheet('汽车之家')#创建一个表
    files = os.listdir(rootPath)
    startRow = 0
    isFlag = True #默认记录表头
    for file in files:
        list = []
        carItem = {}
        print("fileName=="+file.title())
        text = ""
        for fi in open(rootPath+file,'r',encoding="utf-8"):
            text = text+fi
        # else:
            # print("文件内容=="+text)
        #解析基本参数配置参数，颜色三种参数，其他参数
        config = "var config = (.*?);"
        option = "var option = (.*?);var"
        bag = "var bag = (.*?);"

        configRe = re.findall(config,text)
        optionRe = re.findall(option,text)
        bagRe = re.findall(bag,text)
        for a in configRe:
            config = a
        print("++++++++++++++++++++++\n")
        for b in optionRe:
            option = b
            print("---------------------\n")
        for c in bagRe:
            bag = c
        # print(config)
        # print(option)
        # print(bag)

        # print(bag)
        try:
            config = json.loads(config)
            option = json.loads(option)
            bag = json.loads(bag)
            # print(config)
            # print(option)
            # print(bag)
            path = "D:\\sensetime2\\scraper\\python\\autoparamater\\autoHome.xls"

            configItem = config['result']['paramtypeitems'][0]['paramitems']
            optionItem = option['result']['configtypeitems'][0]['configitems']
        except Exception as e:
            directory = "D:\\sensetime2\\scraper\\python\\autoparamater\\异常数据"

            # 如果目录不存在，创建目录
            if not os.path.exists(directory):
                os.makedirs(directory)

            # 打开文件并写入数据
            with open(os.path.join(directory, "exception.txt"), "a", encoding="utf-8") as f:
                f.write(file.title() + "\n")
            continue

        #解析基本参数
        for car in configItem:
            carItem[car['name']]=[]
            for ca in car['valueitems']:
                carItem[car['name']].append(ca['value'])
        # print(carItem)
        #解析配置参数
        for car in optionItem:
            carItem[car['name']]=[]
            for ca in car['valueitems']:
                carItem[car['name']].append(ca['value'])

        if isFlag:
            co1s = 0

            for co in carItem:
                co1s = co1s +1
                worksheet.write(startRow,co1s,co)
            else:
                startRow = startRow+1
                isFlag = False

        #计算起止行号
        if '车型名称' in carItem:
            endRowNum = startRow + len(carItem['车型名称'])  # 车辆款式记录数
        else:
            endRowNum = startRow  # 或者使用其他默认值
        for row in range(startRow,endRowNum):
            print(row)
            colNum = 0
            for col in carItem:

                colNum = colNum +1
                print(str(carItem[col][row-startRow]),end='|')
                worksheet.write(row,colNum,str(carItem[col][row-startRow]))

        else:
            startRow  = endRowNum
    workbook.save('d:\\sensetime2\\scraper\\python\\autoparamater\\Mybook.xls')

if __name__ == "__main__":
    get_html()
    get_newhtml()
    get_json()
    get_content()
    search_json()
    excel_generation()