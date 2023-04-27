from django.contrib import admin

# Register your models here.
from django.contrib import admin
from home.models import SearchQuery, SearchResult, SearchHistory

'''
admin.site.register(Movie)
@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'timestamp')
'''

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'timestamp')
    

# Register the SearchQuery and SearchHistory models with the admin site
admin.site.register(SearchQuery)
admin.site.register(SearchHistory)

# Register the SearchResult model with the admin site
@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'url')