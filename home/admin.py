from django.contrib import admin

# Register your models here.
from django.contrib import admin
from home.models import Movie,SearchHistory

'''
admin.site.register(Movie)
@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'timestamp')
'''

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'timestamp')