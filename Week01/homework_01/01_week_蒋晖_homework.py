# -*- coding:utf-8 -*-
#@Time 2020/9/26 23:01
#@Author: Horse
#@File hw_01.py

# 使用BeautifulSoup解析网页
import requests
from bs4 import BeautifulSoup as bs
import lxml.etree
import pandas as pd

#define function for information
def getInformation(findurl):
    response2 = requests.get(findurl,headers=header)
    selector = lxml.etree.HTML(response2.text)

    #电影名称
    film_name = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/h1/text()')
    print(f'电影名称: {film_name}')

    #电影类型
    file_type = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/a/text()')
    print(f'电影类型: {file_type}')

    # 上映日期
    plan_date = selector.xpath('/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/text()')
    print(f'上映日期: {plan_date}')

    #输出到文件
    mylist = [film_name, file_type, plan_date]
    mymovie = pd.DataFrame(data=mylist)
    mymovie.to_csv('./mymovieList.csv', mode='a',encoding='utf8', index=False, header=False)


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
header = {
    'user-agent':user_agent,
    'Cookie':'uuid_n_v=v1; uuid=DAE71010000311EB91FA17E376A3912E0586C5A74A324BB8927EE47D3F0EC302; _csrf=0fc694075352bae8e7ac8d18d45a4c8930e6c9e45b262cfdebeee6a8940e61be; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1601130215; _lxsdk_cuid=174cacc35b051-0d62941260636a-e323069-161012-174cacc35b1c8; _lxsdk=DAE71010000311EB91FA17E376A3912E0586C5A74A324BB8927EE47D3F0EC302; mojo-uuid=dd7d1ca0d9bff3e52e5f37a07d2300f4; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1601297967; mojo-session-id={"id":"1f6e6b9f3a95077a02ccb5ac5e05eb88","time":1601297967118}; mojo-trace-id=1; __mta=214744744.1601130215343.1601218295126.1601297967596.6; _lxsdk_s=174d4cbe877-e44-529-5c4%7C%7C2'
}
myurl = 'https://maoyan.com/films?showType=3'
response = requests.get(myurl,headers=header)
bs_info = bs(response.text, 'html.parser')

# 遍历子链接获取电影详细信息
for tags in bs_info.find_all('div', attrs={'class': 'channel-detail movie-item-title'} , limit=10):
    for atag in tags.find_all('a'):
        wholeUrl="https://maoyan.com"+atag.get('href')
        getInformation(wholeUrl)