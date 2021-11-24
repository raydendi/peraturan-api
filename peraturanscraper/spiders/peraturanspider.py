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
            try:
                yield {
                    'peraturanNumber': peraturan.css('span.font-blue::text').get().replace('\r\n                                    ','').replace('\r\n                                ', ''),
                    'peraturanDescription': peraturan.css('span.lead.bold a::text').get(),
                    'peraturanMencabut': peraturan.xpath('.//ol [1]').css('li.text-left.font-sm').xpath('normalize-space(./span)').getall(),
                    'peraturanMengubah' : peraturan.xpath('.//ol [2]').css('li.text-left.font-sm').xpath('normalize-space(./span)').getall(),
                    'peraturanLink': 'https://peraturan.bpk.go.id'+ response.css('li.font-sm a::attr(href)').get(),
            }
            except: 
                yield{
        
                    'peraturanName': peraturan.css('span.font-blue::text').get().replace('\r\n                                    ','').replace('\r\n                                ', ''),
                    'peraturanDescription': peraturan.css('span.lead.bold a::text').get(),
                    'link': 'https://peraturan.bpk.go.id'+response.css('li.font-sm a::attr(href)').get(),
                }
        
        anchors = response.css('ul.pagination').css('li a')
        yield from response.follow_all(anchors, callback=self.parse)
