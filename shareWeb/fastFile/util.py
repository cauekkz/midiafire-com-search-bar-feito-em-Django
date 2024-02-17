from django.core.paginator import Paginator
from .models import *
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

def check_inputs(type,input):
    match type:
        case 'password':
            if len(input) < 8:
                return False
        case 'username':
            if User.objects.filter(username=input).exists():
                return False
        case 'email':
            if User.objects.filter(email=input).exists():
                return False
        case _:
            return False
        
    return True