import os
import subprocess


def execute_scrapy():
    print('Scrapy')
    subprocess.run(['scrapy', 'crawl', 'amazon_spider'])
    print('Scrapy done')


def execute_load_to_bronze():
    print('Load to bronze')
    subprocess.run(['python', './staging_to_bronze/main.py'])
    print('Load to bronze done')


def execute_transform_to_dbt():
    print('Transform to dbt')
    os.chdir('./lakehouse_project')
    subprocess.run(['dbt', 'run'])
    os.chdir('..')
    print('Transform to dbt done')


def main():
    execute_scrapy()
    execute_load_to_bronze()
    execute_transform_to_dbt()


if __name__ == '__main__':
    main()
