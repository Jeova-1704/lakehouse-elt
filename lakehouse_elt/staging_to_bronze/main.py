from lakehouse_elt.config.BucketConnection import BucketConnection
from lakehouse_elt.config.LakehouseConnection import LakeHouseConnection


def main():
    lakehouse_conn = LakeHouseConnection()
    bucket_conn = BucketConnection()
    
    df = bucket_conn.get_all_files_in_bucket()
    lakehouse_conn.insert_dataframe_to_bronze(df)
    
    lakehouse_conn.close_connection()


if __name__ == "__main__":
    main()


