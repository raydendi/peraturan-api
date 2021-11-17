import scrapy

class PeraturanSpider(scrapy.Spider):
    name = 'peraturan'
    
    def start_requests(self):
        urls = ['https://peraturan.bpk.go.id/home/search?jenis=8&page=1']
        # automate scrapy at 2 url the same time
        for url in urls:
            yield scrapy.Request(url= url, callback= self.parse)

    def parse(self, response):
        ## catch css in the way have different method when list[1]
        for peraturan in response.css('div.portlet-body'):
            yield {
                'peraturanName': peraturan.css('span.font-blue::text').get().replace('\r\n                                    ','').replace('\r\n                                ', ''),
                'peraturanDescription': peraturan.css('span.lead.bold a::text').get(),
                'peraturanDicabut': peraturan.css('li.text-left.font-sm a::text').get(),
                'peraturanDiubah' : peraturan.css('li.text-left.font-sm a::text').get(),
                'link': 'https://peraturan.bpk.go.id'+peraturan.css('span.lead.bold a::attr(href)').get(),
            }
        
        #anchors = response.css('ul.pagination').css('li a')
        #yield from response.follow_all(anchors, callback=self.parse)
