from itemadapter import ItemAdapter
import json


class SpiderSteamPipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if int(item['release_date'].split(' ')[2]) > 2000:
            line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
            self.file.write(line)
        return item
