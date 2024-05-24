from scrapy.exporters import CsvItemExporter

class HonofofkingPipeline:
    def __init__(self):
        self.fp = open("../../static/csv/source1.csv", "wb")
        self.exporter = CsvItemExporter(self.fp)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        print("catch one record", item['name'])
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fp.close()
