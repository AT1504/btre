from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from listings.choices import price_choices, bedroom_choices, state_choices

from listings.models import Listing

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings,6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings':paged_listings,
    }
    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    list = Listing.objects.all().get(id=listing_id)
    context = {
        'list':list,
        'list_id':listing_id
    }
    return render(request, 'listings/listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    #keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords) #contains the keyword anywhere the sentence
    #City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city) # the exact city key name
    #state
    if 'state' in request.GET:
        state = request.GET['state']
        if state and state!='ALL':
            queryset_list = queryset_list.filter(state__iexact=state) # the exact state key name
    #bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms) # the upto bedrooms key name
    #price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price) # the up to price key name
            
    context = {
        'state_choices':state_choices,
        'bedroom_choices':bedroom_choices,
        'price_choices':price_choices,
        'listings': queryset_list,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)