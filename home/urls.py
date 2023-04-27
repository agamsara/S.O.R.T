from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from home import views
from rest_framework.urlpatterns import format_suffix_patterns
from home import views
from django.urls import path
from home import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    #path('recomendations', views.recomendations, name='recomendations'),
    path('history', views.history_view, name='history'),
    #path('admin/', admin.site.urls),
    path('movies/', views.movie_list),
    path('movies/<int:id>',views.movie_detail),
    path('website/', views.website),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('history/', views.history_view, name='search_history'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)

