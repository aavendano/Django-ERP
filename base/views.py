from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    """Dashboard view"""
    return render(request, 'base/index.html', {})
