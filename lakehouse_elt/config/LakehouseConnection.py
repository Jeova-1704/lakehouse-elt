import psycopg2
from dotenv import load_dotenv
import os
import json
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
        self.delete_table_temp()
        self.create_table_temp()
        self.delete_stored_procedure()
        self.create_stored_procedure()
        
        
    def delete_table_temp(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                            DROP TABLE IF EXISTS raw_amazon_json;
                            """)
                self.conn.commit()
                print('✅ Tabela Temp deletada com sucesso!')
        except Exception as e:
            print(f'❌ Erro ao deletar a tabela Temp: {e}')
        
    
    def create_table_temp(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                            CREATE TABLE IF NOT EXISTS raw_amazon_json (
                                product_name TEXT,
                                rating_value TEXT,
                                extracted_at TEXT,
                                price_whole TEXT
                            );
                            """)
                self.conn.commit()
                print('✅ Tabela Temp verificada/criada com sucesso!')
        except Exception as e:
            print(f'❌ Erro ao criar/verificar a tabela Temp: {e}')
            
    
    def delete_stored_procedure(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                            DROP PROCEDURE IF EXISTS load_raw_to_bronze;
                            """)
                print('✅ Stored Procedure deletada com sucesso!')
        except Exception as e:
            print(f'❌ Erro ao deletar Stored Procedure: {e}')
    
    
    def create_stored_procedure(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                            CREATE OR REPLACE PROCEDURE load_raw_to_bronze()
                            LANGUAGE plpgsql
                            AS $$
                            BEGIN
                                INSERT INTO bronze_amazon_products (product_name, price_whole, rating_value, extracted_at)
                                SELECT
                                    product_name,
                                    price_whole,
                                    rating_value,
                                    extracted_at
                                FROM raw_amazon_json;
                            END $$;
                            """)
                self.conn.commit()
                print('✅ Stored Procedure criada com sucesso!')
        except Exception as e:
            print(f'❌ Erro ao criar Stored Procedure: {e}')


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
                for row in df.rows():
                    product_name = row[0]
                    rating_value = row[1]
                    extracted_at = row[2]
                    price_whole = row[3]
                    cur.execute(""" 
                        INSERT INTO raw_amazon_json (product_name, rating_value, extracted_at, price_whole)
                        VALUES (%s, %s, %s, %s);
                    """, (product_name, rating_value, extracted_at, price_whole))
                    
                cur.execute("CALL load_raw_to_bronze();")
                
                self.conn.commit()
                print('✅ Dados inseridos na tabela Bronze com sucesso!')
                  
        except Exception as e:
            print(f'❌ Erro ao inserir dados na tabela Bronze: {e}')
            
    def close_connection(self):
        """Fecha a conexão com o PostgreSQL."""
        if self.conn:
            self.conn.close()
            print('✅ Conexão com o PostgreSQL encerrada!')
