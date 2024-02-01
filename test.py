import scrapy

class FilmSpider(scrapy.Spider):
    
    name = 'wiki_films2'        
    start_urls = ['https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83']

    def parse(self, response):       

        for link in response.css('div[id="mw-pages"] a::attr(href)'):                                
            yield response.follow(link, callback=self.parse_film)   

    def parse_film(self, response):

        name_film = response.css('th.infobox-above::text').get()

        if response.css('span[data-wikidata-property-id="P136"]').css('a::text').getall():
            genre_film = response.css('span[data-wikidata-property-id="P136"]').css('a::text').getall()
        else:
            genre_film = response.css('span[data-wikidata-property-id="P136"]').css('span::text').getall()

        if response.css('span[data-wikidata-property-id="P57"]').css('span::text').getall():
            director_film = response.css('span[data-wikidata-property-id="P57"]').css('span::text').getall()
        else:
            director_film = response.css('span[data-wikidata-property-id="P57"]').css('a::text').getall()

        country_film = response.css('span.wrap::text').getall()

        if response.css('span.nowrap > a::text').get():
           year_film = response.css('span.nowrap > a::text').getall()
        else:
           year_film = response.css('span.dtstart::text').getall()        
              
        yield {        
        'Название':name_film,                 
        'Жанр':genre_film,
        'Режиссёр':director_film,
        'Страна':country_film,
        'Год':year_film
        }       
                     
        yield response.follow(response.css('div[id="mw-pages"] a::attr(href)').getall()[-1], callback=self.parse) 
