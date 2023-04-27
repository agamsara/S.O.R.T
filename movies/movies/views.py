from django.http import JsonResponse
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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