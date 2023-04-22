from django.shortcuts import render, redirect
import json
from . import maps_api

# Create your views here.
def home(request):
    return render(request, 'website/home.html')

def about(request):
    return render(request, 'website/about.html')

def for_clients(request):
    return render(request, 'website/clients.html')

def for_attorneys(request):
    return render(request, 'website/attorneys.html')

def contact(request):
    return render(request, 'website/contact.html')

def app(request):
    return render(request, 'website/app.html', context={'errors': []})

def renderDirections(request, paths):
    return render(request, 'website/directions.html', context={"paths": paths})

kg_p_g = 8.887
mpg_city = 20
mpg_highway = 30

walking = 0.0195
biking = 0.0085
bus = 0.299
rail = 0.177

tree = 0.065

def execute(request):
    if (request.method != "POST"):
        return render(request, 'website/app.html', context={'errors': []})

    src_addy = {
        'street': request.POST['Starting Street'],
        'city': request.POST['Starting City'],
        'state': request.POST['Starting State'],
        'zipcode': request.POST['Starting Zipcode'],
    }
    dst_addy = {
        'street': request.POST['Destination Street'],
        'city': request.POST['Destination City'],
        'state': request.POST['Destination State'],
        'zipcode': request.POST['Destination Zipcode'],
    }

    for key in src_addy:
        if not src_addy[key]:
            return render(request, 'website/app.html', context={'errors': [f'Error: {key} value required.']})
    for key in dst_addy:
        if not dst_addy[key]:
            return render(request, 'website/app.html', context={'errors': [f'Error: {key} value required.']})
    
    src = maps_api.getCoords(src_addy)
    dst = maps_api.getCoords(dst_addy)

    _paths = ["driving", "walking", "bicycling", "bus", "rail"]
    paths = {}

    for mode in _paths:
        m = 'transit' if mode == 'bus' or mode == 'rail' else mode
        sm = None if mode != 'bus' and mode != 'rail' else mode
        response = maps_api.getMapsResponse(src, dst, mode=m, submode=sm)
        directions = maps_api.getDirections(response)
        steps = maps_api.getSteps(response)
        total_co2 = 0
        for s in steps:
            if mode == 'driving':
                gallons = s[1]/(mpg_highway if s[0] >= 45 else mpg_city)
                total_co2 += gallons*kg_p_g
            elif mode == 'walking':
                total_co2 += s[1]*walking
            elif mode == 'bicycling':
                total_co2 += s[1]*biking
            elif mode == 'bus':
                total_co2 += s[1]*bus
            else:
                total_co2 += s[1]*rail

        if steps:
            m = mode[0].upper() + mode[1:]
            if m == 'Rail':
                m = 'Train/Subway'
            paths[m] = {'co2': round(total_co2, 4), 'tree': int(total_co2/tree)+1, 'directions': directions}
    

    return renderDirections(request, paths)