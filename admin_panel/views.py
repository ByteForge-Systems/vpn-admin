import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

#TODO
#create views api/nodes
@login_required
def dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

@login_required
def servers(request):
    return render(request, 'admin_panel/servers.html')

