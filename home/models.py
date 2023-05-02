# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Define a Movie model with name and description fields
class Movie(models.Model):
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    # awards = models.CharField(max_length = 100)

    def __str__(self):
        return self.name + ' '+self.description #+ ' ' + self.awards

# Define a SearchQuery model to store user search queries
class SearchQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query

# Define a SearchResult model to store search results
class SearchResult(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.title

# Define a SearchHistory model to store user search history
class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.query}"

# Define a UserProfile model to extend the built-in User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
