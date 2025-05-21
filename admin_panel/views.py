import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import DeployForm
from fabric import Connection
from django.http import JsonResponse
from dotenv import load_dotenv
import os


@login_required
def dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

@login_required
def deploy(request):
    if request.method == 'POST':
        node_ip = request.POST.get('node_ip')
        if not node_ip:
            return JsonResponse({'status': 'error', 'message': 'Node IP is required'}, status=400)

        REPOSITORY_URL = "https://github.com/ByteForge-Systems/vpn-node.git"
        REPOSITORY_BRANCH = "dev"
        REPOSITORY_FOLDER = "vpn-node"
        host = node_ip
        user = os.getenv('USERNAME_SERVER')
        password = os.getenv('PASSWORD_SERVER')

        try:
            conn = Connection(host=host, user=user, connect_kwargs={"password": password})
            command = (
                f"apt update && apt upgrade -y && apt install git -y &&"
                f"git clone --branch {REPOSITORY_BRANCH} {REPOSITORY_URL} && "
                f"cd {REPOSITORY_FOLDER} && chmod +x install.sh && ./install.sh"
            )
            result = conn.sudo(command, pty=True, hide=True)
            return JsonResponse({'status': 'success', 'message': f"Success on {host}: {result.stdout}"})
        except Exception as e:
            return JsonResponse({'status': 'error', "System: message": f"Error on {host}: {str(e)}"}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

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

