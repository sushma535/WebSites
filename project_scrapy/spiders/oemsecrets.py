import scrapy
from scrapy.crawler import CrawlerProcess
import os
import csv
from csv import reader
import re

total_data = {}


class SimilarWeb(scrapy.Spider):
    name = 'SW'
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    start_urls = ['https://www.oemsecrets.com/', 'https://www.similarsites.com/site/oemsecrets.com/']
    csv_columns = ['Category', 'Description', 'Name', 'Url']
    csv_file = 'websites1_data.csv'
    count = 0

    def parse(self, response):
        data, desc, cat = '', '', ''
        print('response url:', response.url)
        if response.url == self.start_urls[0]:
            data = response.css('title::text').get()
            if data:
                data = re.sub("\n\t\t", '', data)
            total_data['Name'] = data
            self.count += 1
        elif response.url == self.start_urls[1]:
            cat = response.css(
                'div[class="StatisticsCategoriesDistribution__CategoryTitle-fnuckk-6 jsMDeK"]::text').getall()
            desc = response.css('div[class="SiteHeader__Description-sc-1ybnx66-8 hhZNQm"]::text').get()
            if cat:
                cat = ": ".join(cat[:])

            total_data['Category'] = cat
            total_data['Description'] = desc
            total_data['Url'] = self.start_urls[0]
            self.count += 1
        if self.count == 2:
            print("total data", total_data)
            new_data = [total_data['Category'], total_data['Description'], total_data['Name'],
                        total_data['Url']]
            print("new data", new_data)
            self.row_appending_to_csv_file(new_data)

    def row_appending_to_csv_file(self, data):
        if os.path.exists(self.csv_file):
            need_to_add_headers = False
            with open(self.csv_file, 'a+', newline='') as file:
                file.seek(0)
                csv_reader = reader(file)
                if len(list(csv_reader)) == 0:
                    need_to_add_headers = True
                csv_writer = csv.writer(file)
                if need_to_add_headers:
                    csv_writer.writerow(self.csv_columns)
                csv_writer.writerow(data)

        else:
            with open(self.csv_file, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(self.csv_columns)  # header

                csv_writer.writerow(data)


process = CrawlerProcess()
process.crawl(SimilarWeb)
process.start()
