from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class PriorityChoices(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)
    completed = models.BooleanField(default=False)
    date=models.DateField(auto_now_add = True)
    priority = models.ManyToManyField(PriorityChoices, blank=True, null=True)

    # def __str__(self):
    #     return self.title
    
class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.URLField(default="https://static.vecteezy.com/system/resources/thumbnails/005/129/844/small_2x/profile-user-icon-isolated-on-white-background-eps10-free-vector.jpg", null=True, blank=True)

    def __str__(self):
        return self.user.username