import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

# TODO: сделать кнопку включения
# TODO: отредактировать дополнительную информацию на кнопке
# TODO: ?добавить страничку ноды?
@login_required
def servers(request):
    api_url = "http://46.254.17.174:8080/api/nodes"
    try:
        response = requests.get(api_url)
        nodes = response.json()
    except requests.exceptions.RequestException as e: #тут надо перепроверить
        nodes = []

    return render(request, 'admin_panel/servers.html', {'nodes': nodes})

