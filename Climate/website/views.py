from django.shortcuts import render

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