from django.urls import path, include
from django.conf import settings
from streamapp import views
from django.conf.urls.static import static
from .views import *


urlpatterns = [

    path ('stream/',views.stream),
    path ('category/',views.category),
    path ('register/',views.register),
    path ('login/',views.login),
    path ('videoview/',views.videoview),
    path ('recent/',views.recentvideo),
    path ('home/',views.home,name='home'),
    path ('logout/',views.user_logout),
    path ('recent_updates/',views.recent_updates),
    path ('userprofile/',views.my_profile),
    path ('editprofile/userprofile/',views.my_profile),
    path ('userprofile/home/',views.home),
    path ('contact/',views.contact),
    path ('favorites/', favorites_list, name='favorites_list'),
    path ('favorites/add/<int:video_id>/', add_to_favorites, name='add_to_favorites'),
    path ('removefav/remove/<int:video_id>',remove_from_fav,name='remove_from_fav'),
    path ('videos/like/', views.like_video, name='like_video'),
    path ('editprofile/',views.edit_profile,name='edit_profile'),
    path ('like-video/<int:video_id>/', like_video, name='like_video'),
    path('addcomment/', addcomment, name='addcomment'),
    path ('search/', views.search_videos, name='search_videos'),

    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

