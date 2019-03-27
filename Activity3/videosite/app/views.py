from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def register(request):
    return HttpResponse("Hello, world. You're at the app's register page.")


@login_required
def profile(request):
    return HttpResponse("This page cannot be accessed unless they are a logged-in user")
