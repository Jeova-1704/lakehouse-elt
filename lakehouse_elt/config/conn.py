from supabase import create_client
from dotenv import load_dotenv
from os import getenv


class SupabaseConnection:
    def __init__(self):
        load_dotenv()
        self.supabase_url = getenv('LAKEHOUSE_URL')
        self.supabase_key = getenv('LAKEHOUSE_KEY')

    def create_client_bucket(self):
        client = create_client(self.supabase_url, self.supabase_key)
        return client


def create_connection():
    connection = SupabaseConnection()
    return connection.create_client()
