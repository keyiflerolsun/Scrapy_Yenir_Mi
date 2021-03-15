# Scrapy Başlangıcı

## Proje Oluşturma

```bash
scrapy startproject KitapYurdu_Projesi

cd KitapYurdu_Projesi

scrapy genspider yeni_cikan kitapyurdu.com
```

## Genel Ayarlar

`settings.py`

```python
# keyiflerolsun
FEED_EXPORT_ENCODING           = 'utf-8'
DOWNLOAD_DELAY                 = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 2
HTTPERROR_ALLOWED_CODES        = [404]
USER_AGENT                     = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"
```

## Başlatma

```bash
scrapy crawl yeni_cikan -o bakalim.json
```
