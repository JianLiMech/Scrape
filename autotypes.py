# 请下载到本地后运行！！！不要在服务器运行！！！
# 请下载到本地后运行！！！不要在服务器运行！！！
# 请下载到本地后运行！！！不要在服务器运行！！！

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import csv


## 启动 指定chromedriver的路径
driver = webdriver.Chrome()

# 创建headers，使用requests可能会被网站反爬机制阻止爬虫程序，加上headers模拟用户访问就不会有问题。
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}
## 打开网页
driver.get('https://www.autohome.com.cn/car/#pvareaid=6855968')
response = requests.get("https://www.autohome.com.cn/car/#pvareaid=6855968", headers= headers)
original_window_handle = driver.current_window_handle

time.sleep(5)

# 设置滚动
roll = 1000
while True:
    h_before = driver.execute_script('return document.documentElement.scrollTop')
    time.sleep(0.5)
    driver.execute_script(f'window.scrollTo(0,{roll})')
    time.sleep(0.5)
    h_after = driver.execute_script('return document.documentElement.scrollTop')
    roll += 1000
    # 滚动10行
    if roll > 10000:
        break
    # 滚动到底
    # if h_before == h_after:
    #     break
time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html,"html.parser")

with open('car_brands_and_models.csv', 'w', encoding='utf-8', newline='') as file:  # 使用newline=''以避免写入空行
    writer = csv.writer(file)

    count = 1
    # 所有汽车品牌
    titles = soup.findAll("div", attrs={"class": "h3-tit"})
    for title in titles:
        brand = title.find("a")
        brand_name = brand.string
        # 写入品牌信息到CSV文件
        writer.writerow([f"{count}. 品牌: {brand_name}"])
        count += 1

        click_element = title.find("a")
        relative_path = click_element.get("href")
        relative_path = relative_path.lstrip('/')
        click_url = f"https://{relative_path}"
        driver.execute_script('window.open("' + click_url + '");')
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        autonames_fb = soup.findAll("div", attrs={"class": "main-title"})
        autoprices = soup.findAll("span", attrs={"class": "font-arial"})
        if autonames_fb:
            for autoname, autoprice in zip(autonames_fb, autoprices):
                autoname = autoname.find("a").string
                autoprice = autoprice.string
                # 写入型号和价格信息到CSV文件
                writer.writerow([f"型号: {autoname}", f"价格: {autoprice}"])
        else:
            autonames_fl = soup.findAll("span", attrs={"class": "fn-left"})
            if autonames_fl:
                for autoname in autonames_fl:
                    autoname = autoname.find("a").string
                    # 写入型号和停售信息到CSV文件
                    writer.writerow([f"型号: {autoname}", "停售"])
            else:
                # 写入未知型号和价格信息到CSV文件
                writer.writerow(["型号: 未知", "价格: 未知"])

# 写入txt
# with open('car_brands_and_models.txt', 'w', encoding='utf-8') as file:
#     count = 1
#     # 所有汽车品牌
#     titles = soup.findAll("div", attrs={"class": "h3-tit"})
#     for title in titles:
#         # print(title)
#         brand = title.find("a")
#         brand_name = brand.string
#         file.write(f"\n{count}. 品牌: {brand_name}\n")
#         # click_element = driver.find_element_by_partial_link_text("car.autohome.com.cn/price") 
#         click_element = title.find("a") 
#         relative_path = click_element.get("href")
#         # 去掉前面的双斜杠
#         relative_path = relative_path.lstrip('/')
#         # 构建完整的URL
#         click_url = f"https://{relative_path}"
#         # driver.get(click_url)
#         # 切换到新窗口
#         driver.execute_script('window.open("' + click_url + '");')
#         driver.switch_to.window(driver.window_handles[-1])  
#         time.sleep(2)
#         html = driver.page_source
#         soup = BeautifulSoup(html,"html.parser")

        
#         autonames_fb = soup.findAll("div", attrs={"class": "main-title"}) # 在新窗口中爬取信息
#         autoprices = soup.findAll("span", attrs={"class": "font-arial"})
#         if autonames_fb:
#             for autoname, autoprice in zip(autonames_fb, autoprices):
#                 autoname = autoname.find("a")
#                 file.write(f"型号: {autoname.string}, 价格：{autoprice.string}\n")

#         else:
#             autonames_fl = soup.findAll("span", attrs={"class": "fn-left"})
#             if autonames_fl:
#                 for autoname in autonames_fl:
#                     autoname = autoname.find("a")
#                     file.write(f"型号: {autoname.string}, 停售\n")
#             else:
#                 file.write("型号: 未知, 价格: 未知\n")
        driver.close() # 关闭新窗口
        driver.switch_to.window(original_window_handle) # 切换回原窗口
        html = driver.page_source
        soup = BeautifulSoup(html,"html.parser")
        # count += 1
print(count)
