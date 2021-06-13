import scrapy

class digi(scrapy.Spider): 
    name = "digikala"
    categories = ['تکنولوژی  علمی فناوری', 
     'مالی و سرمایه گذاری ،بانک و بیمه و پول',
     'خودرو و حمل و نقل',
     'پزشکی و سلامت و زیبایی و تناسب اندام',
     'خبرهای سیاسی و اجتماعی، جامعه و فرهنگ',
     'توریستی و گردشگری ،مسافرت، تفریح',
     'تولد، جملات عاشقانه، فال، تعبیر خواب، sms',
     'خانه و مسکن',
     'آشپزی، غذا و نوشیدنی',
     'کتاب و ادبیات، انقلاب اسلامی، دین و اسلام',
     'باغبانی و هنرهای خانگی',
     'حیوانات و جانوران خانگی',
     'اشتغال و آموزش',
     'موبایل و کامپیوتر و تجهیزات جانبی',
     'گیم و بازی، دانلود، فیلم، آهنگ',
     'پوشاک، مد، عطر، زیبایی و آرایشی',
     'سرویس های اینترنتی',
     'لوازم خانگی',
     'نوزاد و کودک',
     'زناشویی',
     'اخبار ورزشی',
    ]

    start_urls = [
        #'https://www.digikala.com/search/?q=%DA%A9%D8%AA%D8%A7%D8%A8%20%D8%AA%DA%A9%D9%86%D9%88%D9%84%D9%88%DA%98%DB%8C', #Technology
        #"https://www.digikala.com/search/?q=%DA%A9%D8%AA%D8%A7%D8%A8%20%D8%B3%D8%B1%D9%85%D8%A7%DB%8C%D9%87%20%DA%AF%D8%B0%D8%A7%D8%B1%DB%8C", #Investing
        #'https://www.digikala.com/search/?q=%D9%84%D9%88%D8%A7%D8%B2%D9%85%20%D8%AE%D9%88%D8%AF%D8%B1%D9%88', #Cars
        #'https://www.digikala.com/search/?q=%D8%AA%D9%86%D8%A7%D8%B3%D8%A8%20%D8%A7%D9%86%D8%AF%D8%A7%D9%85', #Fitness
        #'https://www.digikala.com/search/category-book/?q=%DA%A9%D8%AA%D8%A7%D8%A8%20%D8%B3%DB%8C%D8%A7%D8%B3%DB%8C&key=%D8%B3%DB%8C%D8%A7%D8%B3%DB%8C&pos=2', #Politics
        #'https://www.digikala.com/search/?q=%D8%AA%D8%AC%D9%87%DB%8C%D8%B2%D8%A7%D8%AA%20%D8%B3%D9%81%D8%B1', #Travel
        #'https://www.digikala.com/search/?q=%D8%AA%D9%88%D9%84%D8%AF', #Birthday
        #'https://www.digikala.com/search/category-decorative/', #Home
        #'https://www.digikala.com/search/category-ready-made-food/?fresh=1', #food
        #'https://www.digikala.com/search/category-book/?q=%DA%A9%D8%AA%D8%A7%D8%A8%20%D8%A7%D9%86%D9%82%D9%84%D8%A7%D8%A8%20%D8%A7%D8%B3%D9%84%D8%A7%D9%85%DB%8C&key=%D8%A7%D9%86%D9%82%D9%84%D8%A7%D8%A8%20%D8%A7%D8%B3%D9%84%D8%A7%D9%85%DB%8C&pos=1', #Islam
        #'https://www.digikala.com/search/?q=%DB%8C%D8%A7%D8%BA%D8%A8%D8%A7%D9%86%DB%8C', # Garden
        #'https://www.digikala.com/search/category-pet/', # pet
        #'https://www.digikala.com/search/category-educational-game/?q=%D8%A8%D8%A7%D8%B2%DB%8C%20%D8%A7%D9%85%D9%88%D8%B2%D8%B4%DB%8C&pageno=3&sortby=22', #Educational
        #'https://www.digikala.com/search/category-mobile-phone/', #Phone
        #'https://www.digikala.com/search/category-game/?q=%D8%A8%D8%A7%D8%B2%DB%8C%20%DA%A9%D8%A7%D9%85%D9%BE%DB%8C%D9%88%D8%AA%D8%B1%DB%8C&key=%D8%A8%D8%A7%D8%B2%DB%8C%20%DA%A9%D8%A7%D9%85%D9%BE%DB%8C%D9%88%D8%AA%D8%B1%DB%8C&pos=1', #game
        #https://www.digikala.com/search/category-perfume-all/', #health
        #'https://www.digikala.com/search/?q=%D9%85%D9%88%D8%AF%D9%85'#Internet
        #'https://www.digikala.com/search/category-home-appliance/', #Furniture
        #'https://www.digikala.com/search/category-kids-play-tent/' #kids and infants
        #'https://www.digikala.com/search/category-book/?q=%DA%A9%D8%AA%D8%A7%D8%A8%20%D8%B2%D9%86%D8%A7%D8%B4%D9%88%DB%8C%DB%8C&key=%D8%B2%D9%86%D8%A7%D8%B4%D9%88%DB%8C%DB%8C&pos=1', #books
        'https://www.digikala.com/search/?q=%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1%20%D9%88%D8%B1%D8%B2%D8%B4%DB%8C&pageno=1&sortby=22', #SportsNews
    ]

    def parse(self, response):
        category_product_crawled = 0
        items = response.css('.c-product-box a::attr(href)').getall()
        for item_link in items:
            if category_product_crawled < 100:
                category_product_crawled += 1
                yield scrapy.Request('https://www.digikala.com'+item_link, callback= self.parse_item)
        next_page = 'https://www.digikala.com'+response.css('.js-pagination__item a::attr(href)').getall()[1]
        if next_page is not None:
            yield scrapy.Request(url = next_page, callback = self.parse)

    def parse_item(self, response):
        result = {}
        print(response.url, " !!!! ")
        result['url'] = response.url
        result['Name'] = response.css('.c-product__title::text').get()
        result['Stars'] = response.css('.c-product__engagement-rating::text').get()
        result['#Votes'] = response.css('.c-product__engagement-rating::text').get()
        result['Price'] = response.css('.c-product__seller-price-pure::text').get()
        result['currency'] = response.css('.c-product__seller-price-real::text').get()
        result['category'] = digi.categories[20]
        yield result

