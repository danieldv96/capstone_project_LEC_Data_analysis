import scrapy
# links
# primera columna equipos response.xpath('//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//span[@class="teamname"]/text()').getall()
# segunda columna puntaje de equipos response.xpath('//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//td[@rowspan="1" and @class=""]/text()').getall()
# title response.xpath('//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//th[(@colspan="14") or (@colspan="13")]/text()').getall()
# blueside and redside response.xpath('//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//td[not(@rowspan) and (@class="" or @class="md-winner")]/text()').getall()
# patch = response.xpath('//div[@id="matchlist"]//span[@class="matchlist-patches"]/span/a/text()').getall()
#seasons = response.xpath('//div[@class="tabheader-tab"]/div[@class="tabheader-content"]/a[contains(@href,"Spring_Season") or contains(@href,"Summer_Season")]/@href').getall()
# years = response.xpath('//div[@class="hlist"]//span/a[contains(@href,"LEC")]/@href').getall()
# season title = response.xpath('//table[@class="infobox InfoboxTournament"]//th[@class="infobox-title"]/text()').get()


class FandomLeague(scrapy.Spider):
    name = 'league'

    custom_settings = {
        'FEED_URI': 'lol_2020_2022.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'CONCURRENT_REQUESTS': 1,
        'ROBOTSTXT_OBEY': True
    }

    def start_requests(self):
        yield scrapy.Request('https://lol.fandom.com/wiki/LEC/2020_Season/Spring_Season', self.parse_2020)
        yield scrapy.Request('https://lol.fandom.com/wiki/LEC/2020_Season/Summer_Season', self.parse)
        yield scrapy.Request('https://lol.fandom.com/wiki/LEC/2021_Season/Spring_Season', self.parse)
        yield scrapy.Request('https://lol.fandom.com/wiki/LEC/2021_Season/Summer_Season', self.parse)
        yield scrapy.Request('https://lol.fandom.com/wiki/LEC/2022_Season/Spring_Season', self.parse)
        yield scrapy.Request('https://lol.fandom.com/wiki/LEC/2022_Season/Summer_Season', self.parse)

    def parse_2020(self, response):
        season = response.xpath(
            '//table[@class="infobox InfoboxTournament"]//th[@class="infobox-title"]/text()').get()
        weeks = response.xpath(
            '//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//th[(@colspan="14") or (@colspan="13")]/text()').getall()
        patchs = response.xpath(
            '//div[@id="matchlist"]//span[@class="matchlist-patches"]/span/a/text()').getall()

        teams = response.xpath(
            '//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//span[@class="teamname"]/text()').getall()
        score = response.xpath(
            '//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//td[@rowspan="1" and @class=""]/text()').getall()
        numteam = 0
        for num in range(0, len(score)):

            yield {
                'season': season,
                'week': weeks[int((num/10)+1)],
                'patch': patchs[int(num/10)],
                'team_1_blue_side': teams[numteam],
                'team_2_red_side': teams[numteam+1],
                'score': score[num]
            }
            numteam += 2

    def parse(self, response):
        season = response.xpath(
            '//table[@class="infobox InfoboxTournament"]//th[@class="infobox-title"]/text()').get()
        weeks = response.xpath(
            '//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//th[(@colspan="14") or (@colspan="13")]/text()').getall()
        patchs = response.xpath(
            '//div[@id="matchlist"]//span[@class="matchlist-patches"]/span/a/text()').getall()

        teams = response.xpath(
            '//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//span[@class="teamname"]/text()').getall()
        score = response.xpath(
            '//table[@class="wikitable hoverable-multirows md-table popup-window-container-y"]//td[@rowspan="1" and @class=""]/text()').getall()

        # as the page does not have an explicit way to show there is a super week, I needed to specify this for 2020 summer, 2021 and 2022 when super week was included
        numteam = 0

        for num in range(0, len(score)):
            if num < 15:
                yield {
                    'season': season,
                    'week': weeks[1],
                    'patch': patchs[0],
                    'team_1_blue_side': teams[numteam],
                    'team_2_red_side': teams[numteam+1],
                    'score': score[num],

                }
            elif 15 <= num < 75:

                yield {
                    'season': season,
                    'week': weeks[int(((num-5)/10)+1)],
                    'patch': patchs[int((num-5)/10)],
                    'team_1_blue_side': teams[numteam],
                    'team_2_red_side': teams[numteam+1],
                    'score': score[num],
                    'num': num
                }
            elif 75 <= num < 90:
                yield {
                    'season': season,
                    'week': weeks[8],
                    'patch': patchs[0],
                    'team_1_blue_side': teams[numteam],
                    'team_2_red_side': teams[numteam+1],
                    'score': score[num],
                }

            elif 90 <= num:
                yield {
                    'season': season,
                    'week': weeks[-1],
                    'patch': patchs[-1],
                    'team_1_blue_side': teams[numteam],
                    'team_2_red_side': teams[numteam+1],
                    'score': score[num],
                }

            numteam += 2
