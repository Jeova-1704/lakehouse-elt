from supabase import create_client
from dotenv import load_dotenv
from os import getenv
from datetime import datetime
import json
import polars as pl
from io import StringIO


class BucketConnection:
    def __init__(self):
        """Inicializa a conexão com o Supabase Storage"""
        load_dotenv()
        self.supabase_url = getenv('LAKEHOUSE_URL')
        self.supabase_key = getenv('LAKEHOUSE_KEY')
        self.bucket_name = getenv('BUCKET_NAME')
        self.file_name = getenv('FILE_NAME')

        self.client = create_client(self.supabase_url, self.supabase_key)

    def get_all_files_in_bucket(self):
        """Baixa um arquivo do Supabase Storage e converte para um DataFrame Polars"""
        ano = datetime.now().strftime('%Y')
        mes = datetime.now().strftime('%m')
        file_path = f'{ano}/{mes}/{self.file_name}'

        try:
            response = self.client.storage.from_(self.bucket_name).download(
                file_path
            )

            try:
                data = json.loads(response.decode('utf-8'))
                df = pl.DataFrame(data)
            except json.JSONDecodeError:
                csv_data = StringIO(response.decode('utf-8'))
                df = pl.read_csv(csv_data)

            print(f'✅ Arquivo {file_path} carregado com sucesso!')
            return df

        except Exception as e:
            print(f'❌ Erro ao carregar arquivo do Supabase: {e}')
            return None
