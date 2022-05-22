if one is using class based views
the templates folder needs to be kept inside the app

the structure is something like this
- templates/<appName>/
Inside the appName folder, place all the html files

when creating views, if you want to specify the templates that we are making use of explicitly, it can be mentioned in views
like this
class viewName(view):
    template_name = "appName/htmlfile"

Creating dynamic URLs
path/<int:pk>
path/<str:pk>
etc.

function based views
def viewName(request):
    #for using models
    #for fetching data from the database 
    
    variable = modelName.objects.all() #These are some of the methods that exists in django that can be used to access database value 
    variable = modelName.objects.get() #Refer to documentation for more
    
    if request.method == "POST":
        username = request.GET.get('username')
        password = request.GET.get('password')
        
        user = Contact(username=username, password=password)
        user.save()
        
        if user is not None:
            return render(request, "html file")
        else:
            return render(request, "html file")
    
    return render(request, "html file")


#Class based views
    #viewName.as_view()
#Function based views
    #views.viewName