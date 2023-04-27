from rest_framework import serializers
from home.models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields =['id','name','description']