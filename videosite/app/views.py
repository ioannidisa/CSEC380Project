from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

import urllib.request
import urllib.parse
import os.path

from .models import Video
from .forms import VideoForm, DeleteForm

IS_POSTGRES = 'postgres' in settings.DATABASES['default']['ENGINE']


def home(request):
    videos = Video.objects.order_by('-views')[:10]
    return render(request, 'home.html', {'videos': videos, 'user': request.user})


@login_required
def profile(request):
    videos = Video.objects.filter(owner=request.user).order_by('-views')
    print(videos.query)
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
                    return HttpResponseRedirect('/watch/' + form.cleaned_data['id'])
                    pass

            except Video.DoesNotExist:
                return HttpResponseRedirect('/')


@login_required
def upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data.get('url', None) is None:
                video = Video(
                    file=request.FILES['file'],
                    name=form.cleaned_data['name'], desc=form.cleaned_data['desc'], views=0, owner=request.user
                )
            else:
                # Download the file into the correct folder.
                url = form.cleaned_data['url']
                r = urllib.request.urlopen(url)
                data = r.read()

                # We need to write the file into the downloads folder.
                # To do so, we need to calculate the location of the file based on the name.
                path = urllib.parse.urlparse(url).path
                name = os.path.basename(path)
                new_path = 'media/videos/{}/{}/{}/'.format('2019', '04', '16')

                try:
                    os.makedirs(new_path)
                except:
                    pass

                new_path = '{}/{}'.format(new_path, name)

                with open(new_path, 'wb') as file:
                    file.write(data)
                    video = Video(
                        name=form.cleaned_data['name'], desc=form.cleaned_data['desc'], views=0, owner=request.user
                    )
                    video.file.name = 'videos/{}/{}/{}/{}'.format('2019', '04', '16', name)
                    video.save()

            return HttpResponseRedirect('/watch/' + str(video.id))
        else:
            return render(request, 'upload.html', {'form': form, 'user': request.user})
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
    if not IS_POSTGRES:
        videos = Video.objects.raw("SELECT * FROM app_video WHERE name LIKE '%" + q + "%'")
    else:
        videos = Video.objects.raw('''SELECT "app_video"."id", "app_video"."name", "app_video"."desc", 
        "app_video"."views", "app_video"."owner_id", "app_video"."file" FROM "app_video"
         WHERE "app_video"."name" LIKE \'%%{}%%\' ORDER BY "app_video"."views" DESC'''.format(q))

    return render(request, 'search.html', {'videos': videos, 'user': request.user, 'term': q})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/profile')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
