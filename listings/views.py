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
    context = {
        'state_choices':state_choices,
        'bedroom_choices':bedroom_choices,
        'price_choices':price_choices
    }
    return render(request, 'listings/search.html', context)