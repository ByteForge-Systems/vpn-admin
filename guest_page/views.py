from django.shortcuts import render

def index(request):
    return render(request, 'guest_page/index.html')
