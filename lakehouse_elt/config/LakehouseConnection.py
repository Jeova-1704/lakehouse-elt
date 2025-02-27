import psycopg2
from dotenv import load_dotenv
import os
import polars as pl


class LakeHouseConnection:
    def __init__(self):
        """Inicializa a conexão com o banco de dados do Supabase (Lakehouse)."""
        load_dotenv()
        self.user = os.getenv('USER_PG')
        self.password = os.getenv('PASSWORD_PG')
        self.host = os.getenv('HOST_PG')
        self.port = os.getenv('PORT_PG')
        self.dbname = os.getenv('DBNAME_PG')

        self.conn = self.create_connection()
        self.create_if_not_exists_table_layer_bronze()

    def create_connection(self):
        """Cria e retorna uma conexão com o PostgreSQL no Supabase."""
        try:
            connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                dbname=self.dbname,
            )
            print('✅ Conexão com o PostgreSQL estabelecida com sucesso!')
            return connection

        except Exception as e:
            raise Exception(f'❌ Erro ao conectar ao lakehouse: {e}')

    def create_if_not_exists_table_layer_bronze(self):
        """Cria a tabela Bronze no PostgreSQL se ela não existir."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS bronze_amazon_products (
                        id SERIAL PRIMARY KEY,
                        product_name TEXT,
                        price_whole TEXT,
                        rating_value TEXT,
                        extracted_at TEXT
                    );
                """)
                self.conn.commit()
                print('✅ Tabela Bronze verificada/criada com sucesso!')

        except Exception as e:
            print(f'❌ Erro ao criar/verificar a tabela Bronze: {e}')

    def insert_dataframe_to_bronze(self, df: pl.DataFrame):
        """Insere um DataFrame Polars na tabela Bronze do PostgreSQL."""
        try:
            with self.conn.cursor() as cur:
                for row in df.iter_rows(named=True):
                    cur.execute(
                        """
                        INSERT INTO bronze_amazon_products (product_name, price_whole, rating_value, extracted_at)
                        VALUES (%s, %s, %s, %s);
                    """,
                        (
                            row['product_name'],
                            row['price_whole'],
                            row['rating_value'],
                            row['extracted_at'],
                        ),
                    )

                self.conn.commit()
                print('✅ DataFrame inserido na tabela Bronze com sucesso!')

        except Exception as e:
            print(f'❌ Erro ao inserir DataFrame na tabela Bronze: {e}')

    def close_connection(self):
        """Fecha a conexão com o PostgreSQL."""
        if self.conn:
            self.conn.close()
            print('✅ Conexão com o PostgreSQL encerrada!')


if __name__ == '__main__':
    lakehouse_conn = LakeHouseConnection()

    data = {
        'product_name': ['Smartphone X', 'Smartphone Y'],
        'price_whole': ['R$ 2.199,90', 'R$ 1.399,05'],
        'rating_value': ['4.8', '4.7'],
        'extracted_at': ['2025-02-25', '2025-02-25'],
    }

    df_test = pl.DataFrame(data)

    lakehouse_conn.insert_dataframe_to_bronze(df_test)

    lakehouse_conn.close_connection()
