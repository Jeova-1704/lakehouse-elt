from itemadapter import ItemAdapter
import os
from dotenv import load_dotenv
from datetime import datetime
from supabase import create_client
import json


class SupabasePipeline:
    def __init__(self):
        load_dotenv(override=True)
        self.URL = os.getenv('LAKEHOUSE_URL')
        self.KEY = os.getenv('LAKEHOUSE_KEY')
        self.BUCKET_NAME = os.getenv('BUCKET_NAME')
        self.FILE_NAME = os.getenv('FILE_NAME')
        self.client = create_client(self.URL, self.KEY)

        self.itens = []

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        self.itens.append(item_dict)
        return item

    def close_spider(self, spider):
        if not self.itens:
            spider.log('No items to save')
            return

        now = datetime.now()
        ano = now.strftime('%Y')
        mes = now.strftime('%m')

        folder_path = f'{ano}/{mes}'
        full_path = f'{folder_path}/{self.FILE_NAME}'

        json_data = json.dumps(self.itens, indent=4)

        try:
            existing_files = self.client.storage.from_(self.BUCKET_NAME).list(
                folder_path
            )

            if existing_files and isinstance(existing_files, list):
                for file in existing_files:
                    file_path = f'{folder_path}/{file["name"]}'
                    self.client.storage.from_(self.BUCKET_NAME).remove(
                        file_path
                    )
                    spider.log(f'Deleted old file: {file_path}')

            response = self.client.storage.from_(self.BUCKET_NAME).upload(
                full_path,
                json_data.encode('utf-8'),
                file_options={'content-type': 'application/json'},
            )

            if response:
                spider.log(f'Data saved in {full_path}')

        except Exception as e:
            spider.log(f'Error saving data: {e}')
