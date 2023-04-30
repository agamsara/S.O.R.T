from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.http import JsonResponse
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from home.models import SearchQuery
from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db.models import Q
from home.models import SearchQuery, SearchResult,SearchHistory

# Create your views here.

# TO DO: Not a single comment in sight on so many new lines of code. Please add details as to what is happneing here.

def home(request):
    #This can override the HTML file in its entirety!
    #return HttpResponse("Hello world, this is a python file output!") 

    #Create and pass variable to index.html to say the current time
    today = datetime.datetime.now().date() 
    return render(request,"home.html", {"today": today})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def history(request):
    return render(request, "history.html" )

def website(request):
        return render(request, 'movies/website.html')


@api_view(['GET', 'POST'])

def movie_list(request, format=None):
    
    #get all the movies from the db
    #serialize them
    #return json
    
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET','PUT','DELETE'])        
def movie_detail(request,id, format=None):
    
    try:
        movies = Movie.objects.get(pk=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method =='GET':
        serializer = MovieSerializer(movies)
        return Response(serializer.data)
    
    elif request.method =='PUT':
        serealizer = MovieSerializer(movies, data=request.data)
        if serealizer.is_valid():
            serealizer.save()
            return Response(serealizer.data)
        return Response(serealizer.error, status=status.HTTP_400_BAD_REQUEST)
    elif request.method =='DELETE':
        movies.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

def search(request):
    # Get the user's search query from the request
    query = request.GET.get('q')

    # Save the search query to the database
    if query:
        search_query = SearchQuery(user=request.user, query=query)
        search_query.save()

        # Save the search query to the user's search history
        history_item = SearchHistory(user=request.user, query=query)
        history_item.save()

    # Perform the search
    results = SearchResult.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

    # Render the search results template with the search results
    return render(request, 'search_results.html', {'results': results})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid login credentials'
    else:
        error_message = ''
    return render(request, 'login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('home')

     
def history_view(request):
    if request.user.is_authenticated:
        history_items = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')
        return render(request, 'history.html', {'history_items': history_items})
    else:
        return redirect('login')
    
    