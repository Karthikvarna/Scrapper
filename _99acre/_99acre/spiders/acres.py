from pathlib import Path

import scrapy

from pymongo import MongoClient

import urllib.parse
from urllib.parse import quote_plus

username = quote_plus('karthikvarna')
password = quote_plus('Orange@12')
client = MongoClient('mongodb+srv://' + username +':' + password + '@cluster0.ts0yzkw.mongodb.net/')
db = client.Properties

def inserttodb(page, name, cost, type, locality,city):
    cities = db[page]

    doc={"Property Name":name,"Propertry Cost":cost, "Property Type":type, "Property Locality":locality, "Property City":city}

    inserted = cities.insert_one(doc)

    return inserted.inserted_id


class QuotesSpider(scrapy.Spider):
    name = "acres"

    def start_requests(self):
        urls = [
            "https://www.99acres.com/search/property/buy/pune-all?city=19&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N",
            "https://www.99acres.com/search/property/buy/hyderabad-all?city=38&preference=S&area_unit=1&res_com=R",
            "https://www.99acres.com/search/property/buy/delhi-all?keyword=delhi&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N",
            "https://www.99acres.com/search/property/buy/mumbai-all?city=12&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N",
            "https://www.99acres.com/search/property/buy/lucknow-all?keyword=Lucknow(All)&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N",
            "https://www.99acres.com/search/property/buy/ahmedabad-all?city=45&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N",
            "https://www.99acres.com/search/property/buy/kolkata-all?city=25&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N",
            "https://www.99acres.com/search/property/buy/jaipur-all?keyword=Jaipur(All)&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N",
            "https://www.99acres.com/search/property/buy/chennai-all?city=32&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N",
            "https://www.99acres.com/search/property/buy/bangalore-all?city=20&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1].split("-")[0]
        filename = f"cities-{page}.html"
        cities = {}
        

        names = response.css(".projectTuple__projectName.projectTuple__pdWrap20.ellipsis::text").getall()

        costs = response.css("span.list_header_bold.configurationCards__srpPriceHeading.configurationCards__configurationCardsHeading::text").getall()
        
        tl=response.css("h2.projectTuple__subHeadingWrap.body_med.ellipsis::text").getall()

        proprert_type = []

        localities = []

        property_city = []
        

        new_costs = []
        for cost in costs:
            if cost != '₹ ':
                if cost[0] != "P":
                    new_costs.append('₹ '+cost)
                else:
                    new_costs.append(cost)


        for t in tl:
          proprert_type.append(t.split(" in ")[0])
          localities.append(t.split(" in ")[1].split(", ")[0])
          property_city.append(t.split(" in ")[1].split(", ")[1])

        """
        for p in proprert_type:
            print(p)
        
        for l in localities:
            print(l)

        for c in property_city:
            print(c)

        for cost in new_costs:
            print(cost)

        """
        for i in range(0,len(names)):
            inserttodb(page, names[i], new_costs[i], proprert_type[i], localities[i],property_city[i])
