import csv
from lxml import html
import requests as requests

import pandas as pd


def get_detail(name):
    list_data = []
    tmp_url = "https://db.18183.com" + name
    http_response = requests.get(tmp_url)
    response_text = http_response.text
    selector = html.etree.HTML(response_text)
    hero_name = selector.xpath('//div[@class="name-box"]/h1/text()')[0]
    list_data.append(hero_name)
    basic_type = selector.xpath('//div[@class="hero-basicinfo-box fl"]/div[@class="base"]/dl/dd/text()')[0].strip()
    list_data.append(basic_type)
    basic_data_li = selector.xpath('//div[@class="otherinfo-datapanel"]/ul/li')
    for li in basic_data_li:
        pdata_str = li.xpath("./p/text()")[0]
        pdata = pdata_str.split("：")
        list_data.append(pdata[1].replace('%', ''))
    return list_data


def get_data():
    url = "https://db.18183.com/wzry/"
    http_response = requests.get(url)
    response_text = http_response.text
    selector = html.etree.HTML(response_text)

    div_people_li = selector.xpath("//ul[@class='mod-iconlist']/li")

    datas = []

    headers = ["HeroName", "HeroType", "MaximumHealth", "MaximumMana", "PhysicalAttack", "MagicAttack",
               "PhysicalDefense", "PhysicalDamageReduction", "MagicDefense", "MagicDamageReduction",
               "MovementSpeed", "PhysicalArmorPenetration", "MagicArmorPenetration", "AttackSpeedBonus",
               "CriticalStrikeRate", "CriticalStrikeDamage", "PhysicalLifeSteal", "MagicLifeSteal",
               "CooldownReduction", "AttackRange", "Tenacity", "HealthRegeneration", "ManaRegeneration"]

    count = 1
    for i in div_people_li:
        print('acquire data: ' + str(count))
        item_href = i.xpath('./a/@href')
        list_data = get_detail(
            str(item_href[0]))
        datas.append(list_data)
        count += 1

    df = pd.DataFrame(datas, columns=headers)
    df.fillna(0, inplace=True)
    data = df.drop_duplicates(subset=['HeroName'], keep='first', inplace=False)
    data.to_csv("../../static/csv/source2.csv", index=False, sep="\t")

def handle_data():
    # data
    get_data()


if __name__ == '__main__':
    handle_data()
