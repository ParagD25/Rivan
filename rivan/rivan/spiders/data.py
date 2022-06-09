import scrapy

class CliffData(scrapy.Spider):
    name='shopping'

    start_urls=['https://www.farfetch.com/fr/shopping/men/shoes-2/items.aspx','https://www.farfetch.com/fr/shopping/women/bags-purses-1/items.aspx'] # Taking Both the given urls
    
    #initializing page number for footwear site 
    page_number_men=2  

    #initializing page number for bags and purse site 
    page_number_women=2  


    def parse(self, response):

        # Condition fo finding product category
        if response.css('title::text').get()[:15]=="Sacs pour femme":
            pcat='Bags and Purses'
        else:
            pcat='Footwear'

        base_url='https://www.farfetch.com'  #adding this part of url to product page url 
        

        # Condition for sale products
        if response.css('p.css-7pd6gc-Body-PriceFinal.esd507w0::text').get() is None:
            stxt='No Sale'
        else:
            stxt=response.css('p.css-7pd6gc-Body-PriceFinal.esd507w0::text').get().replace('€','')


        for product in response.css('div.css-1veh5kh-ProductCard.e19e7out0'):

            try:
                yield{
                    'name' : product.css('p.css-4y8w0i-Body.e1s5vycj0::text').get(),  # Fetching name
                    'brand' : product.css('p.e17j0z620.css-14ahplz-Body-BodyBold-ProductCardBrandName.eq12nrx0::text').get(),   # Fetching brand name
                    'original_price' : product.css('p.css-hmsjre-Body-Price.e15nyh750::text').get().replace('€',''),    # Fetching original price
                    'sale_price' : stxt,    # Fetching sale price if exists
                    'image_url' : product.css('img.er03ef60.css-1g1ti7a-BaseImg-ProductCardImagePrimary.e2u0eu40').attrib['src'],    # Fetching image url if exists
                    'product_page_url' : base_url+product.css('a.css-n5nq0d-ProductCardLink.e4l1wga0').attrib['href'],    # Fetching product page url
                    'product_category' : pcat    # Fetching product category
                    
                }

            except:
                # if theres no sale on product and image url cannot be found
                yield{
                    'name' : product.css('p.css-4y8w0i-Body.e1s5vycj0::text').get(),
                    'brand' : product.css('p.e17j0z620.css-14ahplz-Body-BodyBold-ProductCardBrandName.eq12nrx0::text').get(),
                    'original_price' : product.css('p.css-hmsjre-Body-Price.e15nyh750::text').get().replace('€',''),
                    'sale_price' : stxt,
                    'image_url' : 'Not Found',
                    'product_page_url' : base_url+product.css('a.css-n5nq0d-ProductCardLink.e4l1wga0').attrib['href'],
                    'product_category' : pcat
                }

        # Scrapping data from all the webpages that contains men's footwear
        next_page='https://www.farfetch.com/fr/shopping/men/shoes-2/items.aspx?page='+str(CliffData.page_number_men)+'&view=90&sort=3&scale=282'
        
        if next_page is not None:
            CliffData.page_number_men+=1
            yield response.follow(next_page, callback=self.parse)

        # Scrapping data from all the webpages that contains women's bags and purse
        
        next_page='https://www.farfetch.com/fr/shopping/women/bags-purses-1/items.aspx?page='+str(CliffData.page_number_women)+'&view=90&sort=3'
        
        if next_page is not None:
            CliffData.page_number_women+=1
            yield response.follow(next_page, callback=self.parse)