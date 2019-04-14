from django.urls import path

from .views import register, profile, watch, home, upload, search, delete

urlpatterns = [
    path('', home, name='home'),
    path('watch/<int:id>', watch, name='watch'),
    path('register', register, name='register'),
    path('upload', upload, name='upload'),
    path('profile', profile, name='profile'),
    path('search', search, name='search'),
    path('delete', delete, name='delete')
]