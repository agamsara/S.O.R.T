from django.db import models 

class Movie(models.Model):
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500)
    awards = models.CharField(max_length = 100)

    def __str__(self):
        return self.name + ' '+self.description + ' ' + self.awards