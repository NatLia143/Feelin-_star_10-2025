from django.shortcuts import render

def index(request):
    return render(request, 'index.html') 

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

def about(request):
    return render(request, 'about.html')

def feed(request):
    return render(request, 'feed.html')

