from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    """
        models.SET_NULL means if the user gets deleted all the information remains even after the user is
        deleted
    """
    """
        models.CASCADE means if the user gets deleted then all the related information of the user
        is also deleted.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    #auto_now_add adds the system time information as the time information for a field in the database

    def __str__(self):
        return self.title

    class Meta: #This is an optional class in django that can be used to change order, add verbose_name, etc.
        ordering=['complete'] #This will do the ordering on the basis of the complete field
    #What is Meta class