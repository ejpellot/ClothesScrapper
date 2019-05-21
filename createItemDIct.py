from bs4 import BeautifulSoup
import requests
import json
import re
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

def createItemDict(url): # Returns Collection of given item
    name_search = re.search('products/(.+?).html', url)
    name = name_search.group(1).upper()
    r = requests.get(url, headers=agent)
    soup = BeautifulSoup(r.text, 'html.parser')
    item_dic = {}
    item_collection = soup.select(".product-item")
    
    for item in item_collection:
        if item.select(".item-heading"):
            product_page = item.select(".item-link")[0]['href']
            item_link = "https://www2.hm.com" + (product_page)
            style = item.select(".link")[0].text.strip()
            price = item.select(".item-price")[0].text.strip().replace("$","")
            new_price = float(price)
            img = "https:" + item.find('img')['data-src']
            altimg = "https:" + item.find('img')['data-altimage']
            item_id =  item.find('article')['data-articlecode']
            temp= {
                "id": item_id,
                "product_page": item_link,
                "style": style,
                "price": new_price,
                "image": [img, altimg]
                }
            item_dic.setdefault(name,[]) 
            item_dic[name].append(temp)
    return item_dic

def getItemUrl(): # Returns URL of each item in menu
    return url