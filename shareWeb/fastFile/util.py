from django.core.paginator import Paginator

def nav_page(number,posts):
    pages = Paginator(posts,13)
         
    if number is None:
        return pages.page(1), None
    number = int(number)
        
    if number > pages.num_pages or number < 1:
        return None, None
        
    page = pages.page(number)
        
    numberOfPages = pages.num_pages
       
    pageLinks = []
    i = number
    j = 0
    while i < numberOfPages and j < 5:
        i += 1
        pageLinks.append(i)
        j += 1
            
        

        
    return page, pageLinks


