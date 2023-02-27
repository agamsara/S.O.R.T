from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

def index(request):
    #This can override the HTML file in its entirety!
    #return HttpResponse("Hello world, this is a python file output!") 

    #Create and pass variable to index.html to say the current time
    today = datetime.datetime.now().date() 
    return render(request,"index.html", {"today": today})

