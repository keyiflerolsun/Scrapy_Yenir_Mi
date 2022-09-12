# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from crochet import setup
setup()

from contextlib     import suppress
from scrapy         import Spider, Request
from scrapy.crawler import CrawlerRunner
from json           import load
from json.decoder   import JSONDecodeError
from time           import time, sleep
from Kekik          import zaman_donustur
from Kekik.cli      import konsol, hata_yakala, cikis_yap
from os             import remove

baslangic = time()
veriler   = None

class YeniCikanSpider(Spider):
    name            = "yeni_cikan"
    # 0
    allowed_domains = ["kitapyurdu.com", "www.kitapyurdu.com"]
    start_urls      = ["http://kitapyurdu.com/index.php?route=product/best_sellers&list_id=15&filter_in_stock=1"]

    def parse(self, response):
        # 1
        kitaplar = response.xpath("//div[@class='product-grid']/div[@class='product-cr']")
        for kitap in kitaplar:
            kitap_linki = kitap.xpath("./div[@class='name ellipsis']/a/@href").get()
            yield Request(kitap_linki, callback=self.kitap_detay)

        # 3
        sonraki_sayfa = response.xpath("//div[@class='links']/a[@class='next']/@href").get()
        if sonraki_sayfa:
            yield Request(url=sonraki_sayfa, callback=self.parse)

    # 2
    def kitap_detay(self, response):
        detay_alani = response.xpath("//div[@class='pr_details']")
        veri = {
            "ad"        : detay_alani.xpath("normalize-space(./div[@class='pr_header'])").get(),
            "yazar"     : detay_alani.xpath("normalize-space(.//a[@class='pr_producers__link'])").get(),
            "yayin_evi" : detay_alani.xpath("normalize-space(.//div[@class='pr_producers__publisher'])").get(),
            "aciklama"  : detay_alani.xpath("normalize-space(.//span[@class='info__text'])").get(),
            "kapak"     : response.xpath("//div[@class='book-front']/a/img/@src").get()
        }
        konsol.print(veri)
        yield veri

    # Fonksiyon ismi ve parametreleri değiştirilmemeli!
    def closed(self, reason):
        global veriler

        veriler = load(open(f"{YeniCikanSpider.name}.json"))

        konsol.print(f"\n\n[yellow]{len(veriler)} Adet Kitap Dızlandı » {zaman_donustur(time() - baslangic)} » {YeniCikanSpider.name}.json\n\n")


def basla(kac_saniye_arayla:int):
    global baslangic, veriler

    baslangic = time()

    konsol.log("[green]Fonksiyon Başladı!")

    with suppress(FileNotFoundError):
        remove(f"{YeniCikanSpider.name}.json")

    runner = CrawlerRunner({
        "LOG_ENABLED"                    : False,
        "LOG_LEVEL"                      : "ERROR",
        # "DOWNLOAD_DELAY"                 : 1,
        # "CONCURRENT_REQUESTS"            : 1,
        # "CONCURRENT_REQUESTS_PER_DOMAIN" : 2,
        "HTTPERROR_ALLOWED_CODES"        : [404],
        "USER_AGENT"                     : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
        "FEEDS"                          : {f"{YeniCikanSpider.name}.json" : {"format": "json", "encoding": "utf-8", "indent": 2}},
    })

    runner.crawl(YeniCikanSpider)

    sleep(kac_saniye_arayla)

    veriler = load(open(f"{YeniCikanSpider.name}.json"))

    konsol.print(f"[magenta]Fonksiyon Bitti! » {zaman_donustur(time() - baslangic)} «\n\n")


if __name__ == "__main__":
    try:
        while True:
            basla(kac_saniye_arayla=40)
    except JSONDecodeError:
        konsol.print(f"\n\n\n[bold red][!] Verdiğiniz Saniye Aralığı Örümcek İçin Yetersiz! | {zaman_donustur(time() - baslangic)}")
        cikis_yap()
    except Exception as hata:
        hata_yakala(hata)
