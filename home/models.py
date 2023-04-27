# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    #awards = models.CharField(max_length = 100)

    def __str__(self):
        return self.name + ' '+self.description #+ ' ' + self.awards
    

class SearchQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query
    

class SearchResult(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.title

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.query}"
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
