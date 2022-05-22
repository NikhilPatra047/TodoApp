from django.shortcuts import render, HttpResponse, redirect

from django.contrib.auth.views import LoginView, LogoutView #used for creating the LoginView, and LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin #Used to restrict pages if the user is not logged in. In other words, used to check for authentication 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.views.generic.list import ListView
#The above module is needed for creating class based views
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy #Used for redirecting the user to a different web page.
#UpdateView modifies the data
#CreateView allows for creating forms
#ListView allows for displaying a list of items
#DetailView allows for displaying specific item
#All authentication related modules start with django.contrib.auth

from todoapp.models import Task

from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm

# Create your views here.

class TaskLoginView(LoginView):
    model = Task
    context_object_name = 'task-login'
    template_name = 'todoapp/login.html'
    fields = '__all__'
    
    def get_success_url(self): #this is the same as using success_url = reverse_lazy('name')
        return reverse_lazy('tasks')
    
class TaskLogoutView(LogoutView):
    template_name = 'todoapp/logged_out.html'

class TaskList(LoginRequiredMixin, ListView):
    model = Task #Always bring in the models that we are making use of in the views.
    context_object_name = 'tasks' #This is going to be the same as the name value in urls.py
    template_name = 'todoapp/task_list.html' #This is essential if the html names don't adhere to the 
    #standards of task_list and task_detail
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context["tasks"] = context["tasks"].filter(title__icontains=search_input)
            
        context['search_input'] = search_input
        return context 
    
    #get_context_data is just a way to pass in more data that the HTML page can render instead of using through
    #queries.
    #This thing here is the same as creating a context variable and passing down the render method
    #in function based views
        """def TaskList(request):
                context = {
                    "hello": 'red'
                }
                
                return render(request, "index.html", context)
                
                this context then can be accessed in the index.html page using the key hello to render 
                any value that we are sending.
        """
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task' #The name through which we will be accessing the database fields
    template_name = 'todoapp/task_detail.html'
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'todoapp/task_form.html'
    context_object_name = 'task-create'
    fields = ['title', 'description', 'complete'] #This helps us specifying what all fields that we want to display in our form from a table 
    #setting this to __all__ can show all the fields within a page 
    #But we can also specify individually
    #for example - fields = ['title', 'description', 'users'] etc.
    
    success_url = reverse_lazy('tasks') #reverse_lazy is used to redirect the user to a different 
    #if success, reverse_lazy will send the user back to the url whose name attribute value is tasks
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
        
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    context_object_name = 'task-update'
    fields = ['title', 'complete', 'description'] 
    success_url = reverse_lazy('tasks')
#Each view has a certain role to play when using forms

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task' #Context object name gets in the context data from the url attribute name 
    template_name = 'todoapp/delete.html'
    success_url = reverse_lazy('tasks')
    
class TaskRegister(FormView):
    template_name = 'todoapp/register.html'
    form_class = UserCreationForm #The USERCREATIONFORM is the built-in register form in Django
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    #Once the form is submitted, the form_valid() is triggered and then the validity of the form 
    #is checked and the user is logged in.
    
    def form_valid(self, form): #The form_valid checks for the validity of the form.
        user = form.save() #Once the form is created, saving it in user
        if user is not None:
            login(self.request, user)
        return super(TaskRegister, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(TaskRegister, self).get(*args, **kwargs)
    
class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))

        