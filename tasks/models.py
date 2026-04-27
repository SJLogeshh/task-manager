# from django.db import models
# from django.contrib.auth.models import User

# class Task(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     completed = models.BooleanField(default=False)

#     def __str__(self):
#         return self.title
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    due_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title