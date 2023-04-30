"""djangoBootstrap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from searchMongoDB.views import get_search_history

urlpatterns = [
    # this page will now appear when the url ends with "/searchMongoDB". 
    # It will run the index function defined in views.py. 
    # It uses name for the home.html call for hyperlinking
    path('', views.index, name='searchPage'),

    # This will run the search_results function in the views.py
    path('search_results/', views.search_results, name='search_results'),

    
    path('search-history/', get_search_history, name='search_history'),
]
