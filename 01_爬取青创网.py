import requests
import json
import subprocess
from functools import partial #用来固定某个参数的固定值
subprocess.Popen=partial(subprocess.Popen,encoding='utf-8')
import re
import execjs
import time
import random
import csv
class Crawl_qingchuangwang:
    # keyword为搜索关键词
    def __init__(self,keyword):
        self.url = "https://newopenapiweb.17qcc.com/api/services/app/SearchFactory/GetPageList"

        # headers需要自己去复制替换！！
        self.headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "app-guestid": "24967DED898936B3B31AC57D5F9B6973",
            "app-version": "0",
            "authorization": "Bearer wNYmO41/48SHNstaLVXxHCCre29BZQl1NhC6NM3R3rzpXtPQxVzH6jEzA/QhXFN5tu6Fk7pO53uppm1mVXMZgxbyRVz26dnepi/FyB6axBY+6gq1GL+uRQgoiFUCjRN2p8w6LevViwKlHyWZZJZO1DGVSjAi1m2U+og9pkHw9/Skc+w71JNcZzDPK9Etj0loJfyj+sMvMKO3C1e15tO28ZNuEhr1q4zzwgC4JTMRKRPAc1/FA/GzbvtLGYPwSgjO2tc+8q7NOQY9kuZHTkK+GOHqb+WjdIxpRvQdBW/cAnEzf1FPw7XAOrpHSKuX4na7z8lIDsrlH0eV9SFcgY+vlDnvzhOeTF6am7xdRYmGnJFV0SjFUQ7OnlkZAqfZZNnHxpQl8NsfmXocySJzQ+CeR4UPV9QgZAycEEUxwP+wkYdHMORiLb0Q1Qo7CUX17rjILVvx1WbY3GMUayoX97qxAnRK/ems49RGLs3mx3QX8sw8n6YlIzRVcvF/ZcIK2IpxauX2xivhkp0ahBOO7BezG9xRBaRjArb/q8Z4/UZ//aHqGa4rZBcd2aY0LshY6+QUpjPgwGKiSHg1Gj/Q0TA0fNKDssgeQe3pDM/4ixywf2MmdeVVYejPfvO4LesZdkRXZ0StjmNW3xMu4gQay0VvkqAw1CMGqsgnUT73DoJCffM=",
            "cache-control": "no-cache",
            "content-length": "774",
            "content-type": "application/json",
            "origin": "https://www.17qcc.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.17qcc.com/",
            "sec-ch-ua": "\"Chromium\";v=\"142\", \"Microsoft Edge\";v=\"142\", \"Not_A Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0"
        }

        self.keyword = keyword
        self.qccppm = self.get_qccppm(keyword)

    def get_qccppm(self,keyword):
        main_page_url = "https://www.17qcc.com/list.html"
        main_page_header = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
        }

        for i in range(1,6):
            main_page_content = requests.get(main_page_url, headers=main_page_header)
            match = re.search(r'var qccppm = "([^"]+)"', main_page_content.text)
            # [^"] 表示 “非双引号的任意字符”；
            # + 表示 “匹配
            # 1 次或多次”；
            # 整体意思是 “捕获双引号内的所有内容（直到遇到下一个双引号为止）”。

            if match:
                qccppm_value = match.group(1)
                print("成功提取到的 qccppm 值：", qccppm_value)
                return qccppm_value
            else:
                print("访问页面失败，未找到 qccppm，剩余尝试次数{num}".format(num=5-i))
            time.sleep(random.randint(1,5))

        return 0

    def get_payload(self, page_index):
        f = open("02_加密逻辑.js", "r", encoding="utf-8")
        js_code = f.read()
        js_exec = execjs.compile(js_code)
        print("搜索关键字:{keyword},页码:{page}，准备调用js加密函数，获取加密好的请求负载".format(keyword=self.keyword,page=page_index))
        # 调用js加密函数，传值搜索关键词,页码,qccppm，已获得加密好的请求负载，并返回给get_info函数
        return js_exec.call("get_jiami_data",self.keyword,page_index,self.qccppm)

    def jiemi(self,response):
        # 调用03_解密逻辑.js里的解密函数，处理加密函数
        f = open("03_解密逻辑.js", "r", encoding="utf-8")
        js_code = f.read()
        js_exec = execjs.compile(js_code)
        # 调用解密函数
        return js_exec.call("get_jiemi_data",self.qccppm,response)

    def get_info(self,page_index):
        if self.qccppm == 0:
            print("未有提取到qccppm,即将推出整个函数，请重试...")
            return 0

        # 已获得加密好的请求负载
        get_payload = self.get_payload(page_index)
        get_payload = json.dumps(get_payload, separators=(',', ':'))
        # separators = (',', ':')：自定义JSON中的分隔符，参数是一个元组(item_sep, keyword_sep)
        # item_sep（第一个元素','）：指定不同键值对之间的分隔符（默认是', '，即逗号后带空格）。
        # keyword_sep（第二个元素':'）：指定键和值之间的分隔符（默认是': '，即冒号后带空格）。}

        response = requests.post(url=self.url, headers= self.headers, data=get_payload)
        response = json.loads(response.text)

        # 转化为dict，提取键为dict中的["Result"]["Items"],是个Item列表
        Items_list = json.loads(self.jiemi(response))["Result"]["Items"]
        # print(Items_data)
        self.save_csv(Items_list,page_index)


    def save_csv(self,Items_list,page_index):
        filtered_data = []
        for item in Items_list:
            filtered_item = {
                # 提取item信息，提取不到返回{}
                "商品名": item.get("ProductName", {}),
                "价格": item.get("Price", {}),
                "店铺名": item.get("ShopName", {}),
                "店铺链接": item.get("ShopUrl", {}),
                "年销量": item.get("YearSaleCount", {})
            }
            filtered_data.append(filtered_item)

        # 写入 CSV 文件
        with open("青创网商品数据(实例).csv", "a", newline="", encoding="utf-8-sig") as f:
            if page_index == 1:
            # 定义表头（与 filtered_item 的键对应），并且标头只要第一次写入即可！！！
                fieldnames = ["商品名","价格", "店铺名", "店铺链接", "年销量"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()  # 写入表头

            fieldnames = ["商品名", "价格", "店铺名", "店铺链接", "年销量"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerows(filtered_data)  # 写入所有数据行

        print("{keyword}第{page_index}页，写入csv完成！\n".format(keyword=self.keyword,page_index=page_index))


if __name__ == '__main__':
    print("------------使用之前替换类中self.headers-------------")
    keyword = str(input("输入检索关键字(实例：休闲裤男):"))
    # 创建实例对象
    crawl_qgw = Crawl_qingchuangwang(keyword)

    page_index = int(input("输入爬取到的页码:"))
    for i in range(1,page_index + 1):
        crawl_qgw.get_info(i)
        time.sleep(random.randint(1,5))


