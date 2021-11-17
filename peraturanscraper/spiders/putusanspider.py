import scrapy
class PutusanSpider(scrapy.Spider):
    name = 'putusan'
   
    def start_requests(self):
        urls = ['https://www.mkri.id/index.php?page=web.Putusan&id=1&kat=1&cari=&menu=5&jnsperkara=1&jenis=PUU']
        for url in urls:
            yield scrapy.Request(url= url, callback= self.parse)
    
    # Parsing the url
    def parse(self, response):
        # GET Nomor Putusan
        nomorPutusan = response.xpath('//div[@style="float:left; width:400px;"]').css('::text').getall()
        
        # GET Isi Putusan
        isiPutusan = response.xpath('//div[@style="float:left;width:400px;"]')
        
        # GET Pokok Perkara  
        pokokPutusan = []
        getPokokPerkara = isiPutusan.xpath("//div[contains(./text(), 'Pengujian')]/text()").getall()

        for item in getPokokPerkara: ## Cleaning out data from pokok_perkara 
            if item == "Dalam Pengujian Materiil:" :
                getPokokPerkara.remove(item)
            elif item == "Dalam Pengujian Formil:":
                getPokokPerkara.remove(item)
            elif item == "\r\n":
                getPokokPerkara.remove(item)
        pokokPutusan = getPokokPerkara
        
        # Get status Perkara
        statusPutusan = response.xpath('//div[3][contains(./text(),"Tidak Dapat Diterima") or contains(./text(),"Menolak Seluruhnya") or contains(./text(),"Mengabulkan Seluruhnya") or contains(./text(),"Mengabulkan Sebagian")]/text()').getall()
        

        # GET file Perkara
        filePutusan = response.xpath('//div[@style="float:left;width:400px;"]').css('a::attr(href)').getall()
        
        # Make list of tupple 
        putusan = zip(nomorPutusan, pokokPutusan, statusPutusan, filePutusan)
        

        # Create JSON
        for  nomor, perkara, status ,file  in putusan:
            yield  {
                'nomorPutusan': "Putusan No. "+nomor,
                'pokokPerkara': perkara,
                'statusPerkara': status,
                'filePerkara' : "https://www.mkri.id/"+file,
                }
        
        anchors = response.xpath('//div[@style="text-align:center; padding:10px"]/span/a')
        #if anchors is not None:
        #    yield response.follow(anchors, callback=self.parse)
       # response.css('ul.pagination').css('li a')
        yield from response.follow_all(anchors, callback=self.parse)
