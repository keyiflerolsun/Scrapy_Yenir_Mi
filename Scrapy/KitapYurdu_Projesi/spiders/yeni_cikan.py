import scrapy

class YeniCikanSpider(scrapy.Spider):
    name            = 'yeni_cikan'
    # 0
    allowed_domains = ['kitapyurdu.com', 'www.kitapyurdu.com']
    start_urls      = ['http://kitapyurdu.com/index.php?route=product/best_sellers&list_id=15&filter_in_stock=1']

    def parse(self, response):
        # 1
        kitaplar = response.xpath("//div[@class='product-grid']/div[@class='product-cr']")
        for kitap in kitaplar:
            kitap_linki = kitap.xpath("./div[@class='name ellipsis']/a/@href").get()
            yield scrapy.Request(kitap_linki, callback=self.kitap_detay)

        # 3
        sonraki_sayfa = response.xpath("//div[@class='links']/a[@class='next']/@href").get()
        if sonraki_sayfa:
            yield scrapy.Request(url=sonraki_sayfa, callback=self.parse)

    # 2
    def kitap_detay(self, response):
        detay_alani = response.xpath("//div[@class='pr_details']")
        yield {
            'ad'        : detay_alani.xpath("normalize-space(./div[@class='pr_header'])").get(),
            'yazar'     : detay_alani.xpath("normalize-space(.//a[@class='pr_producers__link'])").get(),
            'yayin_evi' : detay_alani.xpath("normalize-space(.//div[@class='pr_producers__publisher'])").get(),
            'aciklama'  : detay_alani.xpath("normalize-space(.//span[@class='info__text'])").get(),
            'kapak'     : response.xpath("//div[@class='pr_image-default']/a/img/@src").get()
        }