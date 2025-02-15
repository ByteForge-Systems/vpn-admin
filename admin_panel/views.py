from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')
