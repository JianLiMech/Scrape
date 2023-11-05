from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
import csv

# 创建一个Chrome浏览器实例
driver = webdriver.Chrome()

# 打开登录页面
driver.get('http://savvcenter.sensetime.com/#/login?redirect=%2Fdashboard')  # 替换成目标登录页面的URL

time.sleep(2)

# 查找用户名和密码输入框并输入登录信息
username_field = driver.find_element(By.NAME, "username")  # 替换成实际的用户名字段名
password_field = driver.find_element(By.NAME, "password")  # 替换成实际的密码字段名

username = 'lijian2'  # 替换成你的用户名
password = 'LiJian1995,'  # 替换成你的密码

username_field.send_keys(username)
password_field.send_keys(password)

# 提交表单来登录
password_field.send_keys(Keys.RETURN) 

time.sleep(5) # 需要等待页面加载完成

# 在登录后，你可以继续浏览和爬取受限页面的内容
html = driver.page_source
soup = BeautifulSoup(html,"html.parser")

with open('testbetter.txt', 'w', encoding='utf-8') as file:
    count = 1
    # 排名
    rows = soup.findAll("tr", attrs={"class": "el-table__row"})
    for row in rows:
        infos = row.findAll("div", attrs={"class": "cell"})
        file.write(f"\n Rank: ")
        for info in infos:
            file.write(info.string)
time.sleep(10)

# 创建一个CSV文件并写入数据
with open('testbetter.csv', 'w', encoding='utf-8', newline='') as file:  # 使用newline=''以避免写入空行
    writer = csv.writer(file)
    
    # 写入标题行
    writer.writerow(["Rank", "Name", "ID", "Number of tests"])  # 替换为实际的列标题
    
    count = 1
    # 排名
    rows = soup.findAll("tr", attrs={"class": "el-table__row"})
    for row in rows:
        infos = row.findAll("div", attrs={"class": "cell"})
        row_data = []  # 第一个列是排名
        for info in infos:
            row_data.append(info.string)
        writer.writerow(row_data)
        count += 1

# 关闭浏览器窗口
driver.quit()