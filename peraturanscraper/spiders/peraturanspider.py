"""
scrapy import
"""
import re
import scrapy


class PeraturanSpider(scrapy.Spider):
    """class for peraturan spider"""
    name = 'peraturan'
    def start_requests(self):
        website_bpk = []
        jenis_peraturan = [8,10,9,11,36,13,12,168,28,86,90,169,148,140,183,66,218,135,114,226,209,75,227,62,223,54,225,228,78,27,224,49,40,42,122,222,52,76,85,124,87,81,59,89,116,210,83 ,170,111,202,112,147,46,139,100,108,110,101,182,105,106,208,43,73,163,45,104,154,109,107,186,67,48,69,47,134,103,80,221,]
        for i in jenis_peraturan:
            bpk_link = "https://peraturan.bpk.go.id/home/search?jenis={}&page=1".format(i)
            website_bpk.append(bpk_link)

        urls = website_bpk
        for url in urls:
            yield scrapy.Request(url= url, callback= self.parse)

    def parse(self, response):
        for peraturan in response.css('div.portlet-body'):
            try:
                yield {
                    'peraturanNumber': peraturan.css('span.font-blue::text').get().replace('\r\n                                    ','').replace('\r\n                                ', ''),
                    'peraturanDescription': ''.join(peraturan.css('span.font-blue::text').get().replace('\r\n                                    ','').replace('\r\n                                ', '') + ' tentang '+ peraturan.css('span.lead.bold a::text').get()),
                    'peraturanStatus1': peraturan.xpath('.//p [1]').css('span.bold.theme-font::text').get(),
                    'peraturanStatusDescription1': peraturan.xpath('.//ol [1]').css('li.text-left.font-sm').xpath('normalize-space(./span)').getall(),
                    'peraturanStatus2': peraturan.xpath('.//p [2]').css('span.bold.theme-font::text').get(),
                    'peraturanStatusDescription2': peraturan.xpath('.//ol [2]').css('li.text-left.font-sm').xpath('normalize-space(./span)').getall(),
                    'peraturanStatus3': peraturan.xpath('.//p [3]').css('span.bold.theme-font::text').get(),
                    'peraturanStatusDescription3': peraturan.xpath('.//ol [3]').css('li.text-left.font-sm').xpath('normalize-space(./span)').getall(),
                    'peraturanStatus4': peraturan.xpath('.//p [4]').css('span.bold.theme-font::text').get(),
                    'peraturanStatusDescription4': peraturan.xpath('.//ol [4]').css('li.text-left.font-sm').xpath('normalize-space(./span)').getall(),
                    'peraturanNumberSeparated': [int (n) for n in re.findall(r'\b\d+\b',peraturan.css('span.font-blue::text').get().replace('\r\n                                    ','').replace('\r\n                                ', '')) ],
                    'peraturanType': re.findall('UU|Perpu|PP|PERPRES|KEPPRES|INPRES', peraturan.css('span.font-blue::text').get().replace('\r\n                                    ','').replace('\r\n                                ', ''))[0],
                    'peraturanLink': 'https://peraturan.bpk.go.id'+ peraturan.css('li.font-sm').css('a.download-file ::attr(href)').get(),
            }
            except:
                yield{
                    'peraturanNumber': peraturan.css('span.font-blue::text').get().replace('\r\n                                    ','').replace('\r\n                                ', ''),
                    'peraturanDescription': ''.join(peraturan.css('span.font-blue::text').get().replace('\r\n                                    ','').replace('\r\n                                ', '') + ' tentang '+ peraturan.css('span.lead.bold a::text').get()),
                    'peraturanStatus1': peraturan.xpath('.//p [1]').css('span.bold.theme-font::text').get(),
                    'peraturanStatusDescription1': peraturan.xpath('.//ol [1]').css('li.text-left.font-sm').xpath('normalize-space(./span)').getall(),
                    'peraturanStatus2': peraturan.xpath('.//p [2]').css('span.bold.theme-font::text').get(),
                    'peraturanStatusDescription2': peraturan.xpath('.//ol [2]').css('li.text-left.font-sm').xpath('normalize-space(./span)').getall(),
                    'peraturanStatus3': peraturan.xpath('.//p [3]').css('span.bold.theme-font::text').get(),
                    'peraturanStatusDescription3': peraturan.xpath('.//ol [3]').css('li.text-left.font-sm').xpath('normalize-space(./span)').getall(),
                    'peraturanStatus4': peraturan.xpath('.//p [4]').css('span.bold.theme-font::text').get(),
                    'peraturanStatusDescription4': peraturan.xpath('.//ol [4]').css('li.text-left.font-sm').xpath('normalize-space(./span)').getall(),
                    'peraturanNumberSeparated': [int (n) for n in re.findall(r'\b\d+\b',peraturan.css('span.font-blue::text').get().replace('\r\n                                    ','').replace('\r\n                                ', '')) ],
                    'peraturanType': 'Peraturan Kementerian/LPND',
                    'peraturanLink': 'https://peraturan.bpk.go.id'+ peraturan.css('li.font-sm').css('a.download-file ::attr(href)').get(),
                }
        anchors = response.css('ul.pagination').css('li a')
        yield from response.follow_all(anchors, callback=self.parse)
