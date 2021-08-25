from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(User):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
   
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(Profile ,on_delete=models.CASCADE,related_name='todos')
    def __str__(self):
        return self.title
