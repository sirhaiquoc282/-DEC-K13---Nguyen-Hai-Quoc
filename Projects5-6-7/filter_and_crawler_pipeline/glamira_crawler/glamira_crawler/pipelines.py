# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import os


class GlamiraCrawlerPipeline:
    def open_spider(self, spider):
        file_exists = os.path.isfile("products.csv")
        self.file = open("products.csv", "a", newline="", encoding="utf-8")
        self.writer = csv.DictWriter(
            self.file, fieldnames=["product_id", "product_name"]
        )
        if not file_exists:
            self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if "product_id" in item and "product_name" in item:
            self.writer.writerow(item)
        else:
            spider.logger.warning(f"Item thiếu trường cần thiết: {item}")
        return item
