from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Video
from .forms import VideoForm, DeleteForm


def home(request):
    videos = Video.objects.order_by('-views')[:10]
    return render(request, 'home.html', {'videos': videos, 'user': request.user})


@login_required
def profile(request):
    videos = Video.objects.filter(owner=request.user).order_by('-views')
    return render(request, 'profile.html', {'videos': videos, 'user': request.user})


@login_required
def delete(request):
    if request.method == 'POST':
        form = DeleteForm(request.POST)
        if form.is_valid():
            try:
                video = Video.objects.get(pk=form.cleaned_data['id'])

                if video.owner == request.user:
                    video.delete()
                    return HttpResponseRedirect('/')
                else:
                    # TODO: Determine how to handle the wrong user deleting the video.
                    pass

            except Video.DoesNotExist:
                # TODO: Determine how to handle non-existant id.
                pass


@login_required
def upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = Video(
                file=request.FILES['file'],
                name=form.cleaned_data['name'], desc=form.cleaned_data['desc'], views=0, owner=request.user
            )
            video.save()
            return HttpResponseRedirect('/watch/' + str(video.id))
    else:
        form = VideoForm()
        return render(request, 'upload.html', {'form': form, 'user': request.user})


def watch(request, id):
    video = Video.objects.get(pk=id)
    video.views = video.views + 1
    video.save()
    return render(request, 'watch.html', {'video': video, 'user': request.user})


def search(request):
    q = request.GET.get("q", None)
    if q is None:
        return HttpResponseRedirect('/')

    # NOTE: This is where we introduce SQL Injection
    videos = Video.objects.raw("SELECT * FROM app_video WHERE name LIKE '%" + q + "%'" )
    return render(request, 'search.html', {'videos': videos, 'user': request.user, 'term': q})


def register(request):
    if request.method == 'POST':
        # TODO: Create the user and redirect to login page.
        pass
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            # TODO: Make a nicer register page.
            return HttpResponseRedirect('/login')
