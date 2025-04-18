from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import DeployForm
from fabric import Connection


@login_required
def dashboard(request):
    return render(request, 'admin_panel/dashboard.html')

def deploy(request):
    if request.method == 'POST':
        form = DeployForm(request.POST)
        if form.is_valid():
            REPOSITORY_URL = "https://github.com/ByteForge-Systems/vpn-node.git"
            REPOSITORY_BRANCH = "dev"
            REPOSITORY_FOLDER = "vpn-node"
            host = '104.164.54.91'
            user = 'root'
            password = 'Eds2uqdVUZSP'
            try:
                conn = Connection(host=host, user=user, connect_kwargs={"password": password})
                command = (
                    f"apt update && apt upgrade -y && apt install git -y &&"
                    f"git clone --branch {REPOSITORY_BRANCH} {REPOSITORY_URL} && "
                    f"cd {REPOSITORY_FOLDER} && chmod +x install.sh && ./install.sh"
                )
                result = conn.sudo(command, pty=True, hide=True)
                print(f"Success on {host}: {result.stdout}")
            except Exception as e:
                print(f"Error on {host}: {str(e)}")   
    else:
        form = DeployForm()

    return render(request, 'admin_panel/deploy.html')