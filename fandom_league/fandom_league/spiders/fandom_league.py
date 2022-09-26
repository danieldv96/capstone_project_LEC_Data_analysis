import scrapy
# links
# primera columna equipos response.xpath('//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//span[@class="teamname"]/text()').getall()
# segunda columna puntaje de equipos response.xpath('//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//td[@rowspan="1" and @class=""]/text()').getall()
# title response.xpath('//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//th[@colspan="14"]/text()').getall()
# blueside and redside response.xpath('//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//td[not(@rowspan) and (@class="" or @class="md-winner")]/text()').getall()
# patch = response.xpath('//div[@id="matchlist"]//span[@class="matchlist-patches"]/span/a/text()').getall()
#seasons = response.xpath('//div[@class="tabheader-tab"]/div[@class="tabheader-content"]/a[contains(@href,"Spring_Season") or contains(@href,"Summer_Season")]/@href').getall()
# years = response.xpath('//div[@class="hlist"]//span/a[contains(@href,"LEC")]/@href').getall()


class FandomLeague(scrapy.Spider):
    name = 'league'
    start_urls = [
        'https://lol.fandom.com/wiki/LEC/2020_Season'
    ]
    custom_settings = {
        'FEED_URI': 'lol.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'ROBOTSTXT_OBEY': True
    }
    follow_urls = ['https://lol.fandom.com/wiki/LEC/2021_Season',
                   'https://lol.fandom.com/wiki/LEC/2022_Season']

    def parse(self, response):

        link_seasons = response.xpath(
            '//div[@class="tabheader-tab"]/div[@class="tabheader-content"]/a[contains(@href,"Spring_Season") or contains(@href,"Summer_Season")]/@href').getall()
        for season in link_seasons:

            yield response.follow(season, callback=self.parse_link, cb_kwargs={'url': response.urljoin(season)})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        week = response.xpath(
            '//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//th[@colspan="14"]/text()').getall()
        game_patch = response.xpath(
            '//div[@id="matchlist"]//span[@class="matchlist-patches"]/span/a/text()').getall()

        first_team = response.xpath(
            '//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//span[@class="teamname"]/text()').getall()
        second_team = response.xpath(
            '//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//td[@rowspan="1" and @class=""]/text()').getall()

        game_side = response.xpath(
            '//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//td[not(@rowspan) and (@class="" or @class="md-winner")]/text()').getall()

        yield {
            'url': link,
            'week': week,
            'patch': game_patch,
            'Team 1': first_team,
            'team 2': second_team,
            'Side': game_side

        }
        for follow_url in FandomLeague.follow_urls:
            yield response.follow(follow_url, callback=self.parse)
