import scrapy


class Isd110Spider(scrapy.Spider):
    name = 'isd110'
    #allowed_domains = ['https://isd110.org/our-schools/laketown-elementary/staff-directory']
    start_urls = ['https://isd110.org/our-schools/laketown-elementary/staff-directory']

    def parse(self, response):
        base = response.xpath("//div[@class='node staff teaser']")
        School_name = response.xpath("//div[@class='site-name']/a/text()").get()
        School_address = response.xpath("//p[@class='address']/text()").extract()
        #for concatenating the address
        School_full_address = ""
        for i in School_address:
            School_full_address = School_full_address + " " + i.strip()

        #Fetching the contacts
        for i in base:
            First_Name = i.xpath(".//h2[@class='title']/text()").get()
            Title = i.xpath(".//div[@class='field job-title']/text()").get()
            Phone = i.xpath(".//div[@class='field phone']/a/text()").get()
            Email = i.xpath(".//div[@class='field email']/a/text()").get()

            yield {
                "School Name" : School_name,
                "Address" : School_full_address.strip(),
                "state" : School_address[1].strip().split(",")[1].strip().split(" ")[0],
                "Zipcode" : School_address[1].strip().split(",")[1].strip().split(" ")[1],
                "First Name" : First_Name.split(",")[1].strip(),
                "Last_Name" : First_Name.split(",")[0].strip(),
                "title" : Title.strip(),
                "phone": Phone.strip(),
                "email" : Email.strip()
            }

        next_page = response.xpath("//li[@class='item next']/a/@href").get()
        if next_page:
            yield scrapy.Request(url="https://isd110.org/our-schools/laketown-elementary/staff-directory" + next_page, callback=self.parse)