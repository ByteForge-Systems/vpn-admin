import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import DeployForm
from fabric import Connection
from django.http import JsonResponse, HttpResponse
import pyotp
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from .telegram_notify import send_telegram_notification
import json
import os


def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            request.session["pre_2fa_user"] = user.username
            return redirect("two_factor")
        else:
            error = "Неверный логин или пароль."
    return render(request, "registration/login.html", {"error": error})

def two_factor_view(request):
    error = None
    if request.method == "POST":
        code = request.POST.get("2fa_code")
        username = request.session.get("pre_2fa_user")
        if not username:
            error = "Сессия истекла, попробуйте войти заново."
            return redirect("login")
        totp = pyotp.TOTP(settings.ADMIN_2FA_SECRET)
        if code and totp.verify(code):
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
                auth_login(request, user)
                del request.session["pre_2fa_user"]
                ip = request.META.get("REMOTE_ADDR")
                send_telegram_notification(
                    f"🛡️ Админ <b>{user.username}</b> вошёл в админку.\nIP: <code>{ip}</code>"
                )
                return redirect("/admin/servers")
            except User.DoesNotExist:
                error = "Пользователь не найден."
                return redirect("login")
        else:
            error = "Неверный код."
    return render(request, "registration/two_factor.html", {"error": error})

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

