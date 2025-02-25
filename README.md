para executar a extração dos dados usando scrapy e jogar para a camada de staging, basta executar o comando abaixo:

```bash
scrapy crawl amazon_spider
```

ele já executa a extração, transforma os items no schema e já faz o upload para o bucket do supabase.