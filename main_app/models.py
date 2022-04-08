from django.db import models
from django.contrib.postgres.fields import ArrayField
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    
        profile_image = models.ImageField(upload_to = "profile_images/", blank=True, null=True)

class Destination(models.Model):

    city = models.CharField(max_length = 50)
    country = models.CharField(max_length = 50)
    image = models.ImageField(upload_to = "destination_images/", blank=True)
    description = models.TextField()
    things_to_do = ArrayField(models.CharField(max_length = 250), blank = True)

    def __str__(self):
        return self.city

    class Meta:
        ordering = ['country']

class Travel(models.Model):

    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to = "travel_images/", blank=True)
    destinations = models.ManyToManyField(Destination, blank=True)
    departure_date = models.DateField(auto_now = False, auto_now_add = False)
    return_date = models.DateField(auto_now = False, auto_now_add = False)
    budget = models.IntegerField()
    travelers = models.ManyToManyField(CustomUser)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['departure_date']

class Itinerary(models.Model):

    day = models.IntegerField()
    date = models.DateField(auto_now = False, auto_now_add = False)
    destination = models.ForeignKey(Destination, related_name='itineraries', on_delete = models.CASCADE, null=True, blank=True)
    transportation = models.CharField(max_length=250)
    accomodation = models.CharField(max_length=250)
    things_to_do = ArrayField(models.CharField(max_length=250))
    meals = ArrayField(models.CharField(max_length=50))
    daily_budget = models.IntegerField(default = 0)
    travel = models.ForeignKey(Travel, related_name='itineraries', on_delete = models.CASCADE)

    def __str__(self):
        return 'Day' + str(self.day) + '_'+str(self.travel)
    
    class Meta:
        ordering = ['date']

class Comment(models.Model):

    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    travel = models.ForeignKey(Travel, related_name='comments', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return 'Comment' + str(self.pk) + '_'+ str(self.travel)