import scrapy

class PeraturanSpider(scrapy.Spider):
    name = 'peraturan'
    
    def start_requests(self):
        website_bpk = []
        jenisPeraturanPusat = [8,10,9,11,36,13,12,168,28,86,90,169,148,140,183,66,218,135,114,226,209,75,227,62,223,54,225,228,78,27,224,49,40,42,122,222,52,76,85,124,87,81,59,89,116,210,83 ,170,111,202,112,147,46,139,100,108,110,101,182,105,106,208,43,73,163,45,104,154,109,107,186,67,48,69,47,134,103,80,221,] 
        for i in jenisPeraturanPusat: 
            x = 'https://peraturan.bpk.go.id/home/search?jenis={}&page=1'.format(i)
            website_bpk.append(x)
       

        urls = website_bpk
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
                    'peraturanLink': 'https://peraturan.bpk.go.id'+ peraturan.css('li.font-sm').css('a.download-file ::attr(href)').get(),
            }
            except: 
                yield{
        
                    'peraturanName': peraturan.css('span.font-blue::text').get().replace('\r\n                                    ','').replace('\r\n                                ', ''),
                    'peraturanDescription': peraturan.css('span.lead.bold a::text').get(),
                    'link': 'https://peraturan.bpk.go.id'+response.css('li.font-sm a::attr(href)').get(),
                }
        
        anchors = response.css('ul.pagination').css('li a')
        yield from response.follow_all(anchors, callback=self.parse)
